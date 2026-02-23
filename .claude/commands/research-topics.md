# Research Topics Command

Analyze topical authority by clustering keywords into related topics.

## Usage
`/research-topics`

## Process

```bash
python3 research_topic_clusters.py
```

1. Fetch all ranking keywords from GSC (90 days)
2. Cluster keywords using ML (TF-IDF + K-means) or pattern-based fallback
3. Calculate authority score (0-100) per cluster based on coverage, position, demand
4. Identify coverage gaps via DataForSEO
5. Prioritize weak clusters with high demand
6. Output: `research/topic-clusters-YYYY-MM-DD.md`

## Output

Per cluster: authority score, keyword count, avg position, impressions, clicks, coverage gaps.

**Authority Levels:**
- **Strong:** Topics you dominate -- maintain & expand
- **Moderate:** Partial coverage -- strengthen with 3-5 articles
- **Weak:** BIGGEST OPPORTUNITY -- build comprehensive clusters
- **Minimal:** Major gaps

**Weak Cluster Detail:** Top 5 current keywords, 8-10 coverage gaps with volume, recommended action (build 8-12 article cluster).

## Strategy

1. **Build Weak Clusters:** Select top 2-3 with highest demand. Create pillar page (3000+ words) + 8-12 supporting articles. Internal link everything to pillar.
2. **Maintain Strong Clusters:** Keep fresh, expand with advanced topics.
3. **Strengthen Moderate Clusters:** Add 3-5 articles to reach strong authority.

## Next Steps

- `/research-serp [gap keyword]` for each identified gap
- Create pillar page first, then cluster content
- `/write [keyword]` for each piece

## Time & Cost

- **Time:** 2-3 min
- **API:** ~$0.50 with coverage gap enrichment; free for clustering only
- **Cadence:** Monthly, before content planning, or when entering new niche
