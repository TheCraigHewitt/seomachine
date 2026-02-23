# Performance Review Command

Analyze content performance and generate a prioritized queue of content actions.

## Usage
`/performance-review [days]`

## What This Command Does
1. Pulls data from GA4, GSC, and DataForSEO.
2. Finds opportunities across updates, rewrites, and new content.
3. Scores opportunities by expected ROI.
4. Outputs a ranked action queue with implementation guidance.

## Data Sources
- **Google Analytics 4**: traffic, engagement, conversion trends
- **Google Search Console**: impressions, clicks, CTR, average position
- **DataForSEO**: competitive ranks, SERP features, keyword metrics

## Opportunity Taxonomy

### Quick Wins
- Keywords ranking positions 11-20
- Prioritize by impressions + proximity to page 1 + commercial value

### Declining Content
- Pages with month-over-month traffic/ranking drops
- Prioritize by traffic at risk and severity

### Low CTR Opportunities
- High-impression pages with weak CTR
- Prioritize metadata/title improvements with expected click lift

### Trending Topics
- Rising demand queries not yet covered deeply
- Prioritize by growth velocity and business relevance

### Competitor Gaps
- Keywords competitors rank for where your company is weak/absent
- Prioritize by strategic fit + estimated upside

## Scoring Model (0-100)
Each opportunity uses:
- **Impact (50%)**: expected traffic/conversion upside
- **Effort (30%)**: time/resources/difficulty
- **Confidence (20%)**: data strength and trend stability

## Prerequisites

### 1) Configure credentials
Create and fill `data_sources/config/.env`:
```bash
cp data_sources/config/.env.example data_sources/config/.env
nano data_sources/config/.env
```

Required:
- GA4 property ID + service account JSON
- GSC site URL + credentials
- DataForSEO login + password

### 2) Install dependencies
```bash
pip install -r data_sources/requirements.txt
```

### 3) Test data connections
```bash
python data_sources/modules/google_analytics.py
python data_sources/modules/google_search_console.py
python data_sources/modules/dataforseo.py
```

## Output

### 1) Executive Summary
- analysis date + period
- top-line traffic/click/rank metrics
- key trend deltas

### 2) Priority Queue (Actionable Format)
Each item should include:
- opportunity type
- keyword/page
- current baseline (position/impressions/clicks)
- potential upside
- estimated effort
- recommended action
- opportunity score

Example format:
```text
1) Optimize "podcast analytics dashboard"
Type: Quick Win
Current Position: 12
Impressions: 5,400/month
Potential Impact: +450 clicks/month
Estimated Effort: 3 hours
Action: refresh section depth, update metadata, add internal links
Opportunity Score: 87/100
```

### 3) Detailed Opportunity Tables
- quick wins
- declining content
- low CTR pages
- trending topics
- competitor gaps

### 4) Implementation Roadmap
Week-by-week plan for execution order and ownership.

### 5) Success Metrics
KPIs to track before next review.

## File Management
Save report to:
`research/performance-review-[YYYY-MM-DD].md`

Example: `research/performance-review-2025-10-15.md`

## Integration with Other Commands
- Quick win page: `/analyze-existing [URL]` -> `/optimize [file]`
- Declining page: `/analyze-existing [URL]` -> `/rewrite [topic]`
- Trending gap: `/research [topic]` -> `/write [topic]`

## Recommended Cadence
- **Weekly**: top urgent queue review
- **Monthly**: full `/performance-review`
- **Quarterly**: portfolio and strategy reset

## Troubleshooting
- **No data returned**: verify credentials, IDs, and property access.
- **DataForSEO budget exceeded**: reduce frequency and review budget caps in `.env`.
- **Recommendations misaligned**: adjust scoring weights and apply business-priority overrides.

## Priority Queue Categories
Use explicit queue labels in output:
- `URGENT`: execute this week
- `HIGH`: execute this month
- `MEDIUM`: schedule after urgent/high completion

Each item should include owner and due week when possible.

## Example Weekly Execution Pattern
Week 1:
- 2-3 quick wins (position 11-20 pages)

Week 2:
- 1-2 declining pages (rewrite/refresh)

Week 3:
- low CTR metadata updates on high-impression pages

Week 4:
- one trending topic or competitor-gap content build

## Results Tracking Template
```markdown
## Action Taken (YYYY-MM-DD)
- Opportunity: [keyword/page]
- Changes: [summary]
- Target: [expected position/CTR/click lift]

## Follow-up (YYYY-MM-DD)
- New Position: [value]
- Click Delta: [value]
- Traffic Delta: [value]
- Keep / Iterate / Escalate
```

## Data Freshness Notes
- GA4 is typically near-daily.
- GSC usually lags by ~2-3 days.
- DataForSEO is API-driven and typically freshest.

Account for lag when evaluating short time windows.

## Escalation Criteria
Escalate HIGH to URGENT when:
- large traffic drop on a high-conversion page
- keyword dropped from page 1 to page 2 with rising impressions
- rapid CTR decline on a high-impression page

Document escalation reason in the queue entry. Keep scoring rubric consistent across periods; document any weight overrides when business priorities shift.
