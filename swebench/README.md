# SWE-bench

[SWE-bench](https://www.swebench.com) (MIT) contains real GitHub issues from Python repositories.
The agent edits the repository until it considers the issue fixed; the repository's own tests decide
whether it is resolved. Agent: [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) (MIT).
Each instance runs in its own Docker container.

Versions: `mini-swe-agent==2.4.6`, `swebench==5.0.2`

## Requirements

- Docker
- About 3 GB of disk space per instance image

## Installation

From the repository root:

```bash
uv venv .venv-swe --python 3.11
source .venv-swe/bin/activate
uv pip install mini-swe-agent==2.4.6 swebench==5.0.2 mcp
```

`mcp` is imported by LiteLLM but not declared as a dependency.

## Configuration

```bash
export OPENAI_BASE_URL=$VLLM_BASE_URL
export OPENAI_API_KEY=$VLLM_API_KEY
```

## Run

```bash
mini-extra swebench -c swebench.yaml \
  -c model.cost_tracking=ignore_errors -c environment.pull_timeout=1800 \
  -m openai/qwen3.8-27b \
  --subset verified --split test --slice 0:10 --workers 2 \
  -o runs/swebench
```

| Option | Effect |
| --- | --- |
| `--subset lite` / `verified` | SWE-bench Lite (300 instances) / Verified (500 instances) |
| `--slice A:B` | Instances A to B−1 |
| `--workers N` | N agents in parallel (N containers, N concurrent LLM sessions) |
| `-c agent.step_limit=N` | Maximum steps per instance (default 250) |

Output: `runs/swebench/preds.json` (one patch per instance) and one trajectory per instance.

## Evaluation

```bash
python -m swebench.harness.run_evaluation \
  --dataset_name SWE-bench/SWE-bench_Verified \
  --predictions_path runs/swebench/preds.json \
  --max_workers 2 --run_id swebench
```

The harness applies each patch in a fresh container, runs the tests and writes a report
(`<model>.<run_id>.json`) with the resolved instances.

## Reference run

SWE-bench Verified, instances 0–1, 2 workers:

| Phase | Duration |
| --- | --- |
| Image pull (2.9 GB per instance) | 3 min per instance |
| Agent | 4 min (22 and 28 LLM calls) |
| Evaluation | 1.5 min |

Result: 1 of 2 resolved.
