"""
Social Research Aggregator

Structures and aggregates insights from Reddit and YouTube research.
Used by the /article command during the social research phase.

This module provides data structures and formatting for the research
that is gathered via WebSearch and WebFetch during command execution.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class InsightType(Enum):
    """Types of insights found in social research."""
    PAIN_POINT = "pain_point"
    SUCCESS_STORY = "success_story"
    QUESTION = "question"
    TIP = "tip"
    COMPLAINT = "complaint"
    RECOMMENDATION = "recommendation"
    EXPERT_TAKE = "expert_take"
    DEBATE = "debate"


class EngagementLevel(Enum):
    """Engagement level based on upvotes/views."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class RedditInsight:
    """An insight extracted from a Reddit thread."""
    thread_title: str
    thread_url: str
    insight_type: InsightType
    content: str
    engagement: EngagementLevel
    quotable: Optional[str] = None  # Direct quote that could be used
    context: Optional[str] = None  # Additional context

    def to_dict(self) -> Dict[str, Any]:
        return {
            "thread_title": self.thread_title,
            "url": self.thread_url,
            "type": self.insight_type.value,
            "content": self.content,
            "engagement": self.engagement.value,
            "quotable": self.quotable,
            "context": self.context
        }


@dataclass
class YouTubeInsight:
    """An insight extracted from YouTube research."""
    video_title: str
    video_url: str
    channel: str
    view_count: Optional[int] = None
    insight_type: InsightType = InsightType.TIP
    content: str = ""
    topics_covered: List[str] = field(default_factory=list)
    gaps_identified: List[str] = field(default_factory=list)
    comment_themes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "video_title": self.video_title,
            "url": self.video_url,
            "channel": self.channel,
            "view_count": self.view_count,
            "type": self.insight_type.value,
            "content": self.content,
            "topics_covered": self.topics_covered,
            "gaps_identified": self.gaps_identified,
            "comment_themes": self.comment_themes
        }


@dataclass
class RedditResearch:
    """Aggregated research from Reddit threads."""
    threads_analyzed: int
    insights: List[RedditInsight]
    pain_points: List[str]
    success_stories: List[str]
    questions: List[str]
    recommendations: List[str]
    real_language: List[str]  # Phrases actual users use

    def to_dict(self) -> Dict[str, Any]:
        return {
            "threads_analyzed": self.threads_analyzed,
            "insights": [i.to_dict() for i in self.insights],
            "pain_points": self.pain_points,
            "success_stories": self.success_stories,
            "questions": self.questions,
            "recommendations": self.recommendations,
            "real_language": self.real_language
        }


@dataclass
class YouTubeResearch:
    """Aggregated research from YouTube videos."""
    videos_analyzed: int
    insights: List[YouTubeInsight]
    topics_well_covered: List[str]
    content_gaps: List[str]
    expert_opinions: List[str]
    comment_questions: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "videos_analyzed": self.videos_analyzed,
            "insights": [i.to_dict() for i in self.insights],
            "topics_well_covered": self.topics_well_covered,
            "content_gaps": self.content_gaps,
            "expert_opinions": self.expert_opinions,
            "comment_questions": self.comment_questions
        }


@dataclass
class SocialResearchSynthesis:
    """Synthesized insights ready for article planning."""
    unique_insights: List[str]  # Insights not in SEO content
    real_user_language: List[str]  # Terminology to use
    questions_to_answer: List[str]  # Content opportunities
    story_seeds: List[str]  # Mini-story opportunities
    contrarian_views: List[str]  # Different perspectives
    expert_quotes: List[str]  # Notable quotes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "unique_insights": self.unique_insights,
            "real_user_language": self.real_user_language,
            "questions_to_answer": self.questions_to_answer,
            "story_seeds": self.story_seeds,
            "contrarian_views": self.contrarian_views,
            "expert_quotes": self.expert_quotes
        }


class SocialResearchAggregator:
    """
    Aggregates and synthesizes social research from Reddit and YouTube.

    This class provides structure for the /article command to use
    when organizing social research findings. The actual research
    is gathered via WebSearch/WebFetch during command execution.
    """

    # Relevant subreddits for industry topics
    # Override with industry-specific subreddits for your niche
    INDUSTRY_SUBREDDITS = [
        'r/SaaS',
        'r/startups',
        'r/Entrepreneur',
        'r/smallbusiness',
        'r/marketing',
    ]

    # Pain point indicators in text
    PAIN_INDICATORS = [
        'frustrated', 'annoying', 'hate', 'struggle', 'difficult',
        'hard', 'impossible', 'confused', 'stuck', 'help',
        "can't figure out", "doesn't work", 'issue', 'problem'
    ]

    # Success indicators in text
    SUCCESS_INDICATORS = [
        'finally', 'worked', 'success', 'grew', 'increased',
        'reached', 'hit', 'achieved', 'solved', 'fixed'
    ]

    def build_search_queries(self, topic: str) -> Dict[str, List[str]]:
        """
        Generate search queries for Reddit and YouTube research.

        Args:
            topic: The article topic

        Returns:
            Dict with 'reddit' and 'youtube' query lists
        """
        return {
            "reddit": [
                f'site:reddit.com {topic}',
                f'site:reddit.com {topic} help OR advice',
                f'site:reddit.com {topic} success OR grew',
                f'site:reddit.com {topic} struggle OR frustrated',
                f'site:reddit.com {topic} recommendation OR review',
            ],
            "youtube": [
                f'site:youtube.com {topic} tutorial',
                f'site:youtube.com {topic} review 2025',
                f'site:youtube.com {topic} tips',
                f'site:youtube.com how to {topic}',
                f'site:youtube.com {topic} guide',
            ]
        }

    def categorize_insight(self, text: str) -> InsightType:
        """
        Categorize text into an insight type based on content.

        Args:
            text: The insight text to categorize

        Returns:
            InsightType enum value
        """
        text_lower = text.lower()

        # Check for questions
        if '?' in text:
            return InsightType.QUESTION

        # Check for pain points
        if any(word in text_lower for word in self.PAIN_INDICATORS):
            return InsightType.PAIN_POINT

        # Check for success stories
        if any(word in text_lower for word in self.SUCCESS_INDICATORS):
            return InsightType.SUCCESS_STORY

        # Check for recommendations
        if any(phrase in text_lower for phrase in ['recommend', 'suggest', 'try', 'use']):
            return InsightType.RECOMMENDATION

        # Check for complaints
        if any(word in text_lower for word in ['hate', 'worst', 'terrible', 'awful']):
            return InsightType.COMPLAINT

        return InsightType.TIP

    def synthesize_research(
        self,
        reddit_research: RedditResearch,
        youtube_research: YouTubeResearch
    ) -> SocialResearchSynthesis:
        """
        Combine Reddit and YouTube research into actionable synthesis.

        Args:
            reddit_research: Aggregated Reddit findings
            youtube_research: Aggregated YouTube findings

        Returns:
            SocialResearchSynthesis with actionable insights
        """
        # Combine unique insights
        unique_insights = []
        unique_insights.extend(reddit_research.pain_points[:3])
        unique_insights.extend(youtube_research.content_gaps[:3])

        # Combine questions from both sources
        questions = []
        questions.extend(reddit_research.questions[:5])
        questions.extend(youtube_research.comment_questions[:3])

        # Extract story seeds from success stories
        story_seeds = reddit_research.success_stories[:3]

        return SocialResearchSynthesis(
            unique_insights=unique_insights[:10],
            real_user_language=reddit_research.real_language[:10],
            questions_to_answer=questions[:8],
            story_seeds=story_seeds,
            contrarian_views=[],  # Filled during research
            expert_quotes=youtube_research.expert_opinions[:5]
        )


def format_social_research_report(
    topic: str,
    reddit_research: RedditResearch,
    youtube_research: YouTubeResearch,
    synthesis: SocialResearchSynthesis
) -> str:
    """
    Format social research as a markdown report.

    This generates the social-research-[topic]-[date].md file.
    """
    date = datetime.now().strftime("%Y-%m-%d")

    report = f"""# Social Research: {topic}

**Date**: {date}
**Reddit Threads Analyzed**: {reddit_research.threads_analyzed}
**YouTube Videos Analyzed**: {youtube_research.videos_analyzed}

---

## Reddit Insights

"""

    # Add Reddit thread details
    for i, insight in enumerate(reddit_research.insights[:5], 1):
        report += f"""### Thread {i}: {insight.thread_title}
- **URL**: {insight.thread_url}
- **Type**: {insight.insight_type.value}
- **Key Insight**: {insight.content}
"""
        if insight.quotable:
            report += f'- **Quotable**: "{insight.quotable}"\n'
        report += "\n"

    # Add pain points
    report += "### Pain Points Identified\n"
    for point in reddit_research.pain_points[:5]:
        report += f"- {point}\n"

    # Add questions
    report += "\n### Questions from Real Users\n"
    for question in reddit_research.questions[:5]:
        report += f"- {question}\n"

    # Add success stories
    report += "\n### Success Stories Found\n"
    for story in reddit_research.success_stories[:3]:
        report += f"- {story}\n"

    # Add real language
    report += "\n### Real User Language\n"
    for phrase in reddit_research.real_language[:5]:
        report += f'- Users say: "{phrase}"\n'

    report += """
---

## YouTube Insights

"""

    # Add YouTube video details
    for i, insight in enumerate(youtube_research.insights[:5], 1):
        view_str = f"{insight.view_count:,}" if insight.view_count else "N/A"
        report += f"""### Video {i}: {insight.video_title}
- **Channel**: {insight.channel}
- **URL**: {insight.video_url}
- **Views**: {view_str}
- **Topics Covered**: {', '.join(insight.topics_covered[:5])}
- **Gaps**: {', '.join(insight.gaps_identified[:3]) if insight.gaps_identified else 'None identified'}

"""

    # Add content gaps
    report += "### Content Gaps in Video Tutorials\n"
    for gap in youtube_research.content_gaps[:5]:
        report += f"- {gap}\n"

    # Add expert opinions
    report += "\n### Expert Takes\n"
    for opinion in youtube_research.expert_opinions[:5]:
        report += f"- {opinion}\n"

    # Synthesis section
    report += """
---

## Synthesis: Unique Insights for Article

### Insights NOT Available in SEO Content
"""
    for insight in synthesis.unique_insights[:7]:
        report += f"1. {insight}\n"

    report += "\n### Questions to Answer (from real users)\n"
    for question in synthesis.questions_to_answer[:6]:
        report += f"- {question}\n"

    report += "\n### Story Seeds (for mini-stories)\n"
    for seed in synthesis.story_seeds[:3]:
        report += f"- {seed}\n"

    report += "\n### Language to Use\n"
    for phrase in synthesis.real_user_language[:5]:
        report += f'- Use "{phrase}"\n'

    return report


# Template for empty research (when starting fresh)
def create_empty_reddit_research() -> RedditResearch:
    """Create an empty RedditResearch structure for initialization."""
    return RedditResearch(
        threads_analyzed=0,
        insights=[],
        pain_points=[],
        success_stories=[],
        questions=[],
        recommendations=[],
        real_language=[]
    )


def create_empty_youtube_research() -> YouTubeResearch:
    """Create an empty YouTubeResearch structure for initialization."""
    return YouTubeResearch(
        videos_analyzed=0,
        insights=[],
        topics_well_covered=[],
        content_gaps=[],
        expert_opinions=[],
        comment_questions=[]
    )


if __name__ == "__main__":
    print("Social Research Aggregator")
    print("=" * 50)
    print("This module is used by the /article command")
    print("to structure social research from Reddit and YouTube.")
    print()
    print("Insight Types:")
    for insight_type in InsightType:
        print(f"  - {insight_type.value}")
    print()

    # Example search queries
    aggregator = SocialResearchAggregator()
    queries = aggregator.build_search_queries("content marketing automation")
    print("Example Search Queries:")
    print("\nReddit:")
    for q in queries["reddit"]:
        print(f"  - {q}")
    print("\nYouTube:")
    for q in queries["youtube"]:
        print(f"  - {q}")
