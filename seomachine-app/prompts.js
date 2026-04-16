// SEOMachine Prompts - Ported from .claude/commands/write.md and agents/

function buildSystemPrompt() {
  return `You are an expert SEO content writer for Unifi.me, a stablecoin wallet by LINE NEXT built on the Kaia blockchain.

${BRAND_VOICE}

${PRODUCT_FEATURES}

${SEO_GUIDELINES}

## Critical Rules
1. Write ALL content in KOREAN (한국어) by default unless the user explicitly requests another language
2. Follow all regulatory-safe term rules for Korean content
3. Maintain Unifi's approachable, trustworthy, practical voice throughout
4. Every article must be publish-ready quality`;
}

function buildWritePrompt({ topic, keywords, tone, audience, instructions }) {
  const toneMap = {
    '친근한': 'Approachable and conversational — like explaining to a smart friend',
    '전문적': 'Professional and authoritative — expert tone with data and insights',
    '실용적': 'Practical and actionable — step-by-step, how-to focused',
  };

  const keywordList = keywords
    .split(/[,\n]/)
    .map(k => k.trim())
    .filter(Boolean);

  return `Write a comprehensive, SEO-optimized blog article in KOREAN about: "${topic}"

## Input Parameters
- **Primary Keyword**: ${keywordList[0] || topic}
- **Secondary Keywords**: ${keywordList.slice(1).join(', ') || 'None specified'}
- **Tone**: ${toneMap[tone] || tone}
- **Target Audience**: ${audience || 'Unifi.me users — people new to stablecoins seeking stable earning and easy cross-border payments'}
${instructions ? `- **Special Instructions**: ${instructions}` : ''}

## Article Structure (follow exactly)

### 1. H1 Headline
- Include primary keyword naturally
- Under 60 characters for SERP display
- Compelling, benefit-focused

### 2. Introduction (150-250 words)
**CRITICAL — Direct Answer First**: The first 1-2 sentences MUST directly answer the query. AI scrapers pull from the top of the page.

After the direct answer, use ONE of these hooks:
- Provocative Question
- Specific Scenario (with name, date, numbers)
- Surprising Statistic
- Bold Statement
- Counterintuitive Claim

Then apply APP Formula:
- **Agree**: Acknowledge something the reader already believes
- **Promise**: Tell them exactly what they'll learn
- **Preview**: Brief overview of what's coming

Include primary keyword in first 100 words.

### 3. Key Takeaways Block (REQUIRED, right after introduction)
\`\`\`
> **핵심 요약**
> - [구체적인 결론 #1 — 숫자/이름/결과 포함]
> - [구체적인 결론 #2]
> - [구체적인 결론 #3]
> - [구체적인 결론 #4 — 필요시]
> - [구체적인 결론 #5 — 필요시]
\`\`\`
3-5 bullets. Each is a standalone conclusion with specifics. NOT a table of contents.

### 4. Main Body (1,800-2,500 words)
- 4-7 H2 sections with logical flow
- H3 subsections for complex ideas
- Primary keyword 1-2% density (natural variations)
- Paragraphs: 2-4 sentences MAX
- Sentences: under 25 words average
- Bold key concepts

**REQUIRED: 2-3 Mini-Stories per article**
Each mini-story needs:
- Specific person (use a name, even if fictional: "김민준", "박지원", "이서연")
- Concrete situation with details (dates, numbers, specific amounts)
- Clear outcome that illustrates the point
- 50-150 words each
Place one early, one in middle, one near conclusion.

**REQUIRED: 2-3 Contextual CTAs**
| Location | Type | Example |
|----------|------|---------|
| After first major value section | Soft | "Unifi에서 직접 확인해보고 싶으신가요? [지금 시작하기 →]" |
| After comparison/proof section | Medium | "**지금 바로 시험해볼 준비가 되셨나요?** 회원가입은 LINE 계정만 있으면 됩니다." |
| End of article | Strong CTA | "**[Unifi 지금 시작하기 →]**" |

First CTA MUST appear within first 500 words.

### 5. FAQ Section (4-6 questions)
Write questions in natural language people would type into ChatGPT/Google.
Answer each question directly in first sentence, then expand.

### 6. Conclusion (150-200 words)
- Recap 3-5 key takeaways
- Clear next steps
- Strong CTA
- Empowering, forward-looking tone

## Output Format
Provide the complete article first, then the meta information in this exact format:

---
META_START
Meta Title: [50-60 char title with primary keyword]
Meta Description: [150-160 char description with keyword and CTA]
Primary Keyword: [main keyword]
Secondary Keywords: [kw1, kw2, kw3]
URL Slug: /blog/[slug]
Word Count: [approximate count]
META_END
---

Write the article now. Start with the H1 headline.`;
}

function buildMetaPrompt(articleContent, primaryKeyword) {
  return `You are a conversion-focused copywriter specializing in Korean SEO meta elements.

Based on this article about "${primaryKeyword}", generate 3 compelling meta title options and 3 meta description options.

ARTICLE (first 500 words):
${articleContent.substring(0, 2000)}

## Requirements

### Meta Titles (50-60 characters each)
Generate 3 options using these formats:
1. How-to format: "~하는 방법: 완벽 가이드"
2. List format: "[숫자]가지 [주제] 전략"
3. Benefit-driven: "[혜택] + [방법]"

Each title must include the keyword "${primaryKeyword}" naturally.

### Meta Descriptions (150-160 characters each)
Generate 3 options:
1. Problem-Solution-CTA formula
2. Benefit-Method-CTA formula
3. Question-Answer-CTA formula

Each must include a call-to-action (지금 확인하세요, 바로 시작하기, 자세히 알아보기).

## Output Format (exact JSON)
\`\`\`json
{
  "titles": [
    {"text": "...", "chars": 0, "approach": "How-to"},
    {"text": "...", "chars": 0, "approach": "List"},
    {"text": "...", "chars": 0, "approach": "Benefit-driven"}
  ],
  "descriptions": [
    {"text": "...", "chars": 0, "formula": "Problem-Solution-CTA"},
    {"text": "...", "chars": 0, "formula": "Benefit-Method-CTA"},
    {"text": "...", "chars": 0, "formula": "Question-Answer-CTA"}
  ],
  "recommended_title_index": 0,
  "recommended_desc_index": 0
}
\`\`\`

Return ONLY the JSON block, no other text.`;
}
