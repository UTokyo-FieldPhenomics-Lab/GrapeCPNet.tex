% An article class for author response to reviewer comment.
% Copyright (C) 2017 Martin Schroen
% Modifications Copyright (C) 2020 Kaishuo Zhang
%
% This program is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
%
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with this program.  If not, see <http://www.gnu.org/licenses/>.

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ar2rc}[2020/08/04 Author response to reviewer comment class]
\LoadClass{article}

\RequirePackage[includeheadfoot,top=20mm, bottom=20mm, footskip=2.5cm]{geometry}

% Typography
\RequirePackage[T1]{fontenc}
\RequirePackage{times}
%\RequirePackage{mathptmx} % math also in times font
\RequirePackage{amssymb,amsmath}
\RequirePackage{microtype}
\RequirePackage[utf8]{inputenc}
\RequirePackage{fancyhdr}
\RequirePackage{color}
% Misc
\RequirePackage{graphicx}
\RequirePackage{hyperref} 
\RequirePackage{soul} % Highlight using \hl{}

% Table
\RequirePackage{adjustbox} % center large tables across textwidth by surrounding tabular with \begin{adjustbox}{center}
\renewcommand{\arraystretch}{1.5} % enlarge spacing between rows
\RequirePackage{caption} 
\captionsetup[table]{skip=10pt} % enlarge spacing between caption and table

% Section styles
\RequirePackage{titlesec}
\titleformat{\section}{\normalfont\LARGE}{\makebox[0pt][r]{\bf \hspace{4mm}}}{0em}{\bfseries}
\titleformat{\subsection}{\normalfont}{\makebox[0pt][r]{\bf \hspace{4mm}}}{0em}{\bfseries}
\titlespacing{\subsection}{0em}{1em}{-0.3em} % left before after

% Paragraph styles
\setlength{\parskip}{0.6\baselineskip}%
\setlength{\parindent}{0pt}%

% Quotation styles
\RequirePackage{mdframed}
\renewmdenv[leftmargin=0.4em, rightmargin=0.4em%
innerleftmargin=0.6em,innerrightmargin=0.6em]{quote}

% Table styles
\let\oldtabular=\tabular
\let\endoldtabular=\endtabular
\renewenvironment{tabular}[1]{\begin{adjustbox}{center}\begin{oldtabular}{#1}}{\end{oldtabular}\end{adjustbox}}

% Reviewer comment counter
\RequirePackage{tcolorbox}
\newcounter{reviewercomment}
\setcounter{reviewercomment}{0}
% 定义审稿意见环境
\newenvironment{reviewercomment}[1][]{%
    \refstepcounter{reviewercomment}%
    \begin{tcolorbox}[
        title = {Comment \#\thereviewercomment},
        fonttitle = \bfseries,
        #1
    ]
}{%
    \end{tcolorbox}%
}
% 在每个 \section 后自动重置评论计数器
\let\oldsection\section
\renewcommand{\section}[1]{%
    \oldsection{#1}%
    \setcounter{reviewercomment}{0}%
}

% Shortcuts
%% Let textbf be both, bold and italic
%\DeclareTextFontCommand{\textbf}{\bfseries\em}

%% Add RC and AR to the left of a paragraph
%\def\RC{\makebox[0pt][r]{\bf RC:\hspace{4mm}}}
%\def\AR{\makebox[0pt][r]{AR:\hspace{4mm}}}

%% Define that \RC and \AR should start and format the whole paragraph 
\RequirePackage{suffix}
\long\def\RC#1\par{\makebox[0pt][r]{\bf RC:\hspace{4mm}}\textbf{\textit{#1}}\par} %\RC
\WithSuffix\long\def\RC*#1\par{\textbf{\textit{#1}}\par} %\RC*

\long\def\AR#1\par{\makebox[0pt][r]{AR:\hspace{10pt}}#1\par} %\AR
\WithSuffix\long\def\AR*#1\par{#1\par} %\AR*

\long\def\BT#1\par{\makebox[0pt][r]{\hspace{0pt}}{\textbf{#1}}\par} %\BT
\WithSuffix\long\def\BT*#1\par{#1\par} %\BT

\long\def\BL#1\par{\makebox[0pt][r]{\hspace{10pt}}{#1}\\[10pt]\hrule} %\BL
\WithSuffix\long\def\BL*#1\par{#1\par} %\BL

\RequirePackage{tcolorbox}

\long\def\response#1\par{\makebox[0pt][r]{\hspace{10pt}}{\large\textbf{Response: }\\[2pt]}{#1}\\[4pt]} %\response
\WithSuffix\long\def\response*#1\par{#1\par} %\response


\long\def\manuscript#1\par{\makebox[0pt][r]{\hspace{10pt}}\color[rgb]{0.5,0.5,0.5}{}\\[5pt]{{"$\cdots$ #1 $\cdots$"}}\\[12pt]\color{black}} %\manuscript
\WithSuffix\long\def\manuscript*#1\par{#1\par} %\manuscript

% \long\def\manuscript#1\par{\makebox[0pt][r]{\hspace{10pt}}\\[3pt]\large\color[rgb]{0,1,0}{"#1"}\\[3pt]} %\manuscript
% \WithSuffix\long\def\manuscript*#1\par{#1\par} %\manuscript

%%%
%DIF PREAMBLE EXTENSION ADDED BY LATEXDIFF
%DIF UNDERLINE PREAMBLE %DIF PREAMBLE
\RequirePackage[normalem]{ulem} %DIF PREAMBLE
\RequirePackage{xcolor}
\providecommand{\DIFadd}[1]{{\protect\color{blue}{#1}}} %DIF PREAMBLE
\providecommand{\DIFdel}[1]{{\protect\color{red}\sout{#1}}}                      %DIF PREAMBLE
%DIF SAFE PREAMBLE %DIF PREAMBLE
\providecommand{\DIFaddbegin}{} %DIF PREAMBLE
\providecommand{\DIFaddend}{} %DIF PREAMBLE
\providecommand{\DIFdelbegin}{} %DIF PREAMBLE
\providecommand{\DIFdelend}{} %DIF PREAMBLE
%DIF FLOATSAFE PREAMBLE %DIF PREAMBLE
\providecommand{\DIFaddFL}[1]{\DIFadd{#1}} %DIF PREAMBLE
\providecommand{\DIFdelFL}[1]{\DIFdel{#1}} %DIF PREAMBLE
\providecommand{\DIFaddbeginFL}{} %DIF PREAMBLE
\providecommand{\DIFaddendFL}{} %DIF PREAMBLE
\providecommand{\DIFdelbeginFL}{} %DIF PREAMBLE
\providecommand{\DIFdelendFL}{} %DIF PREAMBLE
%DIF END PREAMBLE EXTENSION ADDED BY LATEXDIFF

% Define title defaults if not defined by user
\let\@journal\@empty
\let\@doi\@empty
\let\@lettertitle\@empty
\let\@corresponding\@empty
\let\@email\@empty
\newcommand{\journal}[1]{\gdef\@journal{#1}}
\newcommand{\doi}[1]{\gdef\@doi{#1}}
\newcommand{\lettertitle}[1]{\gdef\@lettertitle{#1}}
\newcommand{\corresponding}[1]{\gdef\@corresponding{#1}}
\newcommand{\email}[1]{\gdef\@email{#1}}
\renewcommand\thefigure{R\arabic{figure}}
\renewcommand\thetable{R\arabic{table}}
% Make title and legend
\renewcommand\maketitle{
{\LARGE\bf\centering \@lettertitle}\\[1em]
{\@journal, }\\[0.7em]
{Manuscript ID: \@doi}\\[1.4em]
{\Large\bf \@title}\\[0.6em]
{\@author}\\[0.6em]
{\@corresponding}\\[0.6em]
{\@email}\\[1.6em]
% \hrule
% \hfill\small \textcolor[rgb]{0.357,0.608,0.835}{\(\quad\square\) Reviewers' Comment},\(\quad\square\) Authors' Response, \(\quad\square\) Manuscript Text \\[2em]
}