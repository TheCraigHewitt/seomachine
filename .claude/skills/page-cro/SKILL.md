---
name: page-cro
version: 1.0.0
description: Use when optimizing conversion on marketing pages (homepage, landing, pricing, feature, blog). For signup flows use signup-flow-cro; for non-signup forms use form-cro; for post-signup activation use onboarding-cro; for modals/popups use popup-cro.
---

# Page CRO

Optimize marketing pages with an impact-first audit and a concrete test backlog.

## Pre-Work

- If `.claude/product-marketing-context.md` exists, read it first.
- Confirm:
  1. Page type and audience segment.
  2. Primary conversion event and current conversion rate.
  3. Traffic source and message context (ads, organic query intent, email, social).

---

## Impact-Ordered Audit Framework

### 1. Value Proposition Clarity (highest leverage)

Check whether a new visitor can answer within 5 seconds:
- What is this?
- Who is it for?
- Why is it better than alternatives?

Look for specific outcomes, not internal feature language. Strong pages use concrete claims (time saved, revenue lift, risk reduced) instead of vague promises.

Common failure patterns:
- Clever headline, unclear meaning.
- Multiple competing promises in hero.
- Feature lists before problem/outcome context.

### 2. Headline Quality and Message Match

- Headline and subheadline should match the promise from the traffic source.
- One dominant promise per page.
- Subheadline should clarify mechanism and relevance.

Examples:
- Weak: `Modern analytics for teams`
- Stronger: `Ship weekly dashboards in 10 minutes, without SQL bottlenecks`

### 3. CTA Placement, Copy, and Hierarchy

- Keep one clear primary CTA.
- Place primary CTA above fold and repeat after high-intent sections.
- Use value-oriented copy (`Start Free Trial`, `Book 15-Min Demo`) instead of generic (`Submit`).
- If a secondary CTA exists, keep visual hierarchy obvious.

### 4. Visual Hierarchy and Scannability

- Clear H1/H2 structure and short sections.
- Dominant scan path: promise -> proof -> CTA.
- Supporting visuals should reduce uncertainty (product screenshot, workflow preview, before/after), not act as decoration.
- Preserve whitespace so decision points are visible.

### 5. Trust Signals and Social Proof

Prioritize specific proof near claims and CTAs:
- Recognizable customer logos.
- Attributed testimonials with role/company.
- Quantified outcomes (`reduced onboarding time by 38%`).
- Ratings/reviews or compliance/security cues where relevant.

### 6. Objection Handling

Address major decision blockers directly:
- Price/value fit.
- Use-case fit.
- Implementation complexity.
- Risk and reversibility.

Tactics: concise FAQ, guarantees, migration/process clarity, competitor/status-quo comparisons.

### 7. Friction and UX

Identify conversion blockers:
- Extra fields and unnecessary steps.
- Unclear next action.
- Distracting navigation on focused pages.
- Mobile layout problems and slow load performance.

---

## Page-Type Mini-Frameworks

- **Homepage**: orient cold visitors fast, then route to the highest-probability next step.
- **Landing page**: strict message match, minimal navigation, single conversion objective.
- **Pricing page**: scannable plan comparison, recommended plan, objection handlers (`trial`, billing clarity, cancellation terms).
- **Feature page**: feature -> business outcome -> proof -> CTA to try/buy.
- **Blog/resource page**: contextual inline CTAs tied to topic intent, plus end-of-article next action.

---

## Output Format

### Quick Wins
Low-effort fixes with near-term impact.

### High-Impact Changes
Structural changes likely to move conversion significantly.

### A/B Test Plan
For each test: variant, hypothesis, primary metric, guardrail metric, expected direction.

### Copy Alternatives
Provide 2-3 alternatives for key headline/CTA elements and explain why each could win.

For broader page-specific test ideas, see [references/experiments.md](references/experiments.md).

---

## Related Skills

- `signup-flow-cro`
- `form-cro`
- `popup-cro`
- `copywriting`
- `ab-test-setup`
