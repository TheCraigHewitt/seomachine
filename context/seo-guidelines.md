# SEO Guidelines for Freaking Nomads Content

2026 SEO standards optimized for both traditional Google search and AI search engines (ChatGPT, Perplexity, Gemini). Every article must pass all checklist items before publishing.

---

## Content Length

| Content Type | Target Length |
|---|---|
| Destination guides | 2,500–4,000 words |
| Visa guides | 2,000–3,500 words |
| Gear/product reviews | 1,500–3,000 words |
| Best-of listicles | 2,000–4,000 words |
| Trend/opinion pieces | 1,200–2,000 words |
| Café/workspace guides | 1,500–2,500 words |

**Rule**: No padding to hit word counts. Every section earns its place. Better to publish 1,800 substantive words than 3,000 padded words.

---

## Keyword Strategy

### Research Requirements
Before writing any article:
1. Identify primary keyword (long-tail preferred — genuine search intent)
2. Check search volume and keyword difficulty via DataForSEO
3. Analyze top 10 SERP results for format, depth, and gaps
4. Identify 3–5 secondary/LSI keywords
5. Pull "People Also Ask" questions for FAQ section

### Keyword Placement
Primary keyword must appear in:
- [ ] H1 title (naturally, not forced)
- [ ] First 100 words
- [ ] At least 2 H2 subheadings
- [ ] Meta title (within first 60 characters)
- [ ] Meta description
- [ ] URL slug

### Long-Tail Focus
Prioritize long-tail keywords with clear intent over high-volume broad terms:
- ✅ "digital nomad visa Finland requirements 2026" (clear intent, qualified audience)
- ✅ "best eSIM for China digital nomads" (specific, buyer intent)
- ❌ "digital nomad" (too broad, no ranking chance)
- ❌ "travel insurance" (dominated by aggregators)

### Keyword Density
- Primary: ~1% density — never force it, write naturally
- Secondary: Sprinkled naturally throughout
- LSI keywords: Integrated where relevant
- **Stuffing check**: Run `keyword_analyzer.py` before publishing

---

## Content Structure

### Heading Hierarchy
- **H1**: One per article. Include primary keyword near the start. Keep compelling — it's the SERP title too.
- **H2**: 4–8 main sections. At least 2 should contain keyword variations. Write them as questions or clear statements readers scan for.
- **H3**: Subsections under H2. Never jump H2 → H4.

### Article Structure for Freaking Nomads Content

```
# [H1: Primary Keyword + Compelling Promise]

[Hook: 1–3 sentences. Personal story, gut-punch question, or bold statement. Never "In today's world..."]

[Context: What this article covers and who it's for. Max 1 paragraph.]

## [H2: Most common question first — e.g., "Does [Country] Have a Digital Nomad Visa?"]
[Direct answer in first sentence. No teasing.]

## [H2: Core Section 1 — requirements, costs, process, etc.]
### [H3: Subsection if needed]

## [H2: Core Section 2]
...

## [H2: Pros and Cons / What to Expect / Our Assessment]
[Equal weight to positives and negatives]

## [H2: Frequently Asked Questions]
[4–6 PAA-sourced questions, answered concisely]

[Closing: 1–2 paragraphs. Honest verdict. Single CTA.]
```

---

## Meta Elements

### Meta Title
- Length: 50–60 characters
- Include primary keyword near the start
- Format options:
  - `[Primary Keyword]: [Honest Take or Benefit]`
  - `[Destination] Digital Nomad Guide: What You Actually Need to Know`
  - `[Product] Review: Is It Worth It for Nomads?`
- **Never**: Keyword-stuffed titles, clickbait without delivery, Castos-era podcast examples

### Meta Description
- Length: **≤155 characters** (strict — gets truncated otherwise)
- Include primary keyword naturally
- State the specific value the article delivers
- End with implicit or explicit call to action
- Formula: `[Specific thing article covers]. [Who it's for]. [What they'll learn/get].`
- Example: "Finland has no dedicated digital nomad visa — but its Self-Employment Visa works. Requirements, costs, and 4-month timeline explained."

### URL Slug
- Lowercase, hyphens only
- 3–5 words, include primary keyword
- Match existing FN URL pattern: `/[keyword-phrase]/` (no `/blog/` prefix)
- Examples from live site: `/finland-digital-nomad-visa/`, `/holafly-china-esim-review/`, `/nomadic-living-costs/`

---

## Internal Linking

### Requirements (MANDATORY)
- **Minimum**: 3 internal links per article
- **Optimal**: 4–6 internal links
- Always check `context/internal-links-map.md` for available URLs before writing

### Anchor Text Rules
- ✅ Descriptive: "our guide to the Finland digital nomad visa"
- ✅ Natural: "we covered the best eSIMs for China"
- ❌ Generic: "click here," "read more," "this article"
- ❌ Exact-match spam: using the same anchor text every time for the same URL

### Placement
- First link within first 300 words where natural
- Distributed throughout — never clustered in one section
- Max 2 links per paragraph
- Context must be relevant — never force a link

---

## External Linking

### Requirements (MANDATORY)
- **Minimum**: 2 external links per article
- Purpose: Establish EEAT, support claims with authoritative sources

### What to Link To
- Government visa portals (official source, always preferred for visa guides)
- Official country immigration pages
- Established nomad resources (Nomad List for data, NomadGossip for community context)
- Scientific/medical studies when relevant (health/insurance content)
- Manufacturer/product official pages for gear reviews
- **Never**: Random blogs with no authority, sites with thin content, competitors without good reason

### Attributes
- No `rel="nofollow"` needed for editorial links
- Affiliate/sponsored links: `rel="sponsored"` — disclose upfront in article
- External links open in new tab where appropriate

---

## EEAT (Experience, Expertise, Authoritativeness, Trustworthiness)

This is critical for ranking in 2026. Google and AI search engines heavily weight EEAT signals.

### Experience (the most important E in 2026)
- **Every article must be attributed to a real author** — Irene, Luca, or a named contributor
- Author must have verifiable first-person experience with the topic
- State the experience upfront: "I spent three months in China testing this eSIM" / "I've lived in Mazunte as a nomad"
- Reference specific, real-world details: café names, exact speeds, actual prices paid
- Never write "many nomads find..." — use "I found..." or cite a named source

### Expertise
- Include specific data: speeds, costs, processing times, coverage percentages
- Cite official sources for visa and legal information
- Acknowledge limitations of knowledge honestly

### Authoritativeness
- Author bio linking to author profile/page
- Press mentions where relevant (Forbes, Condé Nast, Reader's Digest)
- Community credentials: "Freaking Nomads has 1,433+ community members"
- Cross-link to related authoritative FN content

### Trustworthiness
- Disclose affiliate relationships upfront (not buried)
- State limitations: "We haven't personally visited every destination on this list"
- Update dates shown prominently on evergreen content
- Never claim universal truth: "This worked for us — your mileage may vary"
- Acknowledge product downsides without softening

---

## FAQ Section (MANDATORY)

Every article must include a FAQ section.

### Requirements
- Minimum 4 questions, maximum 8
- Source questions from Google's "People Also Ask" for the primary keyword
- Also include questions from the article's own H2 headings that are question-format
- Each answer: 40–80 words, clear and direct
- Implement FAQPage schema (see Schema section below)

### FAQ Format
```markdown
## Frequently Asked Questions

### Does [Country] have a digital nomad visa?
[Direct answer in 1–2 sentences. Then 1–2 sentences of supporting detail.]

### How much does [Country]'s digital nomad visa cost?
[Specific number(s). No vague "it depends" without specifics.]

### [Next question from PAA]
[Answer]
```

---

## Schema Markup

All articles should include schema recommendations in the draft frontmatter. The developer/CMS handles implementation, but the content must flag which schemas apply.

### Required for All Articles
```
Schema: Article (author, datePublished, dateModified, publisher)
Schema: FAQPage (all FAQ questions and answers)
Schema: BreadcrumbList (Home > Category > Article)
```

### Additional by Content Type
- **Destination guides**: Add `TravelGuide` or `Place` schema where applicable
- **Product reviews**: Add `Review` schema with rating if a rating is given
- **Best-of listicles**: Add `ItemList` schema
- **Visa guides**: Add `HowTo` schema for the application process steps

---

## AI Search Optimization (2026 Priority)

Content is now being surfaced by ChatGPT, Perplexity, Gemini, and other AI search engines. Optimize for extraction:

### Structure for AI extraction
- **Define terms clearly in the first mention**: "A digital nomad visa (a visa specifically designed for remote workers earning income from abroad) allows..."
- **Use direct Q&A format**: H2 headings as questions, direct answers in first sentence
- **Include structured data**: Tables, numbered lists, and bullet points extract better than prose paragraphs
- **Factual claims must be citable**: Every stat should have a source linked. AI engines check sourcing.
- **Summaries at top**: For longer guides, include a "Quick Answer" or "TL;DR" box near the top

### What AI engines surface from FN content
Based on observed FN content structure, these elements get extracted:
- Cost tables and monthly budget breakdowns
- Visa requirements tables (validity, cost, processing time)
- Product comparison tables
- FAQ answers
- Direct "Does X have a digital nomad visa?" answers

---

## AI Detection (MANDATORY POLICY)

**Every article must be checked for AI detection before publishing.**

- **Target**: Score below 40% on AI detection tools
- **If above 40%**: Humanization pass is mandatory — do not publish until score drops
- **Humanization pass includes**:
  - Replace any banned words (see brand-voice.md)
  - Add specific personal details, real prices, location names
  - Vary sentence length more aggressively (shorter punchy sentences)
  - Add a rhetorical question or two
  - Add a fragment or casual aside where natural
  - Remove any passive constructions
  - Replace "moreover/furthermore/in conclusion" with natural transitions or new paragraphs

**Tools to use**: GPTZero, Originality.ai, or similar. The humanization step is not optional.

---

## Readability

- **Reading level**: 8th–10th grade (Flesch-Kincaid) — check with `readability_scorer.py`
- **Sentence length**: Vary. Mix short (5–10 words) with medium (15–20 words). Max 30 words before breaking.
- **Paragraph length**: 2–4 sentences. No walls of text.
- **Subheadings**: Every 300–400 words
- **Lists**: Use for sequential steps, comparisons, specs — not as a substitute for real analysis

---

## Image Optimization

- **File names**: Descriptive, keyword-include. `finland-digital-nomad-visa-requirements.jpg` not `IMG_1234.jpg`
- **Alt text**: Describe what the image shows + keyword where natural. Max 125 characters.
- **Compression**: Optimize before upload (WebP preferred)
- **Placement**: After the concept is explained, not before

---

## Content Refresh Triggers

Refresh an article when:
- It's 12+ months old AND ranks in positions 8–20 (opportunity to push higher)
- Visa information has changed (legislation, costs, eligibility)
- Product has been updated or discontinued
- A competitor has outranked us with fresher content
- GSC shows declining impressions over 3+ months

---

## Pre-Publishing SEO Checklist

### Keyword & Content
- [ ] Primary keyword identified, researched (volume + difficulty)
- [ ] Long-tail keyword with clear intent
- [ ] Keyword in H1, first 100 words, 2+ H2s, meta title, meta description, URL
- [ ] 3–5 secondary keywords naturally integrated
- [ ] No keyword stuffing — `keyword_analyzer.py` run
- [ ] Content matches search intent (informational, commercial, navigational)
- [ ] Provides unique value vs. top 10 competitors

### Structure
- [ ] Hook in first 1–3 sentences
- [ ] Single H1 with primary keyword
- [ ] 4–8 H2 sections
- [ ] Proper H1 > H2 > H3 hierarchy
- [ ] FAQ section with 4–6 PAA questions
- [ ] Conclusion with honest verdict

### EEAT
- [ ] Real author attributed (Irene, Luca, or named contributor)
- [ ] Author's personal experience stated upfront
- [ ] Specific data included (prices, speeds, dates, processing times)
- [ ] External authoritative sources linked (minimum 2)
- [ ] Affiliate disclosure if applicable (upfront, not buried)

### Meta & Technical
- [ ] Meta title 50–60 characters, keyword included
- [ ] Meta description ≤155 characters, keyword + value prop + implicit CTA
- [ ] URL slug: short, keyword-included, matches FN URL pattern
- [ ] Schema markup flagged: Article + FAQPage (minimum)
- [ ] Images: descriptive filenames + alt text

### Links
- [ ] 3+ internal links with descriptive anchor text
- [ ] 2+ external authority links
- [ ] All links functional

### Quality & Compliance
- [ ] AI detection score below 40% — humanization pass completed if needed
- [ ] No banned words (check brand-voice.md list)
- [ ] Active voice throughout
- [ ] Cons stated plainly, not buried
- [ ] Reading level 8th–10th grade
- [ ] Proofread — no typos or grammar errors

---

**Remember**: SEO serves readers, not algorithms. The best-ranking Freaking Nomads article is the one that most honestly and specifically answers what a digital nomad actually needs to know.
