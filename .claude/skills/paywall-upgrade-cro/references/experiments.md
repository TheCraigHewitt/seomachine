# Paywall Experiment Ideas

Prioritize tests that change either trigger quality or clarity of value. Track a primary conversion metric plus guardrails (`retention`, `refunds`, `support burden`).

## Trigger and Gate Design

| Test | Hypothesis | Primary Metric |
|------|------------|----------------|
| Trigger at feature attempt vs. trigger after generic time delay | In-context need produces higher upgrade intent | Paywall CTR |
| Hard gate vs. soft gate preview | Soft gate can preserve trust while maintaining upgrade intent | Upgrade completion |
| Usage-limit prompt at 80% vs. 100% of cap | Early warning reduces surprise and improves conversion | Upgrade rate at cap |
| Trial reminders at 7/3/1 days vs. 1 day only | Staggered reminders improve trial-to-paid conversion | Trial conversion rate |

---

## Value and Pricing Presentation

| Test | Hypothesis | Primary Metric |
|------|------------|----------------|
| Benefit-led copy vs. feature-led copy | Outcome framing increases perceived value | Upgrade CTR |
| Single recommended plan vs. full comparison table | Guided choice reduces decision fatigue | Checkout starts |
| Annual savings in dollars vs. percentage | Concrete savings framing increases annual adoption | Annual plan share |
| Personalized usage summary vs. generic paywall copy | Usage-based relevance improves conversion | Upgrade completion |
| "Cancel anytime" / guarantee near CTA vs. absent | Risk reduction copy lowers hesitation | Checkout completion |

---

## Frequency and Dismissal Rules

| Test | Hypothesis | Primary Metric |
|------|------------|----------------|
| 1 prompt/session vs. multiple prompts/session | Frequency cap improves long-term conversion quality | 30-day paid conversion |
| Cool-down 1 day vs. 7 days after decline | Longer cool-down may reduce annoyance and improve later acceptance | Re-exposed upgrade rate |
| Dismiss options (`Not now` vs. `Remind me tomorrow`) | Better decline UX increases future re-engagement | Return-to-upgrade rate |

---

## Personalization and Segmentation

| Test | Hypothesis | Primary Metric |
|------|------------|----------------|
| Highlight most-used locked feature vs. static feature list | Relevance improves perceived necessity | Paywall CTR |
| Power-user paywall vs. casual-user paywall copy | Segment-specific messaging lifts conversion by cohort | Segment upgrade rate |
| B2B messaging (team productivity) vs. B2C messaging (personal output) | Audience-aligned value framing increases conversion | Upgrade completion |

---

## Recommended Core Metrics

- Paywall impressions
- Paywall CTA click-through
- Checkout starts
- Completed upgrades
- Revenue per exposed user
- Refund/cancellation rate
- Free-user churn after exposure
