# Changelog

All notable template changes are recorded here. Versions refer to the template
class release; `\reportversion` remains author-controlled report metadata.

## [1.5.0] - Unreleased release candidate

### Added

- Caption-space protection for environment and external-file listings, with
  optional needspace loading and PDF pagination regression checks.
- Render-only missing-artwork warnings and recovery, including graphics-path
  and implicit-extension support.
- Explicit layout/style validation and bounded mascot width/overlap recovery.
- Opt-in continued box headings, external listing segments, and algorithm
  captions retaining one logical numbered caption and index entry.
- A minimal report starter and nine regression fixtures (twenty fixtures total).
- Four-engine validation CLI and digest/checksum-pinned GitHub Actions matrix,
  exact expected-warning checks, PDF navigation/metadata/continuation assertions,
  and canonical PDF text/render drift checks.
- A decision-complete v1.6.0 Beamer roadmap covering shared design packaging,
  technical and executive layouts, aspect ratios, handouts, and acceptance gates.
- Native navy/teal T logomark, reused in the default brand lockup and bundled
  vector asset via `\reportlogomark`.
- An isolated asset-export option (`--rebuild-assets`) in the validation runner.
- Explicit appendix headings with alphabetic sections, appendix-scoped
  equation/figure/table/algorithm/listing numbers, and cleveref appendix names.
- Two supplementary appendices in the stress example and a default-option
  appendix fixture; validation checks A.1/B.1 resets and reference types.

### Fixed

- Listing captions no longer require the example's manual page-break workaround.
- Optional missing branding no longer aborts a report build.
- Continued algorithms in the stress example retain the first caption identity.

### Release gate

- Local Tectonic 0.17.0 validation and visual review are recorded in the roadmap.
  pdfLaTeX, XeLaTeX, and LuaLaTeX remain pending CI evidence and font review.
  This entry does not declare a completed release or a publication date.

### Changed

- Compact first-page banner: smaller wordmark and custom-logo height, tighter
  partner/rule spacing, and a thinner divider.
- Title reduced from 24/28 pt to 21/25 pt, with a smaller gap before authors.
- Listings use a dedicated Latin Modern monospace font at footnote size
  instead of the wider Libertine monospace font at small size. Body fonts
  remain unchanged; natural glyph widths and indentation are preserved.
- The example bibliography precedes the supplementary appendices, and the
  expanded contents starts on its own page.

### Validation

- All 22 report documents pass Tectonic 0.17.0 validation; four tests verify
  warning parsing, rejection of invalid link destinations, and PDF drift policy.
- The regenerated example is seventeen pages, with resolved navigation,
  citations, and references. Existing flat/cuboid artwork fixture renders match
  the original class exactly. All report pages and fixture titles were reviewed.
- Inline listings retain their surrounding text line, checked in the PDF;
  pagination tests also cover floating and bottom-caption listings.

## [1.4.0] - 2026-10-02

### Added

- Comprehensive report stress example covering typography, structure,
  navigation, citations, advanced mathematics/proofs, tables, real and missing
  artwork, subfigures, and editable TikZ content.
- Multipage tables with repeated headings, all callout themes, continued
  algorithms across pages, and inline/external/multipage code listings.
- Eleven independent title/option fixtures, original bundled vector artwork,
  and synthetic bibliography entries clearly identified as test data.
- Isolated validation runner with warning and optional-package checks.
- Evidence-based v1.5.0 roadmap with priorities and acceptance criteria.

### Fixed

- Missing-image descriptions now wrap inside narrow panels.
- Standard `\and` author separation now works in compact and wide layouts.
- Example pagination keeps the short listing's caption with its code.
- Regenerated tracked PDF reflects the current class and example rather than
  retaining previously removed header/footer branding.

### Changed

- Class metadata and example report metadata identify v1.4.0.
- README documents suite coverage, fixture purposes, and reproduction commands.

### Validation

- Tectonic 0.17.0 compiled the untouched baseline and all twelve release
  documents. The main example is sixteen A4 pages.
- Final suite logs have no LaTeX/package warnings, overfull/underfull boxes,
  missing glyphs, or unresolved citations/references. Rendered pages and
  title fixtures were inspected. PDF checks verified all five navigation
  indexes, 20 bookmarks, 94 internal links, 5 external links, and metadata.
- Tectonic reports font-resolution diagnostics and an encoding warning from a
  Latin-1 copyright comment in bundled `algorithm.sty`; these do not indicate
  missing document glyphs and do not affect the rendered examples.
- Standalone pdfLaTeX, XeLaTeX, and LuaLaTeX were unavailable and remain
  unverified. Tagged PDF and arbitrary Unicode listings are not validated.

## Earlier history (release versions and dates unverified)

These changes are derived from Git history, not reconstructed release records.
The preceding class declared v1.3; no historical release tags were present.

- `faf6647` — removed running-header branding and footer version text.
- `bff0e44` — reduced the report title font size.
- `4b9a15c` — added first-page `banner` and `nobanner` options.
- `74ce10a` — initial standalone template, bibliography style, and example.
