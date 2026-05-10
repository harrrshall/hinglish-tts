# Compute Resources

Single source of truth for **what hardware we have locally** and **what free cloud compute we can pull from** for the Hinglish TTS work. Update when quotas, credits, or local hardware change.

---

## 1. Local machine (cybernovas-HP-Laptop-15s-du3xxx)

Captured 2026-05-07.

| Component | Spec |
|---|---|
| OS | Ubuntu 24.04.4 LTS (noble), kernel 6.17.0-23-generic |
| CPU | Intel Core i3-1125G4 (11th gen, Tiger Lake), 4 cores / 8 threads, 2.0 GHz base / 3.7 GHz boost |
| RAM | **15 GiB** total, ~8 GiB available, 4 GiB swap |
| Disk | 468 GB NVMe, **241 GB free** (46% used) |
| GPU | **Intel UHD Graphics G4 (integrated only — no CUDA, no dedicated VRAM)** |
| Python | 3.12.3, pip 24.0 |

### What this means for the project

- **No local GPU training, ever.** The integrated Intel UHD G4 has no CUDA path and ~1 GB shared VRAM. All model training and meaningful inference goes to cloud.
- **15 GB RAM is tight but usable** for: data preprocessing, tokenization, audio resampling, eval-set scoring on small clips, building text-normalization pipelines, running CPU-only inference on small models (Kokoro 82M is borderline OK, IndicF5 330M will swap, Indic Parler 880M will OOM).
- **241 GB free disk** is enough to keep audio datasets locally before pushing to HF/Drive. Watch the `audit/` folder once it crosses 100 GB — move to cloud storage.
- **Default workflow:** code locally, push to git, run training/inference in cloud, pull checkpoints + audio samples back for listening.

---

## 2. Free cloud compute — Tier 1 (no application, instant)

Listed in priority order for this project. Quotas as of 2026-05-07.

| Platform | Hardware | Free quota | Best for |
|---|---|---|---|
| **Kaggle Notebooks** | NVIDIA P100 16GB **or** T4×2; TPU v3-8 | **30 GPU-hrs/week + 30 TPU-hrs/week**, resets Saturday | Phase 1 audit inference, longest single sessions |
| **Modal.com** | T4 / A10G / L40S / A100 / H100 / H200 (serverless, per-second billing) | **$30/month recurring credit** (~50 hrs T4 or ~7.5 hrs H100); $30 one-time on signup | Phase 2 LoRA pipeline, jobs > 4 hrs that would lose Colab session, the only easy path to H100 |
| **Google Colab (free)** | T4 16GB (when available) | ~15–30 GPU-hrs/week, 12-hr session cap, no SLA | Quick prototyping, notebook iteration |
| **Lightning AI Studios** | T4/L4, persistent dev env | **22 GPU-hrs/month** | When we need a stable env across sessions (VS Code-like, persistent storage) |
| **Saturn Cloud** | T4 | **30 GPU-hrs/month** | Backup when other quotas exhausted |
| **HF Spaces ZeroGPU** | H200 (dynamic, per-request) | Free daily quota | Demo space for the eval audio outputs |
| **HF Inference Providers** | Hosted LLM APIs | **100K credits/month** | Calling LLMs for synthetic data generation, NOT for TTS inference |
| **AWS SageMaker Studio Lab** | T4 | **4 GPU-hrs / 24-hr window**, 4-hr session cap | Last resort fallback |

**Realistic monthly ceiling without applications:** ~150–200 GPU-hrs of mixed T4/P100, plus ~7 hrs of H100 via Modal.

---

## 3. Free cloud compute — Tier 2 (apply, larger pools)

Worth pursuing once Phase 2 pipeline works:

| Program | Amount | Eligibility |
|---|---|---|
| GCP new-account trial | **$300**, 90 days | New customer, card required |
| Azure for Students | **$100 + free services**, 12 months | .edu email, no card |
| GCP Research Credits | **$1K (PhD)** → **$5K (faculty)** | Academic research framing |
| AWS Activate Founders | up to **$1,000** | Self-funded |
| Modal for Academics | up to **$10,000** | Academic application |
| Modal for Startups | up to **$25,000** | Startup application |

**Note on GCP $300:** activate only when we have a known-good training script. Credits expire 90 days after activation, so burning them on debugging is wasteful.

---

## 4. CLI setup — copy-paste ready

### Kaggle

```bash
# Get token: https://www.kaggle.com/settings/api → "Create New Token" → kaggle.json
pip install kaggle
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
kaggle competitions list   # verify

# Push a notebook to run on GPU
kaggle kernels init -p ./my-notebook
# edit kernel-metadata.json → "enable_gpu": true
kaggle kernels push -p ./my-notebook
kaggle kernels status <user>/<slug>
kaggle kernels output <user>/<slug> -p ./output
```
Docs: https://www.kaggle.com/docs/api

### Modal

```bash
pip install modal
modal setup   # browser login, writes ~/.modal.toml
```

Minimal `gpu_probe.py`:
```python
import modal
app = modal.App("probe")

@app.function(gpu="T4", image=modal.Image.debian_slim().pip_install("torch"))
def probe():
    import torch
    return torch.cuda.get_device_name(0), torch.cuda.get_device_properties(0).total_memory

@app.local_entrypoint()
def main():
    print(probe.remote())
```
```bash
modal run gpu_probe.py
modal deploy gpu_probe.py   # persistent endpoint
```
Docs: https://modal.com/docs/guide

### Lightning AI

```bash
pip install lightning-sdk
lightning login
lightning list studios
lightning run studio --name hinglish-tts --machine T4
lightning ssh hinglish-tts
```
Docs: https://lightning.ai/docs/overview/cli-reference/studio

### Hugging Face

```bash
pip install huggingface_hub
huggingface-cli login   # token from https://huggingface.co/settings/tokens

# Push audit outputs to a private dataset repo
huggingface-cli repo create hinglish-audit --type=dataset --private
git clone https://huggingface.co/datasets/<user>/hinglish-audit
```

### Colab

No CLI. Either use it via browser, or connect a local Jupyter to a Colab GPU runtime:
```bash
pip install jupyter_http_over_ws
jupyter serverextension enable --py jupyter_http_over_ws
jupyter notebook \
  --NotebookApp.allow_origin='https://colab.research.google.com' \
  --port=8888 --NotebookApp.port_retries=0
```
Then in Colab: **Connect → Connect to a local runtime**.

### Saturn Cloud

```bash
pip install saturn-client
export SATURN_TOKEN="..."   # from https://app.community.saturnenterprise.io/api/user/token
export SATURN_BASE_URL="https://app.community.saturnenterprise.io"
saturn-client list resources
saturn-client start <resource-name>
```

---

## 5. Allocation strategy for this project

| Phase | Target compute | Source |
|---|---|---|
| **Phase 1 (audit)** | Pure inference on 4 base models × 30 sentences. Maybe 2–4 GPU-hrs total. | Kaggle (P100). Single session is enough. |
| **Phase 2 (pipeline shakedown)** | LoRA on ~30 min audio, single speaker, ~1 hr T4 training. | Colab T4 (notebook iteration) → Modal T4 (final shakedown run, decoupled from session timeout). |
| **Phase 3 (real fine-tune)** | LoRA / partial fine-tune on curated Hinglish corpus. Estimate from Phase 2's measured time-per-step × planned steps. | Modal credits + Kaggle weekly quota. Apply for GCP Research Credits if estimate > 80 GPU-hrs. |

---

## 6. Rules

- **Always probe before training.** First step on any new runtime: 10-step probe that prints time-per-step and `torch.cuda.max_memory_allocated()`. T4 OOM at step 500 = wasted session (per AGENT.md §3).
- **Never start a long run on Colab free.** Session timeouts will kill it. Modal or Kaggle for anything > 3 hrs.
- **Don't activate GCP $300 yet.** 90-day clock starts on activation. Save it for Phase 3.
- **Stack quotas, don't abandon them.** Kaggle (30/wk) + Modal ($30/mo) + Colab + Lightning gives ~150+ GPU-hrs/month without spending anything. That's enough for Phase 1+2 entirely.
- **Log every cloud run** in `RESEARCH_LOG.md`: platform, GPU, hours used, credits remaining, what we learned.

---

## 7. Sources

- [Kaggle API docs](https://www.kaggle.com/docs/api)
- [Modal pricing](https://modal.com/pricing)
- [Modal user account setup](https://modal.com/docs/guide/modal-user-account-setup)
- [Lightning AI CLI reference](https://lightning.ai/docs/overview/cli-reference/studio)
- [Hugging Face ZeroGPU docs](https://huggingface.co/docs/hub/en/spaces-zerogpu)
- [Free Cloud GPU Credits 2026 — Thunder Compute](https://www.thundercompute.com/blog/free-cloud-gpu-credits)
- [Free GPU Cloud Trials 2026 — GMI Cloud](https://www.gmicloud.ai/en/blog/where-can-i-get-free-gpu-cloud-trials-in-2026-a-complete-guide)
- [GCP Research Credits — CU Boulder](https://curc.readthedocs.io/en/latest/cloud/gcp/Google-Cloud-research-credits.html)
- [Compute Grants Guide for Students](https://nightingal3.github.io/blog/2026/04/16/compute-grants/)
