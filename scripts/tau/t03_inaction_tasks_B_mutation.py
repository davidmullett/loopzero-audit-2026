"""t03 - Repository B (tau2-bench v1.0.1): the mutation analysis Q7 left open.

Completes for B what t01 established for A: how many tasks have a goal state
that an inactive trial satisfies, because the reference actions change no state.

WHICH ANNOTATION GOVERNS, and it is not the obvious one. Tools carry
@is_tool(ToolType.WRITE|READ|GENERIC), but src/tau2/environment/toolkit.py:44-49
says of ToolType: "It does **not** control evaluation-replay behaviour -- see
the ``mutates_state`` parameter on :func:`is_tool` for that." The governing flag
is `mutates_state`, documented at toolkit.py:72-80:

    mutates_state: Whether this tool mutates environment / DB state.
        When ``None`` (the default) the value is **inferred** from
        *tool_type*: ``True`` for WRITE, ``False`` otherwise. ...
        During evaluation replay (``set_state``), only tools with
        ``mutates_state=True`` are re-executed; all others are skipped.

So the replay-relevant set is: WRITE tools, PLUS explicit mutates_state=True
overrides, MINUS explicit mutates_state=False overrides. Taking ToolType at
face value would have produced a wrong set in both directions.

A task whose reference actions contain no such tool leaves the database as it
was found, so the state a no-op trial leaves matches the state the reference
produces -- the same structure as A, in B's architecture.

Reads source and task JSON. No execution, no model calls.
Counts are graded [I]: the annotation is read directly ([E]) but the inference
from "no mutating reference action" to "inaction-satisfiable" is traced, not run.

Run:  python3 t03_inaction_tasks_B_mutation.py
"""

import ast
import json
import os

ROOT = os.environ.get("TAU_B", "/Volumes/MULLETT_T7/tau-bench-audit/tau2-bench-v1.0.1")
DOMAINS = ("airline", "retail", "telecom", "banking_knowledge", "mock")


def pct(a, b):
    return 0.0 if not b else 100.0 * a / b


def mutating_tools(pyfile):
    """Names of tools whose mutates_state resolves True, per toolkit.py:82-83."""
    if not os.path.exists(pyfile):
        return set(), set()
    tree = ast.parse(open(pyfile).read())
    mutate, seen = set(), set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for dec in node.decorator_list:
            if not (isinstance(dec, ast.Call) and
                    getattr(dec.func, "id", getattr(dec.func, "attr", None)) == "is_tool"):
                continue
            seen.add(node.name)
            tool_type = None
            explicit = None
            for a in dec.args:
                if isinstance(a, ast.Attribute):
                    tool_type = a.attr
            for kw in dec.keywords:
                if kw.arg == "tool_type" and isinstance(kw.value, ast.Attribute):
                    tool_type = kw.value.attr
                if kw.arg == "mutates_state" and isinstance(kw.value, ast.Constant):
                    explicit = kw.value.value
            resolved = explicit if explicit is not None else (tool_type == "WRITE")
            if resolved:
                mutate.add(node.name)
    return mutate, seen


def main():
    print("Repository B - tau2-bench v1.0.1 @ fc0055dc4e0a316c3f83133267fbd6faaa770992")
    print("Governing flag: mutates_state (toolkit.py:64-91), NOT ToolType.\n")
    grand_n = grand_inaction = 0
    for dom in DOMAINS:
        ddir = os.path.join(ROOT, "src", "tau2", "domains", dom)
        mut, seen = mutating_tools(os.path.join(ddir, "tools.py"))
        mut2, seen2 = mutating_tools(os.path.join(ddir, "user_tools.py"))
        mut |= mut2
        seen |= seen2
        tpath = os.path.join(ROOT, "data", "tau2", "domains", dom, "tasks.json")
        if not os.path.exists(tpath):
            continue
        tasks = json.load(open(tpath))
        n = len(tasks)

        by_basis = {}
        inaction = []
        for t in tasks:
            ec = t.get("evaluation_criteria") or {}
            acts = ec.get("actions") or []
            names = [a.get("name") for a in acts]
            rb = tuple(sorted(ec.get("reward_basis") or []))
            has_mut = any(nm in mut for nm in names)
            # nothing that a no-op trial can fail:
            #   no state-changing reference action, no env assertions,
            #   no required communication, no NL assertions
            nothing_else = (not (ec.get("env_assertions") or [])
                            and not (ec.get("communicate_info") or [])
                            and not (ec.get("nl_assertions") or []))
            rec = by_basis.setdefault(rb, [0, 0])
            rec[0] += 1
            if not has_mut and nothing_else:
                rec[1] += 1
                inaction.append(t)

        print(f"=== {dom} : {n} tasks ===")
        print(f"  tools declared {len(seen)}  |  mutates_state=True: {len(mut)}")
        print(f"  {sorted(mut)}")
        print(f"  INACTION-SATISFIABLE (no state-changing reference action,")
        print(f"    no env/communicate/NL criteria)          : {len(inaction):>5}"
              f"   ({pct(len(inaction), n):.2f}%)")
        for rb, (tot, aff) in sorted(by_basis.items(), key=lambda x: -x[1][0]):
            print(f"    basis {str(rb) if rb else '(none)':<40} {aff:>5} / {tot:<5}"
                  f" ({pct(aff, tot):.2f}%)")
        print()
        grand_n += n
        grand_inaction += len(inaction)

    print("=== TOTAL ===")
    print(f"  tasks {grand_n}   inaction-satisfiable {grand_inaction}"
          f"   ({pct(grand_inaction, grand_n):.2f}%)")
    print("\n  Compare repository A: 24 of 165 test tasks (14.55%).")
    print("  Materiality reference: the frozen plan fixes 5% of tasks in the suite.")


if __name__ == "__main__":
    main()
