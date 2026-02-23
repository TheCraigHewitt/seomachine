# Google Tag Manager Implementation Reference

## Container Structure

### Tags
- GA4 config and event tags
- Ad platform conversion tags
- Custom HTML tags when required

### Triggers
- Page view
- Link/click
- Form submit
- Scroll/visibility
- Custom event (from dataLayer)

### Variables
- Built-in click/page/form variables
- dataLayer variables
- lookup/regex/constant/custom JS variables

## Naming Conventions

```text
[Type] - [Purpose] - [Detail]

GA4 - Config - Base
GA4 - Event - Signup Completed
Ads - Conversion - Demo Request
Trigger - Form Submit - Contact
DL - user_id
```

## dataLayer Patterns

### Initialization and Event Push

```javascript
window.dataLayer = window.dataLayer || [];

dataLayer.push({
  event: 'event_name',
  property1: 'value1'
});
```

### Page Context Push

```javascript
dataLayer.push({
  pageType: 'product',
  contentGroup: 'products',
  user: {
    loggedIn: true,
    userId: '12345',
    userType: 'premium'
  }
});
```

### Form Submission

```javascript
document.querySelector('#contact-form')?.addEventListener('submit', function () {
  dataLayer.push({
    event: 'form_submitted',
    formName: 'contact',
    formLocation: 'footer'
  });
});
```

### CTA Click

```javascript
document.querySelector('.cta-button')?.addEventListener('click', function () {
  dataLayer.push({
    event: 'cta_clicked',
    ctaText: this.innerText,
    ctaLocation: 'hero'
  });
});
```

### E-commerce Pattern

```javascript
dataLayer.push({ ecommerce: null });
dataLayer.push({
  event: 'purchase',
  ecommerce: {
    transaction_id: 'T12345',
    value: 99.99,
    currency: 'USD',
    items: [{ item_id: 'SKU123', item_name: 'Product Name', price: 99.99, quantity: 1 }]
  }
});
```

## Common Tag Configurations

### GA4 Configuration Tag
- Type: GA4 Configuration
- Measurement ID: `G-XXXXXXXX`
- Trigger: All Pages

### GA4 Event Tag
- Type: GA4 Event
- Config tag: base GA4 tag
- Event name: static or dataLayer variable
- Trigger: custom event match

### Custom Pixel/Event Tags

```html
<script>
  // Example pattern: fire platform event from GTM on mapped trigger
  platform('track', 'Lead', { source: '{{Page URL}}' });
</script>
```

## Preview and Debug

### Preview Mode Workflow
1. Open GTM preview
2. Connect target URL
3. Inspect fired/not fired tags
4. Validate variable values and dataLayer payloads

### Debug Checks
- Tag not firing -> trigger condition mismatch
- Wrong values -> variable path/timing issue
- Duplicate fires -> overlapping triggers or duplicate tags

## Workspaces and Versioning

- Use separate workspaces for larger changes
- Name versions clearly and include rollback notes
- Record what changed and where it was tested

Example note:

```text
v15: Added purchase conversion tracking
- Tag: GA4 - Event - Purchase
- Trigger: Custom Event - purchase
- Variables: DL - transaction_id, DL - value
- Tested: Chrome, Safari, mobile
```

## Consent Management

```javascript
gtag('consent', 'default', {
  analytics_storage: 'denied',
  ad_storage: 'denied'
});

function grantConsent() {
  gtag('consent', 'update', {
    analytics_storage: 'granted',
    ad_storage: 'granted'
  });
}
```

In GTM:
1. Enable consent overview.
2. Set required consent type per tag.
3. Verify behavior in preview.

## Advanced Patterns

### Tag Sequencing
- Fire base config before event tags.
- Use sequencing for dependency chains.

### Trigger Exceptions
- Exclude internal/test environments.
- Prevent firing on irrelevant routes.

### Custom JavaScript Variables

```javascript
function() {
  const params = new URLSearchParams(window.location.search);
  return params.get('campaign') || '(not set)';
}
```
