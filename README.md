# SEO Machine

A specialized Claude Code workspace for creating long-form, SEO-optimized blog content for any business. This system helps you research, write, analyze, and optimize content that ranks well and serves your target audience.

## Overview

SEO Machine is built on Claude Code and provides:
- **Custom Commands**: `/research`, `/write`, `/rewrite`, `/analyze-existing`, `/optimize`, `/performance-review`, `/publish-draft`, `/article`, `/priorities`, plus specialized research and landing page commands
- **Specialized Agents**: Content analyzer, SEO optimization, meta element creation, internal linking, keyword mapping, editor, performance analysis, headline generator, CRO analyst, landing page optimizer
- **Marketing Skills**: 26 marketing skills for copywriting, CRO, A/B testing, email sequences, pricing strategy, and more
- **Advanced SEO Analysis**: Search intent detection, keyword density & clustering, content length comparison, readability scoring, SEO quality rating (0-100)
- **Data Integrations**: Google Analytics 4, Google Search Console, DataForSEO for real-time performance insights
- **Context-Driven**: Brand voice, style guide, SEO guidelines, and examples guide all content
- **Workflow Organization**: Structured directories for topics, research, drafts, and published content

## Getting Started

### Prerequisites
- [Claude Code](https://claude.com/claude-code) installed
- Anthropic API account

### Installation

1. Clone this repository:
```bash
git clone https://github.com/[your-username]/seomachine.git
cd seomachine
```

2. Install Python dependencies for analysis modules:
```bash
pip install -r data_sources/requirements.txt
```

This installs:
- Google Analytics/Search Console integrations
- DataForSEO API client
- NLP libraries (nltk, textstat)
- Machine learning (scikit-learn)
- Web scraping tools (beautifulsoup4)

3. Open in Claude Code:
```bash
claude-code .
```

4. **Customize Context Files** (Important!):

   All context files are provided as templates. Fill them out with your company's information:

   - `context/brand-voice.md` - Define your brand voice and messaging *(see examples/castos/ for reference)*
   - `context/writing-examples.md` - Add 3-5 exemplary blog posts from your site
   - `context/features.md` - List your product/service features and benefits
   - `context/internal-links-map.md` - Map your key pages for internal linking
   - `context/style-guide.md` - Fill in your style preferences
   - `context/target-keywords.md` - Add your keyword research and topic clusters
   - `context/competitor-analysis.md` - Add competitor analysis and insights
   - `context/seo-guidelines.md` - Review and adjust SEO requirements

   **Quick Start**: Check out `examples/castos/` to see a complete real-world example of all context files filled out for a podcast hosting SaaS company.

## Workflows

### Creating New Content

#### 1. Start with Research
```
/research [topic]
```

**What it does**:
- Performs keyword research
- Analyzes top 10 competitors
- Identifies content gaps
- Creates comprehensive research brief
- Saves to `/research/` directory

**Example**:
```
/research content marketing strategies for B2B SaaS
```

#### 2. Write the Article
```
/write [topic or research brief]
```

**What it does**:
- Creates 2000-3000+ word SEO-optimized article
- Maintains your brand voice from `context/brand-voice.md`
- Integrates keywords naturally
- Includes internal and external links
- Provides meta elements (title, description, keywords)
- Automatically triggers optimization agents
- Saves to `/drafts/` directory

**Example**:
```
/write content marketing strategies for B2B SaaS
```

**Agent Auto-Execution**:
After writing, these agents automatically analyze the content:
- **SEO Optimizer**: On-page SEO recommendations
- **Meta Creator**: Multiple meta title/description options
- **Internal Linker**: Specific internal linking suggestions
- **Keyword Mapper**: Keyword placement and density analysis

#### 3. Final Optimization
```
/optimize [article file]
```

**What it does**:
- Comprehensive SEO audit
- Validates all elements meet requirements
- Provides final polish recommendations
- Generates publishing readiness score
- Creates optimization report

**Example**:
```
/optimize drafts/content-marketing-strategies-2025-10-29.md
```

### Updating Existing Content

#### 1. Analyze Existing Post
```
/analyze-existing [URL or file path]
```

**What it does**:
- Fetches and analyzes current content
- Evaluates SEO performance
- Identifies outdated information
- Assesses competitive positioning
- Provides content health score (0-100)
- Recommends update priority and scope
- Saves analysis to `/research/` directory

**Examples**:
```
/analyze-existing https://yoursite.com/blog/marketing-guide
/analyze-existing published/marketing-guide-2024-01-15.md
```

#### 2. Rewrite/Update Content
```
/rewrite [topic or analysis file]
```

**What it does**:
- Updates content based on analysis findings
- Refreshes statistics and examples
- Improves SEO optimization
- Adds new sections to fill gaps
- Maintains what works from original
- Tracks changes made
- Saves to `/rewrites/` directory

**Example**:
```
/rewrite marketing guide
```

## Commands Reference

### `/research [topic]`
Comprehensive keyword and competitive research for new content.

**Output**: Research brief in `/research/brief-[topic]-[date].md`

**Includes**:
- Primary and secondary keywords
- Competitor analysis (top 10)
- Content gaps and opportunities
- Recommended outline
- Internal linking strategy
- Meta elements preview

---

### `/write [topic]`
Create long-form SEO-optimized article (2000-3000+ words).

**Output**: Article in `/drafts/[topic]-[date].md`

**Includes**:
- Complete article with H1/H2/H3 structure
- SEO-optimized content
- Internal and external links
- Meta elements (title, description, keywords)
- SEO checklist

**Auto-Triggers**:
- SEO Optimizer agent
- Meta Creator agent
- Internal Linker agent
- Keyword Mapper agent

---

### `/rewrite [topic]`
Update and improve existing content.

**Output**: Updated article in `/rewrites/[topic]-rewrite-[date].md`

**Includes**:
- Rewritten/updated content
- Change summary
- Before/after comparison
- Updated SEO elements

---

### `/analyze-existing [URL or file]`
Analyze existing blog posts for improvement opportunities.

**Output**: Analysis report in `/research/analysis-[topic]-[date].md`

**Includes**:
- Content health score (0-100)
- Quick wins (immediate improvements)
- Strategic improvements
- Rewrite priority and scope
- Research brief for rewrite

---

### `/optimize [file]`
Final SEO optimization pass before publishing.

**Output**: Optimization report in `/drafts/optimization-report-[topic]-[date].md`

**Includes**:
- SEO score (0-100)
- Priority fixes
- Quick wins
- Meta element options
- Link enhancement suggestions
- Publishing readiness assessment

---

### `/publish-draft [file]`
Publish article to WordPress via REST API with Yoast SEO metadata.

---

### `/article [topic]`
Simplified article creation workflow.

---

### `/priorities`
Content prioritization matrix using analytics data to identify highest-impact content tasks.

---

### `/scrub [file]`
Remove AI watermarks and patterns from content (em-dashes, filler phrases, robotic patterns).

---

### Research Commands

| Command | Description |
|---------|-------------|
| `/research-serp [keyword]` | SERP analysis for a target keyword |
| `/research-gaps` | Competitor content gap analysis |
| `/research-trending` | Trending topic opportunities |
| `/research-performance` | Performance-based content priorities |
| `/research-topics` | Topic cluster research |

---

### Landing Page Commands

| Command | Description |
|---------|-------------|
| `/landing-write [topic]` | Create conversion-optimized landing page |
| `/landing-audit [file]` | Audit landing page for CRO issues |
| `/landing-research [topic]` | Research competitors and positioning |
| `/landing-competitor [URL]` | Deep competitor landing page analysis |
| `/landing-publish [file]` | Publish landing page to WordPress |

## Agents

Specialized agents that automatically analyze content and provide expert recommendations.

### Content Analyzer (NEW!)
**Purpose**: Comprehensive, data-driven content analysis using 5 specialized modules

**Analyzes**:
- Search intent classification (informational/navigational/transactional/commercial)
- Keyword density and clustering with topic detection
- Content length comparison vs top SERP competitors
- Readability scoring (Flesch Reading Ease, Flesch-Kincaid Grade Level)
- SEO quality rating (0-100 score with category breakdowns)
- Keyword stuffing risk detection
- Passive voice ratio and sentence complexity
- Distribution heatmap showing keyword placement by section

**Output**:
- Executive summary with publishing readiness assessment
- Priority action plan (critical/high priority/optimization)
- Competitive positioning analysis
- Detailed recommendations for each analysis area
- Exact metrics and benchmarks for improvements

**Powered by**:
- `search_intent_analyzer.py` - Search intent detection
- `keyword_analyzer.py` - Keyword density, clustering, LSI keywords
- `content_length_comparator.py` - SERP competitor analysis
- `readability_scorer.py` - Multiple readability metrics
- `seo_quality_rater.py` - Comprehensive SEO scoring

---

### SEO Optimizer
**Purpose**: On-page SEO analysis and optimization recommendations

**Analyzes**:
- Keyword optimization and density
- Content structure and headings
- Internal and external links
- Meta elements
- Readability and user experience
- Featured snippet opportunities

**Output**: SEO score (0-100) with specific improvement recommendations

---

### Meta Creator
**Purpose**: Generate high-converting meta titles and descriptions

**Creates**:
- 5 meta title variations (50-60 chars)
- 5 meta description variations (150-160 chars)
- Testing recommendations
- SERP preview
- Conversion-optimized copy

**Output**: Multiple options with recommendation and reasoning

---

### Internal Linker
**Purpose**: Strategic internal linking recommendations

**Provides**:
- 3-5 specific internal link suggestions
- Exact placement locations
- Anchor text recommendations
- User journey mapping
- SEO impact prediction

**References**: `context/internal-links-map.md`

---

### Keyword Mapper
**Purpose**: Keyword placement and integration analysis

**Analyzes**:
- Keyword density and distribution
- Critical placement checklist
- Natural language integration quality
- LSI keyword coverage
- Cannibalization risk

**Output**: Distribution map, gap analysis, specific revision suggestions

---

### Editor
**Purpose**: Transform technically accurate content into human-sounding, engaging articles

**Analyzes**:
- Voice and personality
- Specificity of examples
- Readability and flow
- Robotic vs. human patterns
- Engagement and storytelling

**Provides**:
- Humanity score (0-100)
- Critical edits with before/after
- Pattern analysis
- Specific rewrites to inject personality
- Readability improvements

**Output**: Editorial report with specific improvements to make content sound human

---

### Performance
**Purpose**: Data-driven content prioritization using real analytics

**Analyzes**:
- Google Analytics traffic and trends
- Google Search Console rankings and CTR
- DataForSEO competitive data
- Quick wins (position 11-20)
- Declining content
- Low CTR opportunities
- Trending topics

**Provides**:
- Priority queue of content tasks
- Opportunity scores (0-100)
- Impact and effort estimates
- Week-by-week roadmap
- Success metrics

**Output**: Comprehensive performance report with actionable priorities

---

### Headline Generator
**Purpose**: Generate high-converting headline variations and A/B testing recommendations

**Provides**:
- 10+ headline variations using proven formulas
- Conversion potential scoring
- A/B testing strategies
- Audience-specific headline options

---

### CRO Analyst
**Purpose**: Conversion rate optimization analysis for landing pages

**Analyzes**:
- Above-the-fold effectiveness
- CTA quality and distribution
- Trust signal presence
- Friction points
- Page structure

---

### Landing Page Optimizer
**Purpose**: Comprehensive landing page optimization recommendations

**Provides**:
- CRO scoring (0-100) with category breakdowns
- Above-fold, CTA, trust signal, structure, and SEO analysis
- A/B testing recommendations
- Priority action list

## Marketing Skills

SEO Machine includes 26 marketing skills accessible as slash commands:

| Category | Skills |
|----------|--------|
| **Copywriting** | `/copywriting`, `/copy-editing` |
| **CRO** | `/page-cro`, `/form-cro`, `/signup-flow-cro`, `/onboarding-cro`, `/popup-cro`, `/paywall-upgrade-cro` |
| **Strategy** | `/content-strategy`, `/pricing-strategy`, `/launch-strategy`, `/marketing-ideas` |
| **Channels** | `/email-sequence`, `/social-content`, `/paid-ads` |
| **SEO** | `/seo-audit`, `/schema-markup`, `/programmatic-seo`, `/competitor-alternatives` |
| **Analytics** | `/analytics-tracking`, `/ab-test-setup` |
| **Other** | `/referral-program`, `/free-tool-strategy`, `/marketing-psychology` |

## Data Sources

### Integration with Analytics

SEO Machine integrates with real-time data sources to inform content strategy:

**Google Analytics 4**:
- Traffic and engagement metrics
- Conversion tracking
- Trend analysis
- Traffic sources

**Google Search Console**:
- Keyword rankings and positions
- Impressions and clicks
- CTR analysis
- Query performance

**DataForSEO**:
- Competitive rankings
- SERP features
- Keyword metrics
- Competitor gap analysis

### Advanced SEO Analysis Modules (NEW!)

SEO Machine includes 5 specialized Python modules for comprehensive content analysis:

**Search Intent Analyzer** (`search_intent_analyzer.py`):
- Classifies queries into informational, navigational, transactional, or commercial intent
- Analyzes SERP features and content patterns
- Provides confidence scores and content alignment recommendations

**Keyword Analyzer** (`keyword_analyzer.py`):
- Calculates exact keyword density and distribution
- Detects keyword stuffing risk with warnings
- Performs topic clustering using TF-IDF and K-means
- Generates distribution heatmap by section
- Identifies LSI (semantically related) keywords

**SEO Quality Rater** (`seo_quality_rater.py`):
- Rates content against SEO best practices (0-100 score)
- Category breakdowns: content, keywords, meta, structure, links, readability
- Identifies critical issues, warnings, and suggestions
- Determines publishing readiness

**Content Length Comparator** (`content_length_comparator.py`):
- Fetches and analyzes top 10-20 SERP competitor word counts
- Calculates median, 75th percentile, and optimal length
- Shows competitive positioning and gap to target
- Provides data-driven expansion recommendations

**Readability Scorer** (`readability_scorer.py`):
- Flesch Reading Ease and Flesch-Kincaid Grade Level
- Sentence and paragraph structure analysis
- Passive voice detection and ratio calculation
- Complex word identification
- Transition word usage analysis
- Overall readability score (0-100)

All modules can be used directly in Python or through the Content Analyzer agent.

### CRO Analysis Modules

Six Python modules for landing page conversion optimization:

- `above_fold_analyzer.py` - Above-the-fold content analysis (headline, value prop, CTA, trust)
- `cta_analyzer.py` - CTA effectiveness scoring (quality, distribution, goal alignment)
- `trust_signal_analyzer.py` - Trust signal detection (testimonials, social proof, risk reversals)
- `landing_page_scorer.py` - Overall landing page scoring (0-100 with category breakdowns)
- `landing_performance.py` - Landing page performance tracking via GA4/GSC
- `cro_checker.py` - CRO best practices checklist validation

### Additional Analysis Modules

- `opportunity_scorer.py` - 8-factor opportunity scoring for content prioritization
- `content_scorer.py` - 5-dimension content quality scoring (humanity, specificity, structure, SEO, readability)
- `engagement_analyzer.py` - Content engagement pattern analysis
- `competitor_gap_analyzer.py` - Competitive content gap identification
- `article_planner.py` - Data-driven article planning
- `section_writer.py` - Section-level content guidance
- `social_research_aggregator.py` - Social media research aggregation

### Python Research Scripts

Run from repo root:

```bash
# Content research
python3 research_quick_wins.py
python3 research_competitor_gaps.py
python3 research_performance_matrix.py
python3 research_priorities_comprehensive.py
python3 research_serp_analysis.py
python3 research_topic_clusters.py
python3 research_trending.py

# SEO analysis (config-driven - set up config/competitors.json first)
python3 seo_baseline_analysis.py
python3 seo_bofu_rankings.py
python3 seo_competitor_analysis.py

# Test API connectivity
python3 test_dataforseo.py
```

**Note**: SEO analysis scripts load competitor lists and keywords from `config/competitors.json`. Copy `config/competitors.example.json` and customize for your business.

### WordPress Integration

Publishing uses the WordPress REST API with a custom MU-plugin that exposes Yoast SEO fields.

**Setup**:
1. Install `wordpress/seo-machine-yoast-rest.php` as an MU-plugin on your WordPress site
2. Add `wordpress/functions-snippet.php` to your theme's functions.php
3. Configure WordPress credentials in `.env`:
   ```
   WP_URL=https://yoursite.com
   WP_USERNAME=your_username
   WP_APP_PASSWORD=your_application_password
   ```

See `wordpress/README.md` for detailed setup instructions.

See `data_sources/README.md` for analytics setup instructions.

## Directory Structure

```
seomachine/
├── .claude/
│   ├── commands/          # Custom workflow commands
│   │   ├── analyze-existing.md
│   │   ├── research.md
│   │   ├── write.md
│   │   ├── rewrite.md
│   │   ├── optimize.md
│   │   ├── scrub.md
│   │   ├── performance-review.md
│   │   ├── publish-draft.md
│   │   ├── article.md
│   │   ├── priorities.md
│   │   ├── research-serp.md
│   │   ├── research-gaps.md
│   │   ├── research-trending.md
│   │   ├── research-performance.md
│   │   ├── research-topics.md
│   │   ├── landing-write.md
│   │   ├── landing-audit.md
│   │   ├── landing-research.md
│   │   ├── landing-competitor.md
│   │   └── landing-publish.md
│   ├── agents/            # Specialized analysis agents
│   │   ├── content-analyzer.md
│   │   ├── seo-optimizer.md
│   │   ├── meta-creator.md
│   │   ├── internal-linker.md
│   │   ├── keyword-mapper.md
│   │   ├── editor.md
│   │   ├── performance.md
│   │   ├── headline-generator.md
│   │   ├── cro-analyst.md
│   │   └── landing-page-optimizer.md
│   └── skills/            # 26 marketing skills
├── data_sources/          # Analytics integrations
│   ├── modules/          # Python analysis modules
│   │   ├── google_analytics.py
│   │   ├── google_search_console.py
│   │   ├── dataforseo.py
│   │   ├── data_aggregator.py
│   │   ├── search_intent_analyzer.py
│   │   ├── keyword_analyzer.py
│   │   ├── seo_quality_rater.py
│   │   ├── content_length_comparator.py
│   │   ├── readability_scorer.py
│   │   ├── opportunity_scorer.py
│   │   ├── content_scorer.py
│   │   ├── engagement_analyzer.py
│   │   ├── social_research_aggregator.py
│   │   ├── competitor_gap_analyzer.py
│   │   ├── article_planner.py
│   │   ├── section_writer.py
│   │   ├── wordpress_publisher.py
│   │   ├── above_fold_analyzer.py
│   │   ├── cro_checker.py
│   │   ├── cta_analyzer.py
│   │   ├── landing_page_scorer.py
│   │   ├── landing_performance.py
│   │   └── trust_signal_analyzer.py
│   ├── config/           # API credentials (not in git)
│   ├── utils/            # Helper functions
│   ├── cache/            # Cached API responses
│   └── README.md         # Setup instructions
├── config/                # Configuration files
│   └── competitors.example.json  # Competitor config template
├── context/               # Configuration and guidelines
│   ├── brand-voice.md
│   ├── writing-examples.md
│   ├── style-guide.md
│   ├── seo-guidelines.md
│   ├── target-keywords.md
│   ├── internal-links-map.md
│   ├── competitor-analysis.md
│   └── cro-best-practices.md
├── wordpress/             # WordPress integration
│   ├── seo-machine-yoast-rest.php
│   ├── functions-snippet.php
│   └── README.md
├── topics/                # Raw topic ideas
├── research/              # Research briefs and analysis reports
├── drafts/                # Work in progress articles
├── review-required/       # Articles pending review
├── published/             # Final versions ready to publish
├── rewrites/              # Updated existing content
├── landing-pages/         # Landing page content
├── audits/                # Audit reports
└── README.md              # This file
```

## Context Files (Important!)

The quality of your content depends on well-configured context files:

### `context/brand-voice.md`
Defines your brand voice, tone, and messaging framework.

**Must include**:
- Voice pillars
- Tone guidelines by content type
- Core brand messages
- Writing style guidelines
- Terminology preferences

**Purpose**: Ensures all content sounds like your brand

---

### `context/writing-examples.md`
Contains 3-5 exemplary blog posts from your site.

**Must include**:
- Full article content
- What makes each example great
- Key takeaways for voice and structure

**Purpose**: Teaches AI your specific writing style through examples

---

### `context/style-guide.md`
Editorial and formatting standards.

**Must include**:
- Grammar and mechanics rules
- Capitalization conventions
- Formatting standards
- Preferred terminology

**Purpose**: Maintains consistency across all content

---

### `context/seo-guidelines.md`
SEO best practices and requirements.

**Includes**:
- Content length requirements
- Keyword optimization rules
- Meta element standards
- Link strategy guidelines
- Readability requirements

**Purpose**: Ensures all content meets SEO standards

---

### `context/target-keywords.md`
Keyword research organized by topic cluster.

**Must include**:
- Pillar keywords by cluster
- Cluster keywords (subtopics)
- Long-tail variations
- Search intent classification
- Current rankings

**Purpose**: Guides keyword targeting for new content

---

### `context/internal-links-map.md`
Catalog of key pages from your site for internal linking.

**Must include**:
- Product pages and features
- Pillar content URLs
- Top performing blog articles
- Topic cluster mapping
- Recommended anchor text

**Purpose**: Enables strategic internal linking in every article

---

### `context/competitor-analysis.md`
Competitive intelligence and content gaps.

**Must include**:
- Primary competitors
- Their content strategies
- Keyword gaps
- Differentiation opportunities

**Purpose**: Informs content strategy and competitive positioning

## Content Quality Standards

Every article must meet these requirements:

### Content
- [ ] Minimum 2,000 words (2,500-3,000+ preferred)
- [ ] Provides unique value vs. competitors
- [ ] Factually accurate and current
- [ ] Actionable advice for your target audience
- [ ] Brand voice maintained

### SEO
- [ ] Primary keyword density 1-2%
- [ ] Keyword in H1, first 100 words, 2-3 H2s
- [ ] 3-5 internal links with descriptive anchor text
- [ ] 2-3 external authority links
- [ ] Meta title 50-60 characters
- [ ] Meta description 150-160 characters
- [ ] Proper H1>H2>H3 hierarchy

### Readability
- [ ] 8th-10th grade reading level
- [ ] Average sentence length 15-20 words
- [ ] Paragraphs 2-4 sentences
- [ ] Subheadings every 300-400 words
- [ ] Lists and formatting for scannability

### Structure
- [ ] Compelling introduction (hook, problem, promise)
- [ ] Logical section flow
- [ ] Clear conclusion with CTA
- [ ] Examples and data included

## Best Practices

### Before Writing
1. **Research first**: Always run `/research` before `/write`
2. **Review context**: Read `brand-voice.md` and relevant `writing-examples.md`
3. **Check keywords**: Verify target keyword in `target-keywords.md`
4. **Plan internal links**: Review `internal-links-map.md` for linking opportunities

### During Writing
1. **Follow the brief**: Use research brief as your outline
2. **Natural keywords**: Integrate keywords naturally, never force them
3. **Add value**: Every section should provide actionable insights
4. **Use examples**: Include real scenarios and use cases from your industry
5. **Cite sources**: Link to statistics and data sources

### After Writing
1. **Review agent output**: Read all agent recommendations carefully
2. **Make improvements**: Address high-priority issues before optimizing
3. **Run optimize**: Use `/optimize` for final polish
4. **Self-edit**: Read article as if you're the target reader
5. **Check quality**: Verify all checklist items met

### For Rewrites
1. **Analyze first**: Run `/analyze-existing` to understand scope
2. **Determine strategy**: Light update vs. major rewrite?
3. **Preserve what works**: Keep effective sections
4. **Focus on gaps**: Add what's missing from competitive content
5. **Update everything**: Stats, examples, screenshots, links

## Workflow Examples

### Example 1: Creating New Content from Scratch

```
# Step 1: Add topic idea
# Create file in topics/ directory with initial thoughts

# Step 2: Research the topic
/research content marketing strategies

# Step 3: Review research brief
# Read research/brief-content-marketing-strategies-[date].md

# Step 4: Write article
/write content marketing strategies

# Step 5: Review agent feedback
# Read all agent reports in drafts/

# Step 6: Make improvements
# Edit article based on agent recommendations

# Step 7: Final optimization
/optimize drafts/content-marketing-strategies-[date].md

# Step 8: Publish to WordPress (optional)
/publish-draft drafts/content-marketing-strategies-[date].md
```

### Example 2: Updating Existing Content

```
# Step 1: Analyze existing post
/analyze-existing https://yoursite.com/blog/product-comparison

# Step 2: Review analysis
# Read research/analysis-product-comparison-2025-10-29.md
# Check content health score and priority level

# Step 3: Rewrite content
/rewrite product comparison

# Step 4: Review changes
# Read rewrites/product-comparison-rewrite-2025-10-29.md
# Review change summary

# Step 5: Optimize
/optimize rewrites/product-comparison-rewrite-2025-10-29.md

# Step 6: Publish
# Move to published/ when ready
```

### Example 3: Quick Content Audit

```
# Analyze multiple existing posts to prioritize updates
/analyze-existing https://yoursite.com/blog/post-1
/analyze-existing https://yoursite.com/blog/post-2
/analyze-existing https://yoursite.com/blog/post-3

# Review content health scores
# Prioritize rewrites based on:
# - Lowest scores
# - Highest traffic potential
# - Strategic importance
```

## Tips & Tricks

### Maximizing Content Quality
- **Study examples**: Read your `writing-examples.md` before each writing session
- **Use data**: Always include current statistics and cite sources
- **Be specific**: "40% increase" beats "significant improvement"
- **Show, don't tell**: Use real examples and scenarios from your industry
- **Answer questions**: Address "People Also Ask" questions from research

### SEO Optimization
- **Keywords early**: Get primary keyword in first 100 words
- **Natural integration**: Read content aloud - if keywords sound forced, rewrite
- **Vary anchor text**: Don't use same anchor text for all internal links
- **Link strategically**: Link to pillar content and related cluster articles
- **Update regularly**: Refresh top-performing content every 6-12 months

### Workflow Efficiency
- **Batch research**: Research multiple topics in one session
- **Follow structure**: Use consistent article structure from `/write` command
- **Address high-priority first**: Fix critical issues before optimizing details
- **Use agents wisely**: Let agents handle analysis, you focus on writing
- **Build templates**: Save commonly used sections for reuse

### Avoiding Common Mistakes
- ❌ Skipping research phase
- ❌ Ignoring brand voice guidelines
- ❌ Forcing keywords unnaturally
- ❌ Forgetting internal links
- ❌ Not citing data sources
- ❌ Publishing without optimization
- ❌ Copying competitor content instead of differentiating

## Maintenance

### Weekly
- Add new topic ideas to `/topics/`
- Update `target-keywords.md` with new keyword opportunities
- Check for broken links in `internal-links-map.md`

### Monthly
- Review published content performance
- Update `writing-examples.md` if better examples emerge
- Add newly published content to `internal-links-map.md`
- Track competitor activity in `competitor-analysis.md`

### Quarterly
- Full audit of context files
- Update SEO guidelines based on algorithm changes
- Comprehensive competitor analysis refresh
- Review and update topic clusters in `target-keywords.md`

## Troubleshooting

### "Content doesn't sound like my brand"
- **Solution**: Update `context/brand-voice.md` with more specific guidance
- **Solution**: Add more diverse examples to `context/writing-examples.md`
- **Solution**: Reference specific examples when using `/write` command

### "Keyword density too high/low"
- **Solution**: Review `seo-guidelines.md` target density (1-2%)
- **Solution**: Use `/optimize` to get specific keyword placement suggestions
- **Solution**: Use Keyword Mapper agent for distribution analysis

### "Internal links aren't relevant"
- **Solution**: Update `context/internal-links-map.md` with current pages
- **Solution**: Organize by topic cluster for easier agent matching
- **Solution**: Provide more context about what each page covers

### "Articles too similar to competitors"
- **Solution**: Update `competitor-analysis.md` with differentiation opportunities
- **Solution**: Add your unique advantages to `brand-voice.md` and `features.md`
- **Solution**: Reference specific differentiation angles in `/research` command

## Support & Contributions

### Getting Help
- Review this README thoroughly
- Check context files are properly configured
- Consult [Claude Code documentation](https://docs.claude.com/claude-code)

### Contributing
- Report issues via GitHub Issues
- Suggest improvements to commands or agents
- Share successful workflows or tips

## License

[Add your license information]

## Credits

Built with [Claude Code](https://claude.com/claude-code) by Anthropic.

Originally developed for Castos, now available as an open-source tool for any business to streamline long-form SEO content creation.

## Examples & Community

**See It In Action**: Check out `examples/castos/` for a complete real-world example of how a podcast hosting SaaS company uses SEO Machine.

**Contributions Welcome**: Found a bug? Have a feature request? Want to share your own industry example? Contributions and PRs are welcome!

---

**Ready to start creating?**

1. Configure your context files (use the templates as your guide)
2. Run `/research [your topic]`
3. Review the brief
4. Run `/write [your topic]`
5. Publish amazing content!

Happy writing! 📝
