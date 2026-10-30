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

| Setting | Value |
| --- | --- |
| Max. context length | 131072 tokens |
| KV-cache dtype | FP8 |
| Max. concurrent sequences | 64 |
| Prefix caching | on |
| Tool calling | auto, `qwen3_coder` parser |
| Thinking mode | off |
| Vision encoder | not loaded |

## Endpoint check

```bash
curl -s -H "Authorization: Bearer $VLLM_API_KEY" "$VLLM_BASE_URL/models"
```

Prometheus metrics: `<endpoint>/metrics`.
