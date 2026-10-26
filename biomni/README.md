# Biomni

General-purpose biomedical AI agent from Stanford
([snap-stanford/Biomni](https://github.com/snap-stanford/Biomni), Apache-2.0).
It plans with retrieval over 150+ tools, software packages and databases, then writes
Python, R or Bash code, executes it and iterates on the results.

Pinned version: commit `400c1f366b96` (PyPI release `biomni==0.0.8` is older).

## Install

The environment is large. Pick one option:

| Option | Command | Size / time |
| --- | --- | --- |
| Basic agent | `conda env create -f biomni_env/environment.yml` | minutes |
| Reduced (no R, no CLI tools) | `conda env create -f biomni_env/fixed_env.yml` | ≥ 13 GB |
| Full E1 environment | `bash biomni_env/setup.sh` | ≥ 30 GB, > 10 h, tested on Ubuntu 22.04 |

```bash
git clone https://github.com/snap-stanford/Biomni.git
cd Biomni && git checkout 400c1f366b96
conda env create -f biomni_env/environment.yml
conda activate biomni_e1
pip install -e .
```

## Connect to the local LLM

Copy [`.env.example`](.env.example) to `.env`, fill in the key and export it before starting Python:

```bash
set -a; source .env; set +a
```

```env
BIOMNI_SOURCE=Custom
BIOMNI_LLM=qwen3.8-27b
BIOMNI_CUSTOM_BASE_URL=http://siena01.cit.tu-berlin.de:8000/v1
BIOMNI_CUSTOM_API_KEY=<shared-key>
BIOMNI_DATA_PATH=/data/biomni
```

Biomni reads its configuration from the environment when it is imported, before it loads `.env`
itself, so the variables must already be exported. They cover both the agent and Biomni's internal
database queries, so no request leaves for a hosted provider.

## Run

```python
from biomni.agent import A1

agent = A1()  # settings from the environment; downloads the data lake on first start
agent.go("Predict ADMET properties for this compound: CC(C)CC1=CC=C(C=C1)C(C)C(=O)O")
```

Explicit arguments override the environment:

```python
agent = A1(path="/data/biomni", llm="qwen3.8-27b", source="Custom",
           base_url="http://siena01.cit.tu-berlin.de:8000/v1", api_key="<shared-key>",
           timeout_seconds=600)
```

## Data lake

On first start Biomni downloads about 11 GB of datasets into `<path>/biomni_data/data_lake/`.
Put it on the agent host's local disk. To skip the download (only tools without data lake files work):

```python
agent = A1(expected_data_lake_files=[])
```

## Benchmark

[Biomni-Eval1](https://huggingface.co/datasets/biomni/Eval1): 433 instances in 10 task types
(GWAS causal genes, lab-bench Q&A, rare disease diagnosis, CRISPR delivery, …).

```python
from biomni.eval import BiomniEval1

evaluator = BiomniEval1()
score = evaluator.evaluate("gwas_causal_gene_opentargets", 0, "BRCA1")
```

## Notes

- Generated code runs directly in the Biomni process (`exec`) and in subprocesses on the host,
  without a sandbox. Run it on a dedicated agent host or inside gVisor.
- Biomni marks actions with `<execute>` tags in plain text; it doesn't need native tool calling.
- `timeout_seconds` (default 600) limits each code execution.
- Some packages are left out of the environment because of dependency conflicts,
  see [`docs/known_conflicts.md`](https://github.com/snap-stanford/Biomni/blob/main/docs/known_conflicts.md).
