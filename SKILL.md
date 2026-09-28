---
name: openrouter-free
description: Directly consult or write code using OpenRouter 100% free tier models (Nex-N2.5 Pro, Cohere North Mini Code, Poolside Laguna, Nvidia Nemotron Lightning, Gemma 4, etc.) with smart context pruning, dual-key instant failover, network auto-recovery, automatic fence stripping, and live credit savings tracking ($0.00 cost). Trigger with @openrouter-free, @openrouter, or when asking to generate code with free models.
---

# OpenRouter Free Models Skill (v2.6 Speed & Deep Reasoning Edition)

This skill routes code generation, critical thinking, architecture plans, refactoring, and logic directly through OpenRouter's curated **$0.00 free tier models**. It implements an automated **Four-Pillar Optimization (A, B, C, D)** to maximize throughput and eliminate latency:

- **Pillar A (Dual-Tier Routing):**
  - **Lightning Speed for Everyday Tasks:** Defaults to ultralight models (`cohere/north-mini-code`, `nvidia/nemotron-3.5-lightning`, `nex-n2.5-mini`) for instant Time-To-First-Token and zero queue delay.
  - **Heavy Flagship Models for Critical Thinking & Reasoning:** Automatically escalates to 120B–550B powerhouse models (`nvidia/nemotron-3-ultra-550b`, `nvidia/nemotron-3-super-120b`, `thinkingmachines/inkling`) whenever complex logic, trade-offs, architecture, or deep reasoning is detected or requested.
- **Pillar B (Real-time Token Streaming):**
  - Instant live terminal rendering (`stream: True`) with provider fallback preferences so you never wait on long blank pauses.
- **Pillar C (Smart Context & Signature Pruning):**
  - Eliminates prompt bloat and cold-start latency by extracting only target functions/interfaces (`--symbol`) or essential type signatures instead of uploading massive 5,000-line files.
- **Pillar D (Low-Latency Provider Routing):**
  - Automatically routes queries to the fastest active inference providers (`Together`, `DeepInfra`, `Fireworks`, `Chutes`, `Lepton`) with `--providers` flag and automatic seamless fallback (`allow_fallbacks: True`).

---

## 💡 The Architect & Worker Workflow (How Credits Are Saved)

To get maximum quality without wasting paid credits:

```
┌────────────────────────────────────────────────────────┐
│  Primary AI (Cursor / Windsurf / Antigravity / Gemini) │  <-- ARCHITECT
│  • Reads project structure and finds exact file lines  │
│  • Extracts only required Types, Props, or Signatures  │
└─────────────────────────┬──────────────────────────────┘
                          │ Sends pruned prompt
                          ▼
┌────────────────────────────────────────────────────────┐
│  OpenRouter Free Model (Fast or Heavy Reasoning)       │  <-- WORKER ($0.00)
│  • Fast Tier: North Mini / Nemotron Lightning          │
│  • Heavy Tier: Nemotron Ultra 550B / Super 120B        │
│  • Zero paid tokens consumed ($0.00 cost)              │
└─────────────────────────┬──────────────────────────────┘
                          │ Clean code / rationale output
                          ▼
┌────────────────────────────────────────────────────────┐
│  Primary AI (Architect)                                │
│  • Validates syntax, imports, and builds               │
│  • Surgically patches code into the project            │
└────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Execution Guide

### 1. Fast Everyday Coding & Tasks (Default / Speed Tier)
Lightning-fast response for everyday code, components, and fixes:
```powershell
python "C:\Users\yasht\.gemini\config\skills\openrouter-free\runner.py" "Create an animated React status badge" fast
```

### 2. Critical Thinking & Deep Architecture (Heavy 120B–550B Tier)
For complex algorithms, system architecture, RCA, trade-off evaluations, and deep logic:
```powershell
python "C:\Users\yasht\.gemini\config\skills\openrouter-free\runner.py" "Analyze distributed caching trade-offs and evaluate race conditions" reasoning
```
*(Or use aliases `critical`, `ultra`, `nemotron-ultra`, `heavy`)*

### 3. Direct File Output with Auto-Clean (`--out` and `--clean`)
Directly generates and writes ready-to-compile code with markdown code fences stripped:
```powershell
python "C:\Users\yasht\.gemini\config\skills\openrouter-free\runner.py" "Write a complete Next.js contact modal" code --out "src\components\ContactModal.tsx" --clean
```

### 4. Smart Context Pruning (`--file` & `--symbol`) - *Token Saver & Latency Reducer*
Instead of dumping a huge 3,000-line file into the prompt, `--symbol` surgically extracts only the target interface or function, saving massive prompt tokens:
```powershell
python "C:\Users\yasht\.gemini\config\skills\openrouter-free\runner.py" "Refactor this function to handle errors" --file "src\context\CMSContext.tsx" --symbol "CMSProvider"
```

### 5. Check API Key Health
```powershell
python "C:\Users\yasht\.gemini\config\skills\openrouter-free\runner.py" --status
```

### 6. View Your Credit & Money Savings Dashboard
Shows exact tokens and dollar value saved compared to paid models (Claude 3.5 / GPT-4o):
```powershell
python "C:\Users\yasht\.gemini\config\skills\openrouter-free\runner.py" --savings
```

---

## 🎯 Curated Free Models & Routing Tiers

| Tier / Category | Recommended Alias | Model Name | Description & Scale |
| :--- | :--- | :--- | :--- |
| **Auto Router (Universal)** | `router`, `free`, `auto` | `openrouter/free` | OpenRouter's official smart router selecting the best available free model with zero hassle |
| **Speed / MoE King** | `fast`, `gemma-moe`, `code` | `google/gemma-4-26b-a4b-it:free`<br>`cohere/north-mini-code:free` | 26B MoE (3.8B active params) with 256K context & near-zero latency |
| **Critical Reasoning** | `reasoning`, `critical`, `ultra` | `nvidia/nemotron-3-ultra-550b-a55b:free`<br>`nvidia/nemotron-3-super-120b-a12b:free`<br>`google/gemma-4-31b-it:free` | 550B / 120B / 31B parameters for deep thinking & complex proofs |
| **Agentic Coding** | `nex`, `laguna` | `nex-agi/nex-n2.5-pro:free`<br>`poolside/laguna-s-2.1:free` | 118B Coding Agent for full multi-file components |
| **Multimodal & Vision** | `gemma`, `ling` | `google/gemma-4-31b-it:free`<br>`inclusionai/ling-3.0-flash-vl:free` | Text, image understanding, and structured outputs |

---

## ⚙️ Environment Variables (Optional for Portability)

You can share this skill with friends or use it across machines without modifying code. Set either:
- `OPENROUTER_API_KEYS="sk-or-v1-key1,sk-or-v1-key2"`
- `OPENROUTER_API_KEY="sk-or-v1-key1"`

If no environment variables are set, the runner automatically falls back to its built-in dual-key pool.

