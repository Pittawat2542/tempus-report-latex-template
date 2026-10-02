% Derived from the Lovart report template.
% Copyright (c) 2026 Pittawat Taveekitworachai.
% Copyright (c) 2026 Lovart report template contributors.
% Distributed under the MIT license; see LICENSE.
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{tempusreport}[2026/10/02 v1.4.0 Tempus Reports]
\newif\iftempus@algorithms
\newif\iftempus@listings
\newif\iftempus@banner
\tempus@bannertrue
\DeclareOption{algorithms}{\tempus@algorithmstrue}
\DeclareOption{listings}{\tempus@listingstrue}
\DeclareOption{banner}{\tempus@bannertrue}
\DeclareOption{nobanner}{\tempus@bannerfalse}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass[10pt,a4paper]{article}
% Keep consumed feature options out of downstream packages (tcolorbox also
% recognizes a global listings option, which would load extra libraries).
\edef\tempus@filteroptions{%
  \noexpand\@removeelement{algorithms}{\@classoptionslist}\noexpand\@classoptionslist}
\tempus@filteroptions
\edef\tempus@filteroptions{%
  \noexpand\@removeelement{listings}{\@classoptionslist}\noexpand\@classoptionslist}
\tempus@filteroptions
\RequirePackage[T1]{fontenc}
\RequirePackage{libertine}
\RequirePackage{iftex}
\ifPDFTeX
  \RequirePackage[scaled=0.94]{helvet}
\else
  % Helvetica-compatible OpenType fonts for XeTeX/Tectonic and LuaTeX.
  \setsansfont{texgyreheros}[Extension=.otf,Scale=0.94,
    UprightFont=*-regular,BoldFont=*-bold,
    ItalicFont=*-italic,BoldItalicFont=*-bolditalic]
\fi
\RequirePackage[margin=21mm,top=20mm,bottom=22mm,headheight=19pt,
  headsep=11pt,footskip=24pt]{geometry}
\RequirePackage[table]{xcolor}
\definecolor{TempusInk}{HTML}{17212B}
\definecolor{TempusPaper}{HTML}{F0F4F8}
\definecolor{TempusAccent}{HTML}{1E3A5F}
\definecolor{TempusLight}{HTML}{F0F4F8}
\definecolor{TempusMuted}{HTML}{596979}
\definecolor{TempusRule}{HTML}{CBD5E1}
\definecolor{TempusSage}{HTML}{93A9BF}
\definecolor{TempusSageDark}{HTML}{536D87}
% Supporting hues: dark enough for text on the corresponding pale surfaces.
\definecolor{TempusTeal}{HTML}{27665E}
\definecolor{TempusTealLight}{HTML}{EDF5F2}
\definecolor{TempusAmber}{HTML}{885A20}
\definecolor{TempusAmberLight}{HTML}{FBF4E8}
\definecolor{TempusBurgundy}{HTML}{8A4053}
\definecolor{TempusBurgundyLight}{HTML}{F8EFF2}
\definecolor{TempusCodeBackground}{HTML}{F5F7FA}
\RequirePackage{graphicx}
\RequirePackage{amsmath,amssymb}
\RequirePackage{booktabs,tabularx,array}
\RequirePackage{enumitem}
\RequirePackage{microtype}
\RequirePackage{fancyhdr}
\RequirePackage{caption,subcaption}
\RequirePackage{tikz}
\usetikzlibrary{arrows.meta,positioning,calc}
\RequirePackage{tcolorbox}
\tcbuselibrary{breakable,skins}
% Optional content packages are loaded before hyperref and user-side cleveref.
\iftempus@algorithms
  \RequirePackage{algorithm}
  \RequirePackage{algpseudocode}
\fi
\iftempus@listings
  \RequirePackage{listings}
  % Keep code font selection local; do not replace the report's body fonts.
  \ifPDFTeX
    \newcommand{\tempuscodefont}{\fontfamily{lmtt}\selectfont}
  \else
    \newfontfamily\tempuscodefont{lmmonolt10}[Extension=.otf,
      UprightFont=*-regular,BoldFont=*-bold,
      ItalicFont=*-oblique,BoldItalicFont=*-boldoblique]
  \fi
\fi
\RequirePackage[authoryear,round]{natbib}
\RequirePackage{xurl}
\RequirePackage[pdfusetitle]{hyperref}
\RequirePackage{bookmark}
\hypersetup{colorlinks=true,linkcolor=TempusAccent,citecolor=TempusAccent,
  urlcolor=TempusAccent,bookmarksnumbered=true,pdfborder={0 0 0}}
\urlstyle{same}
\AtBeginDocument{\color{TempusInk}}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt plus 1pt minus 1pt}
\linespread{1.08}
\setlength{\emergencystretch}{1.5em}
\clubpenalty=8000
\widowpenalty=8000
\displaywidowpenalty=8000
\newcommand{\tempus@sectionprefix}{}
\renewcommand\@seccntformat[1]{%
  \textcolor{TempusAccent}{%
    \ifcsname tempus@#1prefix\endcsname
      \csname tempus@#1prefix\endcsname
    \fi
    \csname the#1\endcsname}\quad}
% Preserve article's alphabetic section reset, then scope object numbers.
\AddToHook{cmd/appendix/after}{%
  \renewcommand{\tempus@sectionprefix}{\appendixname\space}
  \counterwithin{equation}{section}%
  \counterwithin{figure}{section}%
  \counterwithin{table}{section}%
  \iftempus@algorithms\counterwithin{algorithm}{section}\fi
  \iftempus@listings\counterwithin{lstlisting}{section}\fi
  \@ifpackageloaded{cleveref}{%
    \crefalias{section}{appendix}%
    \crefname{appendix}{appendix}{appendices}%
    \Crefname{appendix}{Appendix}{Appendices}%
  }{}%
}
\renewcommand\section{\@startsection{section}{1}{\z@}
  {-2.6ex \@plus -.7ex \@minus -.2ex}{1ex \@plus .2ex}
  {\normalfont\sffamily\large\bfseries\color{TempusInk}}}
\renewcommand\subsection{\@startsection{subsection}{2}{\z@}
  {-2.1ex \@plus -.5ex \@minus -.2ex}{.7ex \@plus .2ex}
  {\normalfont\sffamily\normalsize\bfseries\color{TempusInk}}}
\renewcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}
  {-1.8ex \@plus -.4ex \@minus -.2ex}{.6ex \@plus .2ex}
  {\normalfont\sffamily\small\bfseries\color{TempusInk}}}
\renewcommand\paragraph{\@startsection{paragraph}{4}{\z@}
  {1.2ex \@plus .3ex \@minus .2ex}{-.7em}
  {\normalfont\sffamily\small\bfseries}}
\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{2}
\setlist[itemize]{leftmargin=1.5em,itemsep=3pt,topsep=4pt,parsep=0pt}
\setlist[enumerate]{leftmargin=1.8em,itemsep=3pt,topsep=4pt,parsep=0pt}
\newcommand{\reportbrand}[2]{\gdef\tempus@lab{#1}\gdef\tempus@group{#2}}
\newcommand{\reporttype}[1]{\gdef\tempus@type{#1}}
\newcommand{\reportnumber}[1]{\gdef\tempus@number{#1}}
\newcommand{\reportversion}[1]{\gdef\tempus@version{#1}}
\newcommand{\reportshorttitle}[1]{\gdef\tempus@shorttitle{#1}}
\newcommand{\reportauthornote}[1]{\gdef\tempus@authornote{#1}}
\newcommand{\reportauthorlayout}[1]{\gdef\tempus@authorlayout{#1}}
\def\tempus@wideauthorlayout{wide}
\newcommand{\reportlinks}[1]{\gdef\tempus@links{#1}}
\newcommand{\reportlogo}[1]{\gdef\tempus@logo{#1}}
\newcommand{\reportmascot}[2][40mm]{\gdef\tempus@mascotwidth{#1}\gdef\tempus@mascot{#2}}
\newcommand{\reportmascotoverlap}[1]{\gdef\tempus@mascotoverlap{#1}}
\newcommand{\reportabstractstyle}[1]{\gdef\tempus@abstractstyle{#1}}
\def\tempus@cuboidstyle{cuboid}
\def\tempus@cubedepth{8mm}
\def\tempus@cubeside{4mm}
\newlength{\tempus@mascotheight}
\newcommand{\reportpartners}[1]{\gdef\tempus@partners{#1}}
\newcommand{\partnerwordmark}[3][]{%
  \begin{minipage}[c]{#2}\centering
    \includegraphics[#1,width=\linewidth,height=20pt,keepaspectratio]{#3}%
  \end{minipage}%
}
\newcommand{\partnerinstitution}[3][46mm]{%
  \begin{minipage}[c]{#1}\setlength{\parskip}{0pt}%
    \if\relax\detokenize{#3}\relax
      \includegraphics[width=\linewidth,height=20pt,keepaspectratio]{#2}%
    \else
      \begin{minipage}[c]{20pt}\centering
        \if\relax\detokenize{#2}\relax
          \begin{tikzpicture}
            \draw[TempusRule,line width=.5pt] (0,0) circle[radius=9pt];
            \node[text=TempusMuted,font=\sffamily\fontsize{5}{6}\selectfont] at (0,0) {LOGO};
          \end{tikzpicture}%
        \else
          \includegraphics[width=20pt,height=20pt,keepaspectratio]{#2}%
        \fi
      \end{minipage}\hspace{5pt}%
      \begin{minipage}[c]{\dimexpr\linewidth-25pt\relax}
        \raggedright\sffamily\fontsize{8}{9.5}\selectfont\color{TempusInk}#3
      \end{minipage}%
    \fi
  \end{minipage}%
}
\reportbrand{Tempus}{Reports}
\reporttype{TECHNICAL REPORT}
\reportnumber{01}
\reportversion{v1.0}
\reportshorttitle{Technical Report}
\reportauthornote{}
\reportauthorlayout{compact}
\reportlinks{}
\reportlogo{}
\reportmascot{}
\reportmascotoverlap{8mm}
\reportabstractstyle{flat}
\reportpartners{}
\author{}
\date{\today}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[R]{\sffamily\fontsize{7}{9}\selectfont\color{TempusMuted}\tempus@shorttitle}
\fancyfoot[R]{\sffamily\fontsize{8}{10}\selectfont\color{TempusInk}%
  \textcolor{TempusAccent}{\rule{10pt}{1.4pt}}\hspace{8pt}\thepage}
\renewcommand{\headrulewidth}{.25pt}
\renewcommand{\footrulewidth}{0pt}
\renewcommand{\headrule}{\hbox to\headwidth{\color{TempusRule}\leaders\hrule height \headrulewidth\hfill}}
\fancypagestyle{opening}{\fancyhead{}\renewcommand{\headrulewidth}{0pt}}
\captionsetup{font=small,labelfont={sf,bf},labelsep=period,
  justification=justified,singlelinecheck=false,skip=7pt}
\captionsetup[table]{position=top}
\iftempus@algorithms
  \captionsetup[algorithm]{font=small,labelfont={sf,bf,color=TempusAccent},
    labelsep=period,skip=7pt}
  \algrenewcommand\algorithmicrequire{\textcolor{TempusAccent}{\textsf{\textbf{Input:}}}}
  \algrenewcommand\algorithmicensure{\textcolor{TempusAccent}{\textsf{\textbf{Output:}}}}
  \algrenewcommand\alglinenumber[1]{\sffamily\scriptsize\color{TempusMuted}#1}
  \algrenewcommand\algorithmiccomment[1]{\hfill\textcolor{TempusTeal}{\(\triangleright\)\ #1}}
  \algrenewcommand\textproc[1]{\textsf{\textcolor{TempusAccent}{#1}}}
  \newcommand{\tempus@algorithmkeyword}[1]{\textcolor{TempusAccent}{\textsf{\textbf{#1}}}}
  \algrenewcommand\algorithmicif{\tempus@algorithmkeyword{if}}
  \algrenewcommand\algorithmicthen{\tempus@algorithmkeyword{then}}
  \algrenewcommand\algorithmicelse{\tempus@algorithmkeyword{else}}
  \algrenewcommand\algorithmicfor{\tempus@algorithmkeyword{for}}
  \algrenewcommand\algorithmicforall{\tempus@algorithmkeyword{for all}}
  \algrenewcommand\algorithmicdo{\tempus@algorithmkeyword{do}}
  \algrenewcommand\algorithmicwhile{\tempus@algorithmkeyword{while}}
  \algrenewcommand\algorithmicrepeat{\tempus@algorithmkeyword{repeat}}
  \algrenewcommand\algorithmicuntil{\tempus@algorithmkeyword{until}}
  \algrenewcommand\algorithmicloop{\tempus@algorithmkeyword{loop}}
  \algrenewcommand\algorithmicend{\tempus@algorithmkeyword{end}}
  \algrenewcommand\algorithmicreturn{\tempus@algorithmkeyword{return}}
  \algrenewcommand\algorithmicfunction{\tempus@algorithmkeyword{function}}
  \algrenewcommand\algorithmicprocedure{\tempus@algorithmkeyword{procedure}}
  \AddToHook{env/algorithmic/begin}{\small}
\fi
\iftempus@listings
  \lstdefinestyle{tempus}{
    basicstyle=\tempuscodefont\footnotesize\color{TempusInk},
    keywordstyle=\color{TempusAccent}\bfseries,
    commentstyle=\color{TempusTeal}\itshape,
    stringstyle=\color{TempusBurgundy},
    backgroundcolor=\color{TempusCodeBackground},
    rulecolor=\color{TempusRule},frame=single,framerule=.4pt,
    framesep=6pt,xleftmargin=7pt,xrightmargin=7pt,
    numbers=left,numberstyle=\sffamily\scriptsize\color{TempusMuted},
    numbersep=10pt,stepnumber=1,
    breaklines=true,breakatwhitespace=false,breakindent=1.5em,
    columns=fullflexible,keepspaces=true,tabsize=4,
    showstringspaces=false,showspaces=false,showtabs=false,
    upquote=true,captionpos=t,aboveskip=10pt,belowskip=10pt
  }
  \lstset{style=tempus}
  \captionsetup[lstlisting]{font=small,labelfont={sf,bf,color=TempusAccent},
    labelsep=period,skip=7pt}
\fi
\setlength{\textfloatsep}{13pt plus 2pt minus 2pt}
\setlength{\floatsep}{10pt plus 2pt minus 2pt}
\setlength{\intextsep}{10pt plus 2pt minus 2pt}
\renewcommand{\topfraction}{.95}
\renewcommand{\bottomfraction}{.85}
\renewcommand{\textfraction}{.08}
\renewcommand{\floatpagefraction}{.80}
\setlength{\bibsep}{4pt}
\renewcommand{\bibfont}{\small}
\newcommand{\tempus@authornames}{%
  \ifx\@author\@empty\else
    % article's \and opens tabular blocks; our author layout is paragraph-based.
    {\def\and{\unskip,\space\ignorespaces}%
      \normalfont\sffamily\normalsize\bfseries\color{TempusInk}\@author\par}
  \fi
}
\newcommand{\tempus@authorblock}{%
  \ifx\tempus@authorlayout\tempus@wideauthorlayout\else
    \tempus@authornames
  \fi
  \ifx\tempus@authornote\@empty\else
    \vspace{2pt}{\sffamily\small\color{TempusMuted}\tempus@authornote\par}
  \fi
  \vspace{7pt}
  {\sffamily\fontsize{8}{11}\selectfont\color{TempusMuted}\@date
    \ifx\tempus@links\@empty\else
      \ifx\@date\@empty\else\quad\textbar\quad\fi\tempus@links\fi\par}
}
\renewcommand{\maketitle}{%
  \thispagestyle{opening}
  \begingroup
  \setlength{\parskip}{0pt}
  \iftempus@banner
  \noindent\begin{minipage}[t]{.47\linewidth}
    \ifx\tempus@logo\@empty
      {\sffamily\bfseries\fontsize{20}{24}\selectfont\color{TempusAccent}\tempus@lab\par}%
    \else
      \includegraphics[height=22pt]{\tempus@logo}\par
    \fi
    \ifx\tempus@group\@empty\else
      \vspace{3pt}{\sffamily\fontsize{8}{10}\selectfont\color{TempusMuted}%
        \MakeUppercase{\tempus@group}\par}%
    \fi
  \end{minipage}\hfill
  \begin{minipage}[t]{.48\linewidth}\raggedleft
    {\sffamily\fontsize{8}{11}\selectfont\color{TempusAccent}\tempus@type\par}
    {\sffamily\fontsize{8}{11}\selectfont\color{TempusMuted}%
      \ifx\tempus@number\@empty\else No.\ \tempus@number\fi
      \ifx\tempus@version\@empty\else
        \ifx\tempus@number\@empty\else\quad/\quad\fi\tempus@version
      \fi\par}
  \end{minipage}\par
  \ifx\tempus@partners\@empty\else
    \vspace{12pt}\noindent\tempus@partners\par
  \fi
  \vspace{14pt}
  {\color{TempusAccent}\hrule height 1.2pt}
  \vspace{20pt}
  \fi
  {\raggedright\sffamily\bfseries\color{TempusInk}\fontsize{24}{28}\selectfont\@title\par}
  \vspace{12pt}
  \ifx\tempus@authorlayout\tempus@wideauthorlayout
    \tempus@authornames
    \vspace{4pt}
  \fi
  \ifx\tempus@mascot\@empty
    \tempus@authorblock
    \vspace{10pt}
    \ifx\tempus@abstractstyle\tempus@cuboidstyle
      \vspace{\tempus@cubedepth}
    \fi
  \else
    \settoheight{\tempus@mascotheight}{\includegraphics[width=\tempus@mascotwidth]{\tempus@mascot}}%
    \noindent\begin{minipage}[b]{\dimexpr\linewidth-\tempus@mascotwidth-12pt\relax}
      \tempus@authorblock
      \vspace{7pt}
    \end{minipage}\hfill
    \begin{minipage}[b]{\tempus@mascotwidth}
      \ifx\tempus@abstractstyle\tempus@cuboidstyle
        \rule{0pt}{\dimexpr\tempus@mascotheight-\tempus@cubedepth\relax}%
      \else
        \rule{0pt}{\dimexpr\tempus@mascotheight-\tempus@mascotoverlap\relax}%
      \fi
    \end{minipage}\par
    \ifx\tempus@abstractstyle\tempus@cuboidstyle
      \vspace{\tempus@cubedepth}
    \else
      \vspace{1pt}
    \fi
  \fi
  \endgroup
}
\newcommand{\tempus@abstractart}{%
  \ifx\tempus@abstractstyle\tempus@cuboidstyle
    \path[fill=TempusRule!60!TempusPaper,draw=TempusRule,line width=.4pt]
      (frame.south east) --
      ([xshift=\tempus@cubeside,yshift=\tempus@cubedepth]frame.south east) --
      ([xshift=\tempus@cubeside,yshift=\tempus@cubedepth]frame.north east) --
      (frame.north east) -- cycle;
    \path[fill=TempusLight,draw=TempusRule,line width=.4pt]
      (frame.north west) --
      ([xshift=\tempus@cubeside,yshift=\tempus@cubedepth]frame.north west) --
      ([xshift=\tempus@cubeside,yshift=\tempus@cubedepth]frame.north east) --
      (frame.north east) -- cycle;
    \draw[TempusRule,line width=.4pt]
      (frame.south west) -- (frame.south east);
    \ifx\tempus@mascot\@empty\else
      \node[anchor=south east,inner sep=0pt,outer sep=0pt]
        at (frame.north east)
        {\includegraphics[width=\tempus@mascotwidth]{\tempus@mascot}};
    \fi
  \else\ifx\tempus@mascot\@empty\else
    \draw[TempusRule,line width=.35pt]
      (frame.north west) -- (frame.north east);
    \begin{scope}[blend mode=darken]
      \node[anchor=south east,inner sep=0pt,outer sep=0pt]
        at ([xshift=1.5mm,yshift=-\tempus@mascotoverlap]frame.north east)
        {\includegraphics[width=\tempus@mascotwidth]{\tempus@mascot}};
    \end{scope}%
  \fi\fi
}
\newtcolorbox{tempusabstractbox}{enhanced,breakable,
  colback=TempusPaper,frame hidden,boxrule=0pt,arc=0pt,
  borderline west={1.5pt}{0pt}{TempusAccent},
  left=14pt,right=14pt,top=11pt,bottom=11pt,
  overlay unbroken={\tempus@abstractart},
  overlay first={\tempus@abstractart},
  before skip=0pt,after skip=12pt}
\renewenvironment{abstract}{%
  \begin{tempusabstractbox}
  {\sffamily\bfseries\fontsize{8}{10}\selectfont\MakeUppercase{\abstractname}\par}
  \vspace{3pt}\normalfont\normalsize
}{\par\end{tempusabstractbox}}
% Named styles can also be used directly in a tcolorbox. No global tcb defaults.
\tcbset{
  tempus base/.style={enhanced,breakable,frame hidden,boxrule=0pt,arc=0pt,
    colback=TempusLight,coltext=TempusInk,
    left=12pt,right=12pt,top=9pt,bottom=9pt,
    before skip=10pt,after skip=10pt,
    fonttitle=\sffamily\small\bfseries,coltitle=TempusAccent,
    attach title to upper={\par\smallskip},
    borderline west={1.5pt}{0pt}{TempusAccent}},
  tempus note/.style={colback=TempusLight,coltitle=TempusAccent,
    borderline west={1.5pt}{0pt}{TempusAccent}},
  tempus tip/.style={colback=TempusTealLight,coltitle=TempusTeal,
    borderline west={1.5pt}{0pt}{TempusTeal}},
  tempus warning/.style={colback=TempusAmberLight,coltitle=TempusAmber,
    borderline west={1.5pt}{0pt}{TempusAmber}},
  tempus important/.style={colback=TempusBurgundyLight,coltitle=TempusBurgundy,
    borderline west={1.5pt}{0pt}{TempusBurgundy}}
}
\newtcolorbox{reportbox}[2][]{tempus base,title={#2},#1}
\newcommand{\best}[1]{\textbf{#1}}
\newcommand{\second}[1]{\underline{#1}}
\newcommand{\placeholder}[1]{\textcolor{TempusMuted}{\textit{[#1]}}}
\newcommand{\reportimage}[2]{%
  \IfFileExists{#2}{%
    \includegraphics[width=\linewidth,height=.66\linewidth,keepaspectratio]{#2}%
  }{%
    \begin{tikzpicture}
      \path[fill=TempusLight] (0,0) rectangle (\linewidth,.66\linewidth);
      \node[align=center,text width=.85\linewidth,text=TempusMuted,font=\sffamily\small]
        at (.5\linewidth,.33\linewidth) {#1\\[4pt]{\scriptsize Image placeholder}};
    \end{tikzpicture}%
  }%
}
\newcommand{\reportcontents}{\tableofcontents\clearpage}
% Table helpers are part of the standalone class.
\arrayrulecolor{TempusRule}
\newcommand{\reporttoprule}{%
  \arrayrulecolor{TempusAccent}\toprule
  \arrayrulecolor{TempusRule}\rowcolor{TempusLight}}
\newcommand{\reporthighlight}{\rowcolor{TempusAccent!8}}
\endinput
