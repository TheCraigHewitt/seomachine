---
name: content-strategy
version: 1.0.0
description: When the user wants to plan a content strategy, choose what to publish, map topic clusters, or prioritize content opportunities. Use for requests like "content strategy," "what should we write about," "content ideas," "blog strategy," "topic clusters," or "content planning." For drafting pages/posts, see copywriting. For technical SEO diagnosis, see seo-audit.
---

# Content Strategy

Plan content that grows qualified traffic and pipeline. Classify every piece as searchable, shareable, or both.

## Before Planning

Check `.claude/product-marketing-context.md` first. Reuse existing context; ask only for what is missing.

### Gather Inputs

1. Business: product, ICP, category, primary content KPI.
2. Buyers: pre-purchase questions, objections, support-ticket themes, voice-of-customer phrasing.
3. Current state: existing content performance, publishing capacity, available formats.
4. Market: competitors, adjacent alternatives, obvious coverage gaps.

---

## Searchable vs Shareable

Prioritize searchable first, then shareable.

### Searchable Content

- Target one query cluster per asset.
- Match intent exactly.
- Put target terms in title, headings, intro, and URL.
- Answer follow-up questions in the same piece.
- Add proof, examples, and authoritative references.

### Shareable Content

- Lead with a novel claim, original data, or contrarian insight.
- Use evidence, not opinion-only takes.
- Include real stories and implementation detail.
- Tie content to current market conversations.

---

## Content Types

### Searchable Types

**Use-case content** -- Formula: `[persona] + [use case]`. Examples: "Project management for designers", "Task tracking for engineering teams".

**Hub and spoke** -- Use when a topic needs layered depth.

```text
/topic (hub)
├── /topic/subtopic-1 (spoke)
├── /topic/subtopic-2 (spoke)
└── /topic/subtopic-3 (spoke)
```

Build hub first, add spokes, cross-link. Use `/blog` for most posts. Reserve dedicated hub URLs for major evergreen resources only.

**Template libraries** -- Target high-intent searches ("template", "checklist"). Deliver standalone value before product pitch.

### Shareable Types

- Thought leadership: name hidden problems, challenge assumptions, provide evidence.
- Data-driven content: product insights, public-data analysis, or original research.
- Expert roundups: one sharp question, multiple credible viewpoints.
- Case studies: Challenge -> Solution -> Results -> Lessons.
- Meta content: transparent breakdowns of wins, losses, and decisions.

For scaled page production, use **programmatic-seo**.

---

## Content Pillars and Topic Clusters

Define 3-5 pillars your brand can sustain for 12+ months.

### Pillar Selection Criteria

- Fits product value and ICP problems.
- Has measurable demand (search and/or social).
- Supports multiple subtopics and formats.
- Can include unique proof (data, stories, examples).

### Cluster Shape

```text
Pillar Topic (Hub)
├── Subtopic Cluster 1
│   ├── Article A / B / C
├── Subtopic Cluster 2
│   ├── Article D / E / F
└── Subtopic Cluster 3
    ├── Article G / H / I
```

---

## Keyword Research by Buyer Stage

| Stage | Modifiers | Typical Format |
|-------|-----------|----------------|
| Awareness | what is, how to, guide, introduction | educational posts, glossaries |
| Consideration | best, top, vs, alternatives, comparison | listicles, comparisons |
| Decision | pricing, reviews, demo, trial, buy | pricing pages, competitor pages |
| Implementation | template, example, tutorial, setup | templates, how-tos |

---

## Content Ideation Sources

### 1. Keyword Exports (Ahrefs, Semrush, GSC)
- Group into clusters, label buyer stage and intent.
- Flag quick wins (low difficulty + relevant demand).
- Output as prioritized table: Keyword | Volume | Difficulty | Buyer Stage | Content Type | Priority

### 2. Calls and Transcripts
- Extract recurring questions, objections, competitor mentions.
- Capture direct quotes for copy and headline language.

### 3. Surveys
- Group open-text responses by theme. Prioritize 30%+ mention topics.

### 4. Community Research
Queries: `site:reddit.com [topic]`, `site:quora.com [topic]`. Extract FAQs, misconceptions, debates, buyer terminology.

### 5. Competitor Content
- Crawl blog/resource hubs. Identify repeated topics, stale pages, missed angles.
- Prioritize "better version" opportunities.

### 6. Sales and Support Inputs
- Pull themes from objection logs, support tickets, feature requests.
- Translate repeated friction into high-intent content.

---

## Prioritizing Content Ideas

Score each idea with weighted factors:

| Factor | Weight |
|--------|--------|
| Customer Impact | 40% |
| Content-Market Fit | 30% |
| Search Potential | 20% |
| Resource Load | 10% |

Scoring template:

| Idea | Impact (40%) | Fit (30%) | Search (20%) | Resources (10%) | Total |
|------|-------------|-----------|--------------|-----------------|-------|
| Topic A | 8 | 9 | 7 | 6 | 8.0 |
| Topic B | 6 | 7 | 9 | 8 | 7.1 |

---

## Output Format

### 1. Content Pillars
- 3-5 pillars with rationale, subtopic clusters, and product relevance.

### 2. Priority Backlog
Per item: working title, searchable/shareable/both, format type, target keyword + buyer stage, evidence from research.

### 3. Cluster Map
Internal linking paths between hubs and spokes.

---

## Related Skills

- **copywriting**: Drafting individual pages/posts
- **seo-audit**: Technical and on-page diagnosis
- **programmatic-seo**: Scaled page production
- **competitor-alternatives**: Comparison and alternative-page strategy
