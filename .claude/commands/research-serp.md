# Research SERP Command

Deep SERP analysis for a specific keyword to understand what Google rewards.

## Usage
`/research-serp "keyword phrase"`

## Process

```bash
python3 research_serp_analysis.py "your target keyword"
```

Fetches top 20 organic results from DataForSEO, analyzes content patterns in top 10:

1. Detect content types from titles
2. Fetch word counts per result
3. Identify SERP features (featured snippet, PAA, video, etc.)
4. Analyze search intent
5. Assess competitive difficulty
6. Generate content brief
7. Output: `research/serp-analysis-[keyword].md`

## Output

**Content Requirements:**
- Recommended word count (top 10 average + 10%)
- Dominant content type and distribution

**SERP Features:** Featured snippet opportunity, PAA questions, video/image requirements

**Content Brief:** Target specs, must-have elements, recommended structure, freshness requirements

**Competitive Analysis:** Domain authority mix, difficulty assessment, timeframe expectations

## Next Steps

- Use content brief to guide `/write [keyword]`
- Match recommended structure and length

## Time & Cost

- **Time:** 1-2 min per keyword
- **API:** ~$0.02/keyword (DataForSEO)
- **Run before:** Creating new content, major updates, or when unsure of format
