# Datasets

Downloads are pinned and stay out of Git.

## ChemGraph benchmark

40 questions with structured ground truth
([Autonomous-Scientific-Agents/groundtruth](https://huggingface.co/datasets/Autonomous-Scientific-Agents/groundtruth)),
used by the `small` workload.

```bash
uv pip install "huggingface_hub[cli]"
hf download Autonomous-Scientific-Agents/groundtruth output_data.json \
  --repo-type dataset \
  --revision 8fe726352eb0437e4958282ca741d064fcfe6959 \
  --local-dir datasets/chemgraph
```
