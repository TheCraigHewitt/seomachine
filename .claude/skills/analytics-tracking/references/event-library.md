# Event Library Reference

## Marketing Site Events

### Navigation & Engagement

| Event Name | Description | Properties |
|------------|-------------|------------|
| page_view | Page loaded | page_title, page_location, content_group |
| scroll_depth | Scroll threshold reached | depth (25, 50, 75, 100) |
| outbound_link_clicked | External link click | link_url, link_text |
| video_played | Video started | video_id, video_title |

### CTA & Form Interactions

| Event Name | Description | Properties |
|------------|-------------|------------|
| cta_clicked | CTA clicked | cta_text, cta_location, page |
| form_submitted | Successful submit | form_name, form_location |
| form_error | Validation or submit error | form_name, error_type |

### Conversion Events

| Event Name | Description | Properties |
|------------|-------------|------------|
| signup_started | Signup initiated | source, page |
| signup_completed | Signup completed | method, plan, source |
| demo_requested | Demo request submitted | company_size, industry |
| newsletter_subscribed | List signup | list_name, source |
| trial_started | Trial created | plan, source |

## Product/App Events

### Onboarding

| Event Name | Description | Properties |
|------------|-------------|------------|
| onboarding_started | Onboarding flow started | plan, source |
| onboarding_step_completed | Step completed | step_number, step_name |
| onboarding_completed | All required steps done | time_to_complete |
| onboarding_skipped | User skipped flow | step_skipped_at |
| first_key_action_completed | First value action done | action_type |

### Core Usage

| Event Name | Description | Properties |
|------------|-------------|------------|
| session_started | Product session started | session_number |
| feature_used | Feature interaction | feature_name, feature_category |
| content_created | New content created | content_type |
| invite_sent | Invite sent | invite_type, count |
| settings_changed | Settings changed | setting_name |

### Errors & Support

| Event Name | Description | Properties |
|------------|-------------|------------|
| error_occurred | Product error surfaced | error_type, error_message, page |
| help_opened | Help surface opened | help_type, page |
| support_contacted | Support request created | contact_method, issue_type |
| feedback_submitted | Product feedback submitted | feedback_type, rating |

## Monetization Events

### Pricing & Checkout

| Event Name | Description | Properties |
|------------|-------------|------------|
| pricing_viewed | Pricing page viewed | source |
| plan_selected | Plan selected | plan_name, billing_cycle |
| checkout_started | Checkout initiated | plan, value |
| payment_info_entered | Payment info submitted | payment_method |
| purchase_completed | Purchase success | transaction_id, value, currency |
| purchase_failed | Purchase failed | error_reason, plan |

### Subscription Lifecycle

| Event Name | Description | Properties |
|------------|-------------|------------|
| trial_started | Trial started | plan, trial_length |
| trial_ended | Trial ended | plan, converted |
| subscription_upgraded | Plan upgrade | from_plan, to_plan, value |
| subscription_cancelled | Subscription cancelled | reason, tenure |
| subscription_renewed | Subscription renewed | plan, value |

## E-commerce Events

### Browsing, Cart, Checkout

| Event Name | Description | Properties |
|------------|-------------|------------|
| product_viewed | Product detail viewed | item_id, item_name, category, price |
| product_added_to_cart | Added item to cart | item_id, price, quantity |
| product_removed_from_cart | Removed item from cart | item_id, quantity |
| cart_viewed | Cart viewed | cart_value, items_count |
| checkout_started | Checkout started | cart_value, items_count |
| shipping_info_entered | Shipping step completed | shipping_method |
| payment_info_entered | Payment step completed | payment_method |
| purchase_completed | Order completed | transaction_id, value, currency |

## B2B / SaaS Events

| Event Name | Description | Properties |
|------------|-------------|------------|
| team_created | Team created | team_size, plan |
| team_member_invited | Team invite sent | role, invite_method |
| team_member_joined | Team invite accepted | role |
| integration_connected | Integration connected | integration_name |
| account_churned | Account closed | reason, tenure, mrr_lost |

## Standard Property Sets

### User Context

```text
user_id
user_type
account_id
plan_type
```

### Session Context

```text
session_id
session_number
page
referrer
```

### Campaign Context

```text
source
medium
campaign
content
term
```

### Commerce Context

```text
item_id
item_name
category
price
quantity
currency
```

## Funnel Event Sequences

### Signup Funnel
1. signup_started
2. signup_step_completed
3. signup_completed
4. onboarding_started
5. first_key_action_completed

### Purchase Funnel
1. pricing_viewed
2. plan_selected
3. checkout_started
4. payment_info_entered
5. purchase_completed

### E-commerce Funnel
1. product_viewed
2. product_added_to_cart
3. cart_viewed
4. checkout_started
5. shipping_info_entered
6. payment_info_entered
7. purchase_completed
