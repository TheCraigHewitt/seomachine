# Priorities Command

Generate a comprehensive, prioritized content roadmap using multiple SEO research angles.

## Usage
`/priorities` - Comprehensive research (all modules, ~10 minutes)
`/priorities quick` - Quick wins only (fast, ~2 minutes)

## What This Command Does

### Comprehensive Mode (Default)
Runs 5 research modules to provide complete content strategy:

1. **Quick Wins** - Keywords ranking 11-20 (page 2)
2. **Competitor Gaps** - What competitors rank for that you don't
3. **Performance Matrix** - Categorize all content by health
4. **Topic Clusters** - Identify topical authority gaps
5. **Trending Topics** - Rising search trends

Generates unified roadmap combining all insights.

### Quick Mode
Runs quick wins analysis only - fast turnaround for immediate opportunities.

## Process

### 1. Execute Quick Wins Research
Run the research_quick_wins.py script:
```bash
python research_quick_wins.py
```

This will:
- Pull 30 days of data from Google Search Console
- Find keywords ranking positions 11-20 (quick win opportunities)
- Cross-reference with DataForSEO for rankings and search volume
- Pull engagement metrics from Google Analytics 4
- Calculate opportunity scores based on impressions, position, commercial intent
- Generate detailed report in `research/quick-wins-YYYY-MM-DD.md`

### 2. Read and Parse Results
- Read the generated markdown report
- Extract the top opportunities with highest opportunity scores
- Identify which URLs are already ranking (existing content to update)
- Identify keywords without ranking URLs (new content needed)

### 3. Categorize Opportunities
For each of the top 10 opportunities, categorize as:

**EXISTING CONTENT UPDATE:**
- Has a ranking URL on your site
- Content exists but needs optimization to move from page 2 to page 1
- Provide current ranking URL
- Estimate: Moderate effort, high impact

**NEW CONTENT CREATION:**
- No ranking URL found OR ranking position too low
- Need to create comprehensive content targeting this keyword
- Opportunity to capture search volume
- Estimate: High effort, high impact

### 4. Calculate Priority Score
Each item should show:
- **Keyword**: The target search term
- **Current Position**: Where it ranks now (or "Not ranking")
- **Search Volume**: Monthly searches (if available from DataForSEO)
- **Impressions (30d)**: How many times it appeared in search
- **Current Clicks**: Current monthly clicks
- **Potential Clicks**: Estimated clicks if moved to positions 5-7
- **Commercial Intent**: Low/Medium/High
- **Opportunity Score**: 0-100 calculated score
- **Priority**: HIGH/MEDIUM/LOW

### 5. Action Items
For EXISTING CONTENT updates, provide:
- [ ] Current ranking URL
- [ ] Review top 5 competitor articles
- [ ] Identify content gaps to fill
- [ ] Update statistics and examples
- [ ] Improve keyword density and placement
- [ ] Add/improve internal links
- [ ] Refresh meta title and description
- [ ] Target position: 5-7 (page 1)

For NEW CONTENT creation, provide:
- [ ] Research top 10 ranking competitors
- [ ] Create comprehensive outline covering all angles
- [ ] Target word count based on competitor analysis
- [ ] Ensure proper keyword integration
- [ ] Build strong internal linking strategy
- [ ] Create compelling meta elements
- [ ] Target position: Top 10 (page 1)

## Output Format

Present results as:

```
# Content Priorities - Top 10 Opportunities
**Generated**: YYYY-MM-DD HH:MM
**Data Period**: Last 30 days
**Total Opportunities Found**: X

---

## 🏆 TOP 10 PRIORITIES

### 1. [Keyword] - EXISTING CONTENT UPDATE | Priority: HIGH
- **Current Position**: 13
- **Search Volume**: 2,400/month
- **Impressions**: 1,850 (30d)
- **Current Clicks**: 45
- **Potential Clicks**: ~102 (+57)
- **Commercial Intent**: High
- **Opportunity Score**: 87/100
- **Ranking URL**: https://yoursite.com/path/to/article

**Why it matters**: High search volume with strong commercial intent. Currently on page 2 but very close to page 1. Small improvements could drive significant traffic.

**Action**: Update existing article, refresh stats, improve keyword placement in H2s, add internal links

---

### 2. [Keyword] - NEW CONTENT CREATION | Priority: HIGH
- **Current Position**: Not ranking top 100
- **Search Volume**: 3,200/month
- **Impressions**: 890 (30d)
- **Current Clicks**: 8
- **Potential Clicks**: ~176 (if rank 5-7)
- **Commercial Intent**: Medium
- **Opportunity Score**: 82/100

**Why it matters**: High search volume, solid impressions despite no strong ranking. Gap in our content portfolio.

**Action**: Create comprehensive 2500+ word guide targeting this keyword

---

[Continue for all 10 opportunities...]
```

## Summary Statistics

At the end, provide:
```
## 📊 SUMMARY

**Content Type Breakdown:**
- Existing Content Updates: X items
- New Content Creation: X items

**Combined Potential:**
- Total Current Monthly Clicks: X
- Total Potential Monthly Clicks: X
- Additional Monthly Clicks: +X

**Recommended Workflow:**
1. Start with top 3 EXISTING CONTENT updates (faster wins)
2. Begin research for top 2 NEW CONTENT pieces
3. Monitor rankings weekly for updated content
4. Iterate through remaining 5 items based on results

**Next Steps:**
- Use `/analyze-existing [URL]` for detailed analysis of existing content
- Use `/write [keyword]` to create new content targeting identified keywords
- Use `/optimize [file]` before publishing any updates
```

## File Management
The command reads from:
- `research/quick-wins-YYYY-MM-DD.md` (auto-generated by script)

The command creates:
- `research/priorities-YYYY-MM-DD.md` (summarized top 10 list)

## Integration
After running `/priorities`, you can:
- Use `/analyze-existing [URL]` on any of the existing content items
- Use `/write [keyword]` to create new content for identified opportunities
- Use `/optimize [file]` to finalize any content before publishing

This command gives you a clear, actionable roadmap of exactly what to work on next, prioritized by potential impact.
