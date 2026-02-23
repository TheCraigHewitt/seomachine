---
name: signup-flow-cro
version: 1.0.0
description: Use for signup, registration, trial activation, and account-creation optimization. For non-signup forms use form-cro; for post-signup activation use onboarding-cro.
---

# Signup Flow CRO

Reduce signup friction while preserving activation quality.

## Scope and Pre-Work

- If `.claude/product-marketing-context.md` exists, read it first.
- Confirm:
  1. Flow type (`freemium`, `free trial`, `paid upfront`, `waitlist`) and audience (`B2B`/`B2C`).
  2. Current funnel by step and device.
  3. Required data at signup vs. data that can be deferred.
  4. What happens immediately after successful signup.

---

## Core Principles

### 1. Minimize Required Inputs

Each additional required field increases abandonment. Default required set:
- `Email` (or phone for phone-first products)
- `Password` (if not passwordless)

Often deferrable:
- Name, company, role, team size, phone, address, use case detail

Only require data that changes immediate eligibility, security, or routing.

### 2. Show Value Before Commitment

- Whenever possible, let users see value before heavy setup.
- If hard signup wall is required, keep first step extremely lightweight.
- Set expectation clearly (`Setup takes ~30 seconds`).

### 3. Lower Perceived Effort and Uncertainty

- Progress indicator for multi-step flows.
- Clear next step after signup.
- No hidden requirements (credit card, verification loops, extra approvals).
- Use activation-quality guardrails so conversion gains do not reduce downstream success.

---

## Field and Auth Optimization

### Email
- Single field, inline validation, typo detection.
- Show recovery path for existing accounts (`Already have an account? Sign in`).

### Password
- Show requirements before submission.
- Allow paste and password manager autofill.
- Provide show/hide toggle and real-time strength feedback.
- Consider passwordless or magic-link variants for lower friction.

### Name
- Test `Full name` vs. split fields.
- Require only if immediately used in product or communications.

### Social / SSO Auth Strategy

Prioritize providers by audience:
- **B2C**: Google, Apple (mobile-heavy), sometimes Facebook.
- **B2B**: Google, Microsoft, SSO/SAML.

Testable decisions:
- SSO buttons above vs. below email form.
- One primary provider vs. multiple providers.
- Provider mix by traffic source/segment.

### Phone and Company Fields
- Defer unless directly tied to account security or sales motion.
- If required, explain why and format inputs automatically.

### Role / Use Case Question
- Keep to one concise question if needed for personalization.
- Move deeper segmentation into onboarding.

---

## Single-Step vs. Multi-Step

### Single-Step Best When
- <=3 required inputs.
- High-intent visitors.
- Simple self-serve product motion.

### Multi-Step Best When
- You need additional segmentation.
- Account setup has natural stages.
- Conditional logic reduces irrelevant questions.

### Multi-Step Best Practices
- `Step X of Y` progress indicator.
- Easy-first sequencing, sensitive-later sequencing.
- Back navigation and progress persistence.
- Each step completable in seconds.

Common progressive commitment pattern:
1. Email or SSO selection
2. Password + minimal profile
3. Optional setup/preferences

---

## Trust, Copy, and Error UX

### Trust Cues Near Form
- `No credit card required` (if true)
- Trial length or free plan clarity
- Privacy reassurance
- Security/compliance badges (if relevant)

### Microcopy Standards
- Persistent labels, concise examples in placeholders.
- Clear error copy with fix path.
- Avoid generic failures.

Good error:
`This email is already registered. Sign in or reset password.`

Bad error:
`Something went wrong.`

---

## Post-Submit and Verification Decisions

Design verification around risk, not habit.

### Verification Timing Options
- **Immediate verification gate**: use only when security/compliance requires it.
- **Deferred verification**: let user enter product, require verify before sensitive actions.
- **Magic link flow**: low friction, especially on mobile.

### Must-Have Elements
- Clear success state with next step.
- Resend verification action.
- Ability to correct wrong email.
- Fallback path if mail is delayed.

If verification is required, avoid dead-end screens; provide product preview or guided next step.

---

## Measurement

### Core Metrics
- Signup start rate
- Signup completion rate
- Step completion/drop-off rate
- Error rate by field
- Time to complete
- Device-specific completion

### Quality Guardrails
- Activation rate after signup
- Day 1 retention
- Fraud/spam rate
- Support tickets tied to signup issues

### Instrumentation
- Field focus/blur/error
- Step progression
- SSO click and completion by provider
- Verification completion timing

---

## Output Format

### Audit Findings
For each issue: **Issue -> Impact -> Fix -> Priority**.

### Recommended Changes
1. Quick wins (same day)
2. High-impact redesigns
3. Tests to validate uncertain assumptions

### Flow Spec (when requested)
- Required field set + rationale
- Step sequence
- Labels/CTA/error copy
- Verification policy and fallback states

---

## Related Skills

- `onboarding-cro`
- `form-cro`
- `page-cro`
- `ab-test-setup`
