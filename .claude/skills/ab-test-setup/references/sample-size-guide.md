# Sample Size Guide

## Sample Size Fundamentals

### Required Inputs
1. Baseline conversion rate
2. Minimum detectable effect (MDE)
3. Significance level (typically 95%)
4. Power (typically 80%)

### Practical Definitions
- **Baseline**: current metric level for this specific page/flow.
- **MDE**: smallest lift that justifies implementation cost.
- **95% significance**: low chance result is random.
- **80% power**: good chance of detecting true effect at chosen MDE.

## Sample Size Quick Reference

| Baseline CVR | 10% Lift | 20% Lift | 50% Lift |
|--------------|----------|----------|----------|
| 1% | 380k/variant | 97k/variant | 16k/variant |
| 5% | 72k/variant | 18k/variant | 3.1k/variant |
| 10% | 34k/variant | 8.7k/variant | 1.5k/variant |

For exact calculations, use calculators and your true baseline.

## Duration Calculator

### Formula

```text
Duration (days) = (Sample per variant x Number of variants) / (Daily traffic x % exposed)
```

### Example
- Need: 20,000 total sample
- Daily eligible traffic: 2,000
- Exposure: 100%
- Duration: 10 days

### Minimum Duration Rules
- Run at least one full week to capture day-of-week effects.
- For B2B cycles, two business weeks is safer.

### Maximum Duration Guidance
- Typical: avoid tests that require >8 weeks unless impact is high.

## Online Calculators

- Evan Miller: https://www.evanmiller.org/ab-testing/sample-size.html
- Optimizely: https://www.optimizely.com/sample-size-calculator/
- AB Test Guide: https://www.abtestguide.com/calc/
- VWO Duration: https://vwo.com/tools/ab-test-duration-calculator/

## Multiple Variants Adjustment

| Variants | Approx Sample Multiplier |
|----------|---------------------------|
| 2 (A/B) | 1x |
| 3 (A/B/C) | ~1.5x |
| 4 (A/B/C/D) | ~2x |

More variants = more comparisons = larger required sample.

## Common Sample Size Mistakes

1. Using sitewide baseline instead of page-level baseline.
2. Choosing unrealistic MDE.
3. Segment analysis without segment-level sample planning.
4. Running too many concurrent variants on limited traffic.

## If Sample Needs Are Too High

Options:
1. Test larger changes (higher MDE).
2. Reduce variants.
3. Test higher-funnel step with more traffic.
4. Aggregate similar pages when valid.
5. Use qualitative evidence instead of forcing low-power tests.

## Sequential Testing

Use sequential/Bayesian methods only with tools that adjust for repeated looks.

Typical tools:
- Optimizely Stats Accelerator
- VWO SmartStats
- PostHog Bayesian methods

## Quick Decision Framework

```text
Daily eligible traffic: _____
Baseline conversion: _____
MDE target: _____

Sample per variant: _____
Estimated days: _____

If >60 days: likely not feasible.
If 30-60 days: run only if high impact.
If <30 days: generally feasible.
```
