# A/B Test Templates Reference

## Test Plan Template

```markdown
# A/B Test: [Name]

## Overview
- Owner: [Name]
- Test ID: [ID]
- Area: [Page/Feature]

## Hypothesis
Because [observation/data],
we believe [change]
will cause [expected outcome]
for [audience].
We'll know this is true when [metrics].

## Test Design
| Element | Details |
|---------|---------|
| Test type | A/B / A/B/n / MVT |
| Duration | X weeks |
| Sample size | X per variant |
| Traffic split | 50/50 |
| Tool | [Tool name] |

## Variants
### Control (A)
[Screenshot]
- Current experience

### Variant (B)
[Screenshot]
- [Specific change]
- Rationale: [Why this should win]

## Metrics
### Primary
- Metric: [name]
- Baseline: [X%]
- MDE: [X%]

### Secondary
- [Metric 1]

### Guardrails
- [Metric 1]

## Segment Plan
- Mobile vs desktop
- New vs returning
- Traffic source

## Success Criteria
- Winner: [threshold]
- Loser: [threshold]
- Inconclusive: [next action]

## Pre-Launch Checklist
- [ ] Hypothesis reviewed
- [ ] Metrics trackable
- [ ] Sample size calculated
- [ ] Variants QA'd
- [ ] Tracking verified
- [ ] Stakeholders informed
```

## Results Documentation Template

```markdown
# A/B Test Results: [Name]

## Summary
| Element | Value |
|---------|-------|
| Test ID | [ID] |
| Dates | [Start] - [End] |
| Duration | X days |
| Result | Winner / Loser / Inconclusive |
| Decision | [Action] |

## Hypothesis (Reminder)
[Copy from plan]

## Results
### Sample Size
| Variant | Target | Actual |
|---------|--------|--------|
| Control | X | Y |
| Variant | X | Y |

### Primary Metric: [Name]
| Variant | Value | 95% CI | vs Control |
|---------|-------|--------|------------|
| Control | X% | [a,b] | -- |
| Variant | Y% | [c,d] | +Z% |

Statistical significance: p = [value]
Practical significance/business impact: [summary]

### Secondary Metrics
| Metric | Control | Variant | Change | Significant? |
|--------|---------|---------|--------|--------------|
| [M1] | X | Y | +Z% | Yes/No |

### Guardrails
| Metric | Control | Variant | Change | Concern? |
|--------|---------|---------|--------|----------|
| [G1] | X | Y | +Z% | Yes/No |

### Segment Analysis
| Segment | Control | Variant | Lift |
|---------|---------|---------|------|
| Mobile | X% | Y% | +Z% |

## Interpretation
- What happened:
- Why this likely happened:
- Caveats:

## Decision
- Winner: [Control/Variant]
- Action: [Roll out / Keep control / Re-test]
- Timeline:

## Learnings
- Key learnings:
- Next tests:
- Projected impact:
```

## Test Repository Entry Template

```markdown
| Test ID | Name | Page | Dates | Primary Metric | Result | Lift | Link |
|---------|------|------|-------|----------------|--------|------|------|
| 001 | Hero headline | Homepage | 1/1-1/15 | CTR | Winner | +12% | [Link] |
```

## Quick Test Brief Template

```markdown
## [Test Name]
- What: [One sentence]
- Why: [Hypothesis]
- Primary metric: [Metric]
- Duration: [X weeks]
- Result: [TBD/Winner/Loser/Inconclusive]
- Learning: [Key takeaway]
```

## Stakeholder Update Template

```markdown
## A/B Test Update: [Name]
- Status: Running / Complete
- Progress: [X% sample reached]
- Estimated decision date: [Date]

### Observations (non-decision)
[Brief notes]

### Next steps
[Actions + owners]
```

## Experiment Prioritization Scorecard

| Factor | Weight | Test A | Test B | Test C |
|--------|--------|--------|--------|--------|
| Potential impact | 30% | | | |
| Confidence | 25% | | | |
| Ease of implementation | 20% | | | |
| Risk if wrong | 15% | | | |
| Strategic alignment | 10% | | | |
| Total | | | | |

## Hypothesis Bank Template

```markdown
| ID | Area | Observation | Hypothesis | Potential Impact | Status |
|----|------|-------------|------------|------------------|--------|
| H1 | Homepage | Low scroll depth | Shorter hero improves scroll | High | Backlog |
```
