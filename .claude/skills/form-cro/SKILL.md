---
name: form-cro
version: 1.0.0
description: Use for optimizing non-signup forms (lead capture, contact, demo request, quote, application, survey, checkout-adjacent forms). For account creation use signup-flow-cro; for popup forms use popup-cro.
---

# Form CRO

Improve form completion rates without sacrificing data quality.

## Scope and Pre-Work

- If `.claude/product-marketing-context.md` exists, read it first.
- Confirm:
  1. Form type and business outcome of a submission.
  2. Current start rate, completion rate, and major drop-off field(s).
  3. Mobile/desktop split and any compliance constraints.
  4. Which collected fields are actually used downstream.

---

## Core Principles

### 1. Every Field Has a Cost

Typical impact of added fields:
- **3 fields**: baseline conversion.
- **4-6 fields**: often **10-25%** completion drop.
- **7+ fields**: often **25-50%+** drop.

For each field, ask:
- Is this required before we can help the user?
- Can this be inferred (email domain, enrichment, CRM data)?
- Can it be collected after submission?

### 2. Value Must Exceed Effort

The form should quickly answer: "What do I get if I complete this?"
- Put value proposition above the form.
- Set expectation (`takes 30 seconds`, `response within 1 business day`).
- Avoid asking for high-friction info before trust is established.

### 3. Reduce Cognitive Load

- Use clear labels and predictable field order.
- Keep one concept per field.
- Group related fields only when necessary.
- Prefer defaults/autofill where possible.

---

## Field Priority Framework

### Required Now (default)
- `Email` (or best contact channel)
- `Name` when needed for follow-up quality
- Core request context (`Message` or `Goal`) if routing requires it

### Usually Deferrable
- `Phone`, `Company size`, `Budget`, `Role`, full address, long qualification questions

### Conditional Only
- Compliance-required information
- Sales qualification fields that materially change routing/response

If a field does not change routing, eligibility, or immediate response quality, defer it.

---

## Field-by-Field Guidance

### Email
- Single email field (no confirmation field).
- Validate format inline; do not block while user is typing.
- Catch common typos (`gmial.com` -> `gmail.com`).
- Use email keyboard on mobile.

### Name
- Test `Full name` vs. `First/Last` split.
- Single field usually reduces friction.
- Split only when downstream systems genuinely require separate components.

### Phone
- Make optional unless legally or operationally required.
- If required, explain why (`Needed for same-day scheduling`).
- Auto-format and handle country codes.

### Company / Organization
- Use autocomplete where possible.
- Infer from email domain when acceptable.
- Consider collecting post-submit if not routing-critical.

### Role / Use Case
- Use concise options when segmentation is required.
- Keep to one question at capture stage.
- Move deeper profiling into follow-up or onboarding.

### Free Text (Message / Details)
- Make optional unless essential for routing.
- Give guidance (`1-2 sentences is enough`).
- Preserve typed content on validation errors.

### Selects and Checkboxes
- Use radios when <=5 mutually exclusive options.
- Use searchable select for large lists.
- Add `Other` only if you can handle unstructured responses.

---

## Layout and Flow

### Field Order
1. Start with easy fields (`Name`, `Email`).
2. Build commitment.
3. Ask sensitive/high-friction info later.
4. Keep related fields adjacent.

### Labels, Placeholders, Help Text
- Labels should remain visible.
- Placeholders are for examples, not core instructions.
- Help text should be brief and adjacent to the field.

Good:
```text
Work Email
name@company.com
```

Bad:
```text
[Enter your email address]
```
(Placeholder disappears on focus.)

### Single vs. Multi-Column
- Default to single column for readability and mobile performance.
- Multi-column only for tightly related short fields.

---

## Multi-Step Forms

Use multi-step when:
- You need more than ~5-6 inputs.
- Inputs naturally split into stages.
- Conditional logic meaningfully changes later questions.

Best practices:
- Progress indicator (`Step 2 of 4`).
- One topic per step.
- Back navigation and saved progress.
- Required/optional state clearly marked.

A common commitment sequence:
1. Contact info.
2. Context and goals.
3. Qualification details.
4. Scheduling/preferences.

---

## Validation and Error Handling

### Inline Validation
- Validate on blur or step transition, not every keystroke.
- Keep entered values on error.
- Show error beside field and summarize at top for long forms.

### Error Copy
- Be specific and actionable.

Good: `Enter a valid work email (example: name@company.com)`

Bad: `Invalid input`

### Submit Behavior
- Disable duplicate submits while loading.
- Show progress/processing state.
- On error, focus first invalid field.
- On success, confirm next step clearly.

---

## CTA and Trust Optimization

### Button Copy
Prefer action + value:
- `Get My Quote`
- `Book My Demo`
- `Send My Request`

Avoid low-signal labels like `Submit` unless context is already explicit.

### Trust and Risk Reduction
Near the form, add only what helps decisions:
- Privacy reassurance (`We never share your information`).
- Expected response SLA.
- Relevant trust proof (testimonial, customer logo, compliance badge).

### Perceived Effort Reducers
- "Takes < 1 minute"
- Minimal visual clutter
- Clear required field count

---

## Measurement

Track by device and traffic source.

### Core Metrics
- **Form start rate**: page visits -> first field interaction.
- **Completion rate**: form starts -> successful submit.
- **Field-level drop-off**: abandonment after each field.
- **Error rate by field**.
- **Time to complete**.
- **Lead quality guardrails**: SQL rate, response quality, spam rate.

### Event Instrumentation
- Form view
- First focus
- Field blur/validation error
- Step progression (multi-step)
- Submit attempt
- Successful submit

---

## Output Format

### Form Audit
For each issue include:
- **Issue**
- **Impact**
- **Fix**
- **Priority** (`High`, `Medium`, `Low`)

### Recommended Form Design
- Required vs. optional fields with rationale
- Proposed field order
- Label/placeholder/button copy
- Error messages for critical fields
- Layout notes (desktop + mobile)

### Test Backlog
For each test: variant, hypothesis, primary metric, guardrail metric.

---

## Related Skills

- `signup-flow-cro`
- `popup-cro`
- `page-cro`
- `ab-test-setup`
