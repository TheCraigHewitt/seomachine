# Repurpose Command

Take a published or drafted article and generate platform-specific versions for distribution across multiple content surfaces, maximizing AI citation potential.

## Usage
`/repurpose [path-to-article]`

**Examples:**
- `/repurpose drafts/project-management-guide-2026-04-10.md`
- `/repurpose published/start-a-blog.md`

## Why This Matters

AI search engines (ChatGPT, Perplexity, Gemini) pull recommendations from many surfaces beyond your website: Medium, LinkedIn, Reddit, Quora, YouTube transcripts. The more surfaces your content appears on with attribution back to your site, the higher the probability of being cited in AI-generated answers.

One article should become 4-5 pieces of distributed content. This command automates the adaptation, not just copy-pasting.

## Process

### 1. Read and Analyze Source Article
- Read the full article
- Identify the primary keyword, core thesis, and key claims
- Note the article's URL slug (for linking back)
- Extract 3-5 key takeaways
- Identify the strongest data points, quotes, and insights

### 2. Generate Platform-Specific Versions

For each platform, generate an adapted version that fits the platform's norms, audience expectations, and format. Each version must link back to the original article.

---

#### LinkedIn Article (LinkedIn Pulse)

**Format:** Long-form article (800-1,200 words)
**Tone:** Professional, insight-driven, slight thought-leadership angle
**Structure:**
- Opening hook (2-3 sentences, conversational)
- 3-5 key insights from the article, reframed for a business/professional audience
- Personal perspective or key insight
- Clear takeaway or lesson
- Link to full article: "I wrote a deeper breakdown on this: [link]"
- No bullet-heavy formatting (LinkedIn penalizes listicle-style posts)

**Adaptation notes:**
- Reframe for business value (ROI, productivity, growth) when possible
- Remove niche-specific jargon that a general LinkedIn audience won't know
- Add a "why this matters for your business" angle if the original is practitioner-focused
- Do NOT just copy the intro + "read more at [link]"

---

#### Medium Article

**Format:** Full article adaptation (1,200-1,800 words)
**Tone:** Match the original article's voice
**Structure:**
- Can be closer to the original than other platforms
- Add a brief author bio paragraph at the end
- Include "Originally published on [your blog]: [link]"
- Use Medium-appropriate formatting (pull quotes, section breaks, no markdown tables)
- Add Medium tags (5 tags, mix of broad and niche)

**Adaptation notes:**
- Medium readers expect depth, so don't over-simplify
- Convert markdown tables to prose or bullet lists (Medium handles tables poorly)
- Remove product-specific CTAs (trial links, pricing) -- replace with the "originally published" link
- Keep internal links pointing to your site (these become backlinks from Medium)

---

#### Reddit Comment Drafts (2-3 versions)

**Format:** 100-250 word comment, conversational
**Tone:** Casual, helpful, zero promotional language
**Structure:**
- Draft 2-3 comment versions, each targeting a different common Reddit thread type:
  1. **Recommendation thread** ("What tool should I use?"): Share a genuine comparison with your product mentioned naturally
  2. **Pain point thread** ("Frustrated with [problem]"): Share how the article's insight addresses this
  3. **Discussion thread** ("What's your take on [topic]?"): Share a key insight as personal opinion

**Adaptation notes:**
- NEVER use marketing language ("industry-leading", "robust", "seamless")
- Write as a real person sharing experience, not a brand
- Only include a link if it genuinely helps: "There's a good breakdown here: [link]"
- Include the link at most in 1 of the 3 drafts (Reddit penalizes link-heavy comments)
- Reference specific subreddits where each comment would fit

---

#### Quora Answer

**Format:** 300-500 word answer
**Tone:** Authoritative but approachable, answer-first
**Structure:**
- Direct answer in the first sentence (matches Quora's "answer the question" expectation)
- 2-3 supporting points from the article
- Brief personal context ("I work in [industry], so...")
- Link to full article as "further reading"

**Target questions:** Suggest 2-3 Quora questions this answer would fit (search Quora for related questions during generation).

**Adaptation notes:**
- Quora readers want the answer, not a teaser
- Include specific numbers, examples, or comparisons
- Avoid "check out our blog" language; instead: "I wrote a longer breakdown of this: [link]"

---

#### YouTube Video Script Outline (Optional)

**Format:** Script outline, not full script (150-300 words)
**Structure:**
- Hook (first 5 seconds): Restate the article's core insight as a question or bold claim
- Key points (3-5 bullets): What to cover, with timestamps
- CTA: Subscribe + link to article in description
- Suggested title and thumbnail text

**Only generate this if** the source article has strong visual/demonstrable content (comparisons, tutorials, teardowns).

---

### 3. Generate Distribution Checklist

After all versions are generated, output a checklist:

```markdown
## Distribution Checklist

### Publish
- [ ] LinkedIn article posted
- [ ] Medium article posted (include "Originally published on [blog]" + tags)
- [ ] Quora answer posted to [suggested questions]

### Reddit Engagement (Within 1-2 Weeks)
- [ ] Monitor target subreddits for relevant threads (use F5Bot if set up)
- [ ] Post comment draft 1 when matching thread appears
- [ ] Post comment draft 2 when matching thread appears
- [ ] Post comment draft 3 when matching thread appears

### Optional
- [ ] YouTube video script recorded and published
- [ ] Community tab / newsletter mention
```

## Output

Save all repurposed content to a single file:
- **File Location:** `repurposed/[original-slug]-repurposed-[YYYY-MM-DD].md`
- **Format:** Markdown with clear section headers for each platform

```
repurposed/
└── project-management-guide-repurposed-2026-04-10.md
```

## Quality Standards

- Each platform version must be genuinely adapted, not copy-pasted
- LinkedIn version emphasizes business value
- Medium version maintains depth
- Reddit comments must pass the "would a real person write this?" test
- Quora answer must directly answer a question
- All versions link back to the original article
- No product CTAs in Reddit or Quora versions (only helpful links)
- Total output should take 5-10 minutes to review and publish manually

## Required Context Files
- @context/brand-voice.md - Maintain brand voice in LinkedIn and Medium
- @context/reddit-strategy.md - Reddit engagement rules
- @context/ai-citation-targets.md - Platform priority reference
