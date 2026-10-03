# v1.6.0 validation and visual review

Reviewed October 3, 2026. Status: implementation candidate; release gate open.
No release tag or publication is implied by this record.

## Report preservation

Before extraction, all 22 report documents passed Tectonic 0.17.0 validation
and the tracked report passed text/render drift checks. The original class
and isolated outputs were captured under `.build/v1.6.0-baseline/`.
After extraction, all 22 documents passed again. Every baseline/new PDF pair
had identical normalized page text and passed the existing 72 dpi render
comparison (at most 0.1% channel differences greater than 16/255).
The tracked report PDF remains unchanged.

`tempusdesign.sty` is the sole palette, font-setup, and vector-mark definition.
Reports retain the original 0.94 sans scale and optional Latin Modern code
font. The deck requests the explicit `slides` scale of 1.0. Unit checks reject
palette/mark duplication and unconditional shared-package listings loading.

## Engine and font review

| Engine | Compilation and PDF inspection | Font/layout review |
| --- | --- | --- |
| Tectonic 0.17.0 | 33 documents pass | Complete at 16:9 and 4:3 |
| pdfLaTeX, pinned TeX Live 2026 | Pending fresh CI run | Pending |
| XeLaTeX, pinned TeX Live 2026 | Pending fresh CI run | Pending |
| LuaLaTeX, pinned TeX Live 2026 | Pending fresh CI run | Pending |

Local TeX Live engines are unavailable and the Docker daemon is not running.
Retained v1.5.0 CI artifacts do not establish v1.6.0 engine compatibility.
The existing digest-pinned four-engine workflow now validates both templates.
A fresh complete matrix and visual review of each engine's outputs are required
before declaring this release complete, together with the prior 1.5.0 gate.

Tectonic PDF resources confirm LinLibertineO body text, TeXGyreHeros headings,
and LMMonoLt10 code. Code uses 8 TeX pt (approximately 7.97 PDF bp), checked in
the PDF. Other engines must pass their own font-resource and minimum-size checks;
pdfLaTeX uses helvet's Helvetica-compatible packaged fonts.

## Deck evidence

| Document | Frames | PDF pages | Purpose |
| --- | ---: | ---: | --- |
| `tempus-deck` | 15 | 17 | Canonical 16:9 comprehensive example |
| `deck-43` | 15 | 17 | Every layout at 4:3 |
| `deck-handout`, `deck-43-handout` | 15 each | 15 each | Standard collapsed overlays |
| `tempus-deck-starter`, `deck-starter-43` | 4 each | 4 each | Minimal starter at both ratios |
| `deck-overlays` | 1 | 3 | Item and important-block reveal order |
| `deck-overlays-handout` | 1 | 1 | All revealed content retained |
| `deck-long-title` | 2 | 2 | Wrapped title, frame title, and subtitle at 4:3 |
| `deck-artwork` | 2 | 2 | Graphics-path/implicit-extension resolution and missing-art recovery |
| `deck-palette` | 2 | 2 | Overrides update headings, blocks, rule, and vector mark |

Logs have no overfull/underfull boxes, missing glyphs, unresolved citations or
references, or unexpected class/package warnings. The artwork fixture declares
exactly one missing-art warning. Report negative fixtures retain their existing
exact warning expectations. The deck has three section bookmarks, 19 internal
links, and two external links (paper title and closing contact).

PDF inspection checks geometry, exact frame/page counts, font presence, code
size, and link destinations. Overlay visibility checks transform text origins
by the PDF text/current matrices; ordinary text extraction includes Beamer's
covered content translated off-page and cannot prove reveal order by itself.
The palette fixture checks actual PDF fill colors, rejecting frozen navy after
the accent is overridden to teal. Deck logs must not load the report class or
its caption, list, header, or box packages.

## Visual review

All 17 comprehensive pages were rendered at 100 dpi and reviewed at both
ratios, including each overlay. Reviewed title/closing, agenda, explicit
section divider, prose/list/note, matched-width comparison, editable diagram,
equation/citation/warning, result table and plot, image/source, fragile code,
three KPI panels, four milestones, recommendation/important block, and
references. The review corrected overlapping plot category labels and shortened
comparison headings for consistent column layout. No clipping, overlap,
unreadable glyphs, or footer collisions remain in reviewed renders.

Both starters and all control-fixture pages were reviewed. Long titles retain
the configured sizes; plain title/closing frames omit the footer; missing art
uses a bounded legible placeholder; all three overlay stages render correctly.
Full handouts undergo automated count/content/geometry checks; cross-engine
handout visual review remains part of the pending matrix gate.

Local renders are under `.build/review-v1.6.0/`; logs, PDFs, toolchain versions,
font lists, counts, and links are under `.build/validation/tectonic/`.
CI retains per-engine evidence for 30 days. These directories are ignored;
this tracked record preserves conclusions and explicit limits.

## Reproduce

```sh
python3 -m pip install -r scripts/requirements.txt
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/validate.py --only-cached --check-example
# After all canonical checks pass, explicitly refresh the deck:
python3 scripts/validate.py --update-deck
# Engine-specific runs (requires TeX Live and BibTeX):
python3 scripts/validate.py --engine pdflatex
python3 scripts/validate.py --engine xelatex
python3 scripts/validate.py --engine lualatex
```

The thirteen unit tests cover warning multiplicity/wrapping, off-page overlay
text, canonical variant content, single shared design definitions, navigation,
PDF drift, and continuation semantics. Full-deck variants are generated from
`examples/decks/variants.json`; only the standard documentclass options change.
The final canonical drift check passes for both tracked report and deck
outputs, comparing page text and 72 dpi renders.
Tagged PDF, arbitrary Unicode listings, PowerPoint export, and report-to-slide
conversion remain outside this release.
