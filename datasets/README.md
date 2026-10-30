# Datasets

All workloads come from the ChemGraph authors (Argonne). Downloads are pinned and stay out of Git.

## Benchmark (`small`)

40 questions with structured ground truth
([Autonomous-Scientific-Agents/groundtruth](https://huggingface.co/datasets/Autonomous-Scientific-Agents/groundtruth)).

```bash
uv pip install "huggingface_hub[cli]"
hf download Autonomous-Scientific-Agents/groundtruth output_data.json \
  --repo-type dataset \
  --revision 8fe726352eb0437e4958282ca741d064fcfe6959 \
  --local-dir datasets/chemgraph
```

## Paper evaluation (`big`, `huge`)

The evaluation of the ChemGraph paper: 30 PubChem molecules or 15 reactions per experiment,
with the hand-run reference workflow for each item.

- Molecules, reactions and reference workflows: [Zenodo 17290519](https://zenodo.org/records/17290519)
- Prompts: `get_query()` in `scripts/evaluations/run_llm_workflow/Exp*/run_llm_workflow.py` at ChemGraph commit
  [`d34da02`](https://github.com/argonne-lcf/ChemGraph/tree/d34da0230d21aff1f8beeabe5583c2cd48843cdf/scripts/evaluations)

| Experiment | Task | Method |
| --- | --- | --- |
| Exp1 | name → SMILES | |
| Exp2 | name → coordinates | |
| Exp4 | name → vibrational frequencies | MACE |
| Exp5 | name → Gibbs free energy, 800 K | GFN2-xTB |
| Exp6 | name → optimized structure, XYZ file | MACE |
| Exp7 | SMILES → coordinates | |
| Exp9 | SMILES → vibrational frequencies | MACE |
| Exp10 | SMILES → Gibbs free energy, 800 K | MACE |
| Exp11 | SMILES → optimized structure, XYZ file | MACE |
| Exp12 | reaction → enthalpy, 400 K | GFN2-xTB |
| Exp13 | reaction → Gibbs free energy, 500 K | MACE |

`big` is Exp9, Exp12 and Exp13 (60 questions), `huge` all of the above (300 questions).
Left out: Exp3 and Exp8 (need NWChem), Exp14 and Exp15 (the questions of Exp12 and Exp13
with the multi-agent workflow, which is set in the profile here).
Exp4 and Exp9 have no prompt script; they use the vibration prompt of Exp5 and Exp10.

The question files in [`chemgraph/questions/`](../chemgraph/questions/) are committed. To rebuild them:

```bash
mkdir -p datasets/chemgraph
curl -L -o datasets/chemgraph/paper.zip \
  "https://zenodo.org/records/17290519/files/ChemGraph_evaluation_data.zip?download=1"
unzip -q datasets/chemgraph/paper.zip -d datasets/chemgraph/paper
git clone https://github.com/argonne-lcf/ChemGraph.git datasets/chemgraph/ChemGraph
python datasets/chemgraph_paper.py datasets/chemgraph/paper datasets/chemgraph/ChemGraph
```
