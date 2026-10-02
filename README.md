# Tempus

A standalone A4 LaTeX report template with slate navy (`#1E3A5F`),
Helvetica-style headings, Libertine body text, and an editorial first page.

## Use

For a new report, copy `tempus-starter.tex` with `tempusreport.cls`,
`acl_natbib.bst`, and `reference.bib`, then run `tectonic tempus-starter.tex`.
Use the comprehensive example below to explore features.

Keep `tempusreport.cls`, `acl_natbib.bst`, and `reference.bib` beside
`tempus-template.tex`.
Edit the example's title,
author, affiliation, short title, report number, version, and content.

Compile with Tectonic:

```sh
tectonic tempus-template.tex
```

Tectonic downloads TeX packages on first use and runs BibTeX and the necessary
LaTeX passes automatically. For editor navigation between source and PDF, use
`tectonic --synctex tempus-template.tex` and enable SyncTeX in your editor/viewer.

With a complete TeX Live or MiKTeX installation, use:

```sh
latexmk -pdf -synctex=1 tempus-template.tex
```

`latexmk` also runs BibTeX and repeats LaTeX as needed. Without `latexmk`, run:

```sh
pdflatex -synctex=1 tempus-template.tex
bibtex tempus-template
pdflatex -synctex=1 tempus-template.tex
pdflatex -synctex=1 tempus-template.tex
```

## Working examples

The example is the v1.5.0 report stress suite. It demonstrates typography,
heading levels, lists, footnotes, links, navigation indexes, citations,
advanced mathematics and proofs, flexible and multipage tables, real and
missing artwork, subfigures, an editable TikZ training diagram, all callout
styles, continued pseudocode, inline/external code, and multipage listings.
All measurements and artwork are synthetic. The missing workflow image and
missing subfigure are intentional placeholder tests.

Compile from the repository root so bundled artwork and source paths resolve.
The example adds `mathtools`, `siunitx`, `longtable`, `amsthm`, and `cleveref`;
these are content-specific dependencies, not new class requirements.

### Reproducible stress checks

With Python 3, Tectonic, and the PDF inspection dependency installed, run:

```sh
python3 -m pip install -r scripts/requirements.txt
python3 scripts/validate.py
python3 -m unittest discover -s scripts -p 'test_*.py'
```

The runner compiles the comprehensive example, minimal starter, and twenty
option/regression fixtures into `.build/validation/<engine>/`. It rejects
layout warnings, missing glyphs, unresolved references/citations, and unexpected
class/package warnings. Negative fixtures declare exact expected class warnings
in `examples/expected-warnings.json`. It also checks optional-package activation,
appendix and continuation numbering, caption/code pagination, PDF metadata,
bookmarks, link destinations, and navigation indexes. PDFs, logs,
`toolchain.txt`, and `inspection.json` remain available for review.

Use `--only-cached` for offline Tectonic checks after the first package download.
Use `--engine pdflatex`, `--engine xelatex`, or `--engine lualatex` with a complete
TeX Live installation and BibTeX. These engines run an initial LaTeX pass,
BibTeX when needed, and three further LaTeX passes. All builds remain
shell-escape-free.

`--update-example` replaces the tracked PDF only after the whole suite passes.
`--check-example` compares the tracked and regenerated PDF's page text and
72 dpi renders, ignoring volatile PDF metadata. It requires Poppler's
`pdftoppm`, and tolerates at most 0.1% color-channel differences exceeding
16/255 for rasterizer antialiasing. Canonical PDF updates/drift checks and asset
exports use Tectonic only. Visual review remains required.

CI runs Tectonic 0.17.0 (download checksum pinned) and all three engines from
an immutable TeX Live 2026 image, retaining evidence for 30 days. Local Tectonic
success does not complete the four-engine release gate. The 1.5.0 implementation
is a release candidate until the matrix and cross-engine font review pass.

| Fixtures | Purpose |
| --- | --- |
| `default`, `banner`, `nobanner` | First-page banner behavior and subsequent-page styling |
| `algorithms`, `listings`, `combined` | Independent optional-package activation |
| `wide`, `empty`, `long-metadata` | Author layout, empty fields, and title/header wrapping |
| `art-flat`, `art-cuboid`, `graphics-path` | Artwork sizing, abstract styling, implicit extensions and graphics paths |
| `listing-pagination`, `continuations` | Caption placement, long listings, continuation identity and numbering |
| `missing-artwork`, `suppressed-artwork`, `suppressed-mascot` | Recovery and render-only artwork validation |
| `invalid-settings`, `invalid-dimensions`, `oversized-dimensions` | Exact warnings and deterministic safe defaults |

Fixture sources live in `examples/`. The validation runner resolves class and
asset paths for them automatically. Rebuild the bundled vector asset with
`python3 scripts/validate.py --rebuild-assets --update-example` from the root.
The isolated export uses the same `\reportlogomark` artwork as the class banner,
so the default mark and bundled PDF remain consistent.

See [CHANGELOG.md](CHANGELOG.md) for release changes and
[the v1.5.0 roadmap](docs/ROADMAP-v1.5.0.md) for implementation and release gates.
[The v1.6.0 roadmap](docs/ROADMAP-v1.6.0.md) specifies a Beamer deck for technical
and executive presentations sharing the report's design language.

The class already includes `graphicx`, `amsmath`, `amssymb`, `booktabs`,
`tabularx`, `array`, `enumitem`, `caption`, `subcaption`, TikZ, `tcolorbox`,
and `microtype`. It also loads `natbib` for author-year citations, `xurl` for long
URL wrapping, and `hyperref` with `bookmark` for links and PDF navigation.
PDF title and author metadata come from `\title` and `\author`; override them
with `\hypersetup{pdftitle={...},pdfauthor={...}}` when needed.

The example adds content-specific helpers that you can remove if unused:

- `mathtools` extends the class's mathematics support.
- `siunitx` provides `\qty{12.3}{\milli\second}`, `\num{10000}`,
  `\unit{\percent}`, and decimal-aligned `S` table columns.
- `cleveref` provides `\cref{eq:mean,tab:results}` with automatic reference
  names and `\Cref{fig:workflow}` at the start of a sentence. Load it after
  your other packages; the example uses `nameinlink,noabbrev`.

Place `\label` immediately after a section heading, inside a numbered equation,
or **after** a figure/table's `\caption`. Use unique prefixes such as `sec:`,
`eq:`, `tab:`, and `fig:` to keep labels easy to find.

### Scientific ML diagram

The example's `fig:ml-training` is an editable supervised training diagram:
mini-batch inputs pass through an encoder and classifier to a cross-entropy
loss, with target labels entering the loss separately. Solid arrows represent
forward computation; dashed burgundy arrows represent gradient flow to the
trainable modules. The caption defines the batch size, class count, and learning
rate.

Copy its `figure` environment to reuse it. The picture defines local `ml block`,
`ml flow`, `ml gradient`, and `ml label` styles using the Tempus palette.
Change node text, colors, or the `right=9mm of ...` spacing to adapt it.
No external artwork or extra packages are needed: the class already loads
TikZ with `arrows.meta`, `positioning`, and `calc`. See the
[TikZ manual](https://tikz.dev/tikz-shapes) for node placement and styling.

### Bibliography

Add entries to `reference.bib` and cite their keys:

```tex
\citet{vaswani2017attention} % Vaswani et al. (2017)
\citep{vaswani2017attention} % (Vaswani et al., 2017)
```

The example ends with:

```tex
\bibliographystyle{acl_natbib}
\bibliography{reference}
```

The bundled official [ACL bibliography style](https://github.com/acl-org/acl-style-files/blob/master/acl_natbib.bst)
lists entries alphabetically, without numeric labels, and links titles to the
entry's DOI or URL when available. The class uses author-year citations in round
parentheses. Only cited entries appear by default; use `\nocite{key}` to include
a specific uncited entry. Keep the
class's `natbib` workflow when following this example; `biblatex` uses a
different setup and is not an additional package to load alongside `natbib`.

### Optional packages

Enable themed pseudocode and code blocks with class options:

```tex
\documentclass[algorithms,listings]{tempusreport}
```

Use either option independently, or omit both for reports without these content
types. The example enables both to demonstrate them. The `algorithms` option
loads `algorithm` for floats and `algpseudocode` (from `algorithmicx`) for
pseudocode. The `listings` option loads `listings` and `needspace`, and selects the `tempus`
style. These follow the standard [algorithmicx](https://ctan.org/pkg/algorithmicx)
and [listings](https://ctan.org/pkg/listings) interfaces.

Add `longtable` for tables spanning multiple pages, or `babel` configured for
your document's language. Tagged-PDF
accessibility requires separate engine and package compatibility validation;
this template does not enable it by default.

### Algorithms

```tex
\begin{algorithm}[htbp]
  \caption{Compute a total.}
  \label{alg:total}
  \begin{algorithmic}[1] % Omit [1] to hide line numbers.
    \Require Measurements $x_1,\ldots,x_n$
    \Ensure Total $s$
    \State $s \gets 0$ \Comment{Running total}
    \For{$i \gets 1$ \textbf{to} $n$}
      \State $s \gets s + x_i$
    \EndFor
    \State \Return $s$
  \end{algorithmic}
\end{algorithm}
```

Keywords and procedure names use navy; comments use teal and line numbers use
muted slate. Captions match the report's figure/table typography. Use
`\listofalgorithms` to generate an index. Algorithm floats stay on one page;
split a long algorithm into separate floats using `\algstore` and `\algrestore`
as described in the package manual. This option uses `algpseudocode` commands
such as `\State`, not the older `algorithmic` package's `\STATE` commands.
Do not also load `algorithmic` or `algorithm2e` with this option.

### Code listings

```tex
\begin{lstlisting}[language=Python,caption={Compute a total.},label={lst:total}]
def total(values):
    # Sum the measurements.
    return sum(values)
\end{lstlisting}
```

The `tempus` style provides a pale background, thin slate frame, navy keywords,
teal comments, burgundy strings, line numbers, and wrapped long lines. Code
uses a dedicated Latin Modern monospace face at `\footnotesize` (8 pt with
the default 10 pt body), preserving natural glyph widths and indentation. Listings
can break across pages unless you request a float. The class reserves the actual
caption height plus space for two initial code lines before display listings,
including external files; explicit user page breaks still take precedence.
Floating and bottom-caption listings retain their standard behavior.
No shell escape is required.
Select the language per listing; no language is assumed globally.

Use `\lstinputlisting[language=Python,caption={...},label={lst:source}]{file.py}`
for external files, `\lstinline[language=Python]|sum(values)|` for inline code,
and `\lstlistoflistings` for an index. Per-listing options override the defaults,
for example `numbers=none` or `basicstyle=\tempuscodefont\scriptsize`.
`\tempuscodefont` selects the class code font when `listings` is enabled.
Use `\lstset{...}` for document-wide changes, or `style=tempus` to reselect the
class style. `listings` does not handle arbitrary Unicode source automatically;
non-ASCII code needs an explicit character mapping or a suitable alternative.

### Continued content

Opt in to repeated box headings with `tempus continued`:

```tex
\begin{reportbox}[tempus continued]{Long explanation}
Content spanning several pages.
\end{reportbox}
```

For explicit source segments, give the first segment its numbered caption and
label, then continue immediately with the helper:

```tex
\lstinputlisting[firstline=1,lastline=20,caption={Training loop.},
  label={lst:training}]{training.py}
\reportcontinuedlisting[firstline=21,lastline=40]{lst:training}{training.py}
```

The continuation heading references the original listing number, resumes line
numbering (`firstnumber=last`), and adds no caption-list entry or label. Options
such as language, source ranges, and font remain available; identity-related
caption/title/label settings are reserved by the helper. Continue segments in
sequence, without an intervening unrelated listing. Automatic listing page
breaks retain the ordinary frame; repeated listing headings use explicit segments.

For split pseudocode, keep `\algstore`/`\algrestore` and replace the second
numbered caption with `\reportcontinuedalgorithmcaption{alg:original}` inside
its `algorithm` float. Label the first numbered caption. The second heading is
unnumbered and references that caption, so the logical algorithm has one number
and one index entry. See `examples/continuations.tex` for both workflows.

## Appendices

Use standard `\appendix` once, followed by ordinary sections:

```tex
\appendix
\section{Supplementary methods}
\label{app:methods}
\subsection{Derivation}
\begin{equation}
  a^2+b^2=c^2.
  \label{eq:appendix-example}
\end{equation}
\section{Additional results}
\label{app:results}
```

Headings display “Appendix A” and “Appendix B”; contents/bookmarks retain
alphabetic section numbers, and subsections use A.1, A.2, and so on.
Equations, figures, tables, algorithms, and listings restart within each
appendix section (A.1, then B.1 in the next appendix). Main-report object
numbering is unchanged. With `cleveref`, `\cref{app:methods}` says “appendix A”
and `\Cref{app:methods}` says “Appendix A”. Without it, ordinary `\ref` works.
Place the bibliography before `\appendix` when it belongs to the main report.
The comprehensive example includes two appendices and references to their objects.

## Customize

The first-page banner is enabled by default (or explicitly with `banner`).
Use the `nobanner` class option to hide the branding, report type and number,
version, partner logos, horizontal rule, and their spacing while keeping the
title and authors:

```tex
\documentclass[algorithms,listings,nobanner]{tempusreport}
```

This option only affects the first-page banner; running headers and footers
on subsequent pages retain their usual appearance.

Default branding is `\reportbrand{Tempus}{Reports}`, paired with a native
navy T mark and teal accent. `\reportlogomark` draws the mark in the current
class palette and can be reused in TikZ figures or scaled with `\scalebox`.
The default banner uses a 17 pt wordmark, tighter rule spacing, and a
21 pt title with 25 pt line spacing. Set optional metadata
with `\reporttype{...}`, `\reportlinks{...}`, and `\date{...}`; empty braces
hide unwanted fields. Use `\reportauthorlayout{wide}` for full-width authors.
`\reportauthorlayout` accepts `compact`/`wide`; `\reportabstractstyle` accepts
`flat`/`cuboid`. Unknown values warn and reset to compact/flat. Mascot widths
must be positive (otherwise 40 mm) and cannot exceed 45% of available line
width. Overlap must be nonnegative and cannot exceed the smaller of 12 mm or
half the rendered mascot height. Corrections warn; dimensions must use ordinary
valid TeX dimension syntax.

Separate authors with `\author{Alice\and Bob}`; both compact and wide
layouts render comma-separated names.

Optional artwork: `\reportlogo{path}`, `\reportmascot[40mm]{path}`, and
`\reportpartners{...}`. No artwork is needed by default. Artwork paths support `\graphicspath` and implicit graphics extensions.
Missing title artwork emits a class warning naming the file: a missing logo
falls back to native branding, a missing mascot and its space are omitted,
and missing partner artwork gets a bounded placeholder. `nobanner` skips checks
for logo/partner artwork it does not render; abstract mascots are still checked.
Existing `\reportimage` missing-image placeholders remain warning-free.

The class provides `reportbox`, `\reportimage{description}{path}` (with a
missing-image placeholder), `\reportcontents`, and table helpers
`\reporttoprule`, `\reporthighlight`, `\best`, and `\second`.
Override colors after the class declaration, for example:

```tex
\definecolor{TempusAccent}{HTML}{001F3F}
```

### Boxes and palette

Existing `\begin{reportbox}{Title}` usage still works. An optional argument
accepts standard `tcolorbox` keys and named Tempus styles:

```tex
\begin{reportbox}[tempus tip]{Practical tip}
Explain a useful next step.
\end{reportbox}

\begin{reportbox}[tempus warning,right=16pt]{Numerical caution}
Explain the limitation and its consequence.
\end{reportbox}
```

Styles are `tempus note` (navy, the default), `tempus tip` (teal),
`tempus warning` (amber), and `tempus important` (burgundy). Each uses a pale
surface and a matching left rule, and can break across pages. Include a
descriptive title so color is not the only way to distinguish the callout.
For custom environments, use `\newtcolorbox{mybox}[1]{tempus base,title={#1}}`.
The abstract retains its own style; the class does not change global
`tcolorbox` defaults.

| Color | Hex | Intended use |
| --- | --- | --- |
| `TempusInk` | `17212B` | Body text |
| `TempusAccent` | `1E3A5F` | Navy headings, links, keywords |
| `TempusMuted` | `596979` | Secondary text and line numbers |
| `TempusRule` | `CBD5E1` | Subtle borders |
| `TempusPaper`, `TempusLight` | `F0F4F8` | Neutral surfaces |
| `TempusSage` | `93A9BF` | Existing blue slate accent |
| `TempusSageDark` | `536D87` | Dark blue slate accent |
| `TempusTeal` / `TempusTealLight` | `27665E` / `EDF5F2` | Tips and comments |
| `TempusAmber` / `TempusAmberLight` | `885A20` / `FBF4E8` | Cautions |
| `TempusBurgundy` / `TempusBurgundyLight` | `8A4053` / `F8EFF2` | Important callouts and strings |
| `TempusCodeBackground` | `F5F7FA` | Code surfaces |

Use the named colors in figures and tables with `\textcolor`, `\rowcolor`,
or TikZ's `draw` and `fill` keys. Override individual colors with
`\definecolor` in the preamble to adapt the palette.

pdfLaTeX uses helvet; Tectonic, XeLaTeX, and LuaLaTeX use the
Helvetica-compatible TeX Gyre Heros fonts. No system font installation is needed.

## License

MIT licensed. Copyright (c) 2026 Pittawat Taveekitworachai.
Derived from the Lovart report template; the original contributors' copyright
notice is retained in `LICENSE`. Include `LICENSE` when redistributing.

The bundled, unmodified `acl_natbib.bst` comes from the official
[ACL style files](https://github.com/acl-org/acl-style-files), retrieved on
October 1, 2026. It is distributed under the LaTeX Project Public License,
as specified in its retained header, rather than the template's MIT license.
Preserve that header when redistributing the bibliography style.
