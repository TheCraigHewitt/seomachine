# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SEO Machine is an open-source Claude Code workspace for creating SEO-optimized blog content. It is configured here for **Freaking Nomads** (freakingnomads.com) — a digital nomad publication, community, and platform built by co-founders Irene Lidia Wang and Luca Mussari.

The workspace combines custom commands, specialized agents, and Python-based analytics to research, write, optimize, and publish articles about digital nomad lifestyle, destinations, visas, gear, remote work, and community.

## Setup

```bash
pip install -r data_sources/requirements.txt
```

API credentials are configured in `data_sources/config/.env` (GA4, GSC, DataForSEO). GA4 service account credentials go in `credentials/ga4-credentials.json`.

## Commands

All commands are defined in `.claude/commands/` and invoked as slash commands:

- `/research [topic]` - Keyword/competitor research, generates brief in `research/`
- `/write [topic]` - Create full article in `drafts/`, auto-triggers optimization agents
- `/rewrite [topic]` - Update existing content, saves to `rewrites/`
- `/optimize [file]` - Final SEO polish pass
- `/analyze-existing [URL or file]` - Content health audit
- `/performance-review` - Analytics-driven content priorities
- `/publish-draft [file]` - Publish to Payload CMS via REST API
- `/article [topic]` - Simplified article creation
- `/cluster [topic]` - Build complete topic cluster strategy with pillar + supporting articles + linking map
- `/priorities` - Content prioritization matrix
- `/research-serp`, `/research-gaps`, `/research-trending`, `/research-performance`, `/research-topics` - Specialized research commands
- `/landing-write`, `/landing-audit`, `/landing-research`, `/landing-publish`, `/landing-competitor` - Landing page commands

## Architecture

### Command-Agent Model

**Commands** (`.claude/commands/`) orchestrate workflows. **Agents** (`.claude/agents/`) are specialized roles invoked by commands. After `/write`, these agents auto-run: SEO Optimizer, Meta Creator, Internal Linker, Keyword Mapper.

Key agents: `content-analyzer.md`, `seo-optimizer.md`, `meta-creator.md`, `internal-linker.md`, `keyword-mapper.md`, `editor.md`, `headline-generator.md`, `cro-analyst.md`, `performance.md`, `cluster-strategist.md`.

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
- `dataforseo.py` - SERP positions, keyword metrics (also available as MCP server)
- `data_aggregator.py` - Combines all sources into unified analytics
- `payload_publisher.py` - Publishes to Payload CMS REST API (in `payload/` directory)

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
- `brand-voice.md` - FN voice, tone, banned words, author personas (Irene, Luca, contributors)
- `writing-examples.md` - Real verbatim excerpts from freakingnomads.com by content type
- `style-guide.md` - Grammar, formatting standards
- `seo-guidelines.md` - 2026 SEO rules: EEAT, AI search, keyword strategy, schema
- `internal-links-map.md` - All key FN pages organized by category with anchor text
- `features.md` - FN content offerings, community, Remote Nomad Jobs, newsletter
- `competitor-analysis.md` - Nomad List, The Remote Nomad, Goats on the Road, Worldpackers, Digital Nomad World
- `cro-best-practices.md` - Conversion optimization guidelines

## Payload CMS Integration

Publishing uses the Payload CMS REST API (part of the Freaking Nomads Next.js app). See `payload/payload_publisher.py` for the implementation. The `/publish-draft` command outputs content in Payload-compatible Lexical format.

**Required environment variables** (set before publishing):
```
PAYLOAD_API_URL=https://freakingnomads.com/api
PAYLOAD_API_TOKEN=your_api_token_here
PAYLOAD_COLLECTION=posts
```

**Note**: The `wordpress/` directory contains the legacy WordPress MU-plugin — see `wordpress/DEPRECATED.md`.

## Freaking Nomads Content Types

Primary content types for this workspace:

1. **Destination guides** — Remote-work-first assessment of nomad destinations (internet, cost, coworking, visa, safety)
2. **Digital nomad visa guides** — Country-by-country: eligibility, requirements, process, costs, tax implications
3. **Gear & tech reviews** — eSIMs, portable monitors, keyboards, travel mice, backpacks — tested by nomads
4. **Insurance & finance reviews** — Travel insurance, health insurance, banking/debit cards, financial services
5. **Remote work guides** — Job boards, home exchange, portable WiFi, time zone management, office setup
6. **Nomad lifestyle pieces** — Health, wellness, productivity, community, personal development
7. **Best-of listicles** — Curated lists with consistent per-item structure and honest assessments
8. **Trend & opinion pieces** — Luca's analytical takes on the nomad landscape
9. **Career guides** — How to become a nomad as a [profession]: software engineer, UX designer, etc.

## MANDATORY Content Requirements

Every article published under the Freaking Nomads brand MUST include:

- [ ] **Real author attribution** — Irene Wang, Luca Mussari, or a named contributor with first-person experience
- [ ] **Minimum 3 internal links** — using descriptive anchor text (check `context/internal-links-map.md`)
- [ ] **Minimum 2 external authoritative links** — official government pages, established publications, manufacturer sites
- [ ] **FAQ section** — at least 4 questions sourced from "People Also Ask" for the target keyword
- [ ] **Schema markup recommendations** — Article + FAQPage (minimum); additional schemas per content type
- [ ] **Meta title** — 50–60 characters, keyword included
- [ ] **Meta description** — ≤155 characters, keyword + value prop
- [ ] **Honest cons** — stated plainly, not buried or softened
- [ ] **Real data** — specific prices, speeds, costs, processing times — no vague descriptors

## MANDATORY Humanization Step

**Never skip this.** After drafting any article:

1. Run AI detection (GPTZero, Originality.ai, or similar)
2. If score is above 40% — rewrite until below 40%
3. Humanization checklist:
   - Remove all banned words (see `context/brand-voice.md`)
   - Add specific real-world details (prices, names, speeds)
   - Vary sentence length (add shorter punchy sentences)
   - Remove passive voice constructions
   - Replace "moreover/furthermore/in conclusion" with natural transitions
   - Add a rhetorical question where natural
   - Ensure first-person voice throughout

Content that sounds AI-generated will not be published. This is non-negotiable.

## DataForSEO

DataForSEO is available both as a Python module (`data_sources/modules/dataforseo.py`) and as an MCP server (pre-configured in this workspace). Use the MCP tools for interactive research and the Python module for batch processing in scripts.
