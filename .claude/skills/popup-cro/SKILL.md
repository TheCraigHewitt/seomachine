---
name: popup-cro
version: 1.0.0
description: Use for conversion popups/modals/slide-ins/banners (email capture, promotions, announcements, exit-intent saves, feature promos). For non-popup forms use form-cro; for page-level CRO use page-cro.
---

# Popup CRO

Design popups that convert without damaging UX, trust, or SEO/accessibility.

## Scope and Pre-Work

- If `.claude/product-marketing-context.md` exists, read it first.
- Confirm:
  1. Popup objective (`email capture`, `lead magnet`, `promo`, `announcement`, `exit save`, `feature promotion`, `survey`).
  2. Current performance (impression, conversion, close rate, complaints).
  3. Trigger logic and pages where it appears.
  4. Audience split (new vs. returning, traffic source, mobile share).

---

## Core Principles

### 1. Timing Controls Perception
Bad timing reads as interruption; good timing reads as assistance.

### 2. Value Must Be Immediate
The offer must be clear and worth the interruption within seconds.

### 3. User Respect Preserves Brand
Visible close affordance, easy dismiss, and suppression after decline are non-negotiable.

---

## Trigger Strategy Taxonomy

| Trigger | Best Use Cases | Risks | Practical Rule |
|--------|----------------|-------|----------------|
| Time-delay | Broad top-of-funnel capture | Too early = annoyance | Start with 30-60s, not 5-10s |
| Scroll-depth | Content/blog engagement | Poor on short pages | 25-50% depth for long content |
| Exit-intent | Last-chance save for abandoning users | Can feel aggressive | Offer should differ from on-entry prompts |
| Click-triggered | Lead magnets, demos, downloads | Lower scale if triggers are hidden | Use explicit trigger text (`Get the guide`) |
| Session/page-count | Comparison journeys | Late exposure may miss users | Use after meaningful engagement (e.g., 2+ pages) |
| Behavior-based | Pricing views, cart events, repeat visits | Overfitting/over-triggering | Gate by intent + frequency cap |

Mobile note: true cursor-based exit-intent is unavailable. Use back-button intent, upward scroll patterns, or inactivity heuristics.

---

## Popup Type Playbooks

### Email Capture
- Lead with clear benefit, not "Subscribe for updates".
- Prefer single field (email).
- Example CTA: `Get Weekly Teardown Tips`.

### Lead Magnet
- Show what is delivered (cover, preview bullets, format).
- Set delivery expectation (`Instant PDF` / `Sent now`).
- Keep fields minimal.

### Discount/Promo
- Explicit value (`10% off`, `$20 off`, free shipping).
- Clarify constraints (new customers, minimum order, expiration).
- Ensure coupon apply path is frictionless.

### Exit-Intent Rescue
- Acknowledge departure and offer a distinct save message.
- Use objection-handling copy or alternative path (`Need help choosing?`).

### Announcement Banner
- Single message, clear destination link, dismissable.
- Time-box banners so they do not become ignored permanent chrome.

### Slide-In
- Lower interruption format for secondary actions, support, or reminders.
- Should not block primary page interactions.

---

## Design and Copy Standards

### Visual Hierarchy
1. Headline (core value)
2. Offer details/subhead
3. Form/CTA
4. Dismiss option

### Sizing and Placement
- Desktop modal width usually 400-600px.
- Avoid full-screen overlays unless legally required.
- On mobile, prefer bottom sheet/slide-up over full-screen takeover.

### Dismiss Mechanics
- Visible `X` in expected location.
- Click outside to close (for modals).
- `Esc` key support on desktop.
- Optional text decline (`No thanks`, `Maybe later`).

### Copy Rules
- Be specific: `Claim My 10% Off` beats `Submit`.
- Keep subhead focused on concrete value + reassurance (`No spam`).
- Avoid guilt-driven decline text.

Examples:
- Headline: `Get 5 proven landing page teardown templates`
- Subhead: `One email each Friday. Unsubscribe anytime.`
- CTA: `Send Me the Templates`
- Decline: `No thanks`

---

## Frequency, Targeting, and Exclusions

### Frequency Capping
- Max once per session by default.
- Persist dismissals via cookie/localStorage.
- Re-show windows typically 7-30 days depending on offer value.

### Targeting Rules
- Segment by new/returning visitor, traffic source, and page context.
- Match popup offer to page intent.
- Exclude users who already converted on that offer.

### Exclusion Rules (Critical)
- Do not interrupt checkout or critical conversion flows.
- Suppress overlapping popups; define priority order.
- Avoid stacking multiple overlays in one session.

---

## Compliance and Accessibility

### Privacy and Consent
- Clear consent text when collecting emails.
- Link to privacy policy.
- No pre-checked consent boxes where regulation disallows it.

### Accessibility Requirements
- Keyboard navigable (`Tab`, `Enter`, `Esc`).
- Focus moves into popup and returns correctly on close.
- Screen reader labels for title, close button, form fields.
- Sufficient contrast and non-color-only cues.

### Search/UX Policy Constraints
- Intrusive mobile interstitials can hurt search performance.
- Prefer reasonable overlays and banners that do not block primary content at load.

---

## Measurement

Track by trigger type, segment, and device.

### Core Metrics
- **Impression rate** (who sees popup)
- **Conversion rate** (impression -> desired action)
- **Immediate close rate**
- **Interaction rate** (focus, click, scroll within popup)
- **Time to close / time to convert**

### Secondary Metrics
- Downstream conversion quality (lead quality, purchase rate)
- Bounce/exit impact after popup display
- Complaint/unsubscribe/support signals

Typical ranges (context-dependent):
- Email capture popups: often low single digits.
- Exit-intent offers: often higher when message/offer is strong.
- Click-triggered modals: usually highest intent and conversion.

---

## Output Format

### Popup Spec
- **Type**
- **Trigger**
- **Audience/targeting**
- **Frequency + suppression rules**
- **Copy** (headline, subhead, CTA, decline)
- **Design notes** (desktop/mobile, accessibility)

### Multi-Popup Strategy (if needed)
- Popup 1: purpose + trigger + audience
- Popup 2: purpose + trigger + audience
- Conflict resolution: priority and suppression logic

### Test Plan
For each test: variant, hypothesis, primary metric, guardrail metric.

---

## Experiment Backlog Starters

### Trigger Tests
- 30s delay vs. 50% scroll vs. exit-intent
- 25% vs. 50% vs. 75% scroll threshold
- Click-triggered inline CTA vs. automatic modal

### Message Tests
- Value-focused vs. urgency-focused headline
- CTA copy variants (`Get My Discount` vs. `Unlock Offer`)
- With vs. without social proof near CTA

### Format Tests
- Center modal vs. slide-in
- Modal size variants by device
- Minimal design vs. visual-rich layout

### Frequency Tests
- Once/session vs. once/7 days
- Re-show timing after dismissal
- Escalating offer after repeated declines vs. static offer

---

## Related Skills

- `form-cro`
- `page-cro`
- `email-sequence`
- `ab-test-setup`
