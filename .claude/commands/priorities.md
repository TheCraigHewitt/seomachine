# Priorities Command

Build a ranked content roadmap from SEO opportunity data.

## Usage
- `/priorities` -> comprehensive mode (all modules, ~10 min)
- `/priorities quick` -> quick wins only (~2 min)

## Modes

### Comprehensive Mode
Runs 5 modules:
1. Quick Wins (positions 11-20)
2. Competitor Gaps
3. Performance Matrix
4. Topic Clusters
5. Trending Topics

Produces a unified ranked roadmap.

### Quick Mode
Runs only quick wins analysis for immediate execution.

## Process

### 1) Execute Quick Wins Module
```bash
python research_quick_wins.py
```

### 2) Parse Output
Read `research/quick-wins-YYYY-MM-DD.md` and extract highest-scoring opportunities.

### 3) Classify Opportunity Type
For each candidate, classify as:
- **EXISTING CONTENT UPDATE**
  - ranking URL exists on your site
  - likely optimization/refresh opportunity
- **NEW CONTENT CREATION**
  - no meaningful ranking URL
  - requires net-new content asset

### 4) Build Top 10 Priority List
Rank by opportunity score and strategic fit.

## Required Fields Per Item
- Keyword
- Current position (or `Not ranking`)
- Search volume
- Impressions (30d)
- Current clicks
- Potential clicks
- Commercial intent
- Opportunity score (0-100)
- Priority (HIGH/MEDIUM/LOW)
- Ranking URL (for existing-content items)

## Action Playbooks

### Existing Content Update
- Review top competitors
- Fill missing sections/gaps
- Refresh statistics/examples
- Improve keyword placement and metadata
- Add/improve internal links
- Target position: 5-7

### New Content Creation
- Research top ranking competitors
- Build full outline with target depth
- Integrate keyword + linking strategy
- Create optimized metadata
- Target position: Top 10

## Output Format
Create `research/priorities-YYYY-MM-DD.md` with:
- Top 10 ranked opportunities
- Existing vs new content breakdown
- Total current vs potential click summary
- Recommended execution order

Example item format:
```text
1) [Keyword] - EXISTING CONTENT UPDATE | Priority: HIGH
Current Position: 13
Search Volume: 2,400/month
Impressions (30d): 1,850
Current Clicks: 45
Potential Clicks: 102 (+57)
Commercial Intent: High
Opportunity Score: 87/100
Ranking URL: https://yoursite.com/example
Action: update content depth, refresh metadata, strengthen internal links
```

## Follow-up Commands
- `/analyze-existing [URL]`
- `/write [keyword]`
- `/optimize [file]`

## Summary Section (Required)
At the end of `research/priorities-YYYY-MM-DD.md`, include:
```text
Content Type Breakdown:
- Existing Content Updates: [count]
- New Content Creation: [count]

Combined Potential:
- Current Monthly Clicks: [total]
- Potential Monthly Clicks: [total]
- Incremental Opportunity: [+delta]
```

## Execution Guidance
Recommended rollout:
1. Start with top 3 existing-content updates (fastest return).
2. Start research on top 2 new-content opportunities in parallel.
3. Review ranking movement weekly and re-rank remaining items.

## Integration Notes
- Existing item -> run `/analyze-existing [URL]` before edits.
- New item -> run `/research [keyword]` before `/write [keyword]`.
- Any finished draft -> run `/optimize [file]` before publish workflow.

Include generation timestamp and input data window on every report.
