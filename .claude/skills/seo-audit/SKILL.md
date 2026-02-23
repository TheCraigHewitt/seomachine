---
name: seo-audit
version: 1.0.0
description: When the user wants to audit, diagnose, or prioritize SEO issues across a site or page set. Use for requests like "SEO audit," "technical SEO review," "why are we not ranking," "on-page SEO check," or "SEO health check." For large-scale page generation, use programmatic-seo. For structured data implementation, use schema-markup.
---

# SEO Audit

Diagnose ranking blockers, quantify impact, and prioritize fixes.

## Initial Assessment

Check `.claude/product-marketing-context.md` first. Ask only for missing scope.

Capture:
1. Site type and business goal.
2. Priority pages/keywords.
3. Recent migrations or major changes.
4. Available data (Search Console, analytics, crawls).

---

## Audit Framework

### Priority Order

1. Crawlability and indexation
2. Technical foundations
3. On-page optimization
4. Content quality
5. Authority and links

---

## Technical SEO Audit

### Crawlability

- Validate `robots.txt` (no accidental blocks).
- Validate XML sitemap (canonical, indexable URLs only).
- Keep important pages within ~3 clicks.
- Find orphan pages and crawl traps.

### Indexation

- Compare expected pages vs indexed pages.
- Check noindex, canonical conflicts, redirect chains, soft 404s.
- Enforce one URL version (HTTPS, hostname, trailing slash policy).

### Core Web Vitals and Speed

Targets: LCP < 2.5s, INP < 200ms, CLS < 0.1

Check: TTFB and caching, image/compression strategy, JS/CSS weight and execution, CDN coverage and font loading.

### Mobile and Security

- Responsive parity between desktop and mobile content.
- Tap targets and viewport correctness.
- HTTPS everywhere, no mixed content.

### URL Hygiene

- Descriptive lowercase paths with hyphens.
- Minimize parameters and duplicate URL states.

---

## On-Page SEO Audit

### Titles and Meta Descriptions

- Unique per page, intent + primary term aligned, click-worthy without stuffing.

### Heading and Content Structure

- One clear H1, logical H2/H3 hierarchy, first section confirms intent match.

### Content Quality Signals

- Sufficient depth for query intent, no thin/duplicative pages, strong internal links to key pages.

### Images and Media

- Descriptive filenames and alt text, compressed modern formats, lazy-loading.

### Keyword Mapping

- One primary target per page, detect cannibalization, fill obvious topic gaps.

---

## Content Quality Assessment

Evaluate E-E-A-T signals:
- Experience: first-hand insight and practical examples.
- Expertise: accurate details and qualified authorship.
- Authoritativeness: external references and brand citations.
- Trustworthiness: transparent policies, contact details, secure UX.

---

## Site-Type Watchouts

| Site Type | Frequent Issues |
|-----------|-----------------|
| SaaS | Thin feature pages, weak comparison coverage, weak product-content linking |
| E-commerce | Duplicate product/category content, faceted duplication, schema gaps |
| Content Sites | Outdated articles, cannibalization, poor cluster linking |
| Local Business | Inconsistent NAP, weak location pages, missing local schema |

---

## Output Format

### Executive Summary
- Overall health state, top 3-5 issues, quick wins.

### Findings Format

Per issue:

```text
Issue:
Impact: High | Medium | Low
Evidence:
Fix:
Priority: P1 | P2 | P3
```

### Prioritized Action Plan
1. Indexation blockers
2. High-impact technical and on-page fixes
3. Quick wins
4. Longer-term improvements

---

## References

- [AI Writing Detection](references/ai-writing-detection.md)
- [AEO & GEO Patterns](references/aeo-geo-patterns.md)

---

## Related Skills

- **programmatic-seo**: Build scalable SEO page systems
- **schema-markup**: Add or repair structured data
- **analytics-tracking**: Measure SEO outcomes
