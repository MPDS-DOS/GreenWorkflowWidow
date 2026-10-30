"""Build chemgraph/questions/{big,huge}.json from the ChemGraph paper evaluation.

Molecules and reactions: Zenodo 17290519. Prompts: get_query() of each experiment's
run_llm_workflow.py at ChemGraph commit d34da02, called with that script's arguments.

Usage: python chemgraph_paper.py <unpacked Zenodo zip> <ChemGraph clone>
"""

import ast
import glob
import json
import subprocess
import sys
from pathlib import Path

COMMIT = "d34da0230d21aff1f8beeabe5583c2cd48843cdf"
ZENODO, REPO = sys.argv[1], sys.argv[2]
OUT = Path(__file__).resolve().parent.parent / "chemgraph" / "questions"

# experiment, script with get_query(), key, (query_name, method) when the experiment has no script.
# Exp3 and Exp8 need NWChem and are left out. Exp4 and Exp9 have no run_llm_workflow.py; their
# manual workflows run mace_mp vib, so they use the vib template of Exp5 (names) and Exp10 (SMILES).
MOLECULES = [
    ("Exp1", "Exp1", "name", None),
    ("Exp2", "Exp2", "name", None),
    ("Exp4", "Exp5", "name", ("name_to_vib", "mace_mp")),
    ("Exp5", "Exp5", "name", None),
    ("Exp6", "Exp6", "name", None),
    ("Exp7", "Exp7", "smiles", None),
    ("Exp9", "Exp10", "smiles", ("smiles_to_vib", "mace_mp")),
    ("Exp10", "Exp10", "smiles", None),
    ("Exp11", "Exp11", "smiles", None),
]
REACTIONS = ["Exp12", "Exp13"]
BIG = {"Exp9", "Exp12", "Exp13"}


def git(*args):
    return subprocess.check_output(["git", "-C", REPO, *args], text=True)


SCRIPTS = git("ls-tree", "-r", "--name-only", COMMIT, "scripts/evaluations/run_llm_workflow").split()


def script(exp):
    """get_query() and the keyword arguments it is called with in the experiment's script."""
    src = git("show", f"{COMMIT}:" + next(s for s in SCRIPTS if f"/{exp}_" in s))
    tree = ast.parse(src)
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "get_query")
    ns = {}
    exec(ast.unparse(fn), ns)
    call = next(n for n in ast.walk(tree) if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "get_query")
    return ns["get_query"], {k.arg: ast.literal_eval(k.value) for k in call.keywords}


def zenodo(exp, name):
    return json.load(open(sorted(glob.glob(f"{ZENODO}/*/{exp}_*/{name}"))[0]))


questions = []
for exp, src, key, fixed in MOLECULES:
    get_query, kwargs = script(src)
    if fixed:
        kwargs = dict(zip(["query_name", "method"], fixed))
    used = zenodo(exp, "manual_workflow.json")
    mols = [m for m in zenodo(exp, "data_from_pubchempy.json") if m[key] in used]
    questions += [{"id": f"{exp}-{i}", "category": exp, "query": get_query(m[key], **kwargs)}
                  for i, m in enumerate(mols)]
for exp in REACTIONS:
    get_query, kwargs = script(exp)
    used = zenodo(exp, "manual_workflow.json")
    rxns = [r for r in zenodo(exp, "reaction_dataset.json") if r["reaction_name"] in used]
    questions += [{"id": f"{exp}-{i}", "category": exp, "query": get_query(r, **kwargs)}
                  for i, r in enumerate(rxns)]

OUT.mkdir(exist_ok=True)
for name, items in [("big", [q for q in questions if q["category"] in BIG]), ("huge", questions)]:
    (OUT / f"{name}.json").write_text(json.dumps(items, indent=1) + "\n")
    print(name, len(items))
