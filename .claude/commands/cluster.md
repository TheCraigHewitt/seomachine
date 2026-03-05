# Cluster Command

Build a complete topic cluster strategy with pillar page definition, 8-12 supporting articles, internal linking map, and creation sequence.

## Usage
`/cluster [topic]`

**Examples:**
- `/cluster "content marketing"`
- `/cluster "podcast monetization"`
- `/cluster "remote team management"`

## Process

### Step 1: Gather Existing Data

Check for existing research that informs this cluster:

1. Search `research/` for any existing `/research-topics` output:
   ```
   Glob: research/topic-clusters-*.md
   ```
2. Search for any existing research on this topic:
   ```
   Glob: research/*[topic-slug]*.md
   ```
3. If found, extract:
   - Authority score for this topic area
   - Keywords already ranking
   - Coverage gaps identified
   - Any SERP analysis already done

Document what exists vs. what needs fresh research.

### Step 2: Keyword Research

Build the complete keyword landscape for this topic.

1. **DataForSEO Keyword Ideas**
   ```bash
   python3 -c "
   import sys; sys.path.insert(0, 'data_sources/modules')
   from dataforseo import DataForSEOClient
   client = DataForSEOClient()
   results = client.get_keyword_ideas('$ARGUMENTS')
   for kw in sorted(results, key=lambda x: x.get('search_volume', 0), reverse=True)[:30]:
       print(f\"{kw.get('keyword', 'N/A')} | Vol: {kw.get('search_volume', 'N/A')} | Diff: {kw.get('keyword_difficulty', 'N/A')} | CPC: {kw.get('cpc', 'N/A')}\")
   "
   ```

2. **DataForSEO Questions**
   ```bash
   python3 -c "
   import sys; sys.path.insert(0, 'data_sources/modules')
   from dataforseo import DataForSEOClient
   client = DataForSEOClient()
   results = client.get_questions('$ARGUMENTS')
   for q in results[:15]:
       print(f\"{q.get('keyword', 'N/A')} | Vol: {q.get('search_volume', 'N/A')}\")
   "
   ```

3. **WebSearch for Additional Keywords**
   ```
   WebSearch: "[topic] guide" site:ahrefs.com OR site:semrush.com OR site:moz.com
   WebSearch: "[topic] related keywords" OR "[topic] subtopics"
   ```

4. **Group Keywords into Tiers**
   - **Pillar-level**: Broad, high-volume (1000+ searches/mo), competitive
   - **Supporting-level**: Specific subtopics, medium volume (100-1000/mo)
   - **Long-tail**: Very specific queries, low volume (<100/mo), low competition

### Step 3: SERP Analysis

Analyze what's winning for the pillar keyword.

1. **Get SERP Data**
   ```bash
   python3 -c "
   import sys; sys.path.insert(0, 'data_sources/modules')
   from dataforseo import DataForSEOClient
   client = DataForSEOClient()
   results = client.get_serp_data('$ARGUMENTS')
   for r in results[:10]:
       print(f\"Position {r.get('position', 'N/A')}: {r.get('title', 'N/A')}\")
       print(f\"  URL: {r.get('url', 'N/A')}\")
       print(f\"  Description: {r.get('description', 'N/A')[:100]}\")
       print()
   "
   ```

2. **Fetch Top 3 Pillar/Guide Pages**
   Use WebFetch on the top 3 ranking comprehensive guides. For each, document:
   - H2/H3 structure
   - Word count estimate
   - Topics covered
   - Gaps and thin sections
   - Unique angles or data

3. **Identify Differentiation Opportunities**
   - What do all top results miss?
   - Where are they thin or generic?
   - What unique angle can we bring?
   - What data or examples are outdated?

### Step 4: Define Pillar Page

Adopt the **cluster-strategist** agent role (@agents/cluster-strategist.md).

Define the pillar page:

| Element | Details |
|---------|---------|
| **Title** | [Compelling H1 targeting pillar keyword] |
| **Primary Keyword** | [Highest-volume broad term] |
| **Secondary Keywords** | [3-5 related terms] |
| **Search Intent** | [Informational / Commercial Investigation] |
| **Target Word Count** | 3,000-5,000 words |
| **Differentiation Angle** | [What makes ours uniquely valuable] |

**Pillar Page Outline:**
- Create full H2/H3 outline
- Each H2 should map to a supporting article topic
- Include sections that competitors cover (Google-validated structure)
- Add sections that fill identified gaps
- Note where each supporting article will be linked from

### Step 5: Define Supporting Articles (8-12)

For each supporting article, specify:

| Field | Value |
|-------|-------|
| **#** | [Sequential number] |
| **Title** | [Working title] |
| **Primary Keyword** | [MUST be distinct from all other articles] |
| **Search Volume** | [Monthly volume] |
| **Keyword Difficulty** | [0-100 score] |
| **Search Intent** | [Informational / How-to / Commercial / Comparison] |
| **Content Angle** | [Specific perspective or approach] |
| **Pillar Relationship** | [Which pillar H2 section this expands on] |
| **Word Count Target** | [1,500-3,000] |
| **Priority Score** | [0-100 using prioritization framework] |

**Prioritization Framework:**
- Volume (30%): Higher search volume = higher score
- Difficulty Inverse (20%): Lower difficulty = higher score
- Commercial Intent (20%): Closer to conversion = higher score
- Pillar Dependency (15%): More essential to pillar completeness = higher score
- Cross-link Value (15%): More connections to other cluster pieces = higher score

### Step 6: Build Internal Linking Map

1. **Pillar-to-Supporting Links**
   - Map each supporting article to specific pillar page sections
   - Every supporting article MUST link back to pillar
   - Pillar MUST link to every supporting article

2. **Cross-Links Between Supporting Articles**
   - Identify related supporting articles that should link to each other
   - Aim for 2-3 cross-links per supporting article
   - Ensure no orphaned pieces

3. **Integration with Existing Content**
   - Review @context/internal-links-map.md
   - Identify existing site pages that should link to/from cluster pieces
   - Note specific anchor text recommendations

4. **Visual Linking Map**

   Create an ASCII diagram showing all connections:
   ```
                    [Pillar Page Title]
                   /    |    |    |    \
                  /     |    |    |     \
   [Article 1] [Art 2] [Art 3] [Art 4] [Art 5]
        \___________/      |      \_________/
              cross-link   |        cross-link
   ```

5. **Link Matrix Table**

   | From \ To | Pillar | Art 1 | Art 2 | Art 3 | ... |
   |-----------|--------|-------|-------|-------|-----|
   | Pillar    | -      | ->    | ->    | ->    | ... |
   | Art 1     | ->     | -     | ->    |       | ... |
   | Art 2     | ->     |       | -     | ->    | ... |

### Step 7: Create Execution Roadmap

**Phase 1: Foundation (Pillar + High-Priority)**
List the pillar page and top 3-4 highest-priority supporting articles.

**Phase 2: Build Authority (Medium-Priority)**
Next 3-4 supporting articles.

**Phase 3: Complete Coverage (Remaining)**
Final 2-4 supporting articles to fill all gaps.

**Copy-Pastable Commands:**
For each piece, provide the exact command:
```
/research "[primary keyword]"
/article "[article title]"
```

## Output

Save to: `research/cluster-strategy-[topic-slug]-[YYYY-MM-DD].md`

### Output Template

```markdown
# Topic Cluster Strategy: [Topic]

**Date**: [YYYY-MM-DD]
**Pillar Keyword**: [keyword]
**Cluster Size**: [X] articles (1 pillar + [X-1] supporting)

---

## Executive Summary

[2-3 sentences: What this cluster covers, the opportunity size, and the strategic approach.]

---

## Keyword Landscape

### Pillar-Level Keywords
| Keyword | Volume | Difficulty | CPC | Intent |
|---------|--------|------------|-----|--------|
| [keyword] | [vol] | [diff] | [cpc] | [intent] |

### Supporting-Level Keywords
| Keyword | Volume | Difficulty | CPC | Intent | Assigned To |
|---------|--------|------------|-----|--------|-------------|
| [keyword] | [vol] | [diff] | [cpc] | [intent] | Article # |

### Long-Tail / Question Keywords
| Keyword | Volume | Assigned To |
|---------|--------|-------------|
| [keyword] | [vol] | Pillar FAQ / Article # |

---

## Pillar Page Strategy

### Overview
| Element | Details |
|---------|---------|
| Title | [title] |
| Primary Keyword | [keyword] |
| Secondary Keywords | [keywords] |
| Search Intent | [intent] |
| Word Count Target | [3,000-5,000] |
| Differentiation | [angle] |

### Competitive Analysis
- **Top Competitor**: [URL] - [Strengths] - [Gaps]
- **Top Competitor**: [URL] - [Strengths] - [Gaps]
- **Top Competitor**: [URL] - [Strengths] - [Gaps]

### Pillar Page Outline
1. **H2: [Section Title]** - [Brief description, links to Article #X]
2. **H2: [Section Title]** - [Brief description, links to Article #X]
[...]

---

## Supporting Articles

### Article 1: [Title]
| Field | Value |
|-------|-------|
| Primary Keyword | [keyword] |
| Search Volume | [vol] |
| Keyword Difficulty | [diff] |
| Search Intent | [intent] |
| Content Angle | [angle] |
| Pillar Relationship | Expands on H2: [section] |
| Word Count Target | [count] |
| Priority Score | [score]/100 |

### Article 2: [Title]
[Same format...]

[Continue for all 8-12 supporting articles...]

---

## Internal Linking Map

### Visual Cluster Map
```
[ASCII diagram showing all connections]
```

### Link Matrix
| From \ To | Pillar | Art 1 | Art 2 | Art 3 | ... |
|-----------|--------|-------|-------|-------|-----|
| Pillar    | -      | ->    | ->    | ->    | ... |
| Art 1     | ->     | -     | ->    |       | ... |

### Integration with Existing Content
- [Existing page] -> [Cluster piece]: [anchor text]
- [Cluster piece] -> [Existing page]: [anchor text]

---

## Content Creation Roadmap

### Phase 1: Foundation
| Order | Piece | Command |
|-------|-------|---------|
| 1 | [Pillar: Title] | `/research "[keyword]"` then `/article "[title]"` |
| 2 | [Article X: Title] | `/research "[keyword]"` then `/article "[title]"` |
| 3 | [Article Y: Title] | `/research "[keyword]"` then `/article "[title]"` |

### Phase 2: Build Authority
| Order | Piece | Command |
|-------|-------|---------|
| 4 | [Article X: Title] | `/research "[keyword]"` then `/article "[title]"` |
[...]

### Phase 3: Complete Coverage
| Order | Piece | Command |
|-------|-------|---------|
| 8 | [Article X: Title] | `/research "[keyword]"` then `/article "[title]"` |
[...]

---

## Cannibalization Check

| Article A | Article B | Potential Overlap | Resolution |
|-----------|-----------|-------------------|------------|
| [title] | [title] | [overlapping query] | [how differentiated] |

**Verdict**: [PASS - No cannibalization risks / WARN - Monitor these pairs]

---

## Success Metrics

| Metric | Target | Timeline |
|--------|--------|----------|
| Pillar page ranking | Top 10 for "[keyword]" | 3-6 months |
| Supporting articles indexed | All [X] indexed | 1-2 months |
| Internal link coverage | 100% bidirectional | At publication |
| Organic traffic (cluster) | [target] sessions/mo | 6-12 months |
| Featured snippets | 2-3 snippets captured | 3-6 months |
```

## Required Context Files

Before building the cluster strategy, review:
- @context/seo-guidelines.md - SEO requirements and keyword rules
- @context/internal-links-map.md - Existing internal linking targets
- @context/target-keywords.md - Current keyword targets (avoid overlap)
