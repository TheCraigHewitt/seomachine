# Research Gaps Command

Identify content gaps where competitors rank but you don't.

## Usage
`/research-gaps`

## Process

```bash
python3 research_competitor_gaps.py
```

Analyzes 7 competitors' top 20 keywords against your GSC rankings. For each gap, scores opportunity by volume, difficulty, and intent.

Steps:
1. Fetch your ranking keywords from GSC
2. Analyze each competitor's top 20 keywords
3. Identify gaps (they rank, you don't)
4. Enrich with volume, difficulty, SERP features
5. Score and prioritize opportunities
6. Output: `research/competitor-gaps-YYYY-MM-DD.md`

Competitors configured in `config/competitors.json` or passed as arguments.

## Output

- Top 20 gap opportunities with priority (CRITICAL/HIGH/MEDIUM)
- Competitor intel (who ranks, at what position)
- Keyword metrics (volume, difficulty, CPC)
- Search intent and recommended content type
- Action steps per gap

## Next Steps

- `/research-serp [keyword]` to analyze top results
- `/write [keyword]` to create content
- Focus on CRITICAL/HIGH gaps first

## Time & Cost

- **Time:** 3-5 min
- **API:** ~$1-3 (DataForSEO, ~300-500 keywords)
- **Cadence:** Monthly, before content planning, or when entering new topics
