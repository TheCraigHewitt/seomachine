---
name: paywall-upgrade-cro
version: 1.0.0
description: Use for in-product paywalls, upgrade prompts, feature gates, and free->paid/tier-upgrade conversion moments. This skill covers in-app upgrade context, not public pricing pages.
---

# Paywall and Upgrade Screen CRO

Optimize upgrade prompts shown after users have experienced product value.

## Scope and Pre-Work

- If `.claude/product-marketing-context.md` exists, read it first.
- Confirm:
  1. Upgrade model (`freemium->paid`, `trial->paid`, tier upgrade).
  2. Trigger type and current conversion (`feature gate`, `usage limit`, `trial expiry`, timed prompts).
  3. What value users have already seen before the paywall appears.

---

## Core Principles

### 1. Value Before Ask
Prompt after meaningful usage or an attempted premium action, not on first sessions.

### 2. Show Concrete Gain
Demonstrate capability and outcome (`unlock unlimited exports`, `remove usage cap`), not just plan names.

### 3. Keep Upgrade Path Short
Minimize clicks to payment, prefill known data, keep context intact.

### 4. Respect the No
Easy dismissal and clear free-path continuation preserve trust.

---

## Trigger Taxonomy

### Feature Gate
Shown when user attempts premium functionality.

Must include:
- What was blocked.
- Why it is premium.
- What outcome unlocks after upgrade.
- Clear downgrade/continue option.

### Usage Limit
Shown at or near cap (projects, reports, seats, API calls).

Must include:
- Current usage vs. limit.
- Immediate consequence.
- Upgrade value (`from 3 projects to unlimited`).

### Trial Expiration
Shown before and at expiration.

Must include:
- Countdown checkpoints (e.g., 7/3/1 days).
- What remains vs. what is lost.
- Value recap from trial usage.

### Time/Behavior Prompt
Use sparingly for engaged free users; suppress for new or disengaged users.

---

## Paywall Screen Anatomy

1. **Headline**: outcome-focused (`Unlock advanced reporting to cut weekly prep time`).
2. **Value proof**: preview, before/after, or recent usage summary.
3. **Plan clarity**: simple comparison with current plan marked.
4. **Pricing clarity**: monthly/annual options with savings logic.
5. **Trust cues**: proof points, guarantee/cancellation terms.
6. **CTA**: specific action (`Upgrade to Pro`).
7. **Escape hatch**: `Not now` / `Continue with Free`.

---

## Example Wireframes

### Feature Lock
```text
[Locked] Advanced Export is on Pro
Generate branded exports for clients in one click.

Includes: watermark removal, templates, scheduling
[Upgrade to Pro - $29/mo]   [Not now]
```

### Usage Limit
```text
You've reached your free limit: 3/3 projects
Pro includes unlimited projects and team permissions.

[Upgrade to Pro]   [Delete a project]
```

### Trial Ending
```text
Trial ends in 3 days
You've created 12 reports and invited 2 teammates.
Keep these workflows active with Pro.

[Continue with Pro]   [Remind me later]   [Downgrade]
```

---

## Frequency and UX Rules

- Cap prompts per session.
- Apply cool-down after dismissal (days, not minutes).
- Avoid interrupting critical flows.
- Suppress repeated prompts when user repeatedly declines in short windows.

---

## Upgrade Flow and Post-Upgrade

### Conversion Path
- Minimize form fields and step count.
- Keep billing context clear.
- Offer payment methods relevant to audience.

### Post-Upgrade Experience
- Immediate feature unlock.
- Confirmation and receipt.
- Contextual "what to do next" for newly unlocked features.

---

## Measurement

### Core Metrics
- Paywall impression rate
- Paywall CTR
- Checkout start rate
- Upgrade completion rate
- Revenue per user

### Guardrails
- Free-user churn
- Support complaints/friction signals
- Refund/cancellation rate

For detailed paywall test ideas, see [references/experiments.md](references/experiments.md).

---

## Anti-Patterns to Avoid

- Hidden close affordance.
- Misleading plan comparisons.
- Guilt-trip or manipulative decline copy.
- Frequent prompts before value realization.
- Blocking essential non-premium workflows.

---

## Related Skills

- `page-cro`
- `onboarding-cro`
- `ab-test-setup`
