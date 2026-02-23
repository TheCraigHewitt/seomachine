# Content Architecture for Competitor Pages

Structure and maintain competitor data for scalable comparison pages.

## Directory Structure

```
competitor_data/
├── notion.md
├── airtable.md
├── monday.md
└── ...
```

---

## Competitor Data Template

```yaml
name: Notion
website: notion.so
tagline: "The all-in-one workspace"
founded: 2016
headquarters: San Francisco

# Positioning
primary_use_case: "docs + light databases"
target_audience: "teams wanting flexible workspace"
market_position: "premium, feature-rich"

# Pricing
pricing_model: per-seat
free_tier: true
free_tier_limits: "limited blocks, 1 user"
starter_price: $8/user/month
business_price: $15/user/month
enterprise: custom

# Features (rate 1-5)
features:
  documents: 5
  databases: 4
  project_management: 3
  collaboration: 4
  integrations: 3
  mobile_app: 3
  offline_mode: 2
  api: 4

# Strengths
strengths:
  - Extremely flexible and customizable
  - Beautiful, modern interface
  - Strong template ecosystem
  - Active community

# Weaknesses
weaknesses:
  - Can be slow with large databases
  - Learning curve for advanced features
  - Limited automations compared to dedicated tools
  - Offline mode is limited

# Best for / Not ideal for
best_for:
  - Teams wanting all-in-one workspace
  - Content-heavy workflows
  - Documentation-first teams
not_ideal_for:
  - Complex project management needs
  - Large databases (1000s of rows)
  - Enterprise with strict compliance

# Common complaints (from reviews)
common_complaints:
  - "Gets slow with lots of content"
  - "Hard to find things as workspace grows"
  - "Mobile app is clunky"

# Migration notes
migration_from:
  difficulty: medium
  data_export: "Markdown, CSV, HTML"
  what_transfers: "Pages, databases"
  what_doesnt: "Automations, integrations setup"
  time_estimate: "1-3 days for small team"
```

Use the same structure for your own product. Be honest.

---

## Page Generation

Each page pulls from centralized data:
- **[Competitor] Alternative**: competitor data + your data
- **[Competitor] Alternatives**: competitor data + your data + other alternatives
- **You vs [Competitor]**: your data + competitor data
- **[A] vs [B]**: both competitor data + your data

Update pricing once, it updates everywhere. Add a feature comparison once, it appears on all pages.

---

## Index Pages

### Alternatives Index (`/alternatives`)
1. Headline + intro on why people switch
2. List of all alternative pages (competitor name, one-line differentiator, link)
3. Aggregated switching reasons
4. CTA

### Comparisons Index (`/vs` or `/compare`)
1. Headline
2. "[Your Product] vs Competitors" section
3. "Head-to-Head Comparisons" section
4. CTA

**Best practices**: Keep updated when adding pages. Link bidirectionally (index <-> individual). Sort by search volume or alphabetically.

---

## Footer Navigation

Add comparison links to site footer for sitewide link equity.

**Minimum**: Link to `/alternatives` and `/vs` index pages.

**Recommended**: Dedicated footer columns per format with top 5-8 competitors by search volume, plus "View all" link. Only create columns for formats you have pages for.

Footer links matter because:
- Sitewide distribution passes link equity to comparison content.
- Helps search engines discover all comparison pages.
- Visitors evaluating your product find comparisons easily.
