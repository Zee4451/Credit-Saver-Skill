# ⚡ Credit-Saver Skill (v2.6)
### High-Performance, Zero-Cost AI Coding & Deep Reasoning Engine

[![OpenRouter Free Tier](https://img.shields.io/badge/OpenRouter-100%25%20Free%20Tier-success?style=flat-square&logo=openai)](https://openrouter.ai/models?q=:free)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-yellow.svg?style=flat-square&logo=python)](https://python.org)
[![Antigravity Compatible](https://img.shields.io/badge/Antigravity-Agent%20Ready-purple?style=flat-square)](https://github.com/Zee4451/Credit-Saver-Skill)

A production-ready skill designed to eliminate **80%–95% of paid AI token expenses** by routing heavy boilerplate, component generation, refactoring, and critical thinking to **OpenRouter's $0.00 free-tier models**.

Built for **Antigravity IDE, Cursor, Windsurf, Claude Code, and Gemini CLI**.

---

## 🌟 Core Features & Four-Pillar Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CREDIT-SAVER ENGINE                             │
├─────────────────────┬──────────────────────┬───────────────────────────┤
│  ⚡ Speed Tier      │  🧠 Deep Reasoning   │  🔄 Dynamic Discovery    │
│  Gemma 4 MoE (26B)  │  Nemotron Ultra 550B │  Auto-fetches new models  │
│  North Mini / Fast  │  Nemotron Super 120B │  from OpenRouter API      │
├─────────────────────┴──────────────────────┴───────────────────────────┤
│  🚀 Optimizations: Persistent HTTP Session | Live Token Streaming     │
│  🛡️ Failover: Dual-Key Auto-Switch on 429 | Low-Latency Provider Order │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Dual-Tier Speed & Reasoning Architecture:**
   - **Speed Tier (Everyday Work):** Uses `openrouter/free` and `google/gemma-4-26b-a4b-it:free` (MoE with only 3.8B active params) for instant sub-second Time-To-First-Token.
   - **Critical Reasoning Tier:** Automatically escalates to flagship **120B to 550B models** (`nvidia/nemotron-3-ultra-550b`, `nvidia/nemotron-3-super-120b`, `google/gemma-4-31b`) when architecture, system trade-offs, or complex logic are detected.

2. **Dynamic Live Auto-Discovery (Zero Manual Updates):**
   - Automatically queries `https://openrouter.ai/api/v1/models` in the background with a 12-hour local cache.
   - New free models are discovered and added dynamically; dead/deprecated models are automatically removed.

3. **Persistent HTTP Session & Low-Latency Routing:**
   - Employs persistent connection pooling (`requests.Session`) to cut TCP/SSL handshake latency.
   - Prioritizes fast inference providers (`Together`, `DeepInfra`, `Fireworks`, `Chutes`) with seamless automatic fallback (`allow_fallbacks: True`).

4. **Smart Context Pruner (`--file` & `--symbol`):**
   - Instead of passing 5,000 lines of code, surgically extracts only target function definitions, types, or interfaces.

5. **Direct File Output & Clean Stripper (`--out` and `--clean`):**
   - Automatically strips markdown backticks (````tsx / ```python) and saves clean, ready-to-run code directly to disk.

6. **Credit Savings Dashboard (`--savings`):**
   - Live telemetry tracking exact tokens and estimated monetary savings in USD and INR.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+ installed.
- Install dependencies:
  ```bash
  pip install requests
  ```

### 2. Setup API Key (100% Free)
Get a free API key with zero deposit from [OpenRouter Keys](https://openrouter.ai/keys).

Create a `.env` file in the skill folder:
```bash
OPENROUTER_API_KEY="sk-or-v1-your-key-here"

# Or comma-separated for instant dual-key auto-failover:
# OPENROUTER_API_KEYS="sk-or-v1-key1,sk-or-v1-key2"
```

---

## ⚡ Usage Examples

### 1. Universal Smart Router (Recommended)
Automatically routes to the best live free model with feature filtering:
```powershell
python runner.py "Build a responsive animated pricing card in React + Tailwind" router
```

### 2. High-Speed Coding (MoE Speed Tier)
```powershell
python runner.py "Write a python script to validate and normalize URLs" fast
```

### 3. Critical Thinking & System Architecture (550B Deep Logic)
```powershell
python runner.py "Compare Redis vs Memcached architecture trade-offs with lock-free concurrency" reasoning
```

### 4. Direct File Output with Code Clean
Writes ready-to-compile code directly to target file without chat preamble or code fences:
```powershell
python runner.py "Write a Next.js contact modal with validation" code --out "src/components/ContactModal.tsx" --clean
```

### 5. Smart Context Pruning (Token Saver)
Extracts only the target interface/symbol from a large file:
```powershell
python runner.py "Refactor this function to handle network retry" --file "src/lib/api.ts" --symbol "fetchUserOrder"
```

### 6. Provider Routing Override
```powershell
python runner.py "Explain event loop in 2 lines" fast --providers "Together,DeepInfra"
```

### 7. Key Health & Savings Dashboard
```powershell
python runner.py --status
python runner.py --savings
```

---

## 🎯 Model Routing Matrix

| Tier / Category | Recommended Alias | Top Free Models | Scale & Notes |
| :--- | :--- | :--- | :--- |
| **Universal Router** | `router`, `free`, `auto` | `openrouter/free` | Smart live router with automatic capability filtering |
| **Speed / MoE King** | `fast`, `gemma-moe`, `code` | `google/gemma-4-26b-a4b-it:free`<br>`cohere/north-mini-code:free` | 26B MoE (3.8B active params), 256K context, ultra-fast |
| **Critical Reasoning** | `reasoning`, `critical`, `ultra` | `nvidia/nemotron-3-ultra-550b-a55b:free`<br>`nvidia/nemotron-3-super-120b-a12b:free` | 550B / 120B parameters for deep thinking & complex proofs |
| **Agentic Coding** | `nex`, `laguna` | `nex-agi/nex-n2.5-pro:free`<br>`poolside/laguna-s-2.1:free` | 118B Coding Agent for complex multi-file components |
| **Multimodal & Vision** | `gemma`, `ling` | `google/gemma-4-31b-it:free`<br>`inclusionai/ling-3.0-flash-vl:free` | Text, image understanding, and structured outputs |

---

## 💡 The "Architect & Worker" Paradigm

1. **Architect (Main AI - Gemini/Claude/GPT):** Reads the codebase, determines requirements, and extracts precise type signatures.
2. **Worker (Credit-Saver Skill):** Generates 300+ line components or heavy boilerplate for **$0.00**.
3. **Architect (Main AI):** Validates the generated code, runs lint checks, and patches it into the workspace.

---

## 📄 License
MIT License. Free to use, modify, and distribute.
