# Changelog

All notable template changes are recorded here. Versions refer to the template
class release; `\reportversion` remains author-controlled report metadata.

## [Unreleased]

### Added

- Native navy/teal T logomark, reused in the default brand lockup and bundled
  vector asset via `\reportlogomark`.
- An isolated asset-export option (`--rebuild-assets`) in the validation runner.
- Explicit appendix headings with alphabetic sections, appendix-scoped
  equation/figure/table/algorithm/listing numbers, and cleveref appendix names.
- Two supplementary appendices in the stress example and a default-option
  appendix fixture; validation checks A.1/B.1 resets and reference types.

### Changed

- Compact first-page banner: smaller wordmark and custom-logo height, tighter
  partner/rule spacing, and a thinner divider.
- Title reduced from 24/28 pt to 21/25 pt, with a smaller gap before authors.
- Listings use a dedicated Latin Modern monospace font at footnote size
  instead of the wider Libertine monospace font at small size. Body fonts
  remain unchanged; natural glyph widths and indentation are preserved.
- The example bibliography precedes the supplementary appendices, and the
  expanded contents starts on its own page.
- All twelve documents pass Tectonic validation, including appendix counter
  and reference checks; the regenerated example is seventeen pages. The code
  font size and rendered pages were verified.

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
