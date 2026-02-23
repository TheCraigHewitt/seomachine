# Landing Page Competitor Analysis Command

Analyze a competitor's landing page for CRO patterns, strengths, and weaknesses.

## Usage
`/landing-competitor [URL]`

**Examples:**
- `/landing-competitor https://competitor.com/pricing/`
- `/landing-competitor https://competitor.com/features/`

## Analysis Framework

Analyze these 7 dimensions:

1. **Page Overview:** URL, page type, word count, structure, conversion goal
2. **Above-the-Fold:** Headline (exact text + approach), subheadline/value prop, CTA (text + visibility), trust signals, first impression
3. **Content Strategy:** Key messages, benefit vs feature balance, pain points addressed, unique value props
4. **CTA Strategy:** All CTAs (text + placement), frequency, text patterns, goal alignment
5. **Trust Signals:** Testimonials (count, quality, specificity), social proof (counts, logos), risk reversals (trials, guarantees), authority signals
6. **Objection Handling:** FAQ quality, objections in copy, comparison content, pricing transparency
7. **Technical/UX:** Load speed estimate, mobile considerations, form complexity, navigation

## Output

Save to: `research/competitor-landing-[domain]-[YYYY-MM-DD].md`

Report includes:
- Quick summary rating table (headline, value prop, CTAs, trust, overall CRO)
- Above-fold breakdown with exact text extracted
- Full CTA inventory with position and strength
- Trust signals inventory (testimonials, social proof, risk reversals, authority)
- Content structure and focus analysis
- Strengths to learn from (what they do, why it works, how to apply)
- Weaknesses to exploit (what's missing, impact, your advantage)
- Key takeaways (must do / should do / avoid)
- Differentiation recommendations
- Headlines and CTAs to beat theirs

## Analysis Focus

**Patterns:** Repeated CTA text, trust signal placement, argument structure.
**Gaps:** Unaddressed objections, missing trust signals, vague/generic copy.
**Differentiation:** Unique angles, claims they can't make, vulnerable positioning.

Competitor list: `config/competitors.json`

## Next Steps

- `/landing-write "[topic]" --type seo --goal trial` to create page that beats competitor
- `/landing-audit https://yoursite.com/[page]/` + this command to compare side-by-side
