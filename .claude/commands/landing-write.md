# Landing Page Write Command

Create high-converting landing pages for organic SEO or paid PPC traffic.

## Usage
`/landing-write [topic or research brief] --type [seo|ppc] --goal [trial|demo|lead]`

**Examples:**
- `/landing-write "product hosting for beginners" --type seo --goal trial`
- `/landing-write "research/landing-brief-private-producting.md" --type ppc --goal demo`

**Defaults:** `--type seo`, `--goal trial`

## Pre-Writing Review

**Required Context:**
- @context/landing-page-templates.md -- structure
- @context/cro-best-practices.md -- conversion guidelines
- @context/brand-voice.md -- tone and messaging

If research brief available: use recommended headlines, identified pain points, suggested trust signals.

---

## SEO Landing Page (--type seo)

**Specs:** 1500-2500 words, 3-5 CTAs distributed, 2-3 internal links

**Structure:** Hook (pain point/stat/question) + trust signal + Primary CTA -> Problem/Pain Point -> Solution + Key Benefits + Secondary CTA -> Features (3-5, tied to benefits) -> Social Proof (2+ testimonials with results) + CTA -> How It Works (3 steps) -> FAQ (4-6 questions) -> Closing CTA + Risk Reversal

## PPC Landing Page (--type ppc)

**Specs:** 400-800 words, 2-3 CTAs (same goal), 0-1 internal links

**Structure:** Headline matching ad copy + trust signal + Prominent CTA -> Benefits (3 bullets) -> Proof (1+ testimonial) + CTA -> What You Get + Risk Reversal + Final CTA

---

## Goal-Specific CTA Guidelines

### Trial (--goal trial)
CTAs: "Start Your Free Trial", "Try Free for 14 Days", "Get Started Free"
Supporting: "No credit card required", trial length, "Cancel anytime", "Set up in minutes"

### Demo (--goal demo)
CTAs: "Book Your Demo", "Schedule a Call", "See It in Action"
Supporting: Demo length ("15-minute walkthrough"), what it covers, "No pressure, no hard sell"

### Lead (--goal lead)
CTAs: "Download the Free Guide", "Get Instant Access", "Claim Your Copy"
Supporting: What they get, "Instant download", "No spam, ever", content preview

---

## Required Elements Checklist

**Above the Fold:** Benefit-focused H1, clear value prop (1-2 sentences), prominent primary CTA, trust signal (count/rating/result).

**Trust Signals:** 2+ named testimonials (SEO) / 1+ (PPC), specific results with numbers, risk reversal near CTAs.

**CTAs:** Action verb (Start, Get, Try, Book) + benefit word (Free, Instant, Today), goal-aligned, first CTA within 20% of page, CTA at end.

**SEO (SEO pages only):** Keyword in headline + meta title + first 100 words, 2-3 internal links.

## Headline Formulas

**Benefit:** "[Achieve Outcome] Without [Pain Point]" / "The [Adjective] Way to [Achieve Outcome]" / "Finally, [Solution] for [Audience]"

**Number:** "[Number] [Audience] Trust [Product] to [Benefit]"

**Question:** "Ready to [Achieve Outcome]?"

**Don'ts:** No "Welcome to...", no "The Best..." without proof, no starting with "Our"/"We", max 70 chars.

---

## File Output

Save to: `landing-pages/[topic-slug]-[YYYY-MM-DD].md`

## Post-Save Pipeline

1. **Scrub:** `/scrub landing-pages/[filename].md`
2. **Score:**
```bash
python data_sources/modules/landing_page_scorer.py landing-pages/[filename].md --type [seo|ppc] --goal [trial|demo|lead]
```
Minimum 75/100, no critical issues. If below, fix top 3 issues and re-score. If still below, save to `review-required/landing-pages/`.

3. **Run agents:** `landing-page-optimizer` (CRO report), `headline-generator` (10+ variations), `cro-analyst` (psychology analysis)

---

## /write vs /landing-write

| Aspect | /write (Blog) | /landing-write |
|--------|---------------|----------------|
| Goal | Educate & inform | Convert visitors |
| Length | 2000-3000+ words | 400-2500 words |
| CTAs | 2-3 contextual | 3-5 prominent (SEO) |
| Structure | Educational flow | Conversion flow |
| Internal Links | 3-5 | 0-3 |
| Output | drafts/ | landing-pages/ |
| Scoring | content_scorer | landing_page_scorer |
