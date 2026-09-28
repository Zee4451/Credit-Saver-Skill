# 🚀 OpenRouter Free Models Skill (Credit-Saver Edition)

A high-performance, **100% Free** AI coding skill for Antigravity, Cursor, Windsurf, Claude Code, and Gemini CLI. 

This skill connects to OpenRouter's curated **$0.00 `:free` models** (Cohere Code, Nex AGI, Nvidia Nemotron, Poolside Laguna, Gemma 4) with **dual-key instant failover**, **smart context pruning**, and **direct file generation** — saving 80% to 95% of paid AI tokens.

---

## 🌟 Why Use This?
- **$0.00 AI Spend**: Never run out of expensive Claude 3.5 Sonnet or GPT-4o credits when generating large components, boilerplate, or CSS styles.
- **Dual-Key Failover**: If Key 1 hits a temporary 429 rate limit, it instantly switches to Key 2 without interrupting your work.
- **Smart Context Pruner**: Extracts only relevant TypeScript interfaces or function signatures instead of passing huge files, keeping responses fast and token-efficient.
- **Clean Code Stripper (`--clean` / `--out`)**: Automatically removes markdown fences (````tsx / ```python) and writes directly into your project files.
- **Savings Dashboard (`--savings`)**: Live counter showing exact tokens and dollar value saved.

---

## 📦 Quick Setup for You or a Friend

### Step 1: Requirements
- Python 3.8+
- Run:
  ```bash
  pip install requests
  ```

### Step 2: (Optional) Set Your Own OpenRouter Keys
OpenRouter free models only require a free account at [openrouter.ai](https://openrouter.ai). No credit card needed!
Set in your environment or `.bashrc` / PowerShell profile:
```powershell
$env:OPENROUTER_API_KEYS="sk-or-v1-key1,sk-or-v1-key2"
```
*(If no keys are provided, the skill has built-in backup free-tier keys ready to go).*

---

## ⚡ Examples & Usage

### 1. Generate a Component Directly to File
```powershell
python runner.py "Create a modern animated review card with star ratings in React + CSS Modules" nex --out "src/components/ReviewCard.tsx" --clean
```

### 2. Inject Context with Smart Symbol Pruning
```powershell
python runner.py "Add an edit review modal that uses this interface" --file "src/types/reviews.ts" --symbol "ReviewItem"
```

### 3. Check Live Key Health & Quotas
```powershell
python runner.py --status
```

### 4. Check Credits Saved
```powershell
python runner.py --savings
```

---

## 🧠 Top Curated Free Models

| Alias | Full Model Identifier | Best For |
| :--- | :--- | :--- |
| `cohere` / `code` | `cohere/north-mini-code:free` | TypeScript, React, Next.js, Clean production code |
| `nex` / `nex-pro` | `nex-agi/nex-n2.5-pro:free` | Complex agentic code generation & state logic |
| `lightning` | `nvidia/nemotron-3.5-lightning:free` | Ultra fast scripts, utilities, regex |
| `poolside` | `poolside/laguna-s-2.1:free` | 118B coding agent for algorithms and backend |
| `nemotron-120b` | `nvidia/nemotron-3-super-120b-a12b:free` | Deep reasoning and architectural planning |
| `ultra` | `nvidia/nemotron-3-ultra-550b-a55b:free` | 550B flagship model for tough bugs |

---

## 🤝 The "Architect & Worker" Formula
1. Let your main Assistant (Architect) read your repository, inspect styles, and construct the exact requirements.
2. Let `openrouter-free` (Worker) generate the heavy code for $0.00.
3. Let your main Assistant review, compile, and place the code into your repository.
