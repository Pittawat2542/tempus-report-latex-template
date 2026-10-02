# Tempus v1.6.0: presentation deck template

Planned October 3, 2026. This release follows the v1.5.0 report release gate;
no presentation theme is implemented in v1.5.0. Both technical talks and
executive updates are first-class use cases.

## Interface and distribution

Use ordinary Beamer, not a new document class:

```tex
\documentclass[11pt,aspectratio=169]{beamer}
\usetheme{Tempus}
\title{Your presentation}
\author{Your Name}
\institute{Your Institute}
\date{Your date}
```

The starter defaults to 16:9. Support `aspectratio=43` and `handout` through
standard [Beamer interfaces](https://tug.ctan.org/macros/latex/contrib/beamer/doc/beameruserguide.pdf).
Keep standard metadata, frames, columns, overlays, blocks, mathematics, and
bibliography commands. Do not replace them with parallel Tempus commands.
Theme selection must not force an aspect ratio or change handout semantics.

Ship `beamerthemeTempus.sty`, `tempusdesign.sty`, `tempus-deck-starter.tex`,
`tempus-deck.tex`, and the comprehensive deck PDF. The report distribution
must include `tempusdesign.sty` beside `tempusreport.cls`; document this new
required file in both quick-start and copying instructions. Retain the root
report entrypoints and existing report commands.

## Shared design package and visual specification

Extract the report's named palette, engine-aware Libertine/Heros font setup,
optional Latin Modern code-font setup, and vector logomark into
`tempusdesign.sty`. Both report and theme require it. Keep report geometry,
headers, captions, pagination, bibliography setup, and optional content
packages in the report class. Beamer owns slide navigation and captions;
do not import the report class or its global package options into the deck.

The shared package exports existing `Tempus*` colors, `\reportlogomark`, and
`\tempuscodefont` when code support is requested. Preserve color overrides
made after class/theme loading. Preserve the report's existing font selection
and scale during extraction; use explicit shared-package options where the
slide scale differs. Do not unconditionally load listings for code fonts.

- Use the existing navy/teal T mark and slate/navy palette without new brand
  colors. Retain semantic navy, teal, amber, and burgundy block styles.
- Keep Helvetica-compatible headings and Libertine body text. Use Beamer's
  11 pt base, 18 pt frame titles, 22 pt title-slide title, and readable 8 pt
  minimum code. Use packaged fonts; require no system font installation.
- Use white slide backgrounds, pale callout surfaces, square corners, thin
  rules, and generous whitespace. Standard content slides have 8 mm side
  margins and a restrained navy frame-title rule.
- Show short title and frame number in a quiet footer. Suppress the footer on
  title/closing slides and hide navigation icons by default. Section dividers
  are explicitly authored; avoid automatic extra frames.
- Keep long titles wrap-capable. Do not silently shrink or clip slide content;
  teach authors to split crowded frames. Maintain these principles in 4:3.

## Layout and content deliverables

The comprehensive deck demonstrates all layouts, with synthetic content:

| Layout | Required demonstration |
| --- | --- |
| Title and closing | Brand mark, title, metadata, optional institution artwork, contact link |
| Agenda and section divider | Standard contents and explicit section-transition frame |
| Single-column content | Clear message, short prose/list, semantic block |
| Two-column comparison | Matched-width alternatives with one shared conclusion |
| Figure/diagram | Editable TikZ diagram and image with descriptive source text |
| Technical results | Equations, booktabs table, plot/image, interpretation, citation |
| KPI summary | Three metrics with units, context, and explanatory labels |
| Timeline | Four labelled milestones using the shared palette |
| Recommendation | Decision, supporting evidence, next step |
| References | Author-year citations and bundled ACL/BibTeX workflow |

Theme standard `block`, `exampleblock`, and `alertblock` as navy note, teal
tip, and amber warning. Supply an opt-in burgundy important block. Labels
and titles convey meaning independently of color. Keep overlays under author
control and demonstrate them without excessive animation.

The minimal starter contains metadata, title, agenda, one content frame, and
closing frame. The full example adds overlays, mathematics, references,
figures, tables, and fragile code frames using optional listings. No shell
escape, minted, or automatic frame-breaking of code is required. Make
missing optional artwork recoverable with bounded placeholders and clear
warnings, following the report's file-resolution policy.

## Implementation sequence and acceptance

1. Capture report visual baselines, then extract the shared package. Compile
   all report fixtures and compare page text/renders before designing slides.
2. Implement the Beamer theme and starter, preserving standard Beamer APIs.
3. Build the comprehensive technical/executive deck and all layout examples.
4. Extend the pinned four-engine validator with 16:9, 4:3, handout, overlays,
   long titles, optional artwork, code, references, and palette-override fixtures.
5. Publish copying/build instructions and regenerate the deck PDF only after
   its canonical validation passes. Record v1.6.0 evidence in the changelog.

Release acceptance requires clean supported-engine logs, resolved citations
and links, no frame overflow or missing glyphs, correct overlay/handout page
counts, and visual review of every layout at both aspect ratios. Report output
must remain equivalent after shared-package extraction. Both templates must
consume the same design definitions; prohibit duplicated palettes or marks.

Retain an explicit engine/font visual-review record. Tagged PDF, arbitrary
Unicode listings, PowerPoint export, and automatic report-to-slide conversion
are outside this release. Tagged output and expanded Unicode support remain
separate evidence-gated investigations from the report roadmap.
