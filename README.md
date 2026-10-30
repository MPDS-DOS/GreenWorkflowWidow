# GreenWorkflowWidow

Reproducible agentic workloads based on [ChemGraph](https://github.com/argonne-lcf/ChemGraph) 0.7.0
and a self-hosted, OpenAI-compatible LLM endpoint.

## Workloads

| Profile | Questions | Source | Approx. duration |
| --- | --- | --- | --- |
| `small` | 40 | ChemGraph ground-truth benchmark | 40 min |
| `big` | 60 | ChemGraph paper evaluation: Exp9, Exp12, Exp13 | 3 h |
| `huge` | 300 | ChemGraph paper evaluation: Exp1–Exp13 without Exp3, Exp8 | 12 h |

Durations refer to one agent host with 24 cores, questions processed sequentially.

## Repository

| Path | Content |
| --- | --- |
| [`chemgraph/`](chemgraph/) | Installation, configuration, workload profiles |
| [`datasets/`](datasets/) | Dataset sources, download, conversion |
| [`llm/`](llm/) | LLM server: hardware, model, serving configuration |

## Licenses

ChemGraph is licensed under Apache-2.0. Datasets are subject to the terms of their sources.
