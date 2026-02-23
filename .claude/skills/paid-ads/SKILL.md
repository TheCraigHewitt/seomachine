---
name: paid-ads
version: 1.0.0
description: "When the user wants help with paid advertising campaigns on Google Ads, Meta (Facebook/Instagram), LinkedIn, Twitter/X, or other ad platforms. Also use when the user mentions 'PPC,' 'paid media,' 'ad copy,' 'ad creative,' 'ROAS,' 'CPA,' 'ad campaign,' 'retargeting,' or 'audience targeting.' This skill covers campaign strategy, ad creation, audience targeting, and optimization."
---

# Paid Ads

Read `.claude/product-marketing-context.md` if it exists.

## Before Starting

Capture:
1. **Objective and target economics** (CPA, ROAS, volume).
2. **Offer and landing experience** (message match, page speed, conversion path).
3. **Audience and data assets** (customer lists, pixel events, CRM segments).
4. **Current baseline** (historical winners/losers, tracking quality).

## Platform Selection Guide

| Platform | Best For | Use When |
|----------|----------|----------|
| Google Ads | High-intent demand capture | Category/search intent already exists |
| Meta | Demand generation + retargeting | Strong creative iteration capability |
| LinkedIn | B2B role/account targeting | Deal value supports higher CPM/CPC |
| Twitter/X | Conversation-led awareness | Audience actively discusses category |
| TikTok | Top-of-funnel video reach | You can ship native short-form creative |

## Campaign Structure Best Practices

```text
Account
├── Campaign: [Objective]-[Audience]
│   ├── Ad Set: [Targeting variant]
│   │   ├── Ad A: [Hook/creative]
│   │   ├── Ad B: [Hook/creative]
│   │   └── Ad C: [Hook/creative]
```

### Naming Convention

```text
[Platform]_[Objective]_[Audience]_[Offer]_[Date]
META_Conv_Lookalike_FreeTrial_2026Q1
GOOG_Search_Brand_Demo_Ongoing
LI_LeadGen_CMOs_SaaS_Mar2026
```

### Budget Allocation
- **Testing phase**: Typical 70% proven / 30% tests.
- **Scaling phase**: increase winning budgets gradually (Typical 20-30% increments).

## Ad Copy Frameworks

Use concise framework selection in [references/ad-copy-templates.md](references/ad-copy-templates.md):
- PAS
- BAB
- Social proof lead
- Feature -> benefit bridge
- Direct response

## Audience Targeting

Use platform-specific targeting playbooks in [references/audience-targeting.md](references/audience-targeting.md).

Core rules:
- Build lookalikes from best customers, not all users.
- Segment retargeting by funnel stage.
- Exclude current customers and recent converters from prospecting.

## Creative Best Practices

### Image Ads
- One idea per creative
- Clear visual hierarchy
- Real product proof over stock-style visuals

### Video Ads (15-30 seconds)
1. Hook (0-3s)
2. Problem (3-8s)
3. Solution/proof (8-20s)
4. CTA (20-30s)

### Testing Hierarchy
1. Angle/concept
2. Hook/headline
3. Visual treatment
4. Body copy
5. CTA

## Campaign Optimization

### KPI by Objective

| Objective | Primary Metrics |
|-----------|-----------------|
| Awareness | CPM, reach, view rate |
| Consideration | CTR, CPC, engaged sessions |
| Conversion | CPA, ROAS, CVR |

### Optimization Levers
- **High CPA**: fix landing conversion, tighten audience, refresh offer/creative.
- **Low CTR**: test new hooks/angles, improve targeting-message fit.
- **High CPM**: broaden audience or adjust placements/creative relevance.

## Retargeting Strategy

| Funnel Stage | Audience | Message | Goal |
|--------------|----------|---------|------|
| Top | Content viewers/visitors | Education + proof | Move to consideration |
| Mid | Pricing/feature visitors | Comparison + case studies | Move to decision |
| Bottom | Trial/cart abandoners | Objection handling + urgency | Convert |

### Window and Exclusions
- Hot: 1-7 days
- Warm: 7-30 days
- Cold: 30-90 days
- Exclude customers, recent converters, low-intent bounces

## Reporting

Weekly review:
- Spend pacing vs plan
- CPA/ROAS trend
- Top and bottom ads
- Audience-level performance
- Frequency and fatigue
- Landing page CVR

Attribution:
- Platform-reported performance is directional.
- Compare with GA4 and blended CAC.

## Setup and Launch QA

Full platform setup checklists: [references/platform-setup-checklists.md](references/platform-setup-checklists.md)

### Universal Pre-Launch Checklist
- [ ] Conversion tracking verified with real test event
- [ ] Landing page message matches ad promise
- [ ] Mobile speed acceptable
- [ ] UTM parameters validated
- [ ] Targeting and exclusions reviewed
- [ ] Budget, schedule, and geo settings confirmed

## Common Mistakes

| Area | Mistake |
|------|---------|
| Strategy | Launching without reliable conversion tracking |
| Structure | Over-fragmenting budget across too many campaigns |
| Targeting | Missing exclusions and audience overlap checks |
| Creative | Running one ad too long without refresh |
| Budgeting | Large abrupt budget changes during learning |
