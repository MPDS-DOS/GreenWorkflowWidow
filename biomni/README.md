# Biomni

[Biomni](https://github.com/snap-stanford/Biomni) (Apache-2.0) is a general-purpose biomedical AI agent.
It selects tools, software and databases for a task, writes Python, R or Bash code, executes it
and iterates on the results.

Version: commit `400c1f366b96`

## Installation

Basic environment (Python packages, no R and no command-line tools):

```bash
git clone https://github.com/snap-stanford/Biomni.git
cd Biomni && git checkout 400c1f366b96
conda env create -f biomni_env/environment.yml
conda activate biomni_e1
pip install -e . pyarrow
```

`pyarrow` is required by the benchmark loader and not part of the environment file.

| Environment | Command | Size |
| --- | --- | --- |
| Basic | `conda env create -f biomni_env/environment.yml` | ≈ 7 GB |
| Full (R, CLI tools) | `bash biomni_env/setup.sh` | ≥ 30 GB, several hours |

## Configuration

Copy [`.env.example`](.env.example) to `.env`, set the values and export them before starting Python:

```bash
set -a; source .env; set +a
```

## Examples

```python
from biomni.agent import A1

agent = A1(expected_data_lake_files=[])
log, answer = agent.go("Predict ADMET properties for this compound: CC(C)CC1=CC=C(C=C1)C(C)C(=O)O")
```

| Task | Prompt |
| --- | --- |
| ADMET prediction | `Predict ADMET properties for this compound: CC(C)CC1=CC=C(C=C1)C(C)C(=O)O` |
| Drug information | `Find FDA active ingredient information for ibuprofen` |
| CRISPR screen design | `Plan a CRISPR screen to identify genes that regulate T cell exhaustion, generate 32 genes that maximize the perturbation effect.` |

`expected_data_lake_files=[]` skips the data lake. Without it, the first `A1()` downloads about 11 GB of
datasets into `$BIOMNI_DATA_PATH/biomni_data/data_lake/`; tasks that query these datasets need it.

## Benchmark

[Biomni-Eval1](https://huggingface.co/datasets/biomni/Eval1): 433 instances in 10 tasks with ground truth
(GWAS causal genes, lab-bench questions, rare disease diagnosis, CRISPR delivery, …).

```python
import re
from biomni.agent import A1
from biomni.eval import BiomniEval1

agent = A1()
evaluator = BiomniEval1()

for _, row in evaluator.get_instances_by_task("crispr_delivery").iterrows():
    log, answer = agent.go(row["prompt"])
    m = re.search(r"<solution>(.*?)</solution>", answer, re.S)
    solution = m.group(1).strip() if m else answer.strip()
    print(row["task_instance_id"], evaluator.evaluate(row["task_name"], row["task_instance_id"], solution))
```

`evaluator.list_tasks()` lists the tasks, `evaluator.get_task_stats()` the number of instances per task.

Reference run without data lake, first instance per task:

| Task | Duration | Score |
| --- | --- | --- |
| `crispr_delivery` | 143 s | 0 |
| `lab_bench_dbqa` | 485 s | 1 |

## Notes

- Generated code runs in the Biomni process and in subprocesses on the host, without a sandbox.
  The agent can install packages into the environment.
- `BIOMNI_TIMEOUT_SECONDS` limits each code execution (default 600).
