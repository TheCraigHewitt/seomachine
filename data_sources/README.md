# Data Sources

This directory contains integrations for analytics and SEO data sources that power the Performance Agent and inform content strategy decisions.

## Overview

Data sources provide real-time performance metrics for:
- **Content Performance**: Which articles drive traffic and conversions
- **SEO Opportunities**: Keywords ranking 11-20 ready to push to page 1
- **Content Gaps**: Topics competitors rank for but Castos doesn't
- **Update Priority**: Articles declining in traffic or outdated

## Supported Data Sources

### Google Analytics 4 (GA4)
- **Purpose**: Traffic, engagement, and conversion data
- **Key Metrics**:
  - Page views and sessions by article
  - Average engagement time
  - Bounce rate and scroll depth
  - Conversion tracking (sign-ups, trials)
  - Traffic sources (organic, direct, referral)

### Google Search Console
- **Purpose**: Search performance and keyword data
- **Key Metrics**:
  - Impressions and clicks by page
  - Average position by keyword
  - Click-through rate (CTR)
  - Queries ranking 11-20 (quick win opportunities)
  - Search appearance features

### DataForSEO
- **Purpose**: Competitive SEO data and keyword research
- **Key Metrics**:
  - Keyword rankings (daily updates)
  - Competitor analysis
  - SERP features and positions
  - Search volume and difficulty
  - Related keywords and questions

## Directory Structure

```
data_sources/
├── config/                 # API credentials and settings
│   ├── .env.example       # Template for environment variables
│   ├── ga4_config.json    # GA4 property settings
│   ├── gsc_config.json    # Search Console property settings
│   └── dataforseo_config.json  # DataForSEO settings
├── modules/               # Integration modules
│   ├── google_analytics.py
│   ├── google_search_console.py
│   ├── dataforseo.py
│   └── data_aggregator.py
├── utils/                 # Utility functions
│   ├── auth.py           # Authentication helpers
│   ├── cache.py          # Caching layer
│   └── formatters.py     # Data formatting utilities
├── cache/                 # Cached API responses
│   └── .gitkeep
└── README.md             # This file
```

## Setup

### 1. Install Dependencies

```bash
pip install google-analytics-data google-auth-oauthlib google-auth-httplib2
pip install google-api-python-client
pip install requests python-dotenv pandas
```

Or use the requirements file:
```bash
pip install -r data_sources/requirements.txt
```

### 2. Configure API Credentials

#### Google Analytics 4
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google Analytics Data API
4. Create service account credentials
5. Download JSON key file
6. Save as `data_sources/config/ga4_credentials.json`
7. Add service account email to GA4 property (View access)

#### Google Search Console
1. Use same Google Cloud project
2. Enable Search Console API
3. Use same service account or create OAuth 2.0 credentials
4. Save credentials as `data_sources/config/gsc_credentials.json`
5. Add service account to Search Console property (Owner or Full access)

#### DataForSEO
1. Sign up at [DataForSEO](https://dataforseo.com/)
2. Get API credentials (login + password)
3. Add to `.env` file:
   ```
   DATAFORSEO_LOGIN=your_login
   DATAFORSEO_PASSWORD=your_password
   ```

### 3. Configure Data Sources

Copy example config:
```bash
cp data_sources/config/.env.example data_sources/config/.env
```

Edit `.env` with your credentials:
```env
# Google Analytics 4
GA4_PROPERTY_ID=123456789
GA4_CREDENTIALS_PATH=data_sources/config/ga4_credentials.json

# Google Search Console
GSC_SITE_URL=https://castos.com
GSC_CREDENTIALS_PATH=data_sources/config/gsc_credentials.json

# DataForSEO
DATAFORSEO_LOGIN=your_login
DATAFORSEO_PASSWORD=your_password
DATAFORSEO_BASE_URL=https://api.dataforseo.com

# Cache settings
CACHE_ENABLED=true
CACHE_TTL_HOURS=24
```

## Usage

### From Command Line

#### Fetch Google Analytics Data
```python
from data_sources.modules.google_analytics import GoogleAnalytics

ga = GoogleAnalytics()

# Get top performing articles (last 30 days)
top_articles = ga.get_top_pages(days=30, limit=10)

# Get traffic trends for specific URL
trends = ga.get_page_trends(
    url="/blog/podcast-monetization-guide",
    days=90
)

# Get conversion data
conversions = ga.get_conversions(days=30)
```

#### Fetch Search Console Data
```python
from data_sources.modules.google_search_console import GoogleSearchConsole

gsc = GoogleSearchConsole()

# Get ranking positions
rankings = gsc.get_keyword_positions(days=30)

# Find quick win opportunities (position 11-20)
quick_wins = gsc.get_quick_wins()

# Get specific page performance
page_data = gsc.get_page_performance(
    url="/blog/podcast-monetization-guide"
)
```

#### Fetch DataForSEO Data
```python
from data_sources.modules.dataforseo import DataForSEO

dfs = DataForSEO()

# Get keyword rankings
rankings = dfs.get_rankings(
    keywords=["podcast hosting", "podcast analytics"]
)

# Analyze competitor rankings
competitor_data = dfs.analyze_competitor(
    competitor_domain="competitor.com",
    keywords=["podcast hosting"]
)

# Get SERP data
serp = dfs.get_serp_data(keyword="podcast monetization")
```

### From Claude Code Agent

The Performance Agent automatically uses these data sources:

```
/performance-review

# This command:
# 1. Fetches data from all sources
# 2. Analyzes performance trends
# 3. Identifies opportunities
# 4. Prioritizes next actions
# 5. Creates recommendations report
```

## Data Aggregation

The `DataAggregator` combines data from all sources:

```python
from data_sources.modules.data_aggregator import DataAggregator

aggregator = DataAggregator()

# Get comprehensive page performance
performance = aggregator.get_page_performance(
    url="/blog/podcast-monetization-guide"
)

# Returns:
# {
#   'url': '/blog/podcast-monetization-guide',
#   'ga4': {
#     'pageviews': 12500,
#     'avg_engagement_time': 245,
#     'bounce_rate': 0.42
#   },
#   'gsc': {
#     'impressions': 45000,
#     'clicks': 3200,
#     'avg_position': 8.5,
#     'ctr': 0.071
#   },
#   'dataforseo': {
#     'primary_keyword': 'podcast monetization',
#     'position': 8,
#     'search_volume': 2900
#   }
# }
```

## Caching

To avoid API rate limits and costs:
- Responses are cached for 24 hours by default
- Cache files stored in `data_sources/cache/`
- Adjust `CACHE_TTL_HOURS` in `.env`
- Clear cache: `rm -rf data_sources/cache/*`

## Performance Agent Integration

The Performance Agent uses this data to:

1. **Identify Declining Content**
   - Articles losing traffic (GA4)
   - Keywords dropping in position (GSC + DataForSEO)
   - Increased bounce rates (GA4)

2. **Find Quick Wins**
   - Keywords ranking 11-20 (GSC + DataForSEO)
   - High impressions, low CTR (GSC)
   - Competitor gaps (DataForSEO)

3. **Prioritize Updates**
   - High-traffic articles with old data
   - Articles on page 2 for valuable keywords
   - Content gaps in topic clusters

4. **Suggest New Content**
   - Rising search queries (GSC)
   - Competitor keyword gaps (DataForSEO)
   - Related questions (DataForSEO)

## Rate Limits & Costs

### Google Analytics 4
- **Free Tier**: 25,000 requests/day
- **Quotas**: Per-property quotas apply
- **Cost**: Free for standard properties

### Google Search Console
- **Free Tier**: Unlimited (reasonable use)
- **Limits**: 1000 rows per request
- **Cost**: Free

### DataForSEO
- **Pricing**: Pay-per-request
- **Typical Costs**:
  - SERP check: $0.006 per keyword
  - Ranking check: $0.0005 per keyword
  - Keyword data: $0.006 per keyword
- **Budget**: Set monthly limits in config
- **Tip**: Use caching aggressively to minimize costs

## Security

**IMPORTANT**: Never commit credentials to git!

- `.env` files are in `.gitignore`
- Credential JSON files are in `.gitignore`
- Use service accounts, not user accounts
- Rotate credentials regularly
- Limit service account permissions to read-only

## Troubleshooting

### "Authentication failed"
- Verify credentials file exists and path is correct
- Check service account has access to property
- Ensure APIs are enabled in Google Cloud Console

### "No data returned"
- Check date ranges (some properties have data delays)
- Verify property IDs and site URLs are correct
- Ensure property has data for requested time period

### "Rate limit exceeded"
- Enable caching to reduce API calls
- Increase cache TTL in `.env`
- For DataForSEO, check account limits and budget

### "Module not found"
- Install dependencies: `pip install -r data_sources/requirements.txt`
- Check Python path includes data_sources directory

## Best Practices

1. **Cache Aggressively**: Use 24-hour cache for historical data
2. **Batch Requests**: Fetch multiple pages/keywords in one request
3. **Monitor Costs**: Track DataForSEO usage, set budget alerts
4. **Refresh Strategically**: Daily updates for priority content only
5. **Validate Data**: Cross-reference between sources for accuracy

## Future Enhancements

Potential additions:
- [ ] Ahrefs integration (backlink data)
- [ ] SEMrush integration (additional keyword data)
- [ ] Automated reporting via email
- [ ] Slack notifications for significant changes
- [ ] Historical data export and visualization
- [ ] A/B test result tracking

## Support

For issues with:
- **Google APIs**: [Google Analytics API docs](https://developers.google.com/analytics/devguides/reporting/data/v1)
- **Search Console API**: [Search Console API docs](https://developers.google.com/webmaster-tools/search-console-api-original)
- **DataForSEO**: [DataForSEO docs](https://docs.dataforseo.com/)

---

**Note**: Data sources power the Performance Agent to make data-driven content decisions. Proper setup ensures accurate, actionable insights.
