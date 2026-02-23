---
name: referral-program
version: 1.0.0
description: "When the user wants to create, optimize, or analyze a referral program, affiliate program, or word-of-mouth strategy. Also use when the user mentions 'referral,' 'affiliate,' 'ambassador,' 'word of mouth,' 'viral loop,' 'refer a friend,' or 'partner program.' This skill covers program design, incentive structure, and growth optimization."
---

# Referral & Affiliate Programs

Read `.claude/product-marketing-context.md` if it exists.

## Before Starting

Capture:
1. Program type (referral, affiliate, or both)
2. Unit economics (LTV, target CAC, margin)
3. Product shareability and natural trigger moments
4. Tooling and reward budget constraints

## Referral vs. Affiliate

| Program | Best For | Reward Pattern |
|---------|----------|----------------|
| Customer referral | Existing customer advocacy | One-time or limited rewards |
| Affiliate | Creator/partner distribution | Ongoing commission relationship |

## Referral Program Design

### Referral Loop

```text
Trigger Moment -> Share Action -> Referred Conversion -> Reward -> Repeat
```

### Step 1: Trigger Moments
- After first value/aha moment
- After milestone completion
- After strong support interaction
- After renewal or upgrade

### Step 2: Share Mechanism (by typical conversion)
1. In-product share flow
2. Personal referral link
3. Email invite
4. Social share
5. Referral code

### Step 3: Incentive Structure
- Single-sided reward
- Double-sided reward
- Tiered/gamified reward

Examples and sizing: [references/program-examples.md](references/program-examples.md)

## Optimization

### If share rate is low
- Improve ask timing
- Reduce sharing friction
- Test incentive type/amount
- Increase in-product visibility

### If referred conversion is low
- Improve referred landing experience
- Clarify value + reward terms
- Add trust proof from referrer context

### High-value A/B tests
- Incentive type/amount
- Ask placement and timing
- Program copy and CTA wording
- Referred landing page variant

### Common Problems

| Problem | Fix |
|---------|-----|
| Low awareness | Persistent in-app placement + lifecycle emails |
| Low share rate | One-click sharing + prefilled messages |
| Low conversion | Improve referred onboarding and offer clarity |
| Fraud risk | Verification, limits, delayed payout |

## Measuring Success

### Program Health Metrics
- Active referrers (30-day)
- Referral-to-signup conversion
- Referral-to-paid conversion
- Reward payout efficiency

### Business Impact Metrics
- % new customers from referrals
- Referral CAC vs other channels
- LTV of referred customers
- Program ROI

### Typical Findings
- Typical: referred users often show higher LTV than channel average.
- Typical: referred users often churn less than paid-acquisition cohorts.
- Typical: strong programs produce second-order referrals.

## Launch Checklist

### Before Launch
- [ ] Goal and KPI targets defined
- [ ] Incentive and terms finalized
- [ ] Tracking and attribution verified
- [ ] Fraud controls configured
- [ ] End-to-end flow QA completed

### Launch
- [ ] Customer announcement sent
- [ ] In-product prompts enabled
- [ ] Program landing page published
- [ ] Support team briefed

### First 30 Days
- [ ] Funnel leak review complete
- [ ] Top referrer cohort identified
- [ ] Incentive and prompt tests running
- [ ] Friction fixes shipped

## Email Sequences

### Referral Program Launch

```text
Subject: You can now earn [reward] by sharing [Product]

We launched a referral program.
Share your link, and earn [reward] when someone signs up.
They get [their reward] too.

[Unique referral link]

1) Share
2) Friend signs up
3) Rewards are applied
```

### Referral Nurture Sequence
- Day 7: reminder + link
- Day 30: "Who else needs this?"
- Day 60: customer success story + prompt
- Post-milestone: personalized referral ask

## Affiliate Program Reference

Detailed affiliate design, recruiting, commission structures, and fraud controls:
[references/affiliate-programs.md](references/affiliate-programs.md)
