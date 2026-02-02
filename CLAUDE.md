# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SEO Machine is an open-source Claude Code workspace for creating SEO-optimized blog content. It combines custom commands, specialized agents, and Python-based analytics to research, write, optimize, and publish articles for any business.

## Setup

```bash
pip install -r data_sources/requirements.txt
```

API credentials are configured in `data_sources/config/.env` (GA4, GSC, DataForSEO, WordPress). GA4 service account credentials go in `credentials/ga4-credentials.json`.

## Commands

All commands are defined in `.claude/commands/` and invoked as slash commands:

- `/research [topic]` - Keyword/competitor research, generates brief in `research/`
- `/write [topic]` - Create full article in `drafts/`, auto-triggers optimization agents
- `/rewrite [topic]` - Update existing content, saves to `rewrites/`
- `/optimize [file]` - Final SEO polish pass
- `/analyze-existing [URL or file]` - Content health audit
- `/performance-review` - Analytics-driven content priorities
- `/publish-draft [file]` - Publish to WordPress via REST API
- `/article [topic]` - Simplified article creation
- `/priorities` - Content prioritization matrix
- `/research-serp`, `/research-gaps`, `/research-trending`, `/research-performance`, `/research-topics` - Specialized research commands
- `/landing-write`, `/landing-audit`, `/landing-research`, `/landing-publish`, `/landing-competitor` - Landing page commands

## Architecture

### Command-Agent Model

**Commands** (`.claude/commands/`) orchestrate workflows. **Agents** (`.claude/agents/`) are specialized roles invoked by commands. After `/write`, these agents auto-run: SEO Optimizer, Meta Creator, Internal Linker, Keyword Mapper.

Key agents: `content-analyzer.md`, `seo-optimizer.md`, `meta-creator.md`, `internal-linker.md`, `keyword-mapper.md`, `editor.md`, `headline-generator.md`, `cro-analyst.md`, `performance.md`.

### Python Analysis Pipeline

Located in `data_sources/modules/`. The Content Analyzer chains:
1. `search_intent_analyzer.py` - Query intent classification
2. `keyword_analyzer.py` - Density, distribution, stuffing detection
3. `content_length_comparator.py` - Benchmarks against top 10 SERP results
4. `readability_scorer.py` - Flesch Reading Ease, grade level
5. `seo_quality_rater.py` - Comprehensive 0-100 SEO score

### Data Integrations

- `google_analytics.py` - GA4 traffic/engagement data
- `google_search_console.py` - Rankings and impressions
- `dataforseo.py` - SERP positions, keyword metrics
- `data_aggregator.py` - Combines all sources into unified analytics
- `wordpress_publisher.py` - Publishes to WordPress with Yoast SEO metadata

### Opportunity Scoring

`opportunity_scorer.py` uses 8 weighted factors: Volume (25%), Position (20%), Intent (20%), Competition (15%), Cluster (10%), CTR (5%), Freshness (5%), Trend (5%).

## Running Python Scripts

```bash
# Research & analysis scripts (run from repo root)
python3 research_quick_wins.py
python3 research_competitor_gaps.py
python3 research_performance_matrix.py
python3 research_priorities_comprehensive.py
python3 research_serp_analysis.py
python3 research_topic_clusters.py
python3 research_trending.py
python3 seo_baseline_analysis.py
python3 seo_bofu_rankings.py
python3 seo_competitor_analysis.py

# Test API connectivity
python3 test_dataforseo.py
```

## Content Pipeline

`topics/` (ideas) → `research/` (briefs) → `drafts/` (articles) → `review-required/` (pending review) → `published/` (final)

Rewrites go to `rewrites/`. Landing pages go to `landing-pages/`. Audits go to `audits/`.

## Context Files

`context/` contains brand guidelines that inform all content generation:
- `brand-voice.md` - Tone, messaging pillars
- `style-guide.md` - Grammar, formatting standards
- `seo-guidelines.md` - Keyword and structure rules
- `internal-links-map.md` - Key pages for internal linking
- `features.md` - Product features
- `competitor-analysis.md` - Competitive intelligence
- `cro-best-practices.md` - Conversion optimization guidelines

## WordPress Integration

Publishing uses the WordPress REST API with a custom MU-plugin (`wordpress/seo-machine-yoast-rest.php`) that exposes Yoast SEO fields. Articles are published in WordPress block format (HTML comments in Markdown files).
