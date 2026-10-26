# Shared example set

[`drugs.json`](drugs.json) holds 10 approved small-molecule drugs with their PubChem SMILES,
so no lookup is needed at run time. Both agents work on the same molecules with different tasks:

| Agent | Tasks | Workload pattern |
| --- | --- | --- |
| ChemGraph | geometry optimization, thermochemistry, IR spectrum (MACE) | LLM tool calls, then CPU-heavy simulation |
| Biomni | ADMET prediction, target and pathway lookup | LLM writes code, runs it, iterates; data-lake reads |

That gives 30 ChemGraph runs and 20 Biomni runs. List them with:

```bash
python prompts.py chemgraph
python prompts.py biomni
```

Each line is `<task-id> <tab> <molecule> <tab> <prompt>`.

## Run with ChemGraph

```bash
python prompts.py chemgraph | while IFS=$'\t' read -r id mol prompt; do
  CHEMGRAPH_LOG_DIR="runs/chemgraph/$id-$mol" \
    chemgraph run -m "$CHEMGRAPH_MODEL" -w single_agent -q "$prompt" --output last_message
done
```

## Run with Biomni

```python
import subprocess
from biomni.agent import A1

agent = A1()
lines = subprocess.run(["python", "prompts.py", "biomni"], capture_output=True, text=True).stdout
for line in lines.splitlines():
    task_id, mol, prompt = line.split("\t")
    log, answer = agent.go(prompt)
    print(task_id, mol, answer[:200])
```

Setup for both agents: [chemgraph/](../chemgraph/), [biomni/](../biomni/).
