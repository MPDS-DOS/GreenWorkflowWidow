# GreenWorkflowWidow

Reproducible agentic workloads with a self-hosted, OpenAI-compatible LLM endpoint.

## Frameworks

| Framework | Domain | Benchmark | Execution |
| --- | --- | --- | --- |
| [ChemGraph](chemgraph/) | Computational chemistry | ChemGraph ground truth and paper evaluation | Simulation tools on the host CPU |
| [SWE-bench](swebench/) | Software engineering | SWE-bench Lite / Verified | One Docker container per instance |
| [Biomni](biomni/) | Biomedicine | Biomni-Eval1 | Generated code on the host |

## ChemGraph workloads

| Profile | Questions | Source | Approx. duration |
| --- | --- | --- | --- |
| `small` | 40 | ChemGraph ground-truth benchmark | 40 min |
| `big` | 60 | ChemGraph paper evaluation: Exp9, Exp12, Exp13 | 3 h |
| `huge` | 300 | ChemGraph paper evaluation: Exp1–Exp13 without Exp3, Exp8 | 12 h |

Durations refer to one agent host with 24 cores, questions processed sequentially.

## Repository

| Path | Content |
| --- | --- |
| [`chemgraph/`](chemgraph/) | ChemGraph: installation, configuration, workload profiles |
| [`swebench/`](swebench/) | SWE-bench with mini-swe-agent: installation, run, evaluation |
| [`biomni/`](biomni/) | Biomni: installation, configuration, examples, benchmark |
| [`datasets/`](datasets/) | ChemGraph dataset sources, download, conversion |
| [`llm/`](llm/) | LLM server: hardware, model, serving configuration |

## Monitoring

Grafana dashboards (URLs provided separately):

| Dashboard | Source | Metrics |
| --- | --- | --- |
| GPU | NVIDIA DCGM exporter | Utilization, memory, power, temperature, clocks |
| LLM server | vLLM `/metrics` | Running and waiting requests, latency, token throughput, KV-cache usage |
| Hosts | Prometheus node exporter | CPU, memory, disk and network per node |

## Licenses

ChemGraph, Biomni: Apache-2.0. SWE-bench, mini-swe-agent: MIT. Datasets are subject to the terms of their sources.
