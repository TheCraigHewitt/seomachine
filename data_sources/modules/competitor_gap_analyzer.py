"""
Competitor Gap Analyzer

Analyzes competitor content to identify knowledge gaps, thin sections,
unsupported claims, missing perspectives, and outdated information.
Builds a "beat them" blueprint for content creation.

Used by the /article command during SERP analysis phase.
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class GapType(Enum):
    """Types of content gaps found in competitor articles."""
    THIN_SECTION = "thin_section"
    UNSUPPORTED_CLAIM = "unsupported_claim"
    MISSING_PERSPECTIVE = "missing_perspective"
    OUTDATED_INFO = "outdated_info"
    STRUCTURAL_GAP = "structural_gap"


class GapPriority(Enum):
    """Priority levels for addressing gaps."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ContentGap:
    """Represents a single gap found in competitor content."""
    gap_type: GapType
    description: str
    location: str  # H2 heading or section name where gap was found
    competitor_url: str
    priority: GapPriority
    opportunity: str  # How your content can address this gap

    def to_dict(self) -> Dict[str, str]:
        return {
            "type": self.gap_type.value,
            "description": self.description,
            "location": self.location,
            "url": self.competitor_url,
            "priority": self.priority.value,
            "opportunity": self.opportunity
        }


@dataclass
class CompetitorAnalysis:
    """Analysis results for a single competitor article."""
    url: str
    title: str
    word_count: int
    structure: List[str]  # H2 headings
    strengths: List[str]
    gaps: List[ContentGap]
    outdated_items: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "title": self.title,
            "word_count": self.word_count,
            "structure": self.structure,
            "strengths": self.strengths,
            "gaps": [g.to_dict() for g in self.gaps],
            "outdated_items": self.outdated_items
        }


@dataclass
class GapBlueprint:
    """The 'beat them' blueprint for content creation."""
    must_fill_gaps: List[ContentGap]  # Gaps found in 3+ competitors
    differentiation_opportunities: List[str]  # Unique angles
    data_needed: List[str]  # Specific data to gather
    outdated_to_update: List[str]  # Old info to replace with 2025 data
    structure_to_match: List[str]  # Common H2s that Google expects

    def to_dict(self) -> Dict[str, Any]:
        return {
            "must_fill_gaps": [g.to_dict() for g in self.must_fill_gaps],
            "differentiation_opportunities": self.differentiation_opportunities,
            "data_needed": self.data_needed,
            "outdated_to_update": self.outdated_to_update,
            "structure_to_match": self.structure_to_match
        }


class CompetitorGapAnalyzer:
    """
    Analyzes competitor content to identify knowledge gaps.

    This class provides structure and patterns for the /article command
    to use when analyzing competitor content. The actual analysis is
    performed by the AI during command execution.
    """

    # Patterns indicating vague/unsupported claims
    UNSUPPORTED_PATTERNS = [
        r'\bmany\s+(?:podcasters?|people|users|creators?)\b',
        r'\bmost\s+(?:podcasters?|people|experts?|creators?)\b',
        r'\bstudies\s+show\b(?!\s*[\[\(])',  # No citation following
        r'\bresearch\s+(?:indicates?|shows?|suggests?)\b(?!\s*[\[\(])',
        r'\bsignificant(?:ly)?\s+(?:increase|improvement|growth|impact)\b',
        r'\bsubstantial\s+(?:results?|benefits?|returns?|improvement)\b',
        r'\bexperts?\s+(?:say|agree|recommend)\b(?!\s*[\[\(])',
        r'\baccording\s+to\s+(?:experts?|studies)\b(?!\s*[\[\(])',
    ]

    # Year patterns for detecting outdated info
    YEAR_PATTERN = r'\b(201[0-9]|202[0-3])\b'  # Pre-2024 years

    # Minimum words for a section to be considered "substantial"
    MIN_SECTION_WORDS = 150

    # Structural elements to check for
    EXPECTED_STRUCTURE = [
        'faq',
        'conclusion',
        'introduction',
        'comparison',
        'how to',
        'steps',
    ]

    def analyze_content(
        self,
        content: str,
        url: str,
        title: str = ""
    ) -> CompetitorAnalysis:
        """
        Analyze a single competitor's content for gaps.

        Args:
            content: The full text content of the competitor article
            url: URL of the competitor article
            title: Title of the article (optional)

        Returns:
            CompetitorAnalysis with identified gaps and structure
        """
        sections = self._extract_sections(content)
        gaps = []
        outdated = []

        # Analyze each section
        for section in sections:
            # Check for thin sections
            thin_gaps = self._find_thin_sections(section, url)
            gaps.extend(thin_gaps)

            # Check for unsupported claims
            claim_gaps = self._find_unsupported_claims(section, url)
            gaps.extend(claim_gaps)

            # Check for outdated info
            outdated_items = self._find_outdated_info(section['content'])
            outdated.extend(outdated_items)

        # Check structural gaps
        structural_gaps = self._find_structural_gaps(content, sections, url)
        gaps.extend(structural_gaps)

        return CompetitorAnalysis(
            url=url,
            title=title,
            word_count=len(content.split()),
            structure=[s['header'] for s in sections if s['level'] == 2],
            strengths=self._identify_strengths(sections),
            gaps=gaps,
            outdated_items=outdated
        )

    def create_blueprint(
        self,
        analyses: List[CompetitorAnalysis]
    ) -> GapBlueprint:
        """
        Create a 'beat them' blueprint from multiple competitor analyses.

        Args:
            analyses: List of CompetitorAnalysis from analyzing competitors

        Returns:
            GapBlueprint with prioritized opportunities
        """
        # Collect all gaps
        all_gaps = []
        for analysis in analyses:
            all_gaps.extend(analysis.gaps)

        # Find gaps that appear in multiple competitors
        gap_counts = {}
        for gap in all_gaps:
            key = f"{gap.gap_type.value}:{gap.description[:50]}"
            if key not in gap_counts:
                gap_counts[key] = {"gap": gap, "count": 0}
            gap_counts[key]["count"] += 1

        # Must-fill gaps appear in 3+ competitors
        must_fill = [
            g["gap"] for g in gap_counts.values()
            if g["count"] >= 3
        ]

        # Collect all outdated items
        all_outdated = []
        for analysis in analyses:
            all_outdated.extend(analysis.outdated_items)

        # Find common structure (appears in 3+ competitors)
        all_structures = []
        for analysis in analyses:
            all_structures.extend(analysis.structure)

        structure_counts = {}
        for heading in all_structures:
            normalized = heading.lower().strip()
            structure_counts[normalized] = structure_counts.get(normalized, 0) + 1

        common_structure = [
            h for h, count in structure_counts.items()
            if count >= 3
        ]

        return GapBlueprint(
            must_fill_gaps=must_fill,
            differentiation_opportunities=[],  # Filled during analysis
            data_needed=[],  # Filled during analysis
            outdated_to_update=list(set(all_outdated)),
            structure_to_match=common_structure
        )

    def _extract_sections(self, content: str) -> List[Dict]:
        """Extract H2/H3 sections with their content."""
        sections = []
        lines = content.split('\n')
        current_section = {'header': 'Introduction', 'content': '', 'level': 1}

        for line in lines:
            h2_match = re.match(r'^##\s+(.+)$', line)
            h3_match = re.match(r'^###\s+(.+)$', line)

            if h2_match or h3_match:
                # Save previous section
                if current_section['content'].strip():
                    sections.append(current_section.copy())

                header = h2_match.group(1) if h2_match else h3_match.group(1)
                level = 2 if h2_match else 3
                current_section = {'header': header, 'content': '', 'level': level}
            else:
                current_section['content'] += line + '\n'

        # Save final section
        if current_section['content'].strip():
            sections.append(current_section)

        return sections

    def _find_thin_sections(
        self,
        section: Dict,
        url: str
    ) -> List[ContentGap]:
        """Identify sections that lack depth."""
        gaps = []
        word_count = len(section['content'].split())

        # H2 sections should have substantial content
        if section['level'] == 2 and word_count < self.MIN_SECTION_WORDS:
            priority = GapPriority.HIGH if word_count < 75 else GapPriority.MEDIUM

            gaps.append(ContentGap(
                gap_type=GapType.THIN_SECTION,
                description=f"Section '{section['header']}' only has {word_count} words",
                location=section['header'],
                competitor_url=url,
                priority=priority,
                opportunity=f"Provide comprehensive coverage of '{section['header']}' "
                           f"with 250-400 words, specific examples, and actionable steps"
            ))

        return gaps

    def _find_unsupported_claims(
        self,
        section: Dict,
        url: str
    ) -> List[ContentGap]:
        """Find claims without data or citations."""
        gaps = []
        content = section['content']

        for pattern in self.UNSUPPORTED_PATTERNS:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                # Only add one gap per pattern per section
                gaps.append(ContentGap(
                    gap_type=GapType.UNSUPPORTED_CLAIM,
                    description=f"Vague claim without data in '{section['header']}'",
                    location=section['header'],
                    competitor_url=url,
                    priority=GapPriority.MEDIUM,
                    opportunity="Replace vague claims with specific data: percentages, "
                               "dollar amounts, cited statistics, or named examples"
                ))
                break  # One gap per section is enough

        return gaps

    def _find_outdated_info(self, content: str) -> List[str]:
        """Identify outdated statistics, years, or references."""
        outdated = []
        current_year = datetime.now().year

        # Find old years
        old_years = re.findall(self.YEAR_PATTERN, content)
        for year in set(old_years):
            if int(year) < current_year - 1:  # More than 1 year old
                outdated.append(f"Reference to {year} - likely outdated")

        return outdated

    def _find_structural_gaps(
        self,
        content: str,
        sections: List[Dict],
        url: str
    ) -> List[ContentGap]:
        """Find missing structural elements."""
        gaps = []
        content_lower = content.lower()
        section_headers_lower = [s['header'].lower() for s in sections]

        # Check for FAQ section
        has_faq = any(
            'faq' in h or 'frequently asked' in h or 'questions' in h
            for h in section_headers_lower
        )
        if not has_faq:
            gaps.append(ContentGap(
                gap_type=GapType.STRUCTURAL_GAP,
                description="No FAQ section for featured snippet opportunity",
                location="Article structure",
                competitor_url=url,
                priority=GapPriority.HIGH,
                opportunity="Add FAQ section with 4-6 real user questions "
                           "from Reddit/YouTube targeting featured snippets"
            ))

        # Check for weak/missing conclusion
        has_conclusion = any(
            'conclusion' in h or 'summary' in h or 'final' in h or 'next step' in h
            for h in section_headers_lower
        )
        if not has_conclusion:
            gaps.append(ContentGap(
                gap_type=GapType.STRUCTURAL_GAP,
                description="No clear conclusion section",
                location="Article structure",
                competitor_url=url,
                priority=GapPriority.MEDIUM,
                opportunity="Add conclusion with actionable takeaways, "
                           "specific next steps, and strong CTA"
            ))

        return gaps

    def _identify_strengths(self, sections: List[Dict]) -> List[str]:
        """Identify what the competitor does well."""
        strengths = []

        for section in sections:
            word_count = len(section['content'].split())

            # Deep sections are a strength
            if word_count > 400:
                strengths.append(f"Comprehensive coverage of '{section['header']}'")

            # Check for specific data patterns
            if re.search(r'\d+%|\$\d+|\d{4}', section['content']):
                strengths.append(f"Uses specific data in '{section['header']}'")

        return list(set(strengths))[:5]  # Limit to top 5


def format_gap_report(
    keyword: str,
    analyses: List[CompetitorAnalysis],
    blueprint: GapBlueprint
) -> str:
    """
    Format the analysis results as a markdown report.

    This is used to generate the serp-analysis-[topic]-[date].md file.
    """
    date = datetime.now().strftime("%Y-%m-%d")

    report = f"""# SERP Analysis: {keyword}

**Date**: {date}
**Keyword**: {keyword}
**Competitors Analyzed**: {len(analyses)}

---

## Top Ranking Articles

"""

    for i, analysis in enumerate(analyses, 1):
        report += f"""### {i}. {analysis.title}
- **URL**: {analysis.url}
- **Word Count**: ~{analysis.word_count}
- **Structure**: {', '.join(analysis.structure[:5])}
- **Strengths**: {', '.join(analysis.strengths[:3]) if analysis.strengths else 'None identified'}
- **Gaps Found**: {len(analysis.gaps)}
- **Outdated Items**: {len(analysis.outdated_items)}

"""

    report += """---

## Google-Validated Structure

Based on what's ranking, these sections appear essential:
"""
    for heading in blueprint.structure_to_match[:7]:
        report += f"- {heading.title()}\n"

    report += """
---

## Competitor Gap Blueprint

### MUST-FILL GAPS (found in 3+ competitors)
"""
    if blueprint.must_fill_gaps:
        for gap in blueprint.must_fill_gaps:
            report += f"- **{gap.description}**\n  - Opportunity: {gap.opportunity}\n"
    else:
        report += "- No universal gaps found across all competitors\n"

    report += """
### OUTDATED INFO TO UPDATE
"""
    if blueprint.outdated_to_update:
        for item in blueprint.outdated_to_update[:5]:
            report += f"- {item}\n"
    else:
        report += "- No outdated information identified\n"

    return report


if __name__ == "__main__":
    # Example usage
    print("Competitor Gap Analyzer")
    print("=" * 50)
    print("This module is used by the /article command")
    print("to analyze competitor content and identify gaps.")
    print()
    print("Gap Types:")
    for gap_type in GapType:
        print(f"  - {gap_type.value}")
