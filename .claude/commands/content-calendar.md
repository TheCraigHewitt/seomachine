# Content Calendar Command

Generate a dated, month-long content calendar mapped to topic clusters, keywords, and publishing cadence using existing research data.

## Usage
`/content-calendar` - Generate calendar for current month (2 posts/week)
`/content-calendar [posts-per-week]` - Custom cadence (e.g., `/content-calendar 3`)
`/content-calendar [posts-per-week] [month]` - Custom cadence and month (e.g., `/content-calendar 3 next-month`)
`/content-calendar [posts-per-week] [month] [focus-cluster]` - Filter to a specific cluster (e.g., `/content-calendar 2 april "content marketing"`)

## What This Command Does

Bridges the gap between `/priorities` (what to work on) and execution (when to publish). Produces a dated publishing schedule with:
- Specific publish dates assigned to each piece
- Content categorized by type (quick win, rewrite, new article, trending)
- Week-by-week strategy (quick wins first, cluster building later)
- Exact commands to run for each piece
- Parking lot for next month's opportunities

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Posts per week | 2 | Number of pieces to publish each week |
| Month | Current month | Target month name or "next-month" |
| Focus cluster | None | Optional topic cluster filter |

## Process

### 1. Parse Parameters

Extract from user input:
- **Posts per week**: Number (default: 2). Calculate total pieces = posts_per_week × weeks in target month.
- **Target month**: Parse month name (e.g., "april", "next-month", "june"). Default to current month. Determine the year, first day, last day, and number of weeks.
- **Focus cluster**: Optional text filter. If provided, prioritize items matching this cluster.

### 2. Run Research Scripts

Check if today's reports already exist before running each script. Skip any script whose report for today is already in `research/`.

```bash
python3 research_quick_wins.py
```
Generates `research/quick-wins-YYYY-MM-DD.md`

```bash
python3 research_topic_clusters.py
```
Generates `research/topic-clusters-YYYY-MM-DD.md`

```bash
python3 research_performance_matrix.py
```
Generates `research/performance-matrix-YYYY-MM-DD.md`

```bash
python3 research_trending.py
```
Generates `research/trending-topics-YYYY-MM-DD.md`

Also check for recent competitor gap reports:
- Read `research/competitor-gaps-*.md` if any exist (use most recent)

**Important**: If a report for today already exists, skip that script to save API credits. Read the existing report instead.

### 3. Read and Parse All Reports

Read each generated report and extract:

**From Quick Wins:**
- Keywords ranking positions 11-20
- Current URLs (existing content)
- Opportunity scores, search volume, impressions
- Commercial intent ratings

**From Topic Clusters:**
- Cluster names and authority scores
- Weak clusters (biggest opportunities)
- Coverage gaps within each cluster
- Keywords per cluster

**From Performance Matrix:**
- Declining content (needs refresh)
- Underperforming content
- Content health categories

**From Trending Topics:**
- Rising search trends
- Time-sensitive opportunities
- Trend velocity scores

**From Competitor Gaps (if available):**
- Keywords competitors rank for that we don't
- Gap difficulty and volume data

### 4. Categorize Each Item

Assign every extracted opportunity to one of four content types:

**Quick Win Update** (Position 11-20, existing content)
- Has a ranking URL
- Needs optimization to move from page 2 to page 1
- Effort: Low-Medium
- Command: `/rewrite [topic]` or `/optimize [file]`

**Rewrite/Refresh** (Declining or underperforming content)
- Performance dropping over time
- Content is stale or outdated
- Effort: Medium
- Command: `/rewrite [topic]`

**New Article** (Gaps, cluster building, unranked opportunities)
- No existing content for this keyword
- Fills a cluster gap or competitor gap
- Effort: Medium-High
- Command: `/article [topic]` or `/write [topic]`

**Trending** (Time-sensitive, rising searches)
- Search volume increasing
- Seasonal or news-driven
- Effort: Medium (speed matters)
- Command: `/article [topic]`

**Deduplication**: If a keyword appears in multiple reports, keep the highest-priority categorization and note all data sources.

### 5. Build the Calendar

Assign items to specific dates within the target month, using these weekly strategies:

**Week 1: Quick Wins + Trending (Fastest ROI)**
- Prioritize quick win updates (low effort, high impact)
- Include any time-sensitive trending topics
- These show results fastest for early momentum

**Week 2: Mix of Updates + New Articles**
- Remaining quick wins
- Begin new article pipeline
- Balance effort across the week

**Week 3: Cluster-Focused (Topical Authority)**
- Group related pieces from the same topic cluster
- Build topical authority through cluster coverage
- Include cluster pillar pieces if needed

**Week 4+: Strategic New Articles + Rewrites**
- Longer-form new content targeting gaps
- Rewrites of declining content
- Competitor gap pieces

**Scheduling rules:**
- Spread posts evenly across the week (e.g., Mon/Thu for 2/week, Mon/Wed/Fri for 3/week)
- Never schedule two pieces from the same cluster in the same week (unless cluster-focused week)
- If a focus cluster was specified, weight 60%+ of slots toward that cluster
- Fill remaining slots with highest-opportunity items regardless of cluster

### 6. Write Output

Save the calendar to `research/content-calendar-YYYY-MM.md` where YYYY-MM is the target month.

## Output Format

```markdown
# Content Calendar: [Month YYYY]

**Generated**: YYYY-MM-DD
**Cadence**: [X] posts per week
**Total Pieces**: [N]
**Focus Cluster**: [cluster name or "None - balanced across all clusters"]
**Data Sources**: Quick Wins, Topic Clusters, Performance Matrix, Trending[, Competitor Gaps]

---

## Month Overview

| Week | Dates | Pieces | Strategy | Content Mix |
|------|-------|--------|----------|-------------|
| 1 | Mon DD - Sun DD | X | Quick Wins + Trending | 2 updates, 1 trending |
| 2 | Mon DD - Sun DD | X | Mixed | 1 update, 2 new |
| 3 | Mon DD - Sun DD | X | Cluster: [name] | 3 new (cluster) |
| 4 | Mon DD - Sun DD | X | Strategic | 1 rewrite, 2 new |

## Content Mix Summary

| Type | Count | Percentage |
|------|-------|------------|
| Quick Win Update | X | XX% |
| Rewrite/Refresh | X | XX% |
| New Article | X | XX% |
| Trending | X | XX% |

---

## Week 1: [Mon DD - Sun DD] — Quick Wins + Trending

### [Day], [Month] [DD] — [Topic/Title]
- **Keyword**: [primary keyword]
- **Type**: Quick Win Update
- **Current Position**: 14 | **Volume**: 1,200/mo
- **Cluster**: [cluster name]
- **Effort**: Low
- **Rationale**: Ranking on page 2 with high impressions. Small optimization moves this to page 1.
- **Data Source**: Quick Wins Report
- **Command**: `/rewrite [topic]` then `/optimize [file]`

### [Day], [Month] [DD] — [Topic/Title]
- **Keyword**: [primary keyword]
- **Type**: Trending
- **Trend Velocity**: +45% | **Volume**: 890/mo
- **Cluster**: [cluster name]
- **Effort**: Medium
- **Rationale**: Rising search trend with low competition. First-mover advantage window.
- **Data Source**: Trending Report
- **Command**: `/article [topic]`

---

## Week 2: [Mon DD - Sun DD] — Mixed

[Same format per entry...]

---

## Week 3: [Mon DD - Sun DD] — Cluster Focus: [Cluster Name]

[Same format, entries grouped by cluster...]

---

## Week 4: [Mon DD - Sun DD] — Strategic

[Same format...]

---

## Parking Lot (Next Month)

Items that didn't fit this month but should be scheduled next:

| Priority | Topic | Keyword | Type | Volume | Cluster | Why Deferred |
|----------|-------|---------|------|--------|---------|--------------|
| 1 | [topic] | [keyword] | New Article | 2,400 | [cluster] | Lower priority than scheduled items |
| 2 | [topic] | [keyword] | Rewrite | 1,100 | [cluster] | Non-urgent refresh |
| ... | | | | | | |

---

## Cluster Progress Tracker

| Cluster | Current Authority | Articles Existing | Articles Planned (This Month) | Expected Authority After |
|---------|-------------------|-------------------|-------------------------------|--------------------------|
| [cluster 1] | Weak (32/100) | 3 | 4 | Moderate (~55) |
| [cluster 2] | Moderate (58/100) | 7 | 2 | Strong (~70) |
| [cluster 3] | Strong (78/100) | 12 | 1 | Strong (~82) |

---

## Quick Reference

| Date | Topic | Type | Cluster | Command |
|------|-------|------|---------|---------|
| Mon, [Month] [DD] | [topic] | Quick Win | [cluster] | `/rewrite [topic]` |
| Thu, [Month] [DD] | [topic] | Trending | [cluster] | `/article [topic]` |
| Mon, [Month] [DD] | [topic] | New Article | [cluster] | `/article [topic]` |
| ... | | | | |

---

## Next Steps

1. Start with Week 1 items — these deliver fastest results
2. Run `/research [topic]` before each new article for deeper keyword research
3. Use `/priorities` mid-month to reassess based on new data
4. Re-run `/content-calendar [posts-per-week] [next-month]` at month end to plan ahead
```

## File Management

The command reads from:
- `research/quick-wins-YYYY-MM-DD.md`
- `research/topic-clusters-YYYY-MM-DD.md`
- `research/performance-matrix-YYYY-MM-DD.md`
- `research/trending-topics-YYYY-MM-DD.md`
- `research/competitor-gaps-*.md` (most recent, if available)

The command creates:
- `research/content-calendar-YYYY-MM.md` (month-based naming since it covers a full month)

## Integration

After running `/content-calendar`:
- Use the exact commands listed for each calendar entry
- Run `/priorities` mid-month to validate direction
- Re-run `/content-calendar` at month end to plan the next month
- Items in the parking lot automatically become candidates for next month's calendar

## When to Run

- **Monthly**: Generate next month's calendar in the last week of the current month
- **After `/priorities`**: Turn prioritized list into a dated schedule
- **Team planning**: Share the calendar with writers and editors for assignment
- **Quarterly planning**: Run for 3 consecutive months to build a content roadmap
