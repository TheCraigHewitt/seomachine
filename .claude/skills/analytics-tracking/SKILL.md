---
name: analytics-tracking
version: 1.0.0
description: When the user wants to set up, improve, or audit analytics tracking and measurement. Also use when the user mentions "set up tracking," "GA4," "Google Analytics," "conversion tracking," "event tracking," "UTM parameters," "tag manager," "GTM," "analytics implementation," or "tracking plan." For A/B test measurement, see ab-test-setup.
---

# Analytics Tracking

Read `.claude/product-marketing-context.md` if it exists.

## Initial Assessment

Capture:
1. **Decision questions** this data must answer.
2. **Current tooling and implementation state**.
3. **Technical and compliance constraints**.

## Core Principles

1. Track for decisions, not volume.
2. Start from business questions, then map events.
3. Enforce naming consistency.
4. Validate data quality continuously.

## Tracking Plan Framework

### Structure

```text
Event Name | Category | Properties | Trigger | Owner | Notes
```

### Event Types

| Type | Examples |
|------|----------|
| Page/Screen | page_view, screen_view |
| User Action | cta_clicked, form_submitted |
| System State | signup_completed, purchase_completed |
| Conversion | demo_requested, trial_started |

Comprehensive event catalog: [references/event-library.md](references/event-library.md)

## Event Naming Conventions

### Preferred Format: object_action

```text
signup_completed
cta_clicked
checkout_started
purchase_completed
```

### Rules
- lowercase + underscores
- specific event names
- put context in properties, not event name
- avoid PII in event payloads

## Essential Events (Starter Set)

### Marketing Site

| Event | Key Properties |
|-------|----------------|
| cta_clicked | cta_text, location, page |
| form_submitted | form_name, form_location |
| signup_started | source, page |
| signup_completed | method, source |
| demo_requested | company_size, industry |

### Product/App

| Event | Key Properties |
|-------|----------------|
| onboarding_started | plan, source |
| onboarding_step_completed | step_name, step_number |
| first_key_action_completed | action_type |
| feature_used | feature_name |
| subscription_upgraded | from_plan, to_plan |
| subscription_cancelled | reason, tenure |

## Event Properties

| Category | Typical Properties |
|----------|--------------------|
| Page Context | page_title, page_path, referrer |
| User Context | user_id, account_id, plan_type |
| Campaign Context | source, medium, campaign, content, term |
| Commerce Context | item_id, category, value, currency |

## GA4 and GTM Implementation

Detailed implementation guides:
- GA4: [references/ga4-implementation.md](references/ga4-implementation.md)
- GTM: [references/gtm-implementation.md](references/gtm-implementation.md)

## UTM Parameter Strategy

| Parameter | Purpose | Example |
|-----------|---------|---------|
| utm_source | Origin | google, newsletter |
| utm_medium | Channel type | cpc, email, social |
| utm_campaign | Campaign identifier | q1_launch |
| utm_content | Creative/version | hero_cta_a |
| utm_term | Paid keyword | project+software |

Rules:
- lowercase only
- consistent separators
- maintain a shared UTM registry

## Debugging and Validation

### Validation Checklist
- [ ] Events fire on intended triggers
- [ ] Event properties populate correctly
- [ ] No duplicate events
- [ ] Conversions are recorded as expected
- [ ] Cross-browser and mobile checks complete
- [ ] No PII in analytics payloads

### Common Failure Modes

| Issue | First Checks |
|-------|--------------|
| Missing events | Trigger config, container publish state |
| Wrong values | dataLayer path, variable mapping |
| Duplicates | duplicate tags, overlapping triggers |

## Privacy and Compliance

- Respect consent before analytics/ad storage where required.
- Do not send personal identifiers in event properties.
- Set retention and deletion workflows intentionally.

## Output Format

```markdown
# [Site/Product] Tracking Plan

## Overview
- Tools: [GA4, GTM, ...]
- Last updated: [Date]

## Events
| Event Name | Description | Properties | Trigger |
|------------|-------------|------------|---------|
| signup_completed | User completes signup | method, plan, source | Success page |

## Custom Dimensions
| Name | Scope | Parameter |
|------|-------|-----------|
| user_type | User | user_type |

## Conversions
| Conversion | Event | Counting |
|------------|-------|----------|
| Signup | signup_completed | Once per session |
```
