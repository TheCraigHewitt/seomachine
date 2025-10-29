"""
Readability Scorer

Calculates multiple readability metrics including Flesch Reading Ease,
Flesch-Kincaid Grade Level, and other readability indicators.
"""

import re
import textstat
from typing import Dict, List, Optional, Any


class ReadabilityScorer:
    """Analyzes content readability using multiple metrics"""

    def __init__(self):
        self.target_reading_level = (8, 10)  # 8th-10th grade
        self.target_flesch_ease = (60, 70)  # Fairly easy to read
        self.max_avg_sentence_length = 20
        self.max_paragraph_sentences = 4

    def analyze(self, content: str) -> Dict[str, Any]:
        """
        Comprehensive readability analysis

        Args:
            content: Article content to analyze

        Returns:
            Dict with readability scores, metrics, and recommendations
        """
        # Clean content for analysis
        clean_text = self._clean_content(content)

        if not clean_text:
            return {'error': 'No readable content provided'}

        # Calculate all metrics
        metrics = self._calculate_metrics(clean_text)

        # Analyze structure
        structure = self._analyze_structure(content, clean_text)

        # Analyze complexity
        complexity = self._analyze_complexity(clean_text)

        # Generate score and grade
        overall_score = self._calculate_overall_score(metrics, structure, complexity)
        grade = self._get_grade(overall_score)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            metrics,
            structure,
            complexity
        )

        return {
            'overall_score': overall_score,
            'grade': grade,
            'reading_level': metrics['flesch_kincaid_grade'],
            'readability_metrics': metrics,
            'structure_analysis': structure,
            'complexity_analysis': complexity,
            'recommendations': recommendations,
            'status': self._get_status(metrics, structure)
        }

    def _clean_content(self, content: str) -> str:
        """Clean content for readability analysis"""
        # Remove markdown headers
        text = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)

        # Remove links but keep text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

        # Remove code blocks
        text = re.sub(r'```[^`]*```', '', text)

        # Remove extra whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = text.strip()

        return text

    def _calculate_metrics(self, text: str) -> Dict[str, Any]:
        """Calculate readability metrics using textstat library"""
        try:
            return {
                # Primary metrics
                'flesch_reading_ease': round(textstat.flesch_reading_ease(text), 1),
                'flesch_kincaid_grade': round(textstat.flesch_kincaid_grade(text), 1),

                # Additional grade level metrics
                'gunning_fog': round(textstat.gunning_fog(text), 1),
                'smog_index': round(textstat.smog_index(text), 1),
                'coleman_liau_index': round(textstat.coleman_liau_index(text), 1),

                # Consensus
                'automated_readability_index': round(textstat.automated_readability_index(text), 1),
                'dale_chall_readability': round(textstat.dale_chall_readability_score(text), 1),

                # Text statistics
                'syllable_count': textstat.syllable_count(text),
                'lexicon_count': textstat.lexicon_count(text),
                'sentence_count': textstat.sentence_count(text),
                'char_count': len(text),
                'letter_count': textstat.letter_count(text),
                'polysyllable_count': textstat.polysyllabcount(text)
            }
        except Exception as e:
            return {
                'error': f'Could not calculate metrics: {str(e)}',
                'flesch_reading_ease': 0,
                'flesch_kincaid_grade': 0
            }

    def _analyze_structure(self, original: str, clean_text: str) -> Dict[str, Any]:
        """Analyze content structure"""
        # Sentence analysis
        sentences = re.split(r'[.!?]+', clean_text)
        sentences = [s.strip() for s in sentences if s.strip()]

        sentence_lengths = [len(s.split()) for s in sentences]
        avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0

        # Paragraph analysis
        paragraphs = [p for p in original.split('\n\n') if p.strip() and not p.strip().startswith('#')]
        paragraph_sentence_counts = []

        for para in paragraphs:
            para_sentences = re.split(r'[.!?]+', para)
            para_sentences = [s.strip() for s in para_sentences if s.strip()]
            if para_sentences:
                paragraph_sentence_counts.append(len(para_sentences))

        avg_sentences_per_paragraph = (
            sum(paragraph_sentence_counts) / len(paragraph_sentence_counts)
            if paragraph_sentence_counts else 0
        )

        # Word analysis
        words = clean_text.split()
        word_lengths = [len(word) for word in words]
        avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0

        return {
            'total_sentences': len(sentences),
            'avg_sentence_length': round(avg_sentence_length, 1),
            'shortest_sentence': min(sentence_lengths) if sentence_lengths else 0,
            'longest_sentence': max(sentence_lengths) if sentence_lengths else 0,
            'sentence_length_variance': round(self._variance(sentence_lengths), 1) if len(sentence_lengths) > 1 else 0,
            'total_paragraphs': len(paragraphs),
            'avg_sentences_per_paragraph': round(avg_sentences_per_paragraph, 1),
            'total_words': len(words),
            'avg_word_length': round(avg_word_length, 1),
            'long_sentences': len([s for s in sentence_lengths if s > 25]),
            'very_long_sentences': len([s for s in sentence_lengths if s > 35])
        }

    def _analyze_complexity(self, text: str) -> Dict[str, Any]:
        """Analyze text complexity indicators"""
        # Transition words
        transition_words = [
            'however', 'moreover', 'furthermore', 'therefore', 'consequently',
            'additionally', 'meanwhile', 'nevertheless', 'thus', 'hence',
            'accordingly', 'subsequently', 'for example', 'for instance',
            'in addition', 'on the other hand', 'as a result', 'in contrast'
        ]

        text_lower = text.lower()
        transition_count = sum(text_lower.count(word) for word in transition_words)

        # Active vs Passive voice (simplified detection)
        sentences = re.split(r'[.!?]+', text)
        passive_indicators = ['was', 'were', 'been', 'being', 'is', 'are', 'am', 'be']

        passive_count = 0
        for sentence in sentences:
            sentence_lower = sentence.lower()
            # Simple passive detection: "to be" verb + past participle
            if any(f' {word} ' in f' {sentence_lower} ' for word in passive_indicators):
                # Check for past participles (words ending in -ed, -en)
                if re.search(r'\b\w+(ed|en)\b', sentence_lower):
                    passive_count += 1

        total_sentences = len([s for s in sentences if s.strip()])
        passive_ratio = (passive_count / total_sentences) if total_sentences > 0 else 0

        # Complex words (3+ syllables)
        words = text.split()
        complex_word_count = 0
        for word in words:
            # Simple syllable count (vowel groups)
            clean_word = re.sub(r'[^a-zA-Z]', '', word.lower())
            syllables = len(re.findall(r'[aeiouy]+', clean_word))
            if syllables >= 3:
                complex_word_count += 1

        complex_word_ratio = (complex_word_count / len(words)) if words else 0

        return {
            'transition_word_count': transition_count,
            'transition_words_per_100': round((transition_count / len(words)) * 100, 1) if words else 0,
            'passive_sentence_count': passive_count,
            'passive_sentence_ratio': round(passive_ratio * 100, 1),
            'complex_word_count': complex_word_count,
            'complex_word_ratio': round(complex_word_ratio * 100, 1)
        }

    def _calculate_overall_score(
        self,
        metrics: Dict,
        structure: Dict,
        complexity: Dict
    ) -> float:
        """Calculate overall readability score (0-100)"""
        score = 100

        # Flesch Reading Ease scoring (30 points)
        flesch = metrics.get('flesch_reading_ease', 0)
        if flesch < 30:  # Very difficult
            score -= 30
        elif flesch < 50:  # Difficult
            score -= 20
        elif flesch < 60:  # Fairly difficult
            score -= 10
        elif flesch > 80:  # Easy
            score -= 5  # Too easy might not sound professional

        # Grade level scoring (25 points)
        grade = metrics.get('flesch_kincaid_grade', 0)
        target_min, target_max = self.target_reading_level
        if grade < target_min - 2:
            score -= 10  # Too simple
        elif grade > target_max + 4:  # Too complex
            score -= 25
        elif grade > target_max + 2:
            score -= 15
        elif grade > target_max:
            score -= 5

        # Sentence length scoring (20 points)
        avg_sentence = structure.get('avg_sentence_length', 0)
        if avg_sentence > 30:
            score -= 20
        elif avg_sentence > 25:
            score -= 10
        elif avg_sentence > 20:
            score -= 5

        # Very long sentences penalty
        very_long = structure.get('very_long_sentences', 0)
        if very_long > 0:
            score -= min(15, very_long * 3)

        # Paragraph structure (10 points)
        avg_para_sentences = structure.get('avg_sentences_per_paragraph', 0)
        if avg_para_sentences > 6:
            score -= 10
        elif avg_para_sentences > 4:
            score -= 5

        # Passive voice penalty (10 points)
        passive_ratio = complexity.get('passive_sentence_ratio', 0)
        if passive_ratio > 30:  # More than 30% passive
            score -= 10
        elif passive_ratio > 20:
            score -= 5

        # Transition words bonus (5 points)
        transition_per_100 = complexity.get('transition_words_per_100', 0)
        if transition_per_100 < 0.5:  # Very few transitions
            score -= 5
        elif transition_per_100 > 2:  # Good use of transitions
            score += 5

        return max(0, min(100, score))

    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return "A (Excellent)"
        elif score >= 80:
            return "B (Good)"
        elif score >= 70:
            return "C (Average)"
        elif score >= 60:
            return "D (Needs Work)"
        else:
            return "F (Poor)"

    def _get_status(self, metrics: Dict, structure: Dict) -> Dict[str, Any]:
        """Get quick status assessment"""
        grade_level = metrics.get('flesch_kincaid_grade', 0)
        flesch_ease = metrics.get('flesch_reading_ease', 0)
        avg_sentence = structure.get('avg_sentence_length', 0)

        target_min, target_max = self.target_reading_level
        grade_status = "optimal" if target_min <= grade_level <= target_max else (
            "too_simple" if grade_level < target_min else "too_complex"
        )

        ease_status = "good" if 60 <= flesch_ease <= 80 else (
            "difficult" if flesch_ease < 60 else "too_easy"
        )

        sentence_status = "good" if avg_sentence <= self.max_avg_sentence_length else "too_long"

        return {
            'grade_level_status': grade_status,
            'ease_status': ease_status,
            'sentence_length_status': sentence_status,
            'overall_assessment': self._get_overall_assessment(grade_status, ease_status, sentence_status)
        }

    def _get_overall_assessment(self, grade: str, ease: str, sentence: str) -> str:
        """Get overall assessment"""
        if all(s == "good" or s == "optimal" for s in [grade, ease, sentence]):
            return "excellent"
        elif any(s in ["too_complex", "difficult", "too_long"] for s in [grade, ease, sentence]):
            return "needs_improvement"
        else:
            return "acceptable"

    def _generate_recommendations(
        self,
        metrics: Dict,
        structure: Dict,
        complexity: Dict
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Reading level
        grade = metrics.get('flesch_kincaid_grade', 0)
        target_min, target_max = self.target_reading_level

        if grade > target_max + 2:
            recommendations.append(
                f"⚠️ Reading level is too high (Grade {grade}). Target is {target_min}-{target_max}. "
                "Simplify sentences and use more common words."
            )
        elif grade > target_max:
            recommendations.append(
                f"ℹ️ Reading level is slightly high (Grade {grade}). Target is {target_min}-{target_max}. "
                "Consider simplifying some complex sentences."
            )
        elif grade < target_min - 2:
            recommendations.append(
                f"ℹ️ Reading level is very simple (Grade {grade}). Consider adding more depth and variation."
            )

        # Flesch Reading Ease
        flesch = metrics.get('flesch_reading_ease', 0)
        if flesch < 50:
            recommendations.append(
                f"⚠️ Content is difficult to read (Flesch score: {flesch}). "
                "Break up complex sentences and use simpler words."
            )
        elif flesch < 60:
            recommendations.append(
                f"ℹ️ Content is fairly difficult (Flesch score: {flesch}). "
                "Aim for 60-70 for better readability."
            )

        # Sentence length
        avg_sentence = structure.get('avg_sentence_length', 0)
        long_sentences = structure.get('long_sentences', 0)
        very_long = structure.get('very_long_sentences', 0)

        if avg_sentence > 25:
            recommendations.append(
                f"⚠️ Average sentence length is too long ({avg_sentence:.1f} words). "
                f"Target is under {self.max_avg_sentence_length} words. Break up long sentences."
            )
        elif avg_sentence > 20:
            recommendations.append(
                f"ℹ️ Average sentence length is high ({avg_sentence:.1f} words). "
                "Consider shortening some sentences for better flow."
            )

        if very_long > 0:
            recommendations.append(
                f"⚠️ {very_long} sentences are very long (35+ words). "
                "These should be split into multiple sentences."
            )
        elif long_sentences > structure['total_sentences'] * 0.2:
            recommendations.append(
                f"ℹ️ {long_sentences} sentences are long (25+ words). "
                "Breaking these up would improve readability."
            )

        # Paragraph structure
        avg_para = structure.get('avg_sentences_per_paragraph', 0)
        if avg_para > 6:
            recommendations.append(
                f"⚠️ Paragraphs are too long (avg {avg_para:.1f} sentences). "
                f"Keep paragraphs to {self.max_paragraph_sentences} sentences or less."
            )
        elif avg_para > 4:
            recommendations.append(
                f"ℹ️ Paragraphs are fairly long (avg {avg_para:.1f} sentences). "
                "Consider breaking into smaller chunks."
            )

        # Passive voice
        passive_ratio = complexity.get('passive_sentence_ratio', 0)
        if passive_ratio > 30:
            recommendations.append(
                f"⚠️ Too much passive voice ({passive_ratio:.0f}% of sentences). "
                "Convert to active voice where possible (target: under 20%)."
            )
        elif passive_ratio > 20:
            recommendations.append(
                f"ℹ️ Passive voice is slightly high ({passive_ratio:.0f}%). "
                "Try to use more active voice for direct, engaging writing."
            )

        # Transition words
        transition_per_100 = complexity.get('transition_words_per_100', 0)
        if transition_per_100 < 0.5:
            recommendations.append(
                "ℹ️ Few transition words detected. Add words like 'however', 'therefore', "
                "'additionally' to improve flow between ideas."
            )

        # Complex words
        complex_ratio = complexity.get('complex_word_ratio', 0)
        if complex_ratio > 15:
            recommendations.append(
                f"ℹ️ High percentage of complex words ({complex_ratio:.1f}%). "
                "Consider simpler alternatives where appropriate."
            )

        if not recommendations:
            recommendations.append("✅ Readability is excellent! Content is clear and accessible.")

        return recommendations

    def _variance(self, values: List[float]) -> float:
        """Calculate variance"""
        if len(values) < 2:
            return 0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)


# Convenience function
def score_readability(content: str) -> Dict[str, Any]:
    """
    Score content readability

    Args:
        content: Article text to analyze

    Returns:
        Comprehensive readability analysis
    """
    scorer = ReadabilityScorer()
    return scorer.analyze(content)


# Example usage
if __name__ == "__main__":
    sample_content = """
# How to Start a Podcast

Starting a podcast is easier than you might think. This guide will walk you through everything you need to know.

## Choose Your Topic

The first step is choosing what you want to talk about. Pick something you're passionate about and that your audience will find valuable. This ensures you'll have plenty to say and stay motivated over time.

## Get Your Equipment

You don't need expensive equipment to start. A decent USB microphone, headphones, and free recording software like Audacity are enough for beginners. As you grow, you can upgrade your gear.

## Record Your First Episode

Don't worry about being perfect. Just hit record and start talking. Your first episode won't be your best, but it's an important step in your podcasting journey. Edit out major mistakes, but don't obsess over every detail.
    """

    result = score_readability(sample_content)

    print("=== Readability Analysis ===")
    print(f"\nOverall Score: {result['overall_score']:.1f}/100")
    print(f"Grade: {result['grade']}")
    print(f"Reading Level: Grade {result['reading_level']}")

    print(f"\nKey Metrics:")
    print(f"  Flesch Reading Ease: {result['readability_metrics']['flesch_reading_ease']}")
    print(f"  Flesch-Kincaid Grade: {result['readability_metrics']['flesch_kincaid_grade']}")

    print(f"\nStructure:")
    print(f"  Avg Sentence Length: {result['structure_analysis']['avg_sentence_length']} words")
    print(f"  Avg Sentences per Paragraph: {result['structure_analysis']['avg_sentences_per_paragraph']}")

    print(f"\nComplexity:")
    print(f"  Passive Voice: {result['complexity_analysis']['passive_sentence_ratio']}%")
    print(f"  Complex Words: {result['complexity_analysis']['complex_word_ratio']}%")

    print(f"\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  {rec}")
