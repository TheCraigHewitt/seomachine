---
name: product-marketing-context
version: 1.0.0
description: "When the user wants to create or update their product marketing context document. Also use when the user mentions 'product context,' 'marketing context,' 'set up context,' 'positioning,' or wants to avoid repeating foundational information across marketing tasks. Creates `.claude/product-marketing-context.md` that other marketing skills reference."
---

# Product Marketing Context

## Workflow

### Step 1: Check Existing Context

If `.claude/product-marketing-context.md` exists:
- Read it.
- Summarize what is already captured.
- Ask which sections to update.

If it does not exist, offer:
1. **Auto-draft from codebase**: Build V1 from README, site copy, docs, and product UI text.
2. **Interview from scratch**: Gather section-by-section with user input.

### Step 2: Gather Information

If auto-drafting:
1. Pull evidence from repository artifacts.
2. Fill all sections with explicit assumptions marked, then ask for corrections.

If interviewing:
1. Ask for one section at a time.
2. Confirm each section before moving on and capture verbatim customer language.

## Sections to Capture

### 1. Product Overview
- One-liner, what it does, category, product type, business model.

### 2. Target Audience
- Company type, decision-makers, primary use case, JTBD, key scenarios.

### 3. Personas (B2B only)
- User, champion, decision-maker, financial buyer, technical influencer.

### 4. Problems & Pain Points
- Core problem, alternative failures, cost of problem, emotional tension.

### 5. Competitive Landscape
- Direct, secondary, indirect alternatives and where each falls short.

### 6. Differentiation
- What is different, why it matters, why buyers choose this product.

### 7. Objections & Anti-Personas
- Top objections with responses; who should not buy.

### 8. Switching Dynamics
- Push, pull, habit, anxiety.

### 9. Customer Language
- Verbatim problem/solution phrases, words to use/avoid, glossary.

### 10. Brand Voice
- Tone, style, personality.

### 11. Proof Points
- Metrics, logos, testimonials, value themes and evidence.

### 12. Goals
- Business goal, primary conversion action, baseline metrics.

## Step 3: Create the Document

Use this template for `.claude/product-marketing-context.md`:

```markdown
# Product Marketing Context

*Last updated: [date]*

## Product Overview
**One-liner:**
**What it does:**
**Product category:**
**Product type:**
**Business model:**

## Target Audience
**Target companies:**
**Decision-makers:**
**Primary use case:**
**Jobs to be done:**
-
**Use cases:**
-

## Personas
| Persona | Cares about | Challenge | Value we promise |
|---------|-------------|-----------|------------------|
| | | | |

## Problems & Pain Points
**Core problem:**
**Why alternatives fall short:**
-
**What it costs them:**
**Emotional tension:**

## Competitive Landscape
**Direct:** [Competitor] — falls short because...
**Secondary:** [Approach] — falls short because...
**Indirect:** [Alternative] — falls short because...

## Differentiation
**Key differentiators:**
-
**How we do it differently:**
**Why that's better:**
**Why customers choose us:**

## Objections
| Objection | Response |
|-----------|----------|
| | |

**Anti-persona:**

## Switching Dynamics
**Push:**
**Pull:**
**Habit:**
**Anxiety:**

## Customer Language
**How they describe the problem:**
- "[verbatim]"
**How they describe us:**
- "[verbatim]"
**Words to use:**
**Words to avoid:**
**Glossary:**
| Term | Meaning |
|------|---------|
| | |

## Brand Voice
**Tone:**
**Style:**
**Personality:**

## Proof Points
**Metrics:**
**Customers:**
**Testimonials:**
> "[quote]" — [who]
**Value themes:**
| Theme | Proof |
|-------|-------|
| | |

## Goals
**Business goal:**
**Conversion action:**
**Current metrics:**
```

## Step 4: Confirm and Save

- Show the completed draft, gather corrections, and save to `.claude/product-marketing-context.md`.
