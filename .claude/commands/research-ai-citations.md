# Research AI Citations Command

Generate high-commercial-intent prompts for a topic, cluster them, and create an audit template for tracking which sources AI tools cite. This is the prompt-driven research counterpart to traditional keyword research.

## Usage
`/research-ai-citations [topic or keyword]`

**Examples:**
- `/research-ai-citations "project management tools"`
- `/research-ai-citations "email marketing platform"`
- `/research-ai-citations "CRM for small businesses"`

## Why This Matters

Traditional SEO research asks: "What keywords do people search on Google?"
AI citation research asks: "What prompts do people type into ChatGPT/Perplexity, and which sources get cited in the answers?"

These are different questions with different answers. A page can rank #1 on Google but never get cited by ChatGPT if the content isn't structured for AI consumption, or if competitors dominate the directories and listicles that AI tools actually pull from.

This command bridges that gap.

## Process

### Step 1: Generate Prompt List (100+ prompts)

Generate a comprehensive list of high-commercial-intent prompts that a potential customer might ask AI tools about this topic.

#### Prompt Categories

**A. Direct Recommendation Prompts (Highest Priority)**
These trigger AI to search the web and cite sources:
- "What is the best [topic]?"
- "Top [topic] for [use case]"
- "Best [topic] for [audience]"
- "Recommend a [topic] for [specific need]"

**B. Comparison Prompts**
- "[Product A] vs [Product B] for [topic]"
- "Compare [options] for [topic]"
- "Which [topic] is better for [use case]?"
- "Alternatives to [competitor] for [topic]"

**C. Feature-Specific Prompts**
- "Best [topic] with [feature]"
- "[Topic] that supports [capability]"
- "Which [topic] has [specific feature]?"

**D. Use-Case Prompts**
- "Best [topic] for [industry/niche]"
- "[Topic] for [specific scenario]"
- "How to [achieve goal] with [topic]"

**E. Pricing/Value Prompts**
- "Cheapest [topic]"
- "Free [topic] options"
- "[Topic] pricing comparison"
- "Is [product] worth it for [topic]?"

**F. Migration/Switching Prompts**
- "How to switch from [competitor] to [alternative]"
- "Best [competitor] alternative"
- "[Competitor] replacement for [topic]"

#### Generation Process

1. Start with the core topic keyword
2. Generate 15-20 prompts per category above
3. Add audience modifiers: beginners, small businesses, enterprises, startups, freelancers, agencies
4. Add platform/ecosystem modifiers relevant to your niche
5. Add intent modifiers: free, cheap, best, easiest, most reliable, fastest
6. Cluster into 5-10 topic groups

### Step 2: Cluster Prompts into Topics

Group the generated prompts into logical clusters. Each cluster represents a topic area where your brand should be visible.

**Output format:**

```markdown
## Prompt Clusters

### Cluster 1: [Name] (e.g., "General Recommendations")
**Core intent:** [What the user is really trying to decide]
**Prompts:**
1. [prompt]
2. [prompt]
3. [prompt]
...

### Cluster 2: [Name] (e.g., "Feature-Specific Comparisons")
**Core intent:** [What the user is really trying to decide]
**Prompts:**
1. [prompt]
2. [prompt]
...
```

### Step 3: Sample Audit (Run 10-15 Key Prompts)

For the highest-priority prompts (pick 10-15 across clusters), manually run them through ChatGPT and/or Perplexity and document:

1. **Was your brand mentioned?** (Yes/No, and in what position)
2. **Which sources were cited?** (List URLs)
3. **Which competitors were mentioned?** (List with positions)
4. **What type of sources dominated?** (Directories, listicles, brand sites, Reddit, etc.)
5. **What information did AI include about each recommendation?** (Features, pricing, pros/cons)

**If AI tools are not available for live testing**, note this in the output and proceed with steps 1-2 plus the audit template for manual execution later.

### Step 4: Gap Analysis

Based on the audit (or projected based on knowledge of the landscape):

1. **Where is your brand present?** List prompts/clusters where you appear
2. **Where is your brand absent?** List prompts/clusters where you should appear but don't
3. **Which sources dominate?** Rank the most-cited domains
4. **Off-page targets:** Which directories, listicles, or platforms should you be added to?
5. **On-page gaps:** Which blog pages need to be created or updated to serve these prompts?
6. **Content format gaps:** Are competitors winning with comparison tables, FAQs, or structured data that you lack?

### Step 5: Action Plan

Generate a prioritized action plan:

```markdown
## Action Plan

### Quick Wins (This Week)
- [ ] [Action]: [Expected impact]
- [ ] [Action]: [Expected impact]

### Content to Create/Update
- [ ] [Article topic]: Targets cluster [X], addresses gap [Y]
- [ ] [Article topic]: Targets cluster [X], addresses gap [Y]

### Off-Page Actions
- [ ] Get listed on [directory]: Cited [N] times across audit
- [ ] Outreach to [listicle URL]: Author is [name], approach via [channel]
- [ ] Update [platform] profile: [What to add/change]

### Monitor
- [ ] Re-run audit in [timeframe] to measure changes
- [ ] Track these prompts: [list of highest-priority prompts]
```

## Output

Save to: `research/ai-citations-[topic-slug]-[YYYY-MM-DD].md`

```markdown
# AI Citation Audit: [Topic]

**Date:** [YYYY-MM-DD]
**Topic:** [topic]
**Total Prompts Generated:** [count]
**Prompts Audited:** [count]

## Prompt Clusters
[Clustered prompt list from Step 2]

## Audit Results
[Results from Step 3, or audit template for manual execution]

## Gap Analysis
[Analysis from Step 4]

## Action Plan
[Prioritized actions from Step 5]

## Update ai-citation-targets.md?
[Note any changes that should be made to context/ai-citation-targets.md based on findings]
```

## Integration with Other Commands

- **Before `/article`**: Run `/research-ai-citations` first to understand which prompts the article should target and which sources to reference
- **After `/publish-draft`**: Run `/repurpose` to distribute the article across citation surfaces identified here
- **Quarterly**: Re-run for core topic clusters to track changes in AI citation patterns

## Required Context Files
- @context/ai-citation-targets.md - Existing citation surface inventory
- @context/competitor-analysis.md - Competitor landscape
- @context/features.md - Product feature set (for accurate prompt generation)
