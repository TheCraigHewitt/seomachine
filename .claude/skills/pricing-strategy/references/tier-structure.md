# Tier Structure and Packaging

## How Many Tiers?

| Tier Count | Tradeoff |
|------------|----------|
| 2 | Simple choice, lower granularity |
| 3 | Good balance (good/better/best) |
| 4+ | More segmentation, higher complexity |

## Good-Better-Best Framework

- **Good**: low-friction entry, core value
- **Better**: default recommendation, strongest value/price balance
- **Best**: premium outcomes, advanced controls, higher limits

## Tier Differentiation Strategies

- Feature gating
- Usage limits
- Support level
- Admin/security/compliance access

## Example Tier Structure

```text
Starter  $29/mo   -> up to 5 users, core features, email support
Pro      $79/mo   -> up to 20 users, advanced features, priority support
Business $199/mo  -> unlimited users, SSO/audit logs, dedicated support
```

## Packaging for Personas

### Persona Mapping Table

| Persona | Typical Needs | Relative WTP |
|---------|---------------|--------------|
| Freelancer | Core workflow | Low |
| Small Team | Collaboration | Medium |
| Growing Co | Integrations + scale | High |
| Enterprise | Security + control + procurement fit | Highest |

### Feature Mapping Pattern

| Feature | Entry | Mid | Enterprise |
|---------|-------|-----|------------|
| Core product | Yes | Yes | Yes |
| Collaboration | Limited | Full | Full |
| Integrations | Limited | Full | Full |
| API access | No | Yes | Yes |
| SSO/SAML | No | No | Yes |
| Audit logs | No | No | Yes |

## Freemium vs Free Trial

### Freemium Works Better When
- Viral/network effects exist
- Free users create distribution/data value
- Marginal servicing cost is low

### Free Trial Works Better When
- Setup time is required to see value
- Price point is higher
- Sales/education motion is needed

### Typical Trial Notes
- Typical: 7-14 days for simple workflows
- Typical: 14-30 days for complex workflows
- Card-upfront trials often increase conversion quality but reduce trial starts

### Hybrid Patterns
- Freemium core + premium trial
- Reverse trial (full access first, then downgrade)

## Enterprise Pricing

### When to Add Custom Pricing
- Higher ACV deals
- Security/procurement requirements
- Contracting and implementation complexity

### Enterprise Tier Elements
- SSO/SAML
- Audit logs/admin controls
- SLA and security docs
- Dedicated support/success
- Optional custom integrations

### Enterprise Pricing Models
- Per-seat with volume discounts
- Platform fee + usage
- Outcome/value-based contracts
