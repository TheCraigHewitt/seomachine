# Research Trending Command

Identify topics gaining search interest NOW for time-sensitive content.

## Usage
`/research-trending`

## Process

```bash
python3 research_trending.py
```

1. Get trending queries from GSC (7d vs 30d comparison)
2. Filter to minimum 20 impressions
3. Enrich with search volume from DataForSEO
4. Calculate opportunity score: Growth rate (40%) + Volume (30%) + Position advantage (30%)
5. Determine urgency level
6. Output: `research/trending-YYYY-MM-DD.md`

## Output

Categorized by urgency:

- **CRITICAL** (+150% growth) -- Act within 1 week
- **HIGH** (+75% growth) -- Act within 2 weeks
- **MODERATE** (+30% growth) -- Act within 1 month

Per trend: growth %, current position, volume, opportunity score, action steps, timeline.

## Key Actions

**Already rank (position <=30) -- Quick Win:**
Update existing content, add trending angle, update title with current year. Timeline: 3-5 days.

**Don't rank (position >30) -- New Content:**
Create 2000+ word guide, publish within 3-7 days, promote on social.

## Next Steps

- `/research-serp [trending keyword]` for content requirements
- `/write [keyword]` to create content quickly
- Publish ASAP -- timing is critical

## Time & Cost

- **Time:** 1-2 min
- **API:** ~$0.20-0.50 with volume enrichment; free for GSC-only
- **Cadence:** Weekly (best on Monday before planning)

## Caveats

Not all trends sustain. Monitor 2-4 weeks to confirm durability. Skip off-niche and purely seasonal spikes.
