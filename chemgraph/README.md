# ChemGraph

[ChemGraph](https://github.com/argonne-lcf/ChemGraph) (Apache-2.0) is an LLM agent framework for
computational chemistry. The model runs on the LLM endpoint; the tools (RDKit, ASE, MACE, xTB)
run on the local CPU.

Version: `chemgraph==0.7.0`

## Installation

Python 3.11, from the repository root:

```bash
uv venv .venv --python 3.11
source .venv/bin/activate
uv pip install "chemgraph[calculators]==0.7.0"
```

`[calculators]` installs xTB, required by `small`.

## Configuration

```bash
export VLLM_BASE_URL=<endpoint>/v1
export VLLM_API_KEY=<key>
```

Test:

```bash
chemgraph run -m qwen3.8-27b -q "Provide the SMILES string corresponding to this molecule: water"
```

## Workloads

```bash
cd chemgraph
chemgraph eval --config config.toml --profile small --models qwen3.8-27b --output-dir ../runs/small
```

| Profile | Dataset | Questions |
| --- | --- | --- |
| `small` | `datasets/chemgraph/output_data.json` | 40 |
| `big` | [`questions/big.json`](questions/big.json) | 60 |
| `huge` | [`questions/huge.json`](questions/huge.json) | 300 |

Profiles are defined in [`config.toml`](config.toml), datasets in [`datasets/`](../datasets/).
All profiles use the `multi_agent` workflow (planner, parallel executors, response agent).
Questions are processed sequentially.

| Option | Effect |
| --- | --- |
| `--max-queries N` | Process the first N questions |
| `--resume` | Skip questions already completed in `--output-dir` |
| `--workflows single_agent` | Use a single agent |

## Output

`--output-dir` contains the report (`benchmark_*.md`), one checkpoint per question and, in `logs/`,
structures, trajectories and agent states (`state_thread_*.json`).

## Known issues (0.7.0)

- The exit code is 0 also for failed questions; see the report.
- Questions can end at the recursion limit (50 steps) without an answer.
- Imprecise MACE model names (e.g. `small`) can lead the agent to request non-existent models (`small-mpa-0`).
- Molecules with more than ~60 atoms fail during RDKit pre-optimization.
