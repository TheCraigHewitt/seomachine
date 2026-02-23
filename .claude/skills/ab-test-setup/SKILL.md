---
name: ab-test-setup
version: 1.0.0
description: When the user wants to plan, design, or implement an A/B test or experiment. Also use when the user mentions "A/B test," "split test," "experiment," "test this change," "variant copy," "multivariate test," or "hypothesis." For tracking implementation, see analytics-tracking.
---

# A/B Test Setup

Read `.claude/product-marketing-context.md` if it exists.

## Initial Assessment

Capture:
1. What behavior/metric should improve.
2. Current baseline conversion and traffic volume.
3. Technical and timeline constraints.

## Core Principles

1. Start with a hypothesis.
2. Isolate the variable being tested.
3. Pre-commit sample size and duration.
4. Track one primary metric + secondary + guardrails.

## Hypothesis Framework

```text
Because [observation/data],
we believe [change]
will cause [expected outcome]
for [audience].
We'll know this is true when [metrics].
```

**Example**
- Weak: "Change button color and see what happens."
- Strong: "Because users miss the CTA in heatmaps, we believe larger contrast CTA will increase signup starts by 15%+ for new users."

## Test Types

| Type | Description | Traffic Need |
|------|-------------|--------------|
| A/B | One control + one variant | Moderate |
| A/B/n | Multiple variants | Higher |
| MVT | Multiple variables combined | Very high |
| Split URL | Different URLs per variant | Moderate |

## Sample Size

### Quick Reference

| Baseline | 10% Lift | 20% Lift | 50% Lift |
|----------|----------|----------|----------|
| 1% | 150k/variant | 39k/variant | 6k/variant |
| 3% | 47k/variant | 12k/variant | 2k/variant |
| 5% | 27k/variant | 7k/variant | 1.2k/variant |
| 10% | 12k/variant | 3k/variant | 550/variant |

Detailed sample-size and duration guidance: [references/sample-size-guide.md](references/sample-size-guide.md)

## Metrics Selection

### Metric Hierarchy
- **Primary**: test winner/loser decision metric
- **Secondary**: context and mechanism metrics
- **Guardrails**: metrics that must not regress

### Example (Pricing Page)
- Primary: plan selection rate
- Secondary: page engagement, plan distribution
- Guardrail: support tickets, refund/cancel rate

## Designing Variants

| Category | What to Vary |
|----------|---------------|
| Messaging | Headline, value prop, proof framing |
| Layout | Hierarchy, section order, visual emphasis |
| CTA | Copy, size, placement |
| Content | Depth, examples, objection handling |

Rules:
- Make one meaningful change.
- Ensure variant reflects hypothesis.

## Traffic Allocation

| Approach | Split | Use Case |
|----------|-------|----------|
| Standard | 50/50 | Most A/B tests |
| Conservative | 80/20 or 90/10 | Higher downside risk |
| Ramped | Start low then increase | Technical risk mitigation |

## Running the Test

### Pre-Launch Checklist
- [ ] Hypothesis documented
- [ ] Primary metric and guardrails defined
- [ ] Sample size and duration calculated
- [ ] Variant QA completed
- [ ] Tracking validated

### During the Test
**Do**
- Monitor technical quality and traffic integrity
- Log unusual external factors

**Don't**
- Stop early based on interim wins
- Edit variants mid-test
- Change acquisition mix without documentation

## Analyzing Results

### Analysis Checklist
1. Reached target sample?
2. Statistically significant?
3. Practically meaningful lift?
4. Secondary and guardrail consistency?
5. Segment differences worth follow-up?

### Interpretation Guide

| Result | Action |
|--------|--------|
| Significant winner | Roll out variant |
| Significant loser | Keep control and document why |
| No significant diff | Keep control or rerun with bolder change |
| Mixed/segment-only | Investigate and run focused follow-up |

## Documentation

Use templates in [references/test-templates.md](references/test-templates.md).

## Common Mistakes

| Area | Mistake |
|------|---------|
| Design | Tiny change with low detectable impact |
| Execution | Stopping early (peeking bias) |
| Analysis | Ignoring confidence interval and effect size |
| Learning | Not logging outcomes and follow-up ideas |
