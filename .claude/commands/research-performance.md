# Research Performance Command

Categorize all content by traffic and rankings to prioritize optimization.

## Usage
`/research-performance`

## Process

```bash
python3 research_performance_matrix.py
```

Fetches GA4 data (90 days) + GSC rankings, calculates 180-day traffic trends, and categorizes into 4 quadrants:

1. **Stars** - High traffic + Good rankings -> Maintain & expand
2. **Overperformers** - High traffic + Poor rankings -> Improve SEO
3. **Underperformers** - Low traffic + Good rankings -> Fix CTR (title/meta) -- QUICK WINS
4. **Declining** - Low traffic + Poor rankings -> Refresh or redirect

Output: `research/performance-matrix-YYYY-MM-DD.md`

## Output

- Distribution across 4 quadrants
- Top performers per category
- Action steps per article with priority
- Expected vs actual traffic calculations

## Next Steps

- `/analyze-existing [URL]` for detailed content analysis
- Fix underperformer titles/meta first (low effort, high impact)
- Refresh declining stars to prevent traffic loss

## Time & Cost

- **Time:** 2-4 min
- **Requirements:** GA4 required, GSC recommended
- **Cost:** Free
- **Cadence:** Monthly, after major updates, or when traffic drops
