# GA4 Implementation Reference

## Configuration

### Data Streams
- Create one stream per platform (web, iOS, Android)
- Enable enhanced measurement where relevant
- Set data retention intentionally
- Enable Google Signals only where consent policy allows

### Enhanced Measurement Events

| Event | Description |
|-------|-------------|
| page_view | Page load |
| scroll | Scroll depth tracking |
| outbound_click | External click |
| site_search | On-site search |
| video_engagement | Embedded video interactions |
| file_download | Supported file download |

### Recommended Events
- Core: sign_up, login, search, share
- Commerce: view_item, add_to_cart, begin_checkout, add_payment_info, purchase, refund

Reference: https://support.google.com/analytics/answer/9267735

## Custom Events

### gtag.js

```javascript
gtag('event', 'signup_completed', {
  method: 'email',
  plan: 'free'
});

gtag('event', 'purchase', {
  transaction_id: 'T12345',
  value: 99.99,
  currency: 'USD',
  items: [{ item_id: 'SKU123', item_name: 'Product Name', price: 99.99 }]
});

gtag('set', 'user_properties', {
  user_type: 'premium',
  plan_name: 'pro'
});
```

### GTM via dataLayer

```javascript
dataLayer.push({
  event: 'signup_completed',
  method: 'email',
  plan: 'free'
});

dataLayer.push({ ecommerce: null });
dataLayer.push({
  event: 'purchase',
  ecommerce: {
    transaction_id: 'T12345',
    value: 99.99,
    currency: 'USD'
  }
});
```

## Conversion Setup

1. Verify event collection in DebugView.
2. Mark event as conversion in Admin.
3. Set counting method appropriately.
4. Import conversions to Google Ads when needed.

### Conversion Value Example

```javascript
gtag('event', 'purchase', {
  value: 99.99,
  currency: 'USD'
});
```

## Custom Dimensions and Metrics

### Typical Uses
- Custom dimensions: segment/filter fields (user_type, industry)
- Custom metrics: numeric values (scores, durations, counts)

### Setup Steps
1. Admin -> Custom definitions
2. Create dimension/metric
3. Choose scope (event/user/item)
4. Match parameter name exactly

## Audiences

Use audiences for:
- remarketing exports
- lifecycle segment analysis
- trigger-based campaigns

Example audiences:
- pricing viewers (no conversion, last 7 days)
- engaged users (3+ sessions)
- purchasers (for exclusion/lookalike seeds)

## Debugging

### DebugView
- `?debug_mode=true`
- GA Debugger extension
- `debug_mode: true` in config

### Common Issues
- Events missing -> tag/trigger misconfig or filters
- Parameters missing -> no custom definition or name mismatch
- Conversion missing -> event not marked or wrong counting setup

## Data Quality

- Exclude internal/dev traffic
- Configure cross-domain tracking where needed
- Validate session settings for your funnel model

## Integration with Google Ads

1. Link GA4 property to Ads account.
2. Ensure auto-tagging is enabled.
3. Import conversions and/or audiences.
