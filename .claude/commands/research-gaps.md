# Research Gaps Command

Identify content gaps where competitors rank but you don't.

## Usage
`/research-gaps`

## What This Command Does

Analyzes 7 competitors to find keywords they rank for (top 20) that you don't rank for at all:
- **Direct Competitors**: Configured in `config/competitors.json` or passed as arguments
- **Content Competitors**: Industry blogs and media sites in your niche

For each gap:
- Filters out branded/irrelevant keywords
- Scores opportunity based on volume, difficulty, and intent
- Determines content type needed (listicle, how-to, guide)
- Prioritizes by potential impact

## Process

Execute the competitor gap analysis:
```bash
python3 research_competitor_gaps.py
```

This will:
1. Fetch your current ranking keywords from GSC
2. Analyze each competitor's top 20 ranking keywords
3. Identify gaps (they rank, you don't)
4. Enrich with search volume, difficulty, SERP features
5. Score and prioritize opportunities
6. Generate report: `research/competitor-gaps-YYYY-MM-DD.md`

## Output

The report includes:
- Top 20 content gap opportunities
- Priority level (CRITICAL/HIGH/MEDIUM)
- Competitor intel (who ranks, at what position)
- Keyword metrics (volume, difficulty, CPC)
- Search intent and content type needed
- Specific action steps for each gap

## Integration

After running `/research-gaps`:
- Use `/research-serp [keyword]` to analyze what ranks
- Use `/write [keyword]` to create content brief
- Focus on CRITICAL/HIGH priority gaps first

## Time & Cost

**Time:** 3-5 minutes
**API Cost:** ~$1-3 (DataForSEO) - analyzes ~300-500 competitor keywords

## When to Run

- **Monthly**: Full competitive landscape review
- **When entering new topic**: Find what's missing
- **Before content planning**: Identify proven opportunities
