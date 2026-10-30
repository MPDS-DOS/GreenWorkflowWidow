# ChemGraph

Agent framework for computational chemistry from Argonne
([argonne-lcf/ChemGraph](https://github.com/argonne-lcf/ChemGraph), Apache-2.0).
An LLM plans the steps and calls tools; the tools (RDKit, ASE, MACE, xTB) run locally on the CPU.

Pinned version: `chemgraph==0.7.0`.

## Install

From the repository root, Python 3.11:

```bash
uv venv .venv --python 3.11
source .venv/bin/activate
uv pip install "chemgraph[calculators]==0.7.0"
```

`[calculators]` adds xTB, which the `small` benchmark needs.

## Connect

```bash
export VLLM_API_KEY=<key>
cd chemgraph
chemgraph run -m qwen3.8-27b --config config.toml \
  -q "Build water from SMILES O, optimize it with MACE and report the final energy in eV."
```

[`config.toml`](config.toml) sets the endpoint ([llm/](../llm/)) and the workloads.

## Workloads

```bash
chemgraph eval --models qwen3.8-27b --config config.toml --profile small --output-dir ../runs/small
```

| Profile | Dataset | Questions | Duration |
| --- | --- | --- | --- |
| `small` | [benchmark](../datasets/#benchmark-small) | 40, small molecules, graded against ground truth | 38 min (measured) |
| `big` | [`questions/big.json`](questions/big.json) | 60 from the paper evaluation: vibrations, reaction enthalpy and Gibbs free energy | ~2 h (estimated) |
| `huge` | [`questions/huge.json`](questions/huge.json) | 300 from the paper evaluation, all runnable experiments | ~12 h (estimated) |

Questions and their sources: [datasets/](../datasets/).

All profiles use the `multi_agent` workflow: a planner splits each question into subtasks,
executor agents run them in parallel, and a response agent writes the answer.
Questions run one after another. Cost per question grows with molecule size (up to 29 atoms
in the paper set) and task: vibrations and thermochemistry need one force calculation per atom.

| Option | Effect |
| --- | --- |
| `--max-queries N` | Only the first N questions |
| `--resume` | Skip questions already answered in `--output-dir` |
| `--workflows single_agent` | One agent instead of planner and executors |

## Output

`--output-dir` gets a report (`benchmark_*.md`), one checkpoint line per question and, under `logs/`,
every structure, trajectory and agent conversation (`state_thread_*.json`).

Known issues in 0.7.0:

- Exit code is 0 even when a question fails; check the report.
- Some questions end at the recursion limit (50 steps) without an answer, e.g. when the agent
  repeats a finished optimization. The run continues with the next question.
- With a MACE size like `small` in the question, the agent may invent a model name (`small-mpa-0`),
  retry until the recursion limit and return no answer. Use exact names such as `small-0b2`.
- Molecules above ~60 atoms fail in RDKit's pre-optimization ("Failed to optimize 3D geometry").
