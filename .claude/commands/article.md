# Article Command

A unified content creation pipeline that produces comprehensive, SEO-optimized articles through mandatory research, strategic planning, and section-by-section writing.

## Usage
`/article [topic]`

**Examples:**
- `/article "Best Project Management Tools for Small Teams"`
- `/article "Content Marketing Strategy Guide 2025"`
- `/article "How to Migrate from Competitor to Your Product"`

## What This Command Does

Creates high-quality articles by enforcing a 4-step pipeline where **research is mandatory, not optional**:

```
STEP 1: SERP Analysis           → See what Google rewards TODAY
STEP 2: Social Research         → Mine Reddit + YouTube for real insights
STEP 3: Article Planning        → Section-by-section strategy
STEP 4: Section Writing         → Write/edit each section individually
```

This prevents the "AI knows everything" trap that produces generic content matching competitors instead of beating them.

## When to Use This vs /write

| Scenario | Command |
|----------|---------|
| Comprehensive new article | `/article` |
| Competitive topics | `/article` |
| Topics where you need to beat existing content | `/article` |
| Quick drafts from existing research | `/write` |
| Simple updates to existing content | `/write` |

---

## STEP 1: SERP Analysis (MANDATORY)

**You MUST research before writing. No exceptions.**

### Process

1. **Search the Target Keyword**
   Use WebSearch to find what's currently ranking:
   ```
   WebSearch: "[topic] industry" OR "[topic] industrying"
   ```

2. **Analyze Top 5 Ranking Articles**
   For each top-ranking article, use WebFetch and document:

   | Element | What to Capture |
   |---------|-----------------|
   | **Structure** | H2 headings, section order, content type |
   | **Word Count** | Approximate length |
   | **Gaps** | Topics covered superficially (<150 words) |
   | **Missing Angles** | Perspectives not addressed |
   | **Unsupported Claims** | Statements without data/sources |
   | **Outdated Info** | Old statistics, deprecated tools |
   | **What They Do Well** | Strong sections to match |

3. **Build Competitor Gap Blueprint**
   Document opportunities where your brand content can beat, not match:
   - Gaps found in all competitors (must-fill)
   - Unique angles no one covers
   - Data needed to be more specific
   - Outdated info to update with 2025 data

### Output
Save to: `research/serp-analysis-[topic-slug]-[YYYY-MM-DD].md`

```markdown
# SERP Analysis: [Topic]

**Date**: [YYYY-MM-DD]
**Keyword**: [target keyword]
**Search Intent**: [informational/commercial/transactional]

## Top Ranking Articles

### 1. [Article Title] - [Domain]
- URL: [url]
- Word Count: ~[count]
- Structure: [H2 headings list]
- Strengths: [what they do well]
- Gaps: [what they miss]
- Outdated: [old info found]

[Repeat for top 5]

## Google-Validated Structure
Based on what's ranking, these sections appear essential:
1. [Common H2 found across multiple articles]
2. [Another common section]
...

## Competitor Gap Blueprint

### MUST-FILL GAPS (found in 3+ competitors)
- [Gap 1]: [How to address]
- [Gap 2]: [How to address]

### DIFFERENTIATION OPPORTUNITIES
- [Unique angle 1]
- [Unique angle 2]

### DATA NEEDED
- [Specific statistic to find]
- [Expert quote needed]

### OUTDATED INFO TO UPDATE
- [Old stat] → Need 2025 version
```

---

## STEP 2: Social Research (MANDATORY)

**The best insights aren't in SEO content - they're in Reddit threads and YouTube tutorials.**

### Reddit Research (Visit 5 Actual Threads)

1. **Search Reddit**
   ```
   WebSearch: site:reddit.com [topic] industry
   WebSearch: site:reddit.com r/industrying [topic]
   ```

2. **Visit 5 Promising Threads**
   Use WebFetch on each thread URL. Extract:

   | Element | What to Look For |
   |---------|------------------|
   | **OP's Question** | The specific problem/question |
   | **Top Comments** | Upvoted solutions and advice |
   | **Pain Points** | Frustrations users express |
   | **Success Stories** | Real outcomes with details |
   | **Debates** | Different perspectives |
   | **Recommendations** | What the community endorses |
   | **Real Language** | How actual users talk about this |

3. **Extract Quotable Insights**
   Pull specific quotes that can inform (or be used in) the article.

### YouTube Research (Analyze 5 Videos)

1. **Search YouTube**
   ```
   WebSearch: site:youtube.com [topic] industry tutorial
   WebSearch: site:youtube.com [topic] industry review
   ```

2. **Analyze 5 Video Pages**
   Use WebFetch on each video page. Extract:

   | Element | What to Look For |
   |---------|------------------|
   | **Title & Description** | What they cover |
   | **View Count** | Engagement signal |
   | **Topics Covered** | Main points discussed |
   | **Gaps** | What they don't cover well |
   | **Comments** | What viewers ask about |

### Output
Save to: `research/social-research-[topic-slug]-[YYYY-MM-DD].md`

```markdown
# Social Research: [Topic]

**Date**: [YYYY-MM-DD]

## Reddit Insights

### Thread 1: [Title]
- URL: [url]
- OP's Question: "[quote]"
- Key Insight: [summary]
- Quotable: "[specific quote that could inform article]"

[Repeat for 5 threads]

### Pain Points Identified
- [Pain point 1]
- [Pain point 2]

### Success Stories Found
- [Story with specific details]

### Real User Language
- Users say "[phrase]" instead of "[what competitors say]"

## YouTube Insights

### Video 1: [Title] - [Channel]
- URL: [url]
- Views: [count]
- Topics Covered: [list]
- Gaps: [what they miss]
- Top Comment Theme: [what viewers ask]

[Repeat for 5 videos]

### Content Gaps in Video
- [Topic tutorials don't cover well]

### Expert Takes
- [Notable opinion from creator]

## Synthesis: Unique Insights for Article

### Insights NOT Available in SEO Content
1. [Unique insight from social research]
2. [Another unique insight]

### Questions to Answer (from real users)
1. [Real question from Reddit/YouTube]
2. [Another real question]

### Story Seeds (for mini-stories)
- [Story possibility based on real user experience]

### Language to Use
- Use "[real user phrase]" instead of "[generic SEO phrase]"
```

---

## STEP 3: Article Planning

**Create a section-by-section plan before writing.**

### Process

1. **Merge Research**
   Combine:
   - SERP analysis (structure that ranks)
   - Competitor gaps (opportunities to beat)
   - Social research (unique insights)
   - your brand context (features, brand voice)

2. **Create Google-Validated Structure**
   - Include sections that appear in multiple top-ranking articles
   - Add sections to fill identified gaps
   - Order for logical reader flow

3. **Assign Section Details**
   For each section, specify:

   | Element | Purpose |
   |---------|---------|
   | **Type** | intro / body-how-to / body-comparison / body-explanation / faq / conclusion |
   | **Word Target** | Based on competitor depth + gap filling |
   | **Strategic Angle** | What unique perspective we bring |
   | **Engagement Hook** | How this section captures attention |
   | **Knowledge Gaps** | Which competitor gaps this fills |
   | **Unique Data** | Social research insights to include |
   | **Internal Links** | Which your brand pages to link |
   | **CTA** | soft / medium / strong (if applicable) |
   | **Mini-Story** | Whether to place a story here |

4. **Plan Engagement Distribution**
   - Mini-stories: Early, middle, near-end (2-3 total)
   - CTAs: First 500 words (soft), middle (medium), end (strong)
   - Featured snippet opportunities: FAQ, definitions

### Output
Save to: `research/article-plan-[topic-slug]-[YYYY-MM-DD].md`

```markdown
# Article Plan: [Topic]

**Date**: [YYYY-MM-DD]
**Total Word Target**: [count]
**Primary Keyword**: [keyword]
**Secondary Keywords**: [list]

## Meta Elements
- **Title Options**:
  1. [Option 1]
  2. [Option 2]
  3. [Option 3]
- **Meta Description**: [150-160 chars]
- **URL Slug**: /blog/[slug]

## Section Plan

### 1. Introduction
- **Type**: intro
- **Word Target**: 200
- **Hook Strategy**: [question / scenario / statistic / bold statement]
- **APP Elements**: [Agree point, Promise, Preview]
- **Mini-Story**: [Yes - place opening scenario here]
- **CTA**: soft (within first 500 words)
- **Unique Data**: [Insight from social research to include]

### 2. [H2 Title]
- **Type**: body-explanation
- **Word Target**: 300
- **Strategic Angle**: [What unique perspective]
- **Knowledge Gap**: [Which competitor gap this fills]
- **Internal Links**: [your brand page to link]
- **Unique Data**: [Social insight to include]

### 3. [H2 Title]
- **Type**: body-how-to
- **Word Target**: 400
- **Strategic Angle**: [Unique angle]
- **Knowledge Gap**: [Gap being filled]
- **Mini-Story**: [Yes - real user scenario]

[Continue for all sections...]

### N. FAQ
- **Type**: faq
- **Word Target**: 200
- **Questions from Research**:
  1. [Real question from Reddit]
  2. [Another real question]
  3. [Question competitors don't answer]
  4. [Featured snippet opportunity]
- **Featured Snippet**: Yes

### N+1. Conclusion
- **Type**: conclusion
- **Word Target**: 200
- **CTA**: strong
- **Mini-Story**: [Optional - reinforcing story]

## Engagement Map

| Element | Location |
|---------|----------|
| Mini-Story 1 | Introduction |
| Mini-Story 2 | Section [X] |
| Mini-Story 3 | Conclusion (optional) |
| CTA (soft) | Section 1 or 2 |
| CTA (medium) | Section [X] |
| CTA (strong) | Conclusion |

## Gap-to-Section Mapping

| Competitor Gap | Section Addressing It |
|----------------|----------------------|
| [Gap 1] | Section [X] |
| [Gap 2] | Section [Y] |

## Social Insight Mapping

| Unique Insight | Where Used |
|----------------|------------|
| [Insight 1] | Section [X] |
| [Insight 2] | Section [Y] |
```

---

## STEP 4: Section-by-Section Writing

**Write each section individually to maintain quality.**

### Why Section-by-Section?
- Long-form AI writing degrades in quality toward the end
- Each section gets focused attention
- Each section gets its own editing pass
- Maintains consistent quality throughout

### Section Types & Specialized Approaches

#### Introduction
**Requirements:**
- Hook (NOT generic opening - use question/scenario/stat/bold statement)
- APP Formula: Agree, Promise, Preview
- Primary keyword in first 100 words
- Trust signal
- 150-250 words

**Do NOT open with:**
- "[Product category] is..."
- "When it comes to..."
- "If you're looking for..."
- "In today's world..."

#### Body: How-To
**Requirements:**
- Numbered steps for sequential processes
- Each step actionable and specific
- Time estimates where helpful
- Common mistakes to avoid
- 250-400 words per section

#### Body: Comparison
**Requirements:**
- Balanced (acknowledge competitor strengths)
- Data tables for key metrics
- Specific prices/features
- "Best for" recommendations
- 300-400 words per section

#### Body: Explanation
**Requirements:**
- Progressive complexity (simple → advanced)
- Analogies for complex concepts
- Examples with specifics
- 250-400 words per section

#### FAQ
**Requirements:**
- 4-6 questions from research (real user questions)
- 40-60 word answers (featured snippet optimized)
- Direct answer first, then context
- 200-300 words total

#### Conclusion
**Requirements:**
- NOT just a summary - add value
- 3-5 key takeaways as actionable items
- Clear next steps ("This week:", "This month:")
- Strong CTA with risk reversal
- Empowering, forward-looking close
- 150-250 words

### Writing Process Per Section

For each section in the plan:

1. **Write Draft**
   - Use section-specific requirements above
   - Include planned unique data/insights from research
   - Follow word target
   - Apply planned engagement hook

2. **Edit Pass**
   - Remove AI phrases ("In today's", "It's important to note", "When it comes to")
   - Replace vague words with specifics ("many" → "73%")
   - Check paragraph length (max 4 sentences)
   - Vary sentence rhythm (mix 5-10 word + 15-25 word)
   - Add conversational devices (contractions, questions, parenthetical asides)
   - Verify active voice

3. **Verify Requirements**
   - Section-specific criteria met
   - Planned insights included
   - Word target within ±10%

### Assembly

After all sections are written and edited:

1. **Combine Sections**
   - Assemble in planned order
   - Check transitions between sections
   - Verify internal link placement
   - Confirm CTA distribution

2. **Add Meta Elements**
   ```markdown
   ---
   Meta Title: [50-60 chars]
   Meta Description: [150-160 chars]
   Primary Keyword: [keyword]
   Secondary Keywords: [list]
   URL Slug: /blog/[slug]
   Word Count: [count]
   Internal Links: [list]
   External Links: [list]
   ---
   ```

3. **Generate Checklists**

   **SEO Checklist:**
   - [ ] Primary keyword in H1
   - [ ] Primary keyword in first 100 words
   - [ ] Primary keyword in 2+ H2 headings
   - [ ] Keyword density 1-2%
   - [ ] 3-5+ internal links
   - [ ] 2-3 external authority links
   - [ ] Meta title 50-60 chars
   - [ ] Meta description 150-160 chars
   - [ ] 2000+ words

   **Engagement Checklist:**
   - [ ] Hook (not generic opening)
   - [ ] APP Formula in intro
   - [ ] 2-3 mini-stories with names/details/outcomes
   - [ ] 2-3 contextual CTAs
   - [ ] First CTA within 500 words
   - [ ] No paragraphs > 4 sentences
   - [ ] Varied sentence rhythm

   **Research Integration Checklist:**
   - [ ] Addresses 3+ competitor gaps
   - [ ] Includes 5+ social research insights
   - [ ] Uses real user language
   - [ ] Answers questions from Reddit/YouTube
   - [ ] Updates outdated info with 2025 data

### Output
Save to: `drafts/[topic-slug]-[YYYY-MM-DD].md`

---

## Post-Writing Quality Loop

After saving the draft:

### 1. Scrub AI Patterns
```
/scrub drafts/[filename].md
```
Removes invisible Unicode watermarks and AI telltale patterns.

### 2. Score Content Quality
```bash
python data_sources/modules/content_scorer.py drafts/[filename].md
```

**Score Threshold: 70+**

| Dimension | Weight |
|-----------|--------|
| Humanity/Voice | 30% |
| Specificity | 25% |
| Structure Balance | 20% |
| SEO Compliance | 15% |
| Readability | 10% |

### 3. Auto-Revise if Needed
If score < 70:
1. Review `priority_fixes` from scorer
2. Apply top 3-5 fixes
3. Re-score
4. Repeat once more if needed
5. If still < 70 after 2 iterations → move to `review-required/`

### 4. Run Optimization Agents
After passing quality threshold:
- `content-analyzer` agent
- `seo-optimizer` agent
- `meta-creator` agent
- `internal-linker` agent
- `keyword-mapper` agent

---

## Complete Output Structure

```
research/
├── serp-analysis-[topic]-[date].md         # SERP research
├── social-research-[topic]-[date].md       # Reddit/YouTube insights
└── article-plan-[topic]-[date].md          # Section-by-section plan

drafts/
├── [topic]-[date].md                       # Final article
├── content-analysis-[topic]-[date].md      # Content analyzer output
├── seo-report-[topic]-[date].md            # SEO optimizer output
├── meta-options-[topic]-[date].md          # Meta creator output
├── link-suggestions-[topic]-[date].md      # Internal linker output
└── keyword-analysis-[topic]-[date].md      # Keyword mapper output
```

---

## Required Context Files

Before writing, review these context files:
- @context/brand-voice.md - your brand tone and messaging
- @context/style-guide.md - Formatting rules
- @context/seo-guidelines.md - SEO requirements
- @context/internal-links-map.md - Linking targets
- @context/features.md - your brand product information
- @context/writing-examples.md - Style reference

---

## Quality Standards

### Research Standards
- Top 5 competitor articles analyzed
- 5 Reddit threads visited (actual pages, not snippets)
- 5 YouTube videos analyzed
- Competitor gaps documented
- Social insights synthesized

### Content Standards
- 2000-3000+ words
- Proper H1/H2/H3 hierarchy
- 3-5 internal links
- 2-3 external authority links
- Compelling hook (not generic)
- 2-3 mini-stories with specifics
- 2-3 contextual CTAs
- FAQ with real user questions
- Quality score 70+

### Differentiation Standards
- Addresses 3+ competitor gaps
- Includes 5+ unique social insights
- Uses real user language (not SEO-speak)
- Updates outdated competitor info
- Provides depth where competitors are thin
