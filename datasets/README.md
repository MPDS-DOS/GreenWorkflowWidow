# Datasets

Downloads are pinned to fixed revisions so every group runs the same tasks.
Downloaded files stay out of Git (see `.gitignore`).

```bash
uv pip install "huggingface_hub[cli]"
```

## ChemGraph

**Ground-truth benchmark**, 40 queries with structured answers
([Autonomous-Scientific-Agents/groundtruth](https://huggingface.co/datasets/Autonomous-Scientific-Agents/groundtruth)).
Used by `chemgraph eval`, see [chemgraph/](../chemgraph/).

```bash
hf download Autonomous-Scientific-Agents/groundtruth output_data.json \
  --repo-type dataset \
  --revision 8fe726352eb0437e4958282ca741d064fcfe6959 \
  --local-dir chemgraph
```

**Paper evaluation data** ([Zenodo 17290519](https://zenodo.org/records/17290519), 14 MB).

```bash
curl -L -o chemgraph/ChemGraph_evaluation_data.zip \
  "https://zenodo.org/records/17290519/files/ChemGraph_evaluation_data.zip?download=1"
```

## Biomni

**Biomni-Eval1**, 433 instances in 10 task types ([biomni/Eval1](https://huggingface.co/datasets/biomni/Eval1)).
`biomni.eval.BiomniEval1` always reads the current version from Hugging Face. The pinned copy is for
reading the task prompts and running them with your own loop.

```bash
hf download biomni/Eval1 biomni_eval1_dataset.parquet \
  --repo-type dataset \
  --revision 51f97feb9e377fac7384faae49046bc067283c38 \
  --local-dir biomni
```

**Data lake**, about 11 GB, downloaded by Biomni itself on the first `A1()` start into
`$BIOMNI_DATA_PATH/biomni_data/data_lake/`. Keep it on the agent host's local disk.

## Shared example set

[`examples/drugs.json`](../examples/drugs.json) is part of the repository and needs no download.
