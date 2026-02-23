---
name: email-sequence
version: 1.0.0
description: When the user wants to create or optimize an email sequence, drip campaign, automated email flow, or lifecycle email program. Also use when the user mentions "email sequence," "drip campaign," "nurture sequence," "onboarding emails," "welcome sequence," "re-engagement emails," "email automation," or "lifecycle emails." For in-app onboarding, see onboarding-cro.
---

# Email Sequence Design

Read `.claude/product-marketing-context.md` if it exists.

## Initial Assessment

Capture:
1. **Sequence type**: welcome, onboarding, nurture, billing, re-engagement, campaign.
2. **Entry trigger**: behavior, lifecycle event, or date.
3. **Primary conversion goal**: activation, upgrade, renewal, reply, purchase.

## Core Principles

1. **One email, one job**.
2. **Value before ask**.
3. **Relevance over volume**.
4. **Every email has a clear next action**.

## Email Sequence Strategy

### Typical Length and Timing

| Sequence | Typical Length | Cadence |
|----------|----------------|---------|
| Welcome | 3-7 emails | Immediate, then every 1-2 days |
| Onboarding | 5-10 emails | Trigger-based + 1-3 day spacing |
| Lead nurture | 5-10 emails | Every 2-4 days |
| Re-engagement | 3-5 emails | Over 1-2 weeks |

### Subject and Preview Rules
- Subject: clear benefit or clear curiosity, usually 40-60 chars.
- Preview text: extend the subject (no repetition), usually 90-140 chars.
- Prefer specificity over cleverness.

## Sequence Types Overview

| Type | Goal | Core Emails |
|------|------|-------------|
| Welcome (post-signup) | Activate + build trust | Welcome, quick win, proof, objection, conversion |
| Lead nurture (pre-sale) | Educate + convert | Deliver asset, problem deep-dive, framework, case study, offer |
| Re-engagement | Win back or clean list | Check-in, value reminder, incentive, final choice |
| Product onboarding | Reach aha moment | First step, setup help, feature highlight, check-in, expansion |

Detailed templates: [references/sequence-templates.md](references/sequence-templates.md)

## Email Types by Category

Use lifecycle email coverage from: [references/email-types.md](references/email-types.md)

Categories included:
- Onboarding
- Retention
- Billing
- Usage
- Win-back
- Campaigns

## Copy, Personalization, and Testing

Use detailed guidance from: [references/copy-guidelines.md](references/copy-guidelines.md)

Includes:
- Structure, tone, and length rules
- Personalization and segmentation patterns
- Test priorities and key metrics

## Output Format

### Sequence Overview

```text
Sequence Name: [Name]
Trigger: [What starts the sequence]
Goal: [Primary conversion goal]
Length: [Number of emails]
Timing: [Delays between emails]
Exit Conditions: [When user leaves sequence]
```

### Per Email

```text
Email [#]: [Name/Purpose]
Send: [Timing]
Subject: [Subject line]
Preview: [Preview text]
Body: [Full copy]
CTA: [Text] -> [Destination]
Segment/Conditions: [If applicable]
```

### Metrics Plan

```text
Primary metric: [e.g., activation rate]
Secondary metrics: [open rate, click rate, unsubscribe rate]
Decision threshold: [what result is considered a win]
```
