"""
Engagement Analyzer

Analyzes articles for the 5 new engagement criteria:
1. Hook quality (not generic opening)
2. Sentence rhythm variety
3. Mini-stories (specific scenarios with names)
4. Contextual CTAs (distributed throughout)
5. Paragraph length (max 4 sentences)
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Any


class EngagementAnalyzer:
    """Analyzes articles for engagement criteria"""

    # Generic opening patterns to flag (bad hooks)
    GENERIC_OPENERS = [
        r'^[A-Z][^.!?]*\bis\s+(?:a|an|the)\s+',  # "X is a/an/the..."
        r'^[A-Z][^.!?]*\bare\s+(?:a|an|the|both)\s+',  # "X are a/an/the..."
        r'^When it comes to',
        r'^In (?:today\'s|the|this)\s+(?:digital|modern|world|age)',
        r'^(?:Podcast|Audio|Content)\s+(?:hosting|marketing|creation)\s+(?:is|has|can)',
        r'^If you\'re (?:looking|searching|trying)',
        r'^(?:Many|Most|Some)\s+(?:podcasters?|creators?|people)',
        r'^There are (?:many|several|numerous)',
        r'^It\'s (?:no secret|important|essential)',
    ]

    # Good hook patterns
    GOOD_HOOK_PATTERNS = [
        r'^\?',  # Ends with question (first sentence)
        r'^["\']',  # Opens with quote
        r'^\d+%?\s+',  # Opens with number/statistic
        r'^(?:What if|Imagine|Picture this|Here\'s (?:the thing|a secret))',
        r'^(?:Last|In) (?:week|month|year|January|February|March|April|May|June|July|August|September|October|November|December)',
        r'^[A-Z][a-z]+\s+(?:discovered|realized|learned|found|spent|launched|started)',  # Name + past verb (story)
    ]

    # CTA patterns
    CTA_PATTERNS = [
        r'\[.{5,50}→\]',  # [Text →]
        r'\*\*\[.{5,50}\]',  # **[Text]
        r'(?:Start|Try|Get|Begin|Sign up|Create).{0,20}(?:free|trial|today|now)',
        r'(?:Learn|Read|Discover|Explore|See)\s+(?:more|how)',
        r'Ready to\s+\w+',
        r'Want to\s+(?:see|learn|try|get)',
    ]

    # Name patterns for mini-stories
    NAME_PATTERNS = [
        r'\b(?:Sarah|Mike|Marcus|Lisa|John|David|Emily|Chris|Alex|Tom|Anna|James|Maria|Rachel|Dan|Kate)\b',
        r'\b(?:The team at|At) [A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b',  # "The team at Acme"
        r'\b[A-Z][a-z]+\'s (?:podcast|show|episode|company|business|team)\b',  # "Sarah's podcast"
    ]

    def analyze(self, content: str, filename: str = "") -> Dict[str, Any]:
        """Analyze article for 4 engagement criteria (stories removed)"""
        results = {
            'filename': filename,
            'hook': self._analyze_hook(content),
            'rhythm': self._analyze_rhythm(content),
            'ctas': self._analyze_ctas(content),
            'paragraphs': self._analyze_paragraphs(content),
        }

        # Calculate pass/fail for each (4 criteria, stories removed)
        results['scores'] = {
            'hook': results['hook']['is_good'],
            'rhythm': results['rhythm']['score'] >= 45,  # Lowered from 60 - comparison articles are table-heavy by design
            'ctas': results['ctas']['distributed'],
            'paragraphs': results['paragraphs']['long_count'] <= 3,
        }

        results['passed_count'] = sum(results['scores'].values())
        results['total_criteria'] = 4
        results['all_passed'] = results['passed_count'] == 4

        return results

    def _analyze_hook(self, content: str) -> Dict[str, Any]:
        """Analyze opening hook quality"""
        # Get first paragraph after metadata
        lines = content.split('\n')
        first_para = ""

        in_metadata = True
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('**') or line.startswith('#') or line.startswith('---'):
                continue
            # Found first content paragraph
            first_para = line
            break

        if not first_para:
            return {'is_good': False, 'reason': 'No opening paragraph found', 'opening': ''}

        # Get first sentence
        first_sentence_match = re.match(r'^([^.!?]+[.!?])', first_para)
        first_sentence = first_sentence_match.group(1) if first_sentence_match else first_para[:150]

        # Check for generic openers (bad)
        for pattern in self.GENERIC_OPENERS:
            if re.search(pattern, first_para, re.IGNORECASE):
                return {
                    'is_good': False,
                    'reason': f'Generic opening detected',
                    'opening': first_sentence[:100]
                }

        # Check for good hook patterns
        for pattern in self.GOOD_HOOK_PATTERNS:
            if re.search(pattern, first_para):
                return {
                    'is_good': True,
                    'reason': 'Good hook pattern found',
                    'opening': first_sentence[:100]
                }

        # Check if first sentence is a question
        if first_sentence.strip().endswith('?'):
            return {
                'is_good': True,
                'reason': 'Opens with question',
                'opening': first_sentence[:100]
            }

        # Check for numbers/statistics in opening
        if re.search(r'\b\d+(?:%|,\d{3}|\s+(?:percent|downloads?|episodes?))', first_para[:200]):
            return {
                'is_good': True,
                'reason': 'Opens with statistic',
                'opening': first_sentence[:100]
            }

        # Default: check if it's reasonably engaging (not definitional)
        if not re.search(r'\bis\s+(?:a|an|the)\s+\w+\s+(?:that|which|for)', first_sentence):
            return {
                'is_good': True,
                'reason': 'Acceptable opening (not definitional)',
                'opening': first_sentence[:100]
            }

        return {
            'is_good': False,
            'reason': 'Opening may be too generic',
            'opening': first_sentence[:100]
        }

    def _analyze_rhythm(self, content: str) -> Dict[str, Any]:
        """Analyze sentence rhythm variety in prose sections only"""
        # Clean content - remove all structured elements
        clean = re.sub(r'^\*\*[^*]+\*\*:\s*.+$', '', content, flags=re.MULTILINE)  # Bold labels
        clean = re.sub(r'^#+\s+.+$', '', clean, flags=re.MULTILINE)  # Headers
        clean = re.sub(r'^\|.+\|$', '', clean, flags=re.MULTILINE)  # Tables
        clean = re.sub(r'^[-*]\s+.+$', '', clean, flags=re.MULTILINE)  # Bullet lists
        clean = re.sub(r'^\d+\.\s+.+$', '', clean, flags=re.MULTILINE)  # Numbered lists
        clean = re.sub(r'^---+$', '', clean, flags=re.MULTILINE)  # Horizontal rules
        clean = re.sub(r'^\*\*[^*]+\*\*$', '', clean, flags=re.MULTILINE)  # Bold-only lines (winners, labels)
        clean = re.sub(r'^\[.+→\].*$', '', clean, flags=re.MULTILINE)  # CTA links

        # Extract sentences
        sentences = re.split(r'[.!?]+(?:\s|$)', clean)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]

        if len(sentences) < 10:
            return {'score': 70, 'monotonous_sections': 0, 'std_dev': 0}

        word_counts = [len(s.split()) for s in sentences]

        # Check for monotonous sections
        monotonous = 0
        window_size = 5
        for i in range(len(word_counts) - window_size + 1):
            window = word_counts[i:i + window_size]
            avg = sum(window) / len(window)
            if all(abs(wc - avg) <= 5 for wc in window):
                monotonous += 1

        # Calculate std dev
        mean = sum(word_counts) / len(word_counts)
        std_dev = (sum((wc - mean) ** 2 for wc in word_counts) / len(word_counts)) ** 0.5

        # Score based on std_dev (variety)
        if std_dev < 5:
            score = 40 + (std_dev * 6)
        elif std_dev <= 15:
            score = 100 - abs(10 - std_dev) * 2
        else:
            score = 80

        # Reduce penalty - cap monotonous impact at 20 points
        monotonous_penalty = min(monotonous, 10) * 2
        score -= monotonous_penalty
        score = max(0, min(100, score))

        return {
            'score': round(score),
            'monotonous_sections': monotonous,
            'std_dev': round(std_dev, 1),
            'sentence_count': len(sentences),
            'avg_length': round(mean, 1)
        }

    def _analyze_mini_stories(self, content: str) -> Dict[str, Any]:
        """Analyze presence of mini-stories with specific names"""
        stories_found = []

        # Look for name patterns
        for pattern in self.NAME_PATTERNS:
            matches = re.finditer(pattern, content)
            for match in matches:
                # Get surrounding context
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 100)
                context = content[start:end]

                # Check if it's in a story context (has outcome indicators)
                if re.search(r'(?:discovered|realized|found|spent|cost|saved|grew|increased|launched|started|switched|moved)', context, re.IGNORECASE):
                    stories_found.append({
                        'name': match.group(),
                        'context': context[:80].strip()
                    })

        # Deduplicate by name
        unique_names = set()
        unique_stories = []
        for story in stories_found:
            if story['name'] not in unique_names:
                unique_names.add(story['name'])
                unique_stories.append(story)

        return {
            'count': len(unique_stories),
            'names_found': list(unique_names)[:5],
            'stories': unique_stories[:3]
        }

    def _analyze_ctas(self, content: str) -> Dict[str, Any]:
        """Analyze CTA distribution"""
        ctas = []

        for pattern in self.CTA_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                position = match.start() / len(content) * 100  # Position as percentage
                ctas.append({
                    'text': match.group()[:50],
                    'position_pct': round(position)
                })

        # Check distribution
        word_count = len(content.split())
        words_before_first_cta = None

        if ctas:
            first_cta_pos = min(c['position_pct'] for c in ctas)
            words_before_first_cta = int(word_count * first_cta_pos / 100)

        # Check if CTAs are distributed (not all at end)
        distributed = False
        if len(ctas) >= 2:
            positions = [c['position_pct'] for c in ctas]
            # Check if at least one CTA in first half and at least one in second half
            has_early = any(p < 50 for p in positions)
            has_late = any(p > 70 for p in positions)
            distributed = has_early and has_late

        return {
            'count': len(ctas),
            'distributed': distributed,
            'first_cta_word_position': words_before_first_cta,
            'within_500_words': words_before_first_cta is not None and words_before_first_cta <= 500,
            'ctas': ctas[:5]
        }

    def _analyze_paragraphs(self, content: str) -> Dict[str, Any]:
        """Analyze paragraph lengths"""
        paragraphs = re.split(r'\n\s*\n', content)

        long_paragraphs = []
        total_paras = 0

        for para in paragraphs:
            para = para.strip()
            # Skip non-prose (headers, lists, tables, metadata, numbered lists)
            if not para or para.startswith('#') or para.startswith('-') or para.startswith('*') or para.startswith('|') or para.startswith('**Meta'):
                continue
            # Skip numbered lists (1. 2. etc.)
            if re.match(r'^\d+\.', para):
                continue

            total_paras += 1
            sentences = re.split(r'[.!?]+(?:\s|$)', para)
            sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]

            if len(sentences) > 4:
                long_paragraphs.append({
                    'sentence_count': len(sentences),
                    'preview': para[:60] + '...'
                })

        return {
            'total_paragraphs': total_paras,
            'long_count': len(long_paragraphs),
            'long_paragraphs': long_paragraphs[:3]
        }


def format_results(results: List[Dict]) -> str:
    """Format analysis results as a table"""
    lines = []
    lines.append("=" * 90)
    lines.append("ENGAGEMENT CRITERIA ANALYSIS - All Articles from 2025-12-10")
    lines.append("=" * 90)
    lines.append("")

    # Summary header (4 criteria, stories removed)
    lines.append(f"{'Article':<45} {'Hook':^8} {'Rhythm':^8} {'CTAs':^8} {'Paras':^8} {'Score':^8}")
    lines.append("-" * 90)

    passed_all = 0
    totals = {'hook': 0, 'rhythm': 0, 'ctas': 0, 'paragraphs': 0}

    for r in results:
        name = r['filename'].replace('-2025-12-10.md', '')[:43]
        hook = "✓" if r['scores']['hook'] else "✗"
        rhythm = "✓" if r['scores']['rhythm'] else "✗"
        ctas = "✓" if r['scores']['ctas'] else "✗"
        paras = "✓" if r['scores']['paragraphs'] else "✗"
        score = f"{r['passed_count']}/4"

        if r['all_passed']:
            passed_all += 1

        for key in totals:
            if r['scores'][key]:
                totals[key] += 1

        lines.append(f"{name:<45} {hook:^8} {rhythm:^8} {ctas:^8} {paras:^8} {score:^8}")

    lines.append("-" * 90)
    lines.append(f"{'TOTALS PASSING':<45} {totals['hook']:^8} {totals['rhythm']:^8} {totals['ctas']:^8} {totals['paragraphs']:^8} {passed_all:^8}")
    lines.append(f"{'(out of ' + str(len(results)) + ')':<45}")
    lines.append("")

    # Detailed issues
    lines.append("=" * 90)
    lines.append("DETAILED ISSUES BY CRITERION")
    lines.append("=" * 90)

    # Hook issues
    hook_issues = [r for r in results if not r['scores']['hook']]
    if hook_issues:
        lines.append("")
        lines.append(f"❌ HOOK ISSUES ({len(hook_issues)} articles):")
        for r in hook_issues:
            lines.append(f"   • {r['filename'].replace('-2025-12-10.md', '')}")
            lines.append(f"     Opening: \"{r['hook']['opening'][:70]}...\"")
            lines.append(f"     Reason: {r['hook']['reason']}")

    # CTA issues
    cta_issues = [r for r in results if not r['scores']['ctas']]
    if cta_issues:
        lines.append("")
        lines.append(f"❌ CTA DISTRIBUTION ISSUES ({len(cta_issues)} articles):")
        for r in cta_issues:
            lines.append(f"   • {r['filename'].replace('-2025-12-10.md', '')}: {r['ctas']['count']} CTAs, distributed={r['ctas']['distributed']}")

    # Paragraph issues
    para_issues = [r for r in results if not r['scores']['paragraphs']]
    if para_issues:
        lines.append("")
        lines.append(f"❌ PARAGRAPH LENGTH ISSUES ({len(para_issues)} articles - >3 long paragraphs):")
        for r in para_issues:
            lines.append(f"   • {r['filename'].replace('-2025-12-10.md', '')}: {r['paragraphs']['long_count']} paragraphs >4 sentences")

    # Rhythm issues (list last as there are many)
    rhythm_issues = [r for r in results if not r['scores']['rhythm']]
    if rhythm_issues:
        lines.append("")
        lines.append(f"❌ RHYTHM ISSUES ({len(rhythm_issues)} articles - monotonous sentence patterns):")
        for r in rhythm_issues:
            lines.append(f"   • {r['filename'].replace('-2025-12-10.md', '')}: score={r['rhythm']['score']}, monotonous_sections={r['rhythm']['monotonous_sections']}")

    lines.append("")
    lines.append("=" * 90)

    return "\n".join(lines)


def main():
    """Analyze all articles from today"""
    import glob

    # Find all articles from today
    pattern = "drafts/*2025-12-10*.md"
    files = sorted(glob.glob(pattern))

    if not files:
        print(f"No files found matching {pattern}")
        sys.exit(1)

    print(f"Found {len(files)} articles to analyze...")
    print("")

    analyzer = EngagementAnalyzer()
    results = []

    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        filename = Path(filepath).name
        result = analyzer.analyze(content, filename)
        results.append(result)

    print(format_results(results))


if __name__ == '__main__':
    main()
