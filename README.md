# Tempus

A standalone A4 LaTeX report template with slate navy (`#1E3A5F`),
Helvetica-style headings, Libertine body text, and an editorial first page.

## Use

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

The example demonstrates an equation, decimal-aligned numeric table, placeholder
figure, a colored TikZ ML training diagram, themed callouts, pseudocode,
a Python listing, and citations.
Its measurements are illustrative. Replace the content
and image path with your own; a missing image produces a visible placeholder.

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

The starter's `fig:ml-training` is an editable supervised training diagram:
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
types. The starter enables both to demonstrate them. The `algorithms` option
loads `algorithm` for floats and `algpseudocode` (from `algorithmicx`) for
pseudocode. The `listings` option loads `listings` and selects the `tempus`
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
teal comments, burgundy strings, line numbers, and wrapped long lines. Listings
can break across pages unless you request a float. No shell escape is required.
Select the language per listing; no language is assumed globally.

Use `\lstinputlisting[language=Python,caption={...},label={lst:source}]{file.py}`
for external files, `\lstinline[language=Python]|sum(values)|` for inline code,
and `\lstlistoflistings` for an index. Per-listing options override the defaults,
for example `numbers=none` or `basicstyle=\ttfamily\footnotesize`.
Use `\lstset{...}` for document-wide changes, or `style=tempus` to reselect the
class style. `listings` does not handle arbitrary Unicode source automatically;
non-ASCII code needs an explicit character mapping or a suitable alternative.

## Customize

Default branding is `\reportbrand{Tempus}{Reports}`. Set optional metadata
with `\reporttype{...}`, `\reportlinks{...}`, and `\date{...}`; empty braces
hide unwanted fields. Use `\reportauthorlayout{wide}` for full-width authors.

Optional artwork: `\reportlogo{path}`, `\reportmascot[40mm]{path}`, and
`\reportpartners{...}`. No artwork is needed by default.

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
