import re, os
from collections import deque
from functools import lru_cache

def parse_string(s_in):
    raw = s_in.splitlines()
    lines = [ln.strip() for ln in raw if ln.strip() != ""]
    if not lines:
        return None, "empty"
    if not re.fullmatch(r"\d+", lines[0]):
        return None, "bad k"
    k = int(lines[0])
    if len(lines) < 2 + k:
        return None, "too short"
    s = lines[1]
    if not re.fullmatch(r"[a-z]*", s):
        return None, "bad s"
    ts = []
    for i in range(2, 2 + k):
        ti = lines[i]
        if not re.fullmatch(r"[a-zA-Z]*", ti):
            return None, "bad t"
        ts.append(ti)
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
    Gam_used = set("".join(re.findall(r"[A-Z]", "".join(ts))))
    if not Gam_used.issubset(R.keys()):
        return {"k": k, "s": s, "ts": ts, "R": {}}, None
    return {"k": k, "s": s, "ts": ts, "R": R}, None

def all_substring_lengths(s):
    n = len(s)
    Ls = set()
    for i in range(n):
        for j in range(i + 1, n + 1):
            Ls.add(j - i)
    return Ls

def t_length_range(t, R):
    mn = mx = 0
    for ch in t:
        if ch.islower():
            mn += 1; mx += 1
        else:
            lens = [len(w) for w in R[ch]]
            mn += min(lens); mx += max(lens)
    return mn, mx

def expand(t, assign):
    out = []
    for ch in t:
        if ch.islower():
            out.append(ch)
        else:
            if ch not in assign:
                return None
            out.append(assign[ch])
    return "".join(out)

def prune_domains_by_presence(R, s):
    R2 = {}
    for g, dom in R.items():
        keep = [w for w in dom if w in s]
        if not keep:
            return None
        keep.sort(key=len)
        R2[g] = keep
    return R2

@lru_cache(maxsize=100_000)
def build_regex_cached(t, assign_items, dom_key_tuple):
    assign = dict(assign_items)
    dom_map = dict(dom_key_tuple)
    parts = []
    for ch in t:
        if ch.islower():
            parts.append(ch)
        else:
            if ch in assign:
                parts.append(re.escape(assign[ch]))
            else:
                dom = dom_map.get(ch, ())
                if not dom:
                    return None
                alts = "|".join(re.escape(w) for w in dom)
                parts.append(f"(?:{alts})")
    try:
        return re.compile("".join(parts))
    except re.error:
        return None

def regex_feasible(s, t, assign, R):
    if all(c.islower() or (c in assign) for c in t):
        w = expand(t, assign)
        return (w is not None) and (w in s)
    used = sorted({c for c in t if c.isupper()})
    dom_key_tuple = tuple((g, tuple(R[g])) for g in used)
    assign_items = tuple(sorted(assign.items()))
    reg = build_regex_cached(t, assign_items, dom_key_tuple)
    if reg is None:
        return False
    return reg.search(s) is not None

def neighbors_in_t(t):
    return [c for c in t if c.isupper()]

def AC3_regex(s, ts, R):
    scopes = []
    for idx, t in enumerate(ts):
        vs = neighbors_in_t(t)
        if vs:
            scopes.append((idx, t, tuple(sorted(set(vs)))))
    from collections import deque
    Q = deque()
    for _, t, scope in scopes:
        for g in scope:
            Q.append((t, g))
    while Q:
        t, g = Q.popleft()
        dom = R[g]
        new_dom = []
        for v in dom:
            if regex_feasible(s, t, {g: v}, R):
                new_dom.append(v)
        if not new_dom:
            return None
        if len(new_dom) != len(dom):
            R[g] = new_dom
            for _, t2, scope2 in scopes:
                if g in scope2:
                    for g2 in scope2:
                        if g2 != g:
                            Q.append((t2, g2))
    return R

def solve(instance):
    s, ts, R = instance["s"], instance["ts"], dict(instance["R"])
    if not R:
        return None
    for t in ts:
        if all(c.islower() for c in t) and (t not in s):
            return None
    R = prune_domains_by_presence(R, s)
    if R is None:
        return None
    Ls = all_substring_lengths(s)
    for t in ts:
        mn, mx = t_length_range(t, R)
        if not any(L in Ls for L in range(mn, mx + 1)):
            return None
    R = AC3_regex(s, ts, R)
    if R is None:
        return None
    Gam = sorted(R.keys())
    freq = {g: sum(g in t for t in ts) for g in Gam}
    order = sorted(Gam, key=lambda g: (len(R[g]), -freq[g]))

    @lru_cache(maxsize=200_000)
    def dfs(idx, packed_assign):
        assign = dict(packed_assign)
        for t in ts:
            if not regex_feasible(s, t, assign, R):
                return False
        if idx == len(order):
            return True
        g = order[idx]
        for v in R[g]:
            assign[g] = v
            pa = tuple(sorted(assign.items()))
            if dfs(idx + 1, pa):
                return True
            assign.pop(g, None)
        return False

    ok = dfs(0, tuple())
    if not ok:
        return None
    assign = {}
    for i, g in enumerate(order):
        for v in R[g]:
            assign[g] = v
            pa = tuple(sorted(assign.items()))
            if dfs(i + 1, pa):
                break
        else:
            return None
    return {g: assign[g] for g in sorted(assign)}

# Change the swe file
p = "test_cases/test07.swe"
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
            for g, w in sol.items():
                print(f"{g}:{w}")