"""t02 - Repository B (tau2-bench v1.0.1): default-pass and inaction surfaces.

Two distinct pass-without-doing-anything routes exist in B's evaluator
(src/tau2/evaluator/evaluator.py at fc0055dc):

  1. evaluator.py:130-135 -- if `task.evaluation_criteria is None` the function
     returns reward 1.0 with the note "No evaluation criteria", before any
     evaluator runs. Any normally-terminating trial on such a task passes.

  2. A task whose reward_basis does not include DB/ACTION checks, or whose
     criteria contain no actions and no communicate_info, has nothing that a
     no-op trial can fail.

Note what does NOT reach either route: evaluator.py:119-129 returns reward 0.0
whenever termination_reason is not AGENT_STOP or USER_STOP, so crashed,
timed-out and max-steps trials are scored as failures before this point. The
counts below therefore bound the inaction surface for NORMALLY TERMINATING
trials only, which is the honest scope.

Reads task JSON only. No execution, no model calls.

Run:  python3 t02_inaction_tasks_B.py
"""

import json
import os

ROOT = os.environ.get("TAU_B", "/Volumes/MULLETT_T7/tau-bench-audit/tau2-bench-v1.0.1")
DOMAINS = ("airline", "retail", "telecom", "banking_knowledge", "mock")


def pct(a, b):
    return 0.0 if not b else 100.0 * a / b


def main():
    print("Repository B - tau2-bench v1.0.1 @ fc0055dc4e0a316c3f83133267fbd6faaa770992\n")
    grand_n = grand_none = grand_noact = 0
    for dom in DOMAINS:
        path = os.path.join(ROOT, "data", "tau2", "domains", dom, "tasks.json")
        if not os.path.exists(path):
            continue
        tasks = json.load(open(path))
        n = len(tasks)
        no_criteria = [t for t in tasks if not t.get("evaluation_criteria")]
        bases = {}
        no_actions = []
        for t in tasks:
            ec = t.get("evaluation_criteria") or {}
            rb = tuple(sorted(ec.get("reward_basis") or []))
            bases[rb] = bases.get(rb, 0) + 1
            acts = ec.get("actions") or []
            comm = ec.get("communicate_info") or []
            nl = ec.get("nl_assertions") or []
            if not acts and not comm and not nl:
                no_actions.append(t)
        print(f"=== {dom} : {n} tasks ===")
        print(f"  evaluation_criteria absent/empty -> reward 1.0 by default : "
              f"{len(no_criteria):>4}   ({pct(len(no_criteria), n):.2f}%)")
        print(f"  criteria present but no actions, no communicate_info,")
        print(f"    and no nl_assertions                                    : "
              f"{len(no_actions):>4}   ({pct(len(no_actions), n):.2f}%)")
        print(f"  reward_basis distribution:")
        for rb, c in sorted(bases.items(), key=lambda x: -x[1]):
            print(f"    {str(rb) if rb else '(none)':<44} {c:>5}")
        print()
        grand_n += n
        grand_none += len(no_criteria)
        grand_noact += len(no_actions)

    print("=== TOTAL across domains ===")
    print(f"  tasks                                    : {grand_n}")
    print(f"  no evaluation_criteria (default pass)    : {grand_none}"
          f"   ({pct(grand_none, grand_n):.2f}%)")
    print(f"  criteria with nothing to check           : {grand_noact}"
          f"   ({pct(grand_noact, grand_n):.2f}%)")
    print("\n  Materiality reference: the frozen plan fixes 5% of tasks in the suite.")
    print("  Denominator choice matters here: telecom carries 2,285 of the tasks and")
    print("  would dominate any all-domain percentage. Per-domain figures are above.")


if __name__ == "__main__":
    main()
