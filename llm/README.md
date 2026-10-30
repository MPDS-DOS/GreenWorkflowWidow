# LLM server

OpenAI-compatible endpoint used by ChemGraph. Endpoint URL and API key are provided separately.

## Hardware

| Component | Specification |
| --- | --- |
| CPU | AMD EPYC 8224P, 24 cores / 48 threads |
| Memory | 188 GB |
| GPU | 1× NVIDIA L40, 48 GB |
| Storage | 3.5 TB NVMe |

## Software

| Component | Version |
| --- | --- |
| OS | Ubuntu 24.04 LTS, kernel 6.8 |
| NVIDIA driver / CUDA | 595.91 / 13.2 |
| Docker | 29.9 |
| vLLM | 0.32.0 (`vllm/vllm-openai:v0.32.0`) |

## Model

[Qwen/Qwen3.8-27B-FP8](https://huggingface.co/Qwen/Qwen3.8-27B-FP8) (Apache-2.0), served as `qwen3.8-27b`.

- 27B dense parameters, FP8 weights (≈ 31 GB)
- Hybrid attention: linear attention in 48 of 64 layers
- Native tool calling
- KV cache on the L40: 295k tokens (≈ 2 concurrent 128k contexts)

## Serving configuration

```bash
docker run --gpus all -p 8000:8000 --ipc=host \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  vllm/vllm-openai:v0.32.0 \
  Qwen/Qwen3.8-27B-FP8 \
  --served-model-name qwen3.8-27b \
  --api-key "$VLLM_API_KEY" \
  --max-model-len 131072 \
  --kv-cache-dtype fp8 \
  --language-model-only \
  --max-num-seqs 64 \
  --enable-prefix-caching \
  --reasoning-parser qwen3 \
  --enable-auto-tool-choice --tool-call-parser qwen3_coder \
  --default-chat-template-kwargs '{"enable_thinking": false}'
```

| Flag | Purpose |
| --- | --- |
| `--language-model-only` | No vision encoder; memory goes to the KV cache |
| `--max-num-seqs 64` | The default (256) exceeds the model's state slots on the L40 (228) |
| `--enable-prefix-caching` | Reuses the shared prompt prefix across agent calls |
| `--default-chat-template-kwargs` | Thinking mode off |

## Endpoint check

```bash
curl -s -H "Authorization: Bearer $VLLM_API_KEY" "$VLLM_BASE_URL/models"
```

Prometheus metrics: `<endpoint>/metrics`.
