# LLM server

Both agents use one OpenAI-compatible endpoint served by vLLM on siena01 (1× NVIDIA L40, 48 GB).

## Model

[Qwen/Qwen3.8-27B-FP8](https://huggingface.co/Qwen/Qwen3.8-27B-FP8) (Apache-2.0, released 2026-08).

- 27B dense, FP8 weights ≈ 31 GB, leaving the rest of the L40 for the KV cache.
- Hybrid attention (linear attention in 48 of 64 layers), so long agent contexts need little KV memory.
- Native tool calling (needed by ChemGraph) and strong code generation (needed by Biomni).

Faster alternative: [Qwen/Qwen3.6-35B-A3B-FP8](https://huggingface.co/Qwen/Qwen3.6-35B-A3B-FP8)
(MoE, 3B active parameters, ≈ 37.5 GB weights, less KV headroom).

## Serve

Requires `vllm>=0.32.0` (or the image `vllm/vllm-openai:v0.32.0`).

```bash
export VLLM_API_KEY="<shared-key>"

vllm serve Qwen/Qwen3.8-27B-FP8 \
  --served-model-name qwen3.8-27b \
  --host 0.0.0.0 --port 8000 \
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

- `--language-model-only` skips the vision encoder and frees its memory for the KV cache.
- Thinking is off by default to keep runs short and comparable. Remove the last flag to study thinking mode.
- `--max-num-seqs 64`: the default 256 exceeds the model's Mamba state slots (228 on the L40) and vLLM refuses to start.
- Check the startup log for the reported KV-cache size (`GPU KV cache size: … tokens`).

Docker:

```bash
docker run --gpus all -p 8000:8000 --ipc=host \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  vllm/vllm-openai:v0.32.0 \
  Qwen/Qwen3.8-27B-FP8 --served-model-name qwen3.8-27b --api-key "$VLLM_API_KEY" \
  --max-model-len 131072 --kv-cache-dtype fp8 --language-model-only --max-num-seqs 64 --enable-prefix-caching \
  --reasoning-parser qwen3 --enable-auto-tool-choice --tool-call-parser qwen3_coder \
  --default-chat-template-kwargs '{"enable_thinking": false}'
```

On siena01 this runs as container `vllm` (`--restart unless-stopped`), started by `/srv/llm/run.sh`;
weights in `/srv/llm/hf`, key in `/srv/llm/env`. On the L40: 295k tokens of KV cache, ~2 full 128k contexts at once.

## Check the endpoint

Port 8000 is reachable only from the cluster nodes (130.149.248.0/24), Tailscale and dosvpn.

```bash
export LLM_BASE_URL="http://siena01.cit.tu-berlin.de:8000/v1"

curl -s -H "Authorization: Bearer $VLLM_API_KEY" "$LLM_BASE_URL/models"
curl -s -H "Authorization: Bearer $VLLM_API_KEY" -H "Content-Type: application/json" \
  "$LLM_BASE_URL/chat/completions" \
  -d '{"model": "qwen3.8-27b", "messages": [{"role": "user", "content": "Say hello."}]}'
```

Server metrics (queue length, KV-cache usage, prefix-cache hits) are exposed at `http://siena01.cit.tu-berlin.de:8000/metrics`.
