# DTU 02249 — Computationally Hard Problems
## Project: SuperStringWithExpansion (Fall 2025)

This README gives a practical, high-level overview of the assignment scope, required deliverables, grading, and suggested workflow. It complements (but does not replace) the official project statement.

---

## TL;DR (Scope at a Glance)

- You study the decision/optimization problem “SuperStringWithExpansion” (SWE).
- You analyze its complexity (NP, NP-complete via a reduction).
- You design and implement a correct algorithm (can be exponential worst-case), with heuristics to speed up typical cases.
- You read inputs from standard input in a custom .SWE format and print either NO or a valid expansion mapping ($\gamma_i: r_i$ lines).
- You submit:
  - report-group-XX.pdf (theory)
  - code-group-XX.zip (implementation)
  - readme-group-XX.txt (how to compile/run)

Group size: 3 students. Deadline: 03.11.2025, 21:00 UTC+1 (per assignment text; verify timezone).

---

## Problem Summary (Plain Language)

- There are two kinds of letters:
  - Lowercase (a–z): real characters in the final text.
  - Uppercase (A–Z): placeholders that must be replaced by a lowercase word.

- You are given:
  - A long lowercase string $s$ (the “target text”).
  - $k$ pattern strings $t_1,\dots,t_k$ that can mix lowercase letters and uppercase placeholders.
  - For each uppercase letter (like A, B, …) a small list of allowed lowercase words it can stand for.

- Your task is to decide whether you can pick exactly one word for each uppercase letter (from its list) so that:
  - You use the same choice everywhere that letter appears.
  - After replacing the uppercase letters in every pattern $t_i$, the resulting fully-lowercase pattern appears somewhere inside $s$ as one continuous block (a substring).
  - This must be true for all patterns $t_1,\dots,t_k$ at the same time.

- If such a consistent set of choices exists, the answer is YES (and the program should output the chosen word for each uppercase letter). Otherwise, the answer is NO.

Example idea (not from the tests):
- Suppose $s = \text{"abracadabra"}$
- Patterns: $[\text{"Aba"}, \text{"cadA"}]$
- Allowed words: $A \in \{\text{"a"}, \text{"ra"}\}$
- If $A = \text{"a"}$, the expanded patterns are “aba” and “cada”. Both appear in “abracadabra”? “aba” does, “cada” doesn’t, so that choice fails.
- If $A = \text{"ra"}$, the expanded patterns are “raba” and “cadra”. If both show up as substrings, then the answer is YES with $A:\text{"ra"}$. If not, answer is NO.

---

## Input Format (.SWE) Summary

- Plain ASCII; allowed characters: digits 0–9, lowercase a–z, uppercase A–Z, colon “:”, comma “,”, and line feeds.
- Lines:
  1) An integer $k$
  2) The base string $s$ (lowercase only)
  3..$(2+k)$) The $k$ strings $t_1,\dots,t_k$ (each over $\Sigma \cup \Gamma$)
  - Final lines ($\le 26$): one per $\gamma_j$ present, formatted:
    - `ΓLetter:comma,separated,words` where words $\in \Sigma^*$
- Example (from assignment):
  ```
  4
  abdde
  ABD
  DDE
  AAB
  ABd
  A:a,b,c,d,e,f,dd
  B:a,b,c,d,e,f,dd
  C:a,b,c,d,e,f,dd
  D:a,b,c,d,e,f,dd
  E:aa,bd,c,d,e
  ```

Implementation must:
- Read from standard input (stdin) only.
- On malformed input: output NO.
- On YES-instances: print only lines `Γ:word` for each Γ used (example output format):
  ```
  A:a
  B:b
  C:c
  D:d
  E:e
  ```

---

## What You Must Deliver

1) Theory (report-group-XX.pdf)
- b) Decide YES/NO for the provided example test01.SWE and justify.
- c) Define the formal language of .SWE files (single-alphabet formalization) and how to solve its word problem (membership).
- d) Black-box reduction: Given a decision oracle $A_d$ for SWE, design $A_o$ that returns the actual expansion (or NO). Prove correctness and polynomial overhead assuming unit cost for $A_d$ calls.
- e) Prove SWE $\in \mathrm{NP}$.
- f) Prove SWE is NP-complete. Reduce from ONE of the listed NP-complete problems.
- g) Design a correct algorithm (exponential worst-case allowed) for general SWE input. Include heuristics that speed up common/prunable cases. Prove correctness and give running-time bound (e.g., $2^{p(n)}$).
- h) Analyze worst-case running time for your algorithm from (g), in terms of the size of the general input.
- State division of labor among group members.

2) Code (code-group-XX.zip)
- Your full implementation for (i) below; zip must contain the project root (no extra top-level directory).

3) Build/Run Instructions (readme-group-XX.txt)
- Exact compile/run steps, platform prerequisites, language version, and how to run via stdin/stdout.

---

## Grading Weights

- Theory b)–f): ~50%
- Algorithm design and analysis g), h): ~25%
- Implementation i): ~25%

Quality criteria include correctness, clarity, rigor, conformance to I/O specs and file naming, solving as many public/hidden tests as possible, and code quality.

---

## Implementation Requirements (Part i)

- Language: Java, C, C++, or Python (ask course staff for others).
- IO:
  - Read from stdin. Do not use file paths or interactive prompts.
  - Write to stdout only.
- Correctness:
  - Always terminate with NO or a valid expansion assignment.
  - On malformed input: output NO.
- Output on YES:
  - Only lines `Γ:r_i` ($\Gamma$ uppercase; $r_i \in \Sigma^*$ chosen from $R_\Gamma$)
  - No extra text, debug logs, or formatting.
- Performance:
  - Any exponential-time algorithm is allowed, but add heuristics and pruning to handle typical instances faster.

---

## Suggested Workflow

1) Understand the SWE decision problem thoroughly.
2) Theory first:
   - (e) Membership in NP: describe a polynomial-time verifier for a guessed mapping $\Gamma \to \Sigma^*$.
   - (f) NP-completeness: pick one reduction (e.g., 1-In-3-SAT, Graph-3-Coloring, LCS, etc.). Keep your reduction parsimonious and the encoding polynomial-size.
   - (d) Oracle-construction: use decision oracle $A_d$ to pin down each $\gamma$’s choice by self-reduction or filtering over candidate sets $R_j$.
3) Algorithm design (g, h):
   - Baseline complete solver:
     - Systematic search over choices $r_j \in R_j$ (backtracking).
     - Check substring constraints efficiently (e.g., using KMP/automata, suffix automaton/array, Aho–Corasick for multiple patterns).
   - Heuristics:
     - Variable ordering: choose $\gamma$ with smallest $|R_j|$ or with the strongest constraints first.
     - Constraint propagation: eliminate candidate expansions that cannot appear in $s$, or that make some $t_i$ impossible.
     - Precomputation: for each candidate $r$, precompute where it occurs in $s$; precompute expansions of $t_i$ incrementally with early mismatch detection.
     - Early NO detection: if any $t_i$ contains a $\Gamma$ whose $R_\Gamma$ is empty or whose candidates never appear in $s$, prune immediately.
     - Cache partial results: memoize failures for partial assignments.
   - Complexity analysis:
     - Worst-case exponential in $m$ and sizes of $R_j$, but show polynomial factors for each check.
4) Implementation (i):
   - Parse .SWE robustly; validate character sets and structure.
   - Build fast substring-check helpers.
   - Implement backtracking with the heuristics you chose.
   - Respect IO spec strictly.
5) Testing:
   - Use provided test01.SWE–test06.SWE and additional corner cases:
     - $k=0$, minimal alphabets, missing $\Gamma$ definitions, empty $R_j$, candidates not in $\Sigma^*$, illegal characters, large $s$ with small $t_i$, etc.

---

## Hints and Design Notes

- Practical substring checking:
  - If you must check many expanded $t_i$ against $s$ repeatedly, Aho–Corasick across $\Sigma$ may help if you can batch a stable set of patterns. Otherwise, KMP per pattern is simple and fast.
- Backtracking order:
  - Sort $\Gamma$ by increasing $|R_j|$ or by “impact” (how often they appear across $t_1..t_k$).
- Early feasibility filtering:
  - If a candidate $r$ does not appear in $s$ at all and occurs alone in some $t_i$, it’s impossible.
  - If a $t_i$’s lowercase-only part already fails to be a substring of $s$, answer is NO.
- Oracle-to-optimizer (Part d):
  - Typical self-reduction: For each $\gamma_j$, try each $r \in R_j$, fix it, and ask $A_d$ on the restricted instance. If YES, keep; else discard and try next. Polynomial total $A_d$ calls.

---

## Repository Structure (Suggested for your own development)

- src/ … your source files
- tests/ … sample .SWE files and your extra tests
- scripts/ … optional helper scripts
- README.md … this overview (not the required run-instructions file)
- .gitignore

Remember: Final submission requires exactly three files to DTU Learn:
- report-group-XX.pdf
- code-group-XX.zip (rooted at your project; do not include the report or run-instructions here)
- readme-group-XX.txt (build/run instructions)

---

## Division of Labor

State who did what in the report (theory sections, algorithm design, coding, testing). Clear ownership improves grading transparency.

---

## Checklist Before Submission

- [ ] Group of three is registered on DTU Learn.
- [ ] Report covers b)–h), includes proofs and division of labor.
- [ ] Reduction in (f) is correct, polynomial, and well-argued.
- [ ] Algorithm in (g) is complete, correct, and analyzed; heuristics explained.
- [ ] Implementation (i) reads stdin, writes stdout only; prints exactly required lines or NO.
- [ ] Malformed inputs → NO.
- [ ] Solves all provided tests or you attempted improvements.
- [ ] code-group-XX.zip has project root at top level.
- [ ] readme-group-XX.txt has exact compile and run commands for graders.

---

## FAQ

- Q: Can we print extra text on success?
  - A: No. Only lines `Γ:r_i` per chosen expansion. Any deviation may fail tests.
- Q: What if a $\Gamma$ letter appears in $t$ but is not defined in the final lines?
  - A: That’s malformed; your program must output NO.
- Q: Are empty strings allowed in $R_j$?
  - A: The format says words over $\Sigma^*$, finite size; clarify with staff if $\varepsilon$ is intended. If you allow $\varepsilon$, ensure your parser/solver handles it consistently with the substring definition.

Good luck!