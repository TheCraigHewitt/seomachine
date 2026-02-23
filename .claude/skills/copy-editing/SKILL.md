---
name: copy-editing
version: 1.0.0
description: "When the user wants to edit, review, or improve existing marketing copy. Use for prompts like 'edit this copy,' 'review my draft,' 'proofread,' 'polish this,' or 'copy sweep.' Applies a seven-sweep method to improve clarity, persuasion, proof, and conversion without changing the core message."
---

# Copy Editing

Edit existing copy with focused passes. Preserve intent. Improve clarity and conversion.

## Core Philosophy

Check `.claude/product-marketing-context.md` first. Keep brand voice and customer language consistent.

Rules:
- Keep the core message.
- Edit one dimension at a time.
- Justify each edit.
- Preserve author voice unless it blocks comprehension.

---

## The Seven Sweeps Framework

Run sweeps in order. Apply fixes in each sweep before moving to the next.

### Sweep 1: Clarity

**Goal:** Reader understands every line on first read.

Check: ambiguous pronouns, jargon without explanation, overloaded sentences, missing context.

Edits: split long sentences, replace abstract with concrete, move key point to sentence start.

### Sweep 2: Voice and Tone

**Goal:** Consistent voice throughout.

Check: formal/casual drift, inconsistent brand wording, random style shifts.

Edits: standardize vocabulary and cadence, align tone with audience.

### Sweep 3: So What

**Goal:** Every claim connects to buyer value.

Check: features without outcomes, claims that fail "why should I care?"

Edit pattern: `Feature -> consequence -> business/personal outcome`

Example:
- Weak: "Our platform uses AI-powered analytics."
- Strong: "AI analytics surfaces missed patterns, so you decide faster with less manual work."

### Sweep 4: Prove It

**Goal:** Claims supported with evidence.

Check: unsupported superlatives, missing attribution, vague social proof.

Edits: add named testimonials, metrics, case references, guarantees. Soften claims if proof unavailable.

### Sweep 5: Specificity

**Goal:** Replace vague language with concrete detail.

Check: fuzzy verbs (`improve`, `optimize`, `streamline`), generic outcomes without scale/timeline.

Edits: add numbers, timeframe, scope, examples. Remove filler that cannot be made specific.

### Sweep 6: Heightened Emotion

**Goal:** Add emotional resonance without hype.

Check: flat informational sections, pain/aspiration stated but not felt.

Edits: make before/after state vivid, add concrete stakes and relief, keep tone credible.

### Sweep 7: Zero Risk

**Goal:** Remove conversion friction near CTAs.

Check: unanswered objections, weak trust signals, unclear next step.

Edits: add guarantee/trial/cancel terms, place proof close to CTA, clarify what happens after click.

### Back-Check Matrix

After each sweep, re-check earlier passes:

| Completed Sweep | Re-check |
|-----------------|----------|
| 2 | 1 |
| 3 | 2 -> 1 |
| 4 | 3 -> 2 -> 1 |
| 5 | 4 -> 3 -> 2 -> 1 |
| 6 | 5 -> 4 -> 3 -> 2 -> 1 |
| 7 | 6 -> 5 -> 4 -> 3 -> 2 -> 1 |

---

## Quick-Pass Checks

Use when a full seven-sweep pass is unnecessary.

### Word Level
- Remove filler (`very`, `really`, `basically`, `actually`).
- Prefer plain words (`use` over `utilize`).
- Convert passive to active voice.

### Sentence Level
- One idea per sentence.
- Front-load key information.
- Cut conjunction chains.

### Paragraph Level
- One topic per paragraph.
- Short web-friendly blocks.
- Check transition clarity.

---

## Copy Editing Checklist

### Setup
- [ ] Confirm page goal and target audience.
- [ ] Confirm primary CTA.
- [ ] Read draft once without editing.

### Sweep Completion
- [ ] Clarity
- [ ] Voice and Tone
- [ ] So What
- [ ] Prove It
- [ ] Specificity
- [ ] Heightened Emotion
- [ ] Zero Risk

### Final QA
- [ ] Message still matches original intent.
- [ ] Claims are defensible.
- [ ] Formatting and grammar are clean.
- [ ] CTA path is clear.

---

## Common Problems and Fixes

| Problem | Fix |
|---------|-----|
| Feature dump without value | Add outcome sentence after each major feature |
| Corporate language | Rewrite as spoken plain English |
| Weak opening | Lead with core pain or desired outcome |
| Buried CTA | Surface CTA earlier and repeat with risk reduction |
| No proof | Add specific testimonial/data/source or tone down claim |
| Generic claims | Specify who, how, and by how much |
| Mixed audiences | Pick one audience and write directly to them |

---

## References

- [Plain English Alternatives](references/plain-english-alternatives.md)

---

## Related Skills

- **copywriting**: Draft copy from scratch
- **page-cro**: Structural conversion optimization
- **ab-test-setup**: Validate competing copy versions
