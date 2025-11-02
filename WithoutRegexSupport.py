import re, os

# -------------------------
# Parsing (deterministic, unambiguous I/O)
# Input format: general text (part (i) will restrict to .SWE).
# On malformed input, overall program prints "NO".
def parse_string(s_in):
    raw = s_in.splitlines()
    lines = [ln.strip() for ln in raw if ln.strip() != ""]
    if not lines:
        return None, "empty"

    # First line: k (number of patterns)
    if not re.fullmatch(r"\d+", lines[0]):
        return None, "bad k"
    k = int(lines[0])

    # Second line: host string s over lowercase
    if len(lines) < 2:
        return None, "too short"
    s = lines[1]
    if not re.fullmatch(r"[a-z]*", s):
        return None, "bad s"

    # Next k lines: patterns t_i over [a-zA-Z]*
    if len(lines) < 2 + k:
        return None, "too short"
    ts = []
    for i in range(2, 2 + k):
        ti = lines[i]
        if not re.fullmatch(r"[a-zA-Z]*", ti):
            return None, "bad t"
        ts.append(ti)

    # Remaining lines: one domain per uppercase letter, e.g., "A: foo,bar"
    R = {}
    for ln in lines[2 + k:]:
        if ":" not in ln:
            return None, "bad rule"
        L, rhs = ln.split(":", 1)
        L = L.strip()
        rhs = rhs.strip()
        if not re.fullmatch(r"[A-Z]", L):
            return None, "bad Γ"
        if L in R:
            return None, "dup Γ"
        if rhs == "":
            return None, "empty domain"
        parts = [p.strip() for p in rhs.split(",")]
        if any(not re.fullmatch(r"[a-z]+", p) for p in parts):
            return None, "bad domain word"
        R[L] = parts

    # If any uppercase symbol appears in patterns but has no domain, treat as NO-instance.
    used = set("".join(re.findall(r"[A-Z]", "".join(ts))))
    if not used.issubset(R.keys()):
        # Mark with empty domains to force NO later in solve()
        return {"s": s, "ts": ts, "R": {}}, None

    return {"s": s, "ts": ts, "R": R}, None

# -------------------------
# Utility: expand a pattern t with a (possibly partial) assignment.
def expand_full(t, assign):
    out = []
    for ch in t:
        if ch.islower():
            out.append(ch)
        else:
            if ch not in assign:
                return None
            out.append(assign[ch])
    return "".join(out)

# -------------------------
# Lecture-only solver:
# - Quick necessary check for literal-only patterns.
# - Complete deterministic search over all assignments (exponential worst case).
def solve(instance):
    s, ts, R = instance["s"], instance["ts"], dict(instance["R"])

    # If no domains provided for used variables → NO
    if not R and any(any(c.isupper() for c in t) for t in ts):
        return None

    # Quick NO: any literal-only pattern must be a substring of s.
    for t in ts:
        if all(c.islower() for c in t):
            if t not in s:
                return None

    # Collect variables present in patterns; intersect with provided domains
    used = sorted(set(ch for t in ts for ch in t if ch.isupper()))
    for g in used:
        if g not in R or len(R[g]) == 0:
            return None

    # Exponential search over assignments
    def dfs(idx, assign):
        # If all variables assigned, verify every pattern
        if idx == len(used):
            for t in ts:
                w = expand_full(t, assign)
                if w is None:  # pattern still has unassigned var (shouldn't happen)
                    return False
                if w not in s:
                    return False
            return True

        g = used[idx]
        for v in R[g]:
            assign[g] = v
            if dfs(idx + 1, assign):
                return True
            assign.pop(g, None)
        return False

    # Find any satisfying assignment
    assign = {}
    ok = dfs(0, assign)
    if not ok:
        return None

    # Reconstruct a concrete witness deterministically (alphabetical variables, first winning value)
    # We can reuse the dfs logic to pick the first value that leads to success.
    witness = {}
    def reconstruct(idx, partial):
        if idx == len(used):
            return True
        g = used[idx]
        for v in R[g]:
            partial[g] = v
            # Check feasibility by completing deterministically
            if dfs(idx + 1, partial):
                witness[g] = v
                if reconstruct(idx + 1, partial):
                    return True
            partial.pop(g, None)
        return False

    reconstruct(0, {})
    # Return witness mapping (sorted by variable name)
    return {g: witness[g] for g in sorted(witness)}

# -------------------------
# Part (i) I/O: .SWE file restriction
# If malformed or NO-instance → print "NO".
# If YES-instance → print lines "Γ:word" in deterministic (alphabetical) order.
p = "test_cases/hard.swe"
if not os.path.exists(p):
    print("NO")
else:
    with open(p, "r", encoding="utf-8") as f:
        data = f.read()
    inst, err = parse_string(data)
    if err is not None:
        print("NO")
    else:
        sol = solve(inst)
        if sol is None:
            print("NO")
        else:
            for g in sorted(sol.keys()):
                print(f"{g}:{sol[g]}")
