---
name: onboarding-cro
version: 1.0.0
description: Use for post-signup onboarding and activation optimization (first-run experience, time-to-value, empty states, activation funnels). For signup optimization use signup-flow-cro.
---

# Onboarding CRO

Optimize first-run experience to move users to activation fast and predictably.

## Scope and Pre-Work

- If `.claude/product-marketing-context.md` exists, read it first.
- Confirm:
  1. Product type and core value promise.
  2. Activation definition (`aha moment`) and current activation rate.
  3. Current post-signup steps and major drop-off points.

---

## Core Principles

### 1. Time-to-Value First
Remove non-essential steps between signup and first meaningful outcome.

### 2. One Session, One Win
First session should drive one concrete success, not full product education.

### 3. Doing Beats Explaining
Interactive completion of real tasks beats long tours and static tutorials.

### 4. Visible Progress Sustains Momentum
Use progress cues, completion states, and next-step prompts.

---

## Defining Activation (Aha Moment)

Activation is the earliest action strongly correlated with retention.

Examples:
- Project management: create first project + invite collaborator.
- Analytics: install tracking + view first report.
- Design: create and export/share first asset.
- Marketplace: complete first transaction.

Track:
- `% of signups reaching activation`
- `Time to activation`
- `Step count to activation`
- Activation by source/segment

---

## First 30 Seconds: Approach Matrix

| Approach | Best For | Risk |
|----------|----------|------|
| Product-first | Simple B2C or low-complexity products | Blank-state confusion |
| Guided setup | Products requiring configuration | Added friction before value |
| Value-first demo data | Products where sample output is compelling | May feel less "real" |

Whichever model you choose, enforce:
- one clear next action,
- no dead-end states,
- visible step progression when multi-step.

---

## Onboarding Patterns

### Checklist Pattern
Use when multiple setup tasks are required.

Checklist standards:
- 3-7 items max
- Ordered by value, not implementation order
- At least one quick win item first
- Dismiss/skip path available
- Explicit completion state

### Empty States
Treat empty states as guided entry points:
- explain purpose,
- show example end state,
- include one clear primary action,
- optionally preload sample/template data.

### Tooltips and Tours
Use for non-obvious UI or high-value features, with constraints:
- 3-5 steps max,
- dismissable anytime,
- avoid repeating for returning users.

---

## Stalled User Recovery

Define `stalled` objectively (e.g., no key action in 48-72h).

Recovery sequence:
1. In-app resume prompt (`Pick up where you left off`).
2. Triggered email tied to missing step.
3. Human outreach for high-value accounts.

Do not restart users from step 1 if they have partial progress; resume at last completed milestone.

---

## Measurement

### Core Metrics
- Activation rate
- Time to activation
- Onboarding completion rate
- Day 1 / Day 7 / Day 30 retention

### Funnel View
Track drop-off between each onboarding milestone, then prioritize the biggest absolute and relative loss points.

### Instrumentation
- Step view/start/complete
- Checklist item complete
- Empty-state CTA clicks
- Help/tour interactions
- Re-engagement email click-through and completion

---

## Output Format

### Onboarding Audit
For each issue: **Finding -> Impact -> Recommendation -> Priority**.

### Revised Flow
- Activation target
- Step-by-step onboarding path
- Checklist and empty-state copy
- Recovery triggers for stalled users
- Metrics plan and experiment list

For broader test ideas, see [references/experiments.md](references/experiments.md).

---

## Related Skills

- `signup-flow-cro`
- `email-sequence`
- `paywall-upgrade-cro`
- `ab-test-setup`
