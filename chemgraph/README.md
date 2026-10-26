# ChemGraph

Agent framework for computational chemistry and materials science from Argonne
([argonne-lcf/ChemGraph](https://github.com/argonne-lcf/ChemGraph), Apache-2.0).
It turns natural-language requests into molecular construction, simulation and analysis
steps built on LangGraph, ASE and RDKit. The LLM calls tools natively; calculations run locally.

Pinned version: `chemgraph==0.7.0`. Documentation: <https://argonne-lcf.github.io/ChemGraph/>

## Install

Python 3.11 or newer.

```bash
uv venv .venv --python 3.11
source .venv/bin/activate
uv pip install chemgraph==0.7.0
```

The core install includes ASE, EMT and MACE. Optional calculators:

| Calculator | Install | Notes |
| --- | --- | --- |
| EMT | core | Lightweight; for setup checks, not accurate chemistry |
| MACE | core | MACE-MP foundation model; weights download on first use |
| TBLite / xTB | `uv pip install "chemgraph[calculators]"` | May need a Fortran toolchain |

## Connect to the local LLM

ChemGraph routes any model ID it doesn't know to an OpenAI-compatible endpoint
when a base URL is set:

```bash
export VLLM_BASE_URL="http://siena01.cit.tu-berlin.de:8000/v1"
export VLLM_API_KEY="<shared-key>"
export CHEMGRAPH_MODEL="qwen3.8-27b"
```

Alternatively pass [`config.toml`](config.toml) with `--config config.toml`.

Check the setup:

```bash
chemgraph run -m "$CHEMGRAPH_MODEL" --check-keys
chemgraph run -m "$CHEMGRAPH_MODEL" \
  -q "Build water from SMILES O, optimize it with EMT, and report the final energy." \
  --output last_message
```

## Run

```bash
chemgraph run \
  -m "$CHEMGRAPH_MODEL" \
  -w single_agent \
  -q "Calculate the vibrational frequencies of water with MACE." \
  --output last_message
```

| Option | Purpose |
| --- | --- |
| `-m`, `--model` | Model ID (`qwen3.8-27b`) |
| `-w`, `--workflow` | Agent workflow (see below) |
| `-o`, `--output` | Return the full `state` or only the `last_message` |
| `-s`, `--structured` | Request structured final output |
| `-r`, `--report` | Generate an HTML report |
| `--output-file` | Save the response to a file |
| `-v` / `-vv` | INFO / DEBUG logging |

Python API (asynchronous):

```python
import asyncio
from chemgraph.agent.llm_agent import ChemGraph

async def main():
    agent = ChemGraph(model_name="qwen3.8-27b", workflow_type="single_agent",
                      return_option="last_message")
    result = await agent.run("Optimize the geometry of caffeine with MACE.")
    print(result.content)

asyncio.run(main())
```

## Workflows

| Workflow | Use |
| --- | --- |
| `single_agent` | Default. Molecule lookup, ASE calculations, reports |
| `multi_agent` | Planner/executor with parallel subtasks; more LLM calls |
| `main_agent` | Workspace agent with files, shell and delegation; interactive or `--dangerously-skip-approvals` |
| `mock_agent` | One tool-call pass; for development and evaluation |

## Output

Each run writes a session directory under `cg_logs/` (XYZ structures, JSON results,
trajectories, spectra, reports). Set `CHEMGRAPH_LOG_DIR` to choose another location.
Sessions are stored in `~/.chemgraph/sessions.db`.

## Benchmark

ChemGraph ships an evaluator with structured ground truth (dataset: see [datasets/](../datasets/)):

```bash
chemgraph eval \
  --models "$CHEMGRAPH_MODEL" \
  --base-url "$VLLM_BASE_URL" \
  --dataset ../datasets/chemgraph/output_data.json \
  --workflows single_agent \
  --judge-type structured \
  --output-dir eval_results
```

Add `--query-ids 1 2 3` for a subset.

## Notes

- Molecule lookup by name uses PubChem (network). Pass SMILES directly for offline runs.
- The first MACE run pauses while model weights download.
- Startup warnings about missing calculators are harmless unless the workflow needs them.
