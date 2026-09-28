<div align="center">

# ⚡ Credit-Saver Skill (v2.6)
### 💰 Save 95% of Paid AI Credits with 100% Free Models! 💸

[![Free Forever](https://img.shields.io/badge/Cost-%240.00%20Free%20Forever-brightgreen?style=for-the-badge&logo=cashapp)](https://openrouter.ai/models?q=:free)
[![Setup Time](https://img.shields.io/badge/Setup-2%20Minutes%20Only-orange?style=for-the-badge&logo=clockify)]()
[![Beginner Friendly](https://img.shields.io/badge/Beginner-Super%20Easy%20%F0%9F%9A%80-blue?style=for-the-badge)]()
[![Platform](https://img.shields.io/badge/Works%20With-Cursor%20%7C%20Windsurf%20%7C%20Antigravity%20%7C%20Claude-purple?style=for-the-badge)]()

<br/>

**Stop burning expensive Claude 3.5 Sonnet & GPT-4o credits on everyday coding and boilerplate!**  
This skill routes heavy coding, file generation, and deep thinking directly to **OpenRouter's $0.00 Free Models** with zero lag.

---

</div>

## 🎯 What Does This Do in Simple Words?

Imagine you have two helpers:
1. 🧠 **The Senior Architect (Paid AI):** You only ask it to plan and review code (costs very little).
2. 🔨 **The Fast Builder (Credit-Saver Free Models):** Generates 500+ lines of HTML, CSS, React components, and Python scripts **completely FREE ($0.00)**.

👉 **Result:** You get premium quality work without ever running out of AI tokens!

---

## 🚀 2-Minute Setup (Anyone Can Do This!)

### 🟢 Step 1: Clone this Repository
Open your Terminal or PowerShell and run:
```bash
git clone https://github.com/Zee4451/Credit-Saver-Skill.git
cd Credit-Saver-Skill
```

### 🟢 Step 2: Install Requests (Just 1 Library)
```bash
pip install requests
```

### 🟢 Step 3: Get Your Free Key (Zero Money Required)
1. Go to [OpenRouter.ai/keys](https://openrouter.ai/keys) and sign up with Google/GitHub (No credit card needed).
2. Click **"Create Key"** and copy your key.
3. In this folder, create a file named `.env` and paste:
```env
OPENROUTER_API_KEY="sk-or-v1-your-key-here"
```

🎉 **That's it! You are 100% ready to use it!**

---

## 🎮 How to Use (Copy & Paste Commands)

### 1️⃣ Ask Anything (Smart Auto-Select) 🌟
OpenRouter will automatically pick the fastest working free model for you:
```bash
python runner.py "Build an animated React login card with dark mode" router
```

### 2️⃣ Super Fast Coding (MoE Speed Mode) ⚡
For quick scripts, regex, functions, and frontend components:
```bash
python runner.py "Write a python function to scrape website titles" fast
```

### 3️⃣ Big Brain Mode (550B Deep Thinking) 🧠
When you need heavy architecture, math proofs, or complex algorithm logic:
```bash
python runner.py "Compare Redis vs Memcached architecture trade-offs" reasoning
```

### 4️⃣ Write Code Directly to a File (No Copy-Pasting!) 💾
Generates pure code, removes all conversational chat/markdown fences, and saves it directly:
```bash
python runner.py "Write a complete Next.js navbar with dropdown" code --out "Navbar.tsx" --clean
```

### 5️⃣ Inject Only 1 Function from a Giant File (Token Saver) ✂️
Instead of uploading a 3,000-line file, extract only what matters:
```bash
python runner.py "Refactor this function to handle errors" --file "src/api.ts" --symbol "fetchUser"
```

---

## 📊 Live Health & Money Saved Dashboards

### 🩺 Check if your Keys are Active:
```bash
python runner.py --status
```
> Shows green **ACTIVE** status and confirmation that you are on the $0.00 Unlimited Free Tier.

### 💰 See How Much Money You Saved:
```bash
python runner.py --savings
```
```text
==================== [OPENROUTER CREDIT SAVINGS DASHBOARD] ====================
  • Total Free Model Generations : 54 calls
  • Total Code Lines Generated   : 21,899 lines
  • Total AI Tokens Saved        : ~172,600 tokens
  • Actual Money Spent           : $0.00 (100% Free Tier)
  • Estimated Paid AI Cost Saved : ~$2.07 USD (~₹180.20 INR)
===============================================================================
```

---

## 🎨 Super Simple Model Cheatsheet

| If you want... | Use this Command | What it uses under the hood |
| :--- | :--- | :--- |
| **No-brainer best model** | `router` | `openrouter/free` (Official Smart Router) |
| **Lightning fast speed** | `fast` | `google/gemma-4-26b-a4b-it:free` (MoE King) |
| **Deep logic & tough bugs** | `reasoning` | `nvidia/nemotron-3-ultra-550b:free` (550B Monster) |
| **Full website components** | `nex` | `nex-agi/nex-n2.5-pro:free` (118B Agent) |

---

## 🛡️ Self-Healing Magic (Why It Never Breaks)

- 🔄 **Auto-Discovery:** Automatically fetches newly released free models from OpenRouter every 12 hours. You **never** have to update code manually!
- 🔀 **Auto-Failover:** If an API key hits a rate-limit, it silently switches keys without crashing.
- ⚡ **Persistent Speed:** Reuses network connections so responses start typing in 1-2 seconds.

---

## 🤝 Contributing & Support
Give it a **⭐ Star** on GitHub if it saved your money!  
Made with ❤️ by [Zee4451](https://github.com/Zee4451).
