"""t01 - Repository A (tau-bench): how many tasks have a goal state reachable
without acting?

Q7 asks for which tasks the goal state is satisfiable by taking no action at all.
In repository A the reward is computed in tau_bench/envs/base.py:124-164 by
replaying the task's reference actions against a freshly loaded database and
comparing hashes:

    data_hash = self.get_data_hash()          # state the agent left
    ...
    for action in self.task.actions: self.step(action)
    gt_data_hash = self.get_data_hash()       # state the reference produces
    info = RewardActionInfo(r_actions=data_hash == gt_data_hash, ...)

So if a task's reference actions do not MUTATE the database, the goal hash
equals the untouched initial hash, and a trial that acted not at all matches it.
Whether a tool mutates is therefore the question this script answers.

METHOD, and why it is not a regex. A tool mutates iff its `invoke` writes
through a name that traces back to the `data` argument. `refunds.append(refund)`
in cancel_pending_order.py is a local list append and must NOT count;
`orders[order_id]["status"] = ...` must. The script walks the AST of each
invoke, tracks which local names are bound from `data`, and then looks for
writes through those names only: subscript/attribute assignment, augmented
assignment, `del`, and the mutating list/dict methods.

Static analysis, no execution: the benchmark is not run, no model is called.
Claims derived from it are graded [I] (inferred from traced control flow),
not [E], in TAU-ANSWERS.md.

Run:  python3 t01_inaction_tasks_A.py
"""

import ast
import os
import re
import sys

REPO = os.environ.get("TAU_A", "/Volumes/MULLETT_T7/tau-bench-audit/tau-bench")
MUTATING_METHODS = {"append", "extend", "insert", "pop", "remove", "clear",
                    "update", "setdefault", "popitem", "sort", "reverse"}


def root_name(node):
    """Walk Subscript/Attribute chains down to the base Name, if any."""
    while isinstance(node, (ast.Subscript, ast.Attribute)):
        node = node.value
    return node.id if isinstance(node, ast.Name) else None


def invoke_mutates(fn):
    """True if this `invoke` writes through anything bound from `data`."""
    tainted = {"data"}

    def names_in(node):
        return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}

    FRESH_CALLS = {"dict", "list", "set", "tuple", "sorted", "copy", "deepcopy",
                   "loads", "dumps", "str", "int", "float", "round", "len"}

    def is_fresh(node):
        """A newly constructed object. Writing through it cannot reach `data`.
        `result1 = {k: v for k, v in flight1.items()}` is fresh even though
        flight1 is tainted -- that is a copy, not an alias. But a SUBSCRIPT of a
        comprehension, `[i for i in order["items"]][0]`, is a reference INTO the
        data graph and is deliberately not treated as fresh."""
        if isinstance(node, (ast.Dict, ast.List, ast.Set, ast.DictComp,
                             ast.ListComp, ast.SetComp, ast.GeneratorExp,
                             ast.JoinedStr, ast.Constant)):
            return True
        if isinstance(node, ast.Call):
            f = node.func
            nm = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None)
            return nm in FRESH_CALLS
        return False

    # Propagate taint through: x = data[...]; a, b = data["p"], data["q"];
    # order = orders[id]; item = [i for i in order["items"] ...][0]
    # Any binding whose VALUE mentions a tainted name yields a tainted target.
    # Deliberately generous: over-tainting can only mark a read-only tool as
    # mutating, which UNDER-states the inaction count. Under-tainting would
    # overstate it, and this count is the one Q7 turns on.
    for _ in range(6):                      # fixpoint
        grew = False
        for node in ast.walk(fn):
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                val = node.value
                if val is None:
                    continue
                # elementwise for `a, b = x, y`
                if (len(targets) == 1 and isinstance(targets[0], (ast.Tuple, ast.List))
                        and isinstance(val, (ast.Tuple, ast.List))
                        and len(targets[0].elts) == len(val.elts)):
                    pairs = zip(targets[0].elts, val.elts)
                else:
                    pairs = [(t, val) for t in targets]
                for tgt, v in pairs:
                    if is_fresh(v):
                        continue
                    if names_in(v) & tainted:
                        for sub in ([tgt] if not isinstance(tgt, (ast.Tuple, ast.List))
                                    else list(tgt.elts)):
                            if isinstance(sub, ast.Name) and sub.id not in tainted:
                                tainted.add(sub.id)
                                grew = True
            # for-loop bindings: `for item in order["items"]:`
            if isinstance(node, (ast.For, ast.comprehension)):
                it = node.iter
                tgt = node.target
                if names_in(it) & tainted and isinstance(tgt, ast.Name):
                    if tgt.id not in tainted:
                        tainted.add(tgt.id)
                        grew = True
        if not grew:
            break

    for node in ast.walk(fn):
        # data["x"]["y"] = ...   /   alias[...] = ...
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, (ast.Subscript, ast.Attribute)) and root_name(tgt) in tainted:
                    return True
        if isinstance(node, ast.AugAssign):
            if root_name(node.target) in tainted:
                return True
        if isinstance(node, ast.Delete):
            for tgt in node.targets:
                if root_name(tgt) in tainted:
                    return True
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in MUTATING_METHODS and root_name(node.func.value) in tainted:
                return True
    return False


def classify_tools(domain):
    """tool name (as exposed to the agent) -> mutates?"""
    out = {}
    tdir = os.path.join(REPO, "tau_bench", "envs", domain, "tools")
    for fname in sorted(os.listdir(tdir)):
        if not fname.endswith(".py") or fname == "__init__.py":
            continue
        src = open(os.path.join(tdir, fname)).read()
        tree = ast.parse(src)
        # the agent-facing name is in get_info()'s returned dict
        m = re.search(r'"name":\s*"([a-z_]+)"', src)
        if not m:
            continue
        name = m.group(1)
        mutates = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "invoke":
                mutates = invoke_mutates(node)
        out[name] = mutates
    return out


def load_tasks(domain, split):
    """Parse the task list literally; no import, so no dependencies needed."""
    path = os.path.join(REPO, "tau_bench", "envs", domain, f"tasks_{split}.py")
    if not os.path.exists(path):
        return None
    tree = ast.parse(open(path).read())
    tasks = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "Task":
            kw = {k.arg: k.value for k in node.keywords}
            actions = []
            for a in getattr(kw.get("actions"), "elts", []):
                if isinstance(a, ast.Call) and getattr(a.func, "id", None) == "Action":
                    akw = {k.arg: k.value for k in a.keywords}
                    n = akw.get("name")
                    actions.append(n.value if isinstance(n, ast.Constant) else "?")
            outputs = [o.value for o in getattr(kw.get("outputs"), "elts", [])
                       if isinstance(o, ast.Constant)]
            tasks.append({"actions": actions, "outputs": outputs})
    return tasks


def main():
    print("Repository A - tau-bench @ 59a200c6d575d595120f1cb70fea53cef0632f6b\n")
    grand = {}
    for domain in ("retail", "airline"):
        tools = classify_tools(domain)
        writers = {t for t, m in tools.items() if m}
        readers = {t for t, m in tools.items() if not m}
        print(f"=== {domain} ===")
        print(f"  tools total {len(tools)}  |  mutating {len(writers)}  |  read-only {len(readers)}")
        print(f"  mutating : {sorted(writers)}")
        for split in ("test", "dev", "train"):
            tasks = load_tasks(domain, split)
            if tasks is None:
                continue
            n = len(tasks)
            no_write = [t for t in tasks if not any(a in writers for a in t["actions"])]
            no_write_no_out = [t for t in no_write if not t["outputs"]]
            zero_actions = [t for t in tasks if not t["actions"]]
            print(f"  -- split '{split}': {n} tasks")
            print(f"     no mutating action in reference          : {len(no_write):>4}"
                  f"   ({100.0*len(no_write)/n:.2f}%)")
            print(f"     ...AND no required outputs  -> INACTION   : {len(no_write_no_out):>4}"
                  f"   ({100.0*len(no_write_no_out)/n:.2f}%)")
            print(f"     zero reference actions at all             : {len(zero_actions):>4}")
            if split == "test":
                grand[domain] = (n, len(no_write_no_out))
                # Q11 cross-count: transfer_to_human_agents is a terminate tool
                # (envs/*/env.py:37,41), so calling it sets done and triggers
                # calculate_reward. On an inaction-satisfiable task that yields
                # reward 1.0. How many of those tasks EXPECT the transfer?
                expects = [t for t in no_write_no_out
                           if "transfer_to_human_agents" in t["actions"]]
                print(f"     ...of which reference expects a transfer  : {len(expects):>4}")
                print(f"     ...of which reference expects NO transfer : "
                      f"{len(no_write_no_out) - len(expects):>4}"
                      f"   <- immediate refusal scores 1.0 here")
        print()

    print("=== SUMMARY, test splits (the reported suites) ===")
    tot = sum(v[0] for v in grand.values())
    aff = sum(v[1] for v in grand.values())
    for d, (n, a) in grand.items():
        print(f"  {d:<8} {a:>4} / {n:<4}  ({100.0*a/n:.2f}%)")
    print(f"  {'BOTH':<8} {aff:>4} / {tot:<4}  ({100.0*aff/tot:.2f}%)")
    print("\n  Materiality reference: the frozen plan fixes 5% of tasks in the suite.")


if __name__ == "__main__":
    main()
