# Pricing Research Methods

## Van Westendorp Price Sensitivity Meter

### Four Questions
1. At what price is this too expensive to consider?
2. At what price is this so cheap you'd question quality?
3. At what price is this getting expensive but still possible?
4. At what price is this a bargain?

### Analysis
- Plot cumulative distributions.
- Identify intersections:
  - PMC: too cheap x expensive
  - PME: too expensive x cheap
  - OPP: too cheap x too expensive
  - IDP: expensive x cheap

Interpretation:
- Acceptable range: PMC -> PME
- Practical target zone: OPP -> IDP

### Survey Tips
- Typical: 100-300 respondents for directional signal
- Segment by persona whenever possible
- Use realistic product framing

### Sample Output

```text
PMC: $29/mo
OPP: $49/mo
IDP: $59/mo
PME: $79/mo
Recommended zone: $49-59/mo
```

## MaxDiff (Best-Worst Scaling)

### Method
1. List 8-15 candidate features.
2. Show 4-5 per question.
3. Ask most important and least important.
4. Repeat across randomized sets.
5. Convert responses into utility scores.

### Example Prompt

```text
Which feature is MOST important and LEAST important?
- Unlimited projects
- Custom branding
- Priority support
- API access
- Advanced analytics
```

### Packaging Mapping

| Utility Rank | Packaging Decision |
|--------------|--------------------|
| Top 20% | Include in all tiers |
| 20-50% | Use for tier separation |
| 50-80% | Higher tiers only |
| Bottom 20% | Consider add-on or remove |

## Willingness-to-Pay Methods

- Direct question: quick but biased.
- Gabor-Granger: yes/no at price points for demand curve.
- Conjoint: bundle tradeoff model for price-feature sensitivity.

## Usage-Value Correlation Analysis

### Process
1. Instrument real usage depth and breadth.
2. Correlate usage patterns with retention/expansion.
3. Identify value thresholds for pricing/packaging breaks.

### Example

```text
High-LTV cohort: more active users + more integrations.
Churned cohort: low user adoption + low integration depth.
Implication: per-user pricing with integration gating can align value capture.
```
