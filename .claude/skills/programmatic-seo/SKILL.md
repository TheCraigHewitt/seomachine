---
name: programmatic-seo
version: 1.0.0
description: When the user wants to create SEO-driven pages at scale using templates and data. Also use when the user mentions "programmatic SEO," "template pages," "pages at scale," "directory pages," "location pages," "[keyword] + [city] pages," "comparison pages," "integration pages," or "building many pages for SEO." For auditing existing SEO issues, see seo-audit.
---

# Programmatic SEO

Build SEO-optimized pages at scale using templates and data. Rank, provide value, avoid thin content penalties.

## Initial Assessment

Check `.claude/product-marketing-context.md` first. Ask only for missing scope.

Capture:
1. Product/service and conversion goal.
2. Search patterns, potential page count, volume distribution.
3. Who ranks now and what their pages look like.

---

## Core Principles

1. **Unique value per page** -- not just swapped variables in a template.
2. **Data defensibility hierarchy**: proprietary > product-derived > user-generated > licensed > public.
3. **Subfolders, not subdomains**: `yoursite.com/templates/resume/` not `templates.yoursite.com/resume/`.
4. **Match search intent** -- pages answer what people actually search for.
5. **Quality over quantity** -- 100 great pages beat 10,000 thin ones.
6. **No doorway pages, keyword stuffing, or duplicate content.**

---

## The 12 Playbooks

| Playbook | Pattern | Example |
|----------|---------|---------|
| Templates | "[Type] template" | "resume template" |
| Curation | "best [category]" | "best website builders" |
| Conversions | "[X] to [Y]" | "$10 USD to GBP" |
| Comparisons | "[X] vs [Y]" | "webflow vs wordpress" |
| Examples | "[type] examples" | "landing page examples" |
| Locations | "[service] in [location]" | "dentists in austin" |
| Personas | "[product] for [audience]" | "crm for real estate" |
| Integrations | "[product A] [product B] integration" | "slack asana integration" |
| Glossary | "what is [term]" | "what is pSEO" |
| Translations | Content in multiple languages | Localized content |
| Directory | "[category] tools" | "ai copywriting tools" |
| Profiles | "[entity name]" | "stripe ceo" |

**Detailed playbook implementation**: See [references/playbooks.md](references/playbooks.md)

### Choosing Your Playbook

| If you have... | Consider... |
|----------------|-------------|
| Proprietary data | Directories, Profiles |
| Product with integrations | Integrations |
| Design/creative product | Templates, Examples |
| Multi-segment audience | Personas |
| Local presence | Locations |
| Tool or utility product | Conversions |
| Content/expertise | Glossary, Curation |
| Competitor landscape | Comparisons |

Layer multiple playbooks: "Best coworking spaces in San Diego" = Curation + Locations.

---

## Implementation Framework

### 1. Keyword Pattern Research
- Identify repeating structure and variables.
- Validate: aggregate volume, head vs. long tail distribution, trend direction.

### 2. Data Requirements
- Identify sources (first-party, scraped, licensed, public).
- Define update frequency.

### 3. Template Design
- Header with target keyword.
- Unique intro (not just variable swaps).
- Data-driven sections with conditional content.
- Related pages / internal links.
- CTAs matched to intent.

### 4. Internal Linking
- Hub and spoke: category hub -> individual pages -> cross-links between related spokes.
- No orphan pages. XML sitemap for all pages. Breadcrumbs with structured data.

### 5. Indexation Strategy
- Prioritize high-volume patterns.
- Noindex very thin variations.
- Separate sitemaps by page type.

---

## Pre-Launch Checklist

- [ ] Each page provides unique value and answers search intent.
- [ ] Unique titles and meta descriptions per page.
- [ ] Proper heading structure and schema markup.
- [ ] Page speed acceptable.
- [ ] Connected to site architecture, no orphan pages.
- [ ] In XML sitemap, crawlable, no conflicting noindex.

**Post-launch**: Track indexation rate, rankings, traffic, engagement, conversion. Watch for thin content warnings, ranking drops, manual actions.

---

## Common Mistakes

- Thin content (just swapping city names in identical copy).
- Keyword cannibalization across pages.
- Over-generation for zero-demand terms.
- Poor or outdated data.
- Pages built for Google, not users.

---

## Related Skills

- **seo-audit**: Audit programmatic pages after launch
- **schema-markup**: Structured data at scale
- **competitor-alternatives**: Comparison page frameworks
