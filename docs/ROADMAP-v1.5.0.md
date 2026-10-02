# Tempus v1.5.0 roadmap

Reviewed October 2, 2026 against the v1.4.0 stress suite. P1 items should
lead the next release; P2 items follow once the core regression checks pass.
This is a plan, not a claim that the proposed behavior already exists.

## Evidence and current release

The original three-page example and twelve release documents compile with
Tectonic 0.17.0. The comprehensive example is now sixteen pages. Final LaTeX
logs contain no overfull/underfull boxes, missing characters, undefined
citations/references, or LaTeX/package warnings. All example pages and fixture
title pages were rendered and inspected. Separate negative inputs establish
the remaining findings below; they are not passing-suite inputs.

The suite confirms repeated longtable headers, multipage callouts and listings,
restored algorithm line numbering across a real page boundary, alphabetic
appendices, navigation indexes, PDF bookmarks/links, and independent optional
package activation. Long prose titles wrap and the tested running header fits
without warnings; this does not establish unlimited metadata length support.

Fixed in v1.4.0:

- Long placeholder descriptions previously overflowed a narrow panel by
  318.44 pt. Placeholder text now wraps within 85% of its panel width.
- Standard author separation with `\and` caused `Misplaced \crcr` because the
  custom title uses paragraphs rather than article's author table. It now
  renders comma-separated names in compact and wide layouts.
- The tracked PDF still contained branding removed by earlier source commits.
  The release regenerates it from the current class and stress example.

## Confirmed shortcomings and implementation plan

### P1: Keep listing captions with their first lines

**Reproduce:** Remove the explicit `\clearpage` immediately before the main
example's `Code listings` subsection and compile. In the initial stress build,
the caption landed at the bottom of page 4 and all code started on page 5,
with no layout warning. The release example uses an explicit page boundary.

**Impact:** Clean compilation can still produce a confusing caption/code split.

**Change:** When the listings option is enabled, reserve space for the caption
and at least two code lines at listing entry. Apply the behavior to both
`lstlisting` and `\lstinputlisting`; keep long listings breakable. Keep any
supporting package optional with listings, and document explicit user page
breaks as an override.

**Acceptance:** A fixture with little remaining page space moves the caption
and first two lines together. A multipage listing still breaks normally;
numbering, anchors, caption lists, and external-file inclusion remain correct.

### P2: Make missing optional artwork recoverable

**Reproduce:** Add `\reportlogo{does-not-exist.pdf}` to the default fixture.
Tectonic exits 1 at `\maketitle` with `Unable to load picture or PDF file`.
Unlike `\reportimage`, title artwork currently has no missing-file recovery.
Missing mascot/partner handling is a related implementation target; those
individual paths have not yet been exercised as negative runtime cases.

**Impact:** An optional branding asset can prevent the entire report building.

**Change:** Centralize artwork existence checks. Emit a class warning naming
missing files; revert a missing logo to text branding, omit a missing mascot
and its reserved spacing, and render a bounded placeholder for missing partner
artwork. Preserve successful image sizing and the existing public commands.

**Acceptance:** Missing logo, mascot, wordmark, and institutional icon cases
compile with only their expected class warnings. Existing assets remain
visually unchanged, and `nobanner` does not validate artwork it never renders.

### P2: Validate layout and abstract-style values

**Reproduce:** Use `\reportauthorlayout{unknown}` and
`\reportabstractstyle{unknown}` in an otherwise valid report. It compiles
without a class warning, using compact authors and a flat abstract.

**Impact:** Typographical mistakes silently select a different appearance.

**Change:** Recognize `compact`/`wide` and `flat`/`cuboid` explicitly. Warn on
unknown values and use the documented compact/flat defaults. Validate positive
mascot widths and nonnegative overlap before layout calculations; bounds
validation is an additional feature, not a confirmed runtime defect here.

**Acceptance:** Valid existing calls produce no warnings. Invalid enum values
produce actionable warnings and deterministic defaults. Invalid dimensions
cannot result in negative title-column widths or unreadable overlap.

## Coverage gaps and features to investigate

These are not established regressions in the supported release suite.

| Priority | Reproduction or validation target | Impact | Proposed improvement | Acceptance |
| --- | --- | --- | --- | --- |
| P1 | Run the same suite with pdfLaTeX, XeLaTeX, and LuaLaTeX; those standalone executables were unavailable here. | Engine compatibility claims lack release evidence. | Add CI with Tectonic plus the three TeX Live engines, each using its normal bibliography passes. Retain artifacts and pin the toolchain. | All fixtures build on each advertised engine with resolved navigation/citations; font differences receive visual review. |
| P2 | Inspect `pdfinfo tempus-template.pdf`: `Tagged: no`. Assistive reading order has not been validated. | Accessible reading/navigation is unverified. | Prototype an opt-in tagged-PDF setup on a pinned compatible engine before adding a supported class option. Validate the custom title, boxes, tables, figures, and bibliography. | A tagged-PDF validator and reading-order review pass; image alternatives and table semantics are documented. Existing untagged output remains compatible. |
| P2 | Try non-ASCII Python source in a listing and multilingual prose requiring fonts beyond the bundled Latin fonts. | Arbitrary Unicode listings and multilingual reports are outside current evidence. | Define the supported Unicode/font policy, add representative fixtures, and document mappings or an alternative code-rendering workflow. Keep the default shell-escape-free build. | The declared character set renders without missing glyphs on supported engines; unsupported inputs receive clear documentation. |
| P2 | Review the second page of the long listing and callout: neither repeats a continuation heading. | Readers may lose context in standalone page excerpts. | Provide documented opt-in continuation labels for boxes/listings and a continued algorithm example retaining one logical caption identity. | Continuation labels and page references stay correct across two or more pages, without duplicate navigation entries. |
| P2 | Start a new report from the sixteen-page stress example. | Validation content makes quick authoring cumbersome. | Add a separate minimal starter while retaining the exhaustive example and fixtures as the regression suite. | The starter builds with the same class, includes clear metadata/bibliography instructions, and links to feature examples. |

## Release sequence

1. Add caption-pagination regression fixtures and implement the P1 fix.
2. Add multi-engine CI and automated checks for PDF metadata, bookmarks,
   destinations, optional-package activation, and generated PDF/source drift.
3. Add missing-artwork recovery and validated configuration values with
   focused negative fixtures and expected-warning checks.
4. Ship continuation helpers and the minimal starter. Gate accessibility and
   expanded Unicode support on their own compatibility evidence rather than
   promising them automatically in v1.5.0.

Record delivered changes under a new 1.5.0 changelog entry. Keep this document's
remaining items open with updated evidence and retain the v1.4.0 cases.
