// SEOMachine Web App — Alpine.js Component

document.addEventListener('alpine:init', () => {
  Alpine.data('app', () => ({
    // Views: 'form' | 'generating' | 'result' | 'history-detail'
    view: 'form',

    // API Key
    apiKey: localStorage.getItem('sm_api_key') || '',
    showApiModal: false,
    apiKeyInput: '',
    apiKeyError: '',

    // Form fields
    topic: '',
    keywords: '',
    tone: '친근한',
    audience: '',
    instructions: '',
    formError: '',

    // Generation state
    generatingStep: 0,
    generatingSteps: [
      { label: '초안 작성 중...', icon: '✍️' },
      { label: 'SEO 최적화 적용 중...', icon: '🔍' },
      { label: '메타 데이터 생성 중...', icon: '🏷️' },
      { label: '완료!', icon: '✅' },
    ],
    streamingText: '',
    isGenerating: false,

    // Result state
    article: '',
    metaInfo: null,
    metaOptions: null,
    wordCount: 0,
    generatedTopic: '',

    // History
    history: JSON.parse(localStorage.getItem('sm_history') || '[]'),
    selectedHistory: null,

    // Notification
    notification: '',
    notificationTimer: null,

    // Init
    init() {
      if (!this.apiKey) {
        this.showApiModal = true;
        this.apiKeyInput = '';
      }
    },

    // --- API Key Modal ---
    openApiModal() {
      this.apiKeyInput = this.apiKey;
      this.apiKeyError = '';
      this.showApiModal = true;
    },
    saveApiKey() {
      const key = this.apiKeyInput.trim();
      if (!key.startsWith('sk-ant-')) {
        this.apiKeyError = 'Anthropic API 키는 sk-ant- 로 시작해야 합니다.';
        return;
      }
      this.apiKey = key;
      localStorage.setItem('sm_api_key', key);
      this.showApiModal = false;
      this.apiKeyError = '';
    },
    closeApiModal() {
      if (this.apiKey) this.showApiModal = false;
    },

    // --- Generation ---
    async generate() {
      // Validate
      if (!this.topic.trim()) {
        this.formError = '주제를 입력해주세요.';
        return;
      }
      if (!this.apiKey) {
        this.showApiModal = true;
        return;
      }
      this.formError = '';

      // Switch to generating view
      this.view = 'generating';
      this.generatingStep = 0;
      this.streamingText = '';
      this.isGenerating = true;
      this.generatedTopic = this.topic.trim();

      try {
        // Step 1: Write article
        this.generatingStep = 0;
        const rawArticle = await this.callClaudeStreaming(
          buildSystemPrompt(),
          buildWritePrompt({
            topic: this.topic,
            keywords: this.keywords,
            tone: this.tone,
            audience: this.audience,
            instructions: this.instructions,
          })
        );

        // Step 2: SEO (parsing meta from article)
        this.generatingStep = 1;
        await this.sleep(400);

        // Parse article and meta from response
        const { articleContent, metaParsed } = this.parseArticleResponse(rawArticle);
        this.article = articleContent;
        this.metaInfo = metaParsed;
        this.wordCount = this.countWords(articleContent);

        // Step 3: Generate meta options
        this.generatingStep = 2;
        const primaryKeyword = metaParsed?.primaryKeyword || this.topic;
        try {
          const metaRaw = await this.callClaude(
            buildSystemPrompt(),
            buildMetaPrompt(articleContent, primaryKeyword)
          );
          this.metaOptions = this.parseMetaOptions(metaRaw);
        } catch (e) {
          // Meta generation is non-critical
          this.metaOptions = null;
        }

        // Step 4: Done
        this.generatingStep = 3;
        await this.sleep(600);

        // Save to history
        this.saveToHistory();

        // Switch to result view
        this.view = 'result';
      } catch (err) {
        this.view = 'form';
        this.formError = `오류가 발생했습니다: ${err.message}`;
      } finally {
        this.isGenerating = false;
      }
    },

    async callClaudeStreaming(systemPrompt, userPrompt) {
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': this.apiKey,
          'anthropic-version': '2023-06-01',
          'anthropic-dangerous-direct-browser-access': 'true',
        },
        body: JSON.stringify({
          model: 'claude-sonnet-4-6',
          max_tokens: 8192,
          stream: true,
          system: systemPrompt,
          messages: [{ role: 'user', content: userPrompt }],
        }),
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.error?.message || `API 오류: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullText = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          const data = line.slice(6).trim();
          if (data === '[DONE]' || !data) continue;

          try {
            const parsed = JSON.parse(data);
            if (
              parsed.type === 'content_block_delta' &&
              parsed.delta?.type === 'text_delta'
            ) {
              fullText += parsed.delta.text;
              this.streamingText = fullText;
            }
          } catch (_) {}
        }
      }

      return fullText;
    },

    async callClaude(systemPrompt, userPrompt) {
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': this.apiKey,
          'anthropic-version': '2023-06-01',
          'anthropic-dangerous-direct-browser-access': 'true',
        },
        body: JSON.stringify({
          model: 'claude-sonnet-4-6',
          max_tokens: 2048,
          system: systemPrompt,
          messages: [{ role: 'user', content: userPrompt }],
        }),
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.error?.message || `API 오류: ${response.status}`);
      }

      const data = await response.json();
      return data.content?.[0]?.text || '';
    },

    // --- Parsing helpers ---
    parseArticleResponse(raw) {
      const metaStartIdx = raw.indexOf('META_START');
      const metaEndIdx = raw.indexOf('META_END');

      let articleContent = raw;
      let metaParsed = null;

      if (metaStartIdx !== -1 && metaEndIdx !== -1) {
        articleContent = raw.substring(0, raw.indexOf('\n---\nMETA_START') !== -1
          ? raw.indexOf('\n---\nMETA_START')
          : metaStartIdx - 4).trim();

        const metaBlock = raw.substring(metaStartIdx + 10, metaEndIdx).trim();
        metaParsed = this.parseMetaBlock(metaBlock);
      }

      return { articleContent, metaParsed };
    },

    parseMetaBlock(block) {
      const lines = block.split('\n');
      const meta = {};
      for (const line of lines) {
        const colonIdx = line.indexOf(':');
        if (colonIdx === -1) continue;
        const key = line.substring(0, colonIdx).trim();
        const value = line.substring(colonIdx + 1).trim();
        if (key === 'Meta Title') meta.title = value;
        else if (key === 'Meta Description') meta.description = value;
        else if (key === 'Primary Keyword') meta.primaryKeyword = value;
        else if (key === 'Secondary Keywords') meta.secondaryKeywords = value;
        else if (key === 'URL Slug') meta.slug = value;
        else if (key === 'Word Count') meta.wordCount = value;
      }
      return meta;
    },

    parseMetaOptions(raw) {
      const jsonMatch = raw.match(/```json\s*([\s\S]*?)```/) || raw.match(/(\{[\s\S]*\})/);
      if (!jsonMatch) return null;
      try {
        return JSON.parse(jsonMatch[1]);
      } catch (_) {
        return null;
      }
    },

    countWords(text) {
      // Korean word count: count CJK characters + split by spaces
      const cjkChars = (text.match(/[\u3400-\u9FFF\uF900-\uFAFF]/g) || []).length;
      const nonCjkWords = text
        .replace(/[\u3400-\u9FFF\uF900-\uFAFF]/g, '')
        .split(/\s+/)
        .filter(w => w.length > 1).length;
      return cjkChars + nonCjkWords;
    },

    // --- History ---
    saveToHistory() {
      const entry = {
        id: Date.now(),
        topic: this.generatedTopic,
        date: new Date().toLocaleDateString('ko-KR'),
        article: this.article,
        metaInfo: this.metaInfo,
        metaOptions: this.metaOptions,
        wordCount: this.wordCount,
      };
      this.history.unshift(entry);
      if (this.history.length > 20) this.history = this.history.slice(0, 20);
      localStorage.setItem('sm_history', JSON.stringify(this.history));
    },

    loadHistory(entry) {
      this.generatedTopic = entry.topic;
      this.article = entry.article;
      this.metaInfo = entry.metaInfo;
      this.metaOptions = entry.metaOptions;
      this.wordCount = entry.wordCount;
      this.view = 'result';
    },

    deleteHistory(id, event) {
      event.stopPropagation();
      this.history = this.history.filter(h => h.id !== id);
      localStorage.setItem('sm_history', JSON.stringify(this.history));
    },

    // --- Result actions ---
    get renderedArticle() {
      if (!this.article) return '';
      return marked.parse(this.article);
    },

    get displayMetaTitle() {
      if (this.metaOptions?.titles) {
        const idx = this.metaOptions.recommended_title_index ?? 0;
        return this.metaOptions.titles[idx]?.text || this.metaInfo?.title || '';
      }
      return this.metaInfo?.title || '';
    },

    get displayMetaDesc() {
      if (this.metaOptions?.descriptions) {
        const idx = this.metaOptions.recommended_desc_index ?? 0;
        return this.metaOptions.descriptions[idx]?.text || this.metaInfo?.description || '';
      }
      return this.metaInfo?.description || '';
    },

    async copyToClipboard() {
      try {
        await navigator.clipboard.writeText(this.article);
        this.showNotification('클립보드에 복사됐어요!');
      } catch (_) {
        this.showNotification('복사에 실패했습니다.');
      }
    },

    downloadMarkdown() {
      const meta = this.metaInfo
        ? `---\nMeta Title: ${this.metaInfo.title || ''}\nMeta Description: ${this.metaInfo.description || ''}\nPrimary Keyword: ${this.metaInfo.primaryKeyword || ''}\nURL Slug: ${this.metaInfo.slug || ''}\n---\n\n`
        : '';
      const content = meta + this.article;
      const slug = this.metaInfo?.slug?.replace('/blog/', '') || this.generatedTopic.replace(/\s+/g, '-');
      const filename = `${slug}-${new Date().toISOString().split('T')[0]}.md`;

      const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      a.click();
      URL.revokeObjectURL(url);
    },

    newRequest() {
      this.view = 'form';
      this.topic = '';
      this.keywords = '';
      this.tone = '친근한';
      this.audience = '';
      this.instructions = '';
      this.article = '';
      this.metaInfo = null;
      this.metaOptions = null;
      this.streamingText = '';
      this.formError = '';
    },

    // --- Utilities ---
    showNotification(msg) {
      this.notification = msg;
      if (this.notificationTimer) clearTimeout(this.notificationTimer);
      this.notificationTimer = setTimeout(() => { this.notification = ''; }, 3000);
    },

    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    },
  }));
});
