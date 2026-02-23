---
name: schema-markup
version: 1.0.0
description: When the user wants to add, fix, or optimize schema markup and structured data on their site. Also use when the user mentions "schema markup," "structured data," "JSON-LD," "rich snippets," "schema.org," "FAQ schema," "product schema," "review schema," or "breadcrumb schema." For broader SEO issues, see seo-audit.
---

# Schema Markup

Implement schema.org markup for rich results. JSON-LD format only.

## Initial Assessment

Check `.claude/product-marketing-context.md` first. Ask only for missing scope.

Capture:
1. Page type and primary content.
2. Current schema state and errors.
3. Target rich results and business value.

---

## Core Principles

1. **Accuracy first** -- markup must match visible page content.
2. **JSON-LD only** -- place in `<head>` or end of `<body>`.
3. **Follow Google guidelines** -- only supported types, no spam.
4. **Validate before deploy** -- test, monitor Search Console, fix errors fast.

---

## Common Schema Types

| Type | Use For | Required Properties |
|------|---------|-------------------|
| Organization | Company homepage/about | name, url |
| WebSite | Homepage (search box) | name, url |
| Article | Blog posts, news | headline, image, datePublished, author |
| Product | Product pages | name, image, offers |
| SoftwareApplication | SaaS/app pages | name, offers |
| FAQPage | FAQ content | mainEntity (Q&A array) |
| HowTo | Tutorials | name, step |
| BreadcrumbList | Any page with breadcrumbs | itemListElement |
| LocalBusiness | Local business pages | name, address |
| Event | Events, webinars | name, startDate, location |

**Complete JSON-LD examples**: See [references/schema-examples.md](references/schema-examples.md)

---

## Multiple Schema Types

Combine with `@graph`:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", ... },
    { "@type": "WebSite", ... },
    { "@type": "BreadcrumbList", ... }
  ]
}
```

---

## Validation

**Tools**:
- Google Rich Results Test: https://search.google.com/test/rich-results
- Schema.org Validator: https://validator.schema.org/
- Search Console Enhancements reports

**Common errors**: missing required properties, invalid date/URL/enum values, markup-content mismatch.

---

## Implementation by Stack

| Stack | Approach |
|-------|----------|
| Static HTML | JSON-LD in template, use includes for reuse |
| React / Next.js | Schema component, server-side rendered |
| WordPress | Yoast / Rank Math / Schema Pro plugin, or theme mods |

---

## Output

1. Full JSON-LD code block.
2. Testing checklist: validates, no errors, matches content, all required properties.

---

## Related Skills

- **seo-audit**: Overall SEO including schema review
- **programmatic-seo**: Templated schema at scale
