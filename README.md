# DTU 02249 — Computationally Hard Problems
## Project: SuperStringWithExpansion (Fall 2025)

This README gives a practical, high-level overview of the assignment scope, required deliverables, grading, and suggested workflow. It complements (but does not replace) the official project statement.

---

## TL;DR (Scope at a Glance)

- You study the decision/optimization problem “SuperStringWithExpansion” (SWE).
- You analyze its complexity (NP, NP-complete via a reduction).
- You design and implement a correct algorithm (can be exponential worst-case), with heuristics to speed up typical cases.
- You read inputs from standard input in a custom .SWE format and print either NO or a valid expansion mapping (γi: ri lines).
- You submit:
  - report-group-XX.pdf (theory)
  - code-group-XX.zip (implementation)
  - readme-group-XX.txt (how to compile/run)

Group size: 3 students. Deadline: 03.11.2025, 21:00 UTC+1 (per assignment text; verify timezone).

---

## Problem Summary: SuperStringWithExpansion

- Alphabets:
  - Σ: lowercase letters (a–z) (base alphabet)
  - Γ: uppercase letters (subset of A–Z) (placeholder symbols γ1,…,γm)
- Input:
  - A string s ∈ Σ*
  - k strings t1,…,tk ∈ (Σ ∪ Γ)*
  - For each γj ∈ Γ, a finite set Rj ⊆ Σ* of candidate expansions
- Expansion:
  - Choose one word rj ∈ Rj for each γj
  - Replace every γj in each ti by rj to obtain e(ti) over Σ
- Decision question:
  - Is there a choice of r1,…,rm so that every e(ti) appears as a substring of s?
    - If yes, output YES (and in implementation: also output a concrete choice)
    - Else, output NO

---

## Input Format (.SWE) Summary

- Plain ASCII; allowed characters: digits 0–9, lowercase a–z, uppercase A–Z, colon “:”, comma “,”, and line feeds.
- Lines:
  1) An integer k
  2) The base string s (lowercase only)
  3..(2+k)) The k strings t1,…,tk (each over Σ ∪ Γ)
  - Final lines (≤ 26): one per γj present, formatted:
    - `ΓLetter:comma,separated,words` where words ∈ Σ*
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
- d) Black-box reduction: Given a decision oracle Ad for SWE, design Ao that returns the actual expansion (or NO). Prove correctness and polynomial overhead assuming unit cost for Ad calls.
- e) Prove SWE ∈ NP.
- f) Prove SWE is NP-complete. Reduce from ONE of the listed NP-complete problems.
- g) Design a correct algorithm (exponential worst-case allowed) for general SWE input. Include heuristics that speed up common/prunable cases. Prove correctness and give running-time bound (e.g., 2^{poly(n)}).
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
  - Only lines `Γ:ri` (Γ uppercase; ri ∈ Σ* chosen from RΓ)
  - No extra text, debug logs, or formatting.
- Performance:
  - Any exponential-time algorithm is allowed, but add heuristics and pruning to handle typical instances faster.

---

## Suggested Workflow

1) Understand the SWE decision problem thoroughly.
2) Theory first:
   - (e) Membership in NP: describe a polynomial-time verifier for a guessed mapping Γ→Σ*.
   - (f) NP-completeness: pick one reduction (e.g., 1-In-3-SAT, Graph-3-Coloring, LCS, etc.). Keep your reduction parsimonious and the encoding polynomial-size.
   - (d) Oracle-construction: use decision oracle Ad to pin down each γ’s choice by self-reduction or binary-search-like filtering over candidate sets Rj.
3) Algorithm design (g, h):
   - Baseline complete solver:
     - Systematic search over choices rj ∈ Rj (backtracking).
     - Check substring constraints efficiently (e.g., using KMP/automata, suffix automaton/array, Aho–Corasick for multiple patterns).
   - Heuristics:
     - Variable ordering: choose γ with smallest |Rj| or with the strongest constraints first.
     - Constraint propagation: eliminate candidate expansions that cannot appear in s, or that make some ti impossible.
     - Precomputation: for each candidate r, precompute where it occurs in s; precompute expansions of ti incrementally with early mismatch detection.
     - Early NO detection: if any ti contains a Γ whose RΓ is empty or whose candidates never appear in s, prune immediately.
     - Cache partial results: memoize failures for partial assignments.
   - Complexity analysis:
     - Worst-case exponential in m and sizes of Rj, but show polynomial factors for each check.
4) Implementation (i):
   - Parse .SWE robustly; validate character sets and structure.
   - Build fast substring-check helpers.
   - Implement backtracking with the heuristics you chose.
   - Respect IO spec strictly.
5) Testing:
   - Use provided test01.SWE–test06.SWE and additional corner cases:
     - k=0, minimal alphabets, missing Γ definitions, empty Rj, candidates not in Σ*, illegal characters, large s with small ti, etc.

---

## Hints and Design Notes

- Practical substring checking:
  - If you must check many expanded ti against s repeatedly, Aho–Corasick across Σ may help if you can batch a stable set of patterns. Otherwise, KMP per pattern is simple and fast.
- Backtracking order:
  - Sort Γ by increasing |Rj| or by “impact” (how often they appear across t1..tk).
- Early feasibility filtering:
  - If a candidate r does not appear in s at all and occurs alone in some ti, it’s impossible.
  - If a ti’s lowercase-only part already fails to be a substring of s, answer is NO.
- Oracle-to-optimizer (Part d):
  - Typical self-reduction: For each γj, try each r ∈ Rj, fix it, and ask Ad on the restricted instance. If YES, keep; else discard and try next. Polynomial total Ad calls.

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
  - A: No. Only lines `Γ:ri` per chosen expansion. Any deviation may fail tests.
- Q: What if a Γ letter appears in t but is not defined in the final lines?
  - A: That’s malformed; your program must output NO.
- Q: Are empty strings allowed in Rj?
  - A: The format says words over Σ*, finite size; clarify with staff if ε is intended. If you allow ε, ensure your parser/solver handles it consistently with substring definition.

Good luck!