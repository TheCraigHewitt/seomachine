"""
Article Planner

Creates strategic section-by-section article plans from research data.
Merges competitor analysis, social research, and brand context into
a comprehensive writing plan.

Used by the /article command during the planning phase.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class SectionType(Enum):
    """Types of article sections for specialized writing."""
    INTRO = "intro"
    BODY_HOW_TO = "body_how_to"
    BODY_COMPARISON = "body_comparison"
    BODY_EXPLANATION = "body_explanation"
    BODY_LIST = "body_list"
    FAQ = "faq"
    CONCLUSION = "conclusion"


class CTAType(Enum):
    """CTA intensity levels."""
    SOFT = "soft"  # Learn more, explore
    MEDIUM = "medium"  # Try it, start free
    STRONG = "strong"  # Convert, sign up now


@dataclass
class SectionPlan:
    """Detailed plan for a single article section."""
    section_number: int
    section_type: SectionType
    heading: str
    word_target: int
    strategic_angle: str
    engagement_hook: Optional[str] = None
    knowledge_gaps_addressed: List[str] = field(default_factory=list)
    unique_data_to_include: List[str] = field(default_factory=list)
    internal_links: List[str] = field(default_factory=list)
    cta_type: Optional[CTAType] = None
    mini_story_planned: bool = False
    featured_snippet_target: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "section_number": self.section_number,
            "type": self.section_type.value,
            "heading": self.heading,
            "word_target": self.word_target,
            "strategic_angle": self.strategic_angle,
            "engagement_hook": self.engagement_hook,
            "knowledge_gaps": self.knowledge_gaps_addressed,
            "unique_data": self.unique_data_to_include,
            "internal_links": self.internal_links,
            "cta": self.cta_type.value if self.cta_type else None,
            "mini_story": self.mini_story_planned,
            "featured_snippet": self.featured_snippet_target
        }


@dataclass
class MetaElements:
    """Meta elements for the article."""
    title_options: List[str]
    meta_title: str
    meta_description: str
    url_slug: str
    primary_keyword: str
    secondary_keywords: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title_options": self.title_options,
            "meta_title": self.meta_title,
            "meta_description": self.meta_description,
            "url_slug": self.url_slug,
            "primary_keyword": self.primary_keyword,
            "secondary_keywords": self.secondary_keywords
        }


@dataclass
class EngagementMap:
    """Maps engagement elements to sections."""
    mini_story_locations: List[int]  # Section numbers
    cta_locations: Dict[str, int]  # CTAType -> section number
    featured_snippet_sections: List[int]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mini_stories": self.mini_story_locations,
            "ctas": self.cta_locations,
            "featured_snippets": self.featured_snippet_sections
        }


@dataclass
class ArticlePlan:
    """Complete article plan ready for section-by-section writing."""
    topic: str
    date: str
    meta: MetaElements
    total_word_target: int
    sections: List[SectionPlan]
    engagement_map: EngagementMap
    gap_to_section_mapping: Dict[str, int]  # gap description -> section number
    insight_to_section_mapping: Dict[str, int]  # insight -> section number

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "date": self.date,
            "meta": self.meta.to_dict(),
            "total_word_target": self.total_word_target,
            "sections": [s.to_dict() for s in self.sections],
            "engagement_map": self.engagement_map.to_dict(),
            "gap_mapping": self.gap_to_section_mapping,
            "insight_mapping": self.insight_to_section_mapping
        }


class ArticlePlanner:
    """
    Creates strategic article plans from research.

    This class provides structure and logic for the /article command
    to use when creating section-by-section writing plans.
    """

    # Default word targets by section type
    DEFAULT_WORD_TARGETS = {
        SectionType.INTRO: 200,
        SectionType.BODY_HOW_TO: 350,
        SectionType.BODY_COMPARISON: 400,
        SectionType.BODY_EXPLANATION: 300,
        SectionType.BODY_LIST: 400,
        SectionType.FAQ: 250,
        SectionType.CONCLUSION: 200,
    }

    # Keywords that indicate section type
    SECTION_TYPE_KEYWORDS = {
        SectionType.BODY_HOW_TO: ['how to', 'steps', 'guide', 'tutorial', 'process'],
        SectionType.BODY_COMPARISON: ['vs', 'compare', 'versus', 'difference', 'best'],
        SectionType.BODY_EXPLANATION: ['what is', 'why', 'overview', 'understand'],
        SectionType.BODY_LIST: ['top', 'best', 'tips', 'ways', 'methods', 'strategies'],
        SectionType.FAQ: ['faq', 'questions', 'asked'],
        SectionType.CONCLUSION: ['conclusion', 'summary', 'final', 'next step', 'wrap'],
    }

    def classify_section_type(self, heading: str) -> SectionType:
        """
        Classify a section heading into a section type.

        Args:
            heading: The H2 heading text

        Returns:
            SectionType enum value
        """
        heading_lower = heading.lower()

        for section_type, keywords in self.SECTION_TYPE_KEYWORDS.items():
            if any(kw in heading_lower for kw in keywords):
                return section_type

        return SectionType.BODY_EXPLANATION  # Default

    def calculate_word_target(
        self,
        section_type: SectionType,
        competitor_avg: int = 0,
        has_gap: bool = False
    ) -> int:
        """
        Calculate word target for a section.

        Args:
            section_type: The type of section
            competitor_avg: Average words competitors use for similar section
            has_gap: Whether this section addresses a competitor gap

        Returns:
            Target word count
        """
        base = self.DEFAULT_WORD_TARGETS.get(section_type, 300)

        # If competitors are thin here and we have a gap to fill
        if has_gap:
            base = int(base * 1.3)  # 30% more than default

        # Match competitor depth if they're more comprehensive
        if competitor_avg > base:
            base = max(base, int(competitor_avg * 1.1))  # Beat by 10%

        return base

    def plan_engagement_distribution(
        self,
        num_sections: int
    ) -> EngagementMap:
        """
        Plan where engagement elements should go.

        Args:
            num_sections: Total number of sections

        Returns:
            EngagementMap with locations
        """
        # Mini-stories: intro, middle, near-end
        mini_story_locations = [1]  # Always in intro
        if num_sections >= 4:
            mini_story_locations.append(num_sections // 2)
        if num_sections >= 6:
            mini_story_locations.append(num_sections - 1)

        # CTAs: early (soft), middle (medium), end (strong)
        cta_locations = {
            "soft": min(2, num_sections),  # Section 2 or earlier
            "medium": num_sections // 2 + 1,  # Middle
            "strong": num_sections  # Conclusion
        }

        # Featured snippets: FAQ and definition sections
        featured_snippets = []  # Will be identified during planning

        return EngagementMap(
            mini_story_locations=mini_story_locations,
            cta_locations=cta_locations,
            featured_snippet_sections=featured_snippets
        )

    def create_section_plan(
        self,
        section_number: int,
        heading: str,
        gaps_to_address: List[str],
        insights_to_include: List[str],
        internal_links: List[str],
        engagement_map: EngagementMap
    ) -> SectionPlan:
        """
        Create a detailed plan for a single section.

        Args:
            section_number: Position in article (1-indexed)
            heading: H2 heading text
            gaps_to_address: Competitor gaps this section should fill
            insights_to_include: Social research insights to use
            internal_links: Your pages to link
            engagement_map: Overall engagement distribution plan

        Returns:
            SectionPlan with all details
        """
        section_type = self.classify_section_type(heading)

        # Special handling for intro
        if section_number == 1:
            section_type = SectionType.INTRO

        # Special handling for FAQ
        if 'faq' in heading.lower() or 'question' in heading.lower():
            section_type = SectionType.FAQ

        # Determine CTA type if applicable
        cta_type = None
        for cta, section_num in engagement_map.cta_locations.items():
            if section_num == section_number:
                cta_type = CTAType(cta)
                break

        # Check if mini-story planned here
        mini_story = section_number in engagement_map.mini_story_locations

        # Check for featured snippet opportunity
        featured_snippet = section_type in [SectionType.FAQ, SectionType.BODY_EXPLANATION]

        return SectionPlan(
            section_number=section_number,
            section_type=section_type,
            heading=heading,
            word_target=self.calculate_word_target(
                section_type,
                has_gap=len(gaps_to_address) > 0
            ),
            strategic_angle=self._generate_angle(heading, gaps_to_address),
            engagement_hook=self._generate_hook_idea(section_type, insights_to_include),
            knowledge_gaps_addressed=gaps_to_address,
            unique_data_to_include=insights_to_include,
            internal_links=internal_links,
            cta_type=cta_type,
            mini_story_planned=mini_story,
            featured_snippet_target=featured_snippet
        )

    def _generate_angle(
        self,
        heading: str,
        gaps: List[str]
    ) -> str:
        """Generate a strategic angle description."""
        if gaps:
            return f"Address competitor gaps: {', '.join(gaps[:2])}"
        return f"Comprehensive coverage of {heading}"

    def _generate_hook_idea(
        self,
        section_type: SectionType,
        insights: List[str]
    ) -> str:
        """Generate engagement hook suggestion."""
        if section_type == SectionType.INTRO:
            return "Open with scenario/question based on social research pain points"
        elif section_type == SectionType.BODY_HOW_TO:
            return "Lead with the outcome readers will achieve"
        elif section_type == SectionType.BODY_COMPARISON:
            return "Start with the key differentiator"
        elif section_type == SectionType.FAQ:
            return "Use real questions from Reddit/YouTube research"
        else:
            return "Connect to reader's situation immediately"


def format_article_plan(plan: ArticlePlan) -> str:
    """
    Format article plan as markdown.

    This generates the article-plan-[topic]-[date].md file.
    """
    report = f"""# Article Plan: {plan.topic}

**Date**: {plan.date}
**Total Word Target**: {plan.total_word_target} words
**Primary Keyword**: {plan.meta.primary_keyword}
**Secondary Keywords**: {', '.join(plan.meta.secondary_keywords)}

---

## Meta Elements

**Title Options:**
"""
    for i, title in enumerate(plan.meta.title_options, 1):
        report += f"{i}. {title}\n"

    report += f"""
**Meta Description**: {plan.meta.meta_description}
**URL Slug**: /blog/{plan.meta.url_slug}

---

## Section Plan

| # | Type | Heading | Words | CTA | Story |
|---|------|---------|-------|-----|-------|
"""

    for section in plan.sections:
        cta = section.cta_type.value if section.cta_type else "-"
        story = "Yes" if section.mini_story_planned else "-"
        report += f"| {section.section_number} | {section.section_type.value} | {section.heading} | {section.word_target} | {cta} | {story} |\n"

    report += "\n---\n\n## Section Details\n\n"

    for section in plan.sections:
        report += f"""### {section.section_number}. {section.heading}
- **Type**: {section.section_type.value}
- **Word Target**: {section.word_target}
- **Strategic Angle**: {section.strategic_angle}
"""
        if section.engagement_hook:
            report += f"- **Hook**: {section.engagement_hook}\n"
        if section.knowledge_gaps_addressed:
            report += f"- **Gaps Addressed**: {', '.join(section.knowledge_gaps_addressed)}\n"
        if section.unique_data_to_include:
            report += f"- **Unique Data**: {', '.join(section.unique_data_to_include[:3])}\n"
        if section.internal_links:
            report += f"- **Internal Links**: {', '.join(section.internal_links)}\n"
        if section.cta_type:
            report += f"- **CTA Type**: {section.cta_type.value}\n"
        if section.mini_story_planned:
            report += "- **Mini-Story**: Yes - include specific scenario\n"
        if section.featured_snippet_target:
            report += "- **Featured Snippet**: Target for snippet optimization\n"
        report += "\n"

    report += """---

## Engagement Map

| Element | Location |
|---------|----------|
"""
    for loc in plan.engagement_map.mini_story_locations:
        section = plan.sections[loc - 1] if loc <= len(plan.sections) else None
        heading = section.heading if section else f"Section {loc}"
        report += f"| Mini-Story | Section {loc}: {heading} |\n"

    for cta_type, loc in plan.engagement_map.cta_locations.items():
        section = plan.sections[loc - 1] if loc <= len(plan.sections) else None
        heading = section.heading if section else f"Section {loc}"
        report += f"| CTA ({cta_type}) | Section {loc}: {heading} |\n"

    report += """
---

## Gap-to-Section Mapping

"""
    if plan.gap_to_section_mapping:
        for gap, section_num in plan.gap_to_section_mapping.items():
            report += f"- **{gap}** → Section {section_num}\n"
    else:
        report += "- No specific gap mappings defined yet\n"

    report += """
## Insight-to-Section Mapping

"""
    if plan.insight_to_section_mapping:
        for insight, section_num in plan.insight_to_section_mapping.items():
            report += f"- **{insight[:50]}...** → Section {section_num}\n"
    else:
        report += "- No specific insight mappings defined yet\n"

    return report


def create_default_structure(topic: str) -> List[str]:
    """
    Create a default article structure for common topics.

    This provides a starting point that should be modified based
    on competitor research.
    """
    return [
        "Introduction",
        f"What is {topic}?",
        f"Why {topic} Matters",
        f"How to Get Started with {topic}",
        f"Best Practices for {topic}",
        f"Common Mistakes to Avoid",
        "Frequently Asked Questions",
        "Conclusion"
    ]


if __name__ == "__main__":
    print("Article Planner")
    print("=" * 50)
    print("This module is used by the /article command")
    print("to create section-by-section article plans.")
    print()
    print("Section Types:")
    for section_type in SectionType:
        print(f"  - {section_type.value}")
    print()
    print("CTA Types:")
    for cta_type in CTAType:
        print(f"  - {cta_type.value}")
