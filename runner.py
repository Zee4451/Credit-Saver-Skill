import os
import sys
import json
import time
import argparse
import re
import requests

# 1. API KEY POOL (Supports environment variables OPENROUTER_API_KEY / OPENROUTER_API_KEYS / .env file)
env_file_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_file_path):
    try:
        with open(env_file_path, "r", encoding="utf-8") as ef:
            for line in ef:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k and v and k not in os.environ:
                        os.environ[k] = v
    except Exception:
        pass

env_keys = []
if os.getenv("OPENROUTER_API_KEYS"):
    env_keys.extend([k.strip() for k in os.getenv("OPENROUTER_API_KEYS").split(",") if k.strip()])
elif os.getenv("OPENROUTER_API_KEY"):
    env_keys.append(os.getenv("OPENROUTER_API_KEY").strip())

API_KEYS = env_keys if env_keys else []
BASE_URL = "https://openrouter.ai/api/v1"

# Persistent HTTP session with connection pooling for ultra-low latency TCP handshakes
http_session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=20, max_retries=1)
http_session.mount("https://", adapter)
http_session.mount("http://", adapter)

# 2. CURATED FREE MODELS - High quality coding & reasoning models available at $0.00
MODELS = {
    # Fast Coding & Everyday Work (Lightning-fast TTFT, minimal queue)
    "fast": [
        "openrouter/free",
        "google/gemma-4-26b-a4b-it:free",
        "cohere/north-mini-code:free",
        "nvidia/nemotron-3.5-lightning:free",
        "nex-agi/nex-n2.5-mini:free",
        "liquid/lfm-2.5-2.6b:free",
        "poolside/laguna-xs-2.1:free",
    ],
    # Standard Coding Models
    "code": [
        "google/gemma-4-26b-a4b-it:free",
        "google/gemma-4-31b-it:free",
        "cohere/north-mini-code:free",
        "nvidia/nemotron-3.5-lightning:free",
        "nex-agi/nex-n2.5-pro:free",
        "poolside/laguna-s-2.1:free",
        "openrouter/free"
    ],
    # Critical Thinking, Heavy Reasoning & Complex Architecture (Large Models: 120B to 550B)
    "reasoning": [
        "nvidia/nemotron-3-ultra-550b-a55b:free",
        "nvidia/nemotron-3-super-120b-a12b:free",
        "google/gemma-4-31b-it:free",
        "google/gemma-4-26b-a4b-it:free",
        "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        "thinkingmachines/inkling:free",
        "poolside/laguna-s-2.1:free",
        "nex-agi/nex-n2.5-pro:free"
    ],
    # Vision & Multimodal
    "vision": [
        "google/gemma-4-26b-a4b-it:free",
        "google/gemma-4-31b-it:free",
        "inclusionai/ling-3.0-flash-vl:free",
        "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"
    ],
    # General Assistant & Fast Fallbacks
    "general": [
        "openrouter/free",
        "google/gemma-4-26b-a4b-it:free",
        "cohere/north-mini-code:free",
        "nvidia/nemotron-3.5-lightning:free",
        "google/gemma-4-31b-it:free",
        "dots-studio/dots-3-note-preview:free"
    ]
}

MODELS_CACHE_FILE = os.path.join(os.path.dirname(__file__), "live_free_models_cache.json")
CACHE_TTL_SECONDS = 12 * 3600  # 12 hours auto-refresh

def get_live_free_models():
    """Dynamically fetches all currently active :free models from OpenRouter API, cached for 12 hours."""
    # Check cache first
    if os.path.exists(MODELS_CACHE_FILE):
        try:
            mtime = os.path.getmtime(MODELS_CACHE_FILE)
            if (time.time() - mtime) < CACHE_TTL_SECONDS:
                with open(MODELS_CACHE_FILE, "r", encoding="utf-8") as f:
                    cached_data = json.load(f)
                    if cached_data and isinstance(cached_data, list):
                        return cached_data
        except Exception:
            pass

    # Fetch live from OpenRouter public API
    try:
        resp = requests.get(f"{BASE_URL}/models", timeout=8)
        if resp.status_code == 200:
            all_models = resp.json().get("data", [])
            live_free = ["openrouter/free"]
            for m in all_models:
                mid = m.get("id", "")
                pricing = m.get("pricing", {})
                prompt_price = float(pricing.get("prompt", 0) or 0)
                completion_price = float(pricing.get("completion", 0) or 0)
                if mid.endswith(":free") or (prompt_price == 0 and completion_price == 0):
                    if mid not in live_free:
                        live_free.append(mid)

            if len(live_free) > 2:
                try:
                    with open(MODELS_CACHE_FILE, "w", encoding="utf-8") as f:
                        json.dump(live_free, f, indent=2)
                except Exception:
                    pass
                return live_free
    except Exception:
        pass

    # Fallback to local hardcoded curated list if offline
    return ALL_FREE_MODELS

DEFAULT_CODING_SYSTEM_PROMPT = (
    "You are an elite, highly practical software engineer and frontend designer. "
    "Rules: 1. Write clean, self-contained, working production code. "
    "2. Do NOT import uninstalled third-party libraries (such as react-icons, lucide, font-awesome, tailwind) "
    "unless explicitly requested. Use native SVG, CSS Modules, or clean standard icons instead. "
    "3. Preserve existing variable naming and application architecture. "
    "4. When asked for code, return pure, complete code directly without conversational chit-chat."
)

DEFAULT_REASONING_SYSTEM_PROMPT = (
    "You are a master systems architect and principal engineer specializing in deep critical thinking, "
    "mathematical rigor, root-cause analysis, and architecture trade-offs. "
    "Approach problems systematically: 1. Identify constraints, edge cases, and failure modes. "
    "2. Provide step-by-step rigorous deductions. 3. Recommend optimal solutions with rationale."
)

# Cost comparison metrics: Standard Paid AI rates (Claude 3.5 Sonnet / GPT-4o blend ~ $0.003 / 1k input tokens, $0.015 / 1k output tokens)
EQUIVALENT_PAID_PER_1K_TOKENS = 0.012  # $12 per 1M tokens avg

def check_keys_status():
    """Display real-time quota, rate-limit, and connection health for all keys in the pool"""
    print("\n==================== [OPENROUTER DUAL KEY HEALTH CHECK] ====================", file=sys.stderr)
    for i, key in enumerate(API_KEYS, 1):
        masked = key[:10] + "..." + key[-4:] if len(key) > 14 else key
        try:
            resp = requests.get(
                f"{BASE_URL}/auth/key",
                headers={"Authorization": f"Bearer {key}"},
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json().get("data", {})
                usage = data.get("usage", 0)
                limit = data.get("limit") or "Unlimited / Free Tier"
                print(f"  Key {i} [{masked}]: ACTIVE (Usage: ${usage:.4f} | Limit: {limit})", file=sys.stderr)
            else:
                print(f"  Key {i} [{masked}]: ERROR HTTP {resp.status_code}", file=sys.stderr)
        except Exception as e:
            print(f"  Key {i} [{masked}]: UNREACHABLE ({e})", file=sys.stderr)
    print("============================================================================\n", file=sys.stderr)

def show_savings_dashboard():
    """Display total tokens and estimated monetary credits saved using Free OpenRouter models"""
    log_path = os.path.join(os.path.dirname(__file__), "generation_stats.json")
    if not os.path.exists(log_path):
        print("No generation history found yet.", file=sys.stderr)
        return

    try:
        with open(log_path, "r", encoding="utf-8") as f:
            history = json.load(f)
    except Exception as e:
        print(f"Error reading stats: {e}", file=sys.stderr)
        return

    total_runs = len(history)
    total_tokens = sum(entry.get("approx_tokens_saved", 0) for entry in history)
    total_lines = sum(entry.get("lines_written", 0) for entry in history)
    money_saved = (total_tokens / 1000.0) * EQUIVALENT_PAID_PER_1K_TOKENS

    print("\n==================== [OPENROUTER CREDIT SAVINGS DASHBOARD] ====================", file=sys.stderr)
    print(f"  • Total Free Model Generations : {total_runs:,} calls", file=sys.stderr)
    print(f"  • Total Code Lines Generated   : {total_lines:,} lines", file=sys.stderr)
    print(f"  • Total AI Tokens Saved        : ~{total_tokens:,} tokens", file=sys.stderr)
    print(f"  • Actual Money Spent           : $0.00 (100% Free Tier)", file=sys.stderr)
    print(f"  • Estimated Paid AI Cost Saved : ~${money_saved:.2f} USD (~₹{money_saved * 87:.1f} INR)", file=sys.stderr)
    print("===============================================================================\n", file=sys.stderr)

def strip_code_fences(text):
    """Clean markdown code fences (```tsx, ```python, etc.) from AI output"""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return cleaned

def extract_smart_context(file_path, symbol=None, max_lines=250):
    """Extracts targeted types, interfaces, or functions from a file instead of passing 5,000 lines"""
    if not os.path.exists(file_path):
        return None, f"File not found: {file_path}"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    filename = os.path.basename(file_path)
    total_lines = len(content.splitlines())

    # If specific symbol/function requested, extract its definition block
    if symbol:
        pattern = rf"(?:export\s+)?(?:type|interface|function|const|class)\s+{re.escape(symbol)}\b[\s\S]*?(?=\n\n(?:export\s+)?(?:type|interface|function|const|class)|\Z)"
        match = re.search(pattern, content)
        if match:
            snippet = match.group(0).strip()
            header = f"\n--- Smart Context: Symbol `{symbol}` from `{filename}` ---\n```\n{snippet}\n```\n"
            return header, f"Extracted symbol `{symbol}` ({len(snippet.splitlines())} lines)"

    # If file is compact (< max_lines), send whole file
    if total_lines <= max_lines:
        header = f"\n--- Context File: `{filename}` ({file_path}) ---\n```\n{content}\n```\n--- End of File ---\n"
        return header, f"Injected full file ({total_lines} lines)"

    # Otherwise extract signatures: types, interfaces, and exported component headers
    type_matches = re.findall(r"((?:export\s+)?(?:type|interface)\s+\w+[\s\S]*?\{[\s\S]*?\})", content)
    imports = [line for line in content.splitlines()[:40] if line.startswith("import ")]
    
    extracted_parts = []
    if imports:
        extracted_parts.append("// Top Imports:\n" + "\n".join(imports[:15]))
    if type_matches:
        extracted_parts.append("// Types & Interfaces:\n" + "\n\n".join(type_matches[:8]))
    
    summary = "\n\n".join(extracted_parts)
    if summary.strip():
        header = f"\n--- Smart Pruned Context from `{filename}` (Types/Signatures Only) ---\n```\n{summary}\n```\n"
        return header, f"Pruned {total_lines} lines down to {len(summary.splitlines())} signature lines (Token Saver)"
    
    # Fallback: First 200 lines
    snippet = "\n".join(content.splitlines()[:max_lines])
    header = f"\n--- Head Snippet from `{filename}` (First {max_lines} lines) ---\n```\n{snippet}\n```\n"
    return header, f"Truncated to first {max_lines} lines"

def detect_task_category(prompt):
    """Smart Task Detection: picks reasoning (120B-550B), code, or fast everyday models."""
    p_lower = prompt.lower()

    # High-intensity critical thinking & architecture keywords (Calls heavy 120B-550B models)
    critical_reasoning_keywords = [
        "critical thinking", "reasoning", "deep reason", "complex logic", "architecture",
        "tradeoff", "trade-off", "tradeoffs", "root cause", "rca", "mathematical proof",
        "algorithm design", "formal verification", "concurrency", "distributed system",
        "scalable design", "why does", "explain deeply", "deduce", "evaluate deeply"
    ]
    if any(k in p_lower for k in critical_reasoning_keywords):
        return "reasoning"

    code_keywords = [
        "function", "code", "typescript", "javascript", "python", "react", 
        "component", "def ", "class ", "bug", "fix", "refactor", "const ", 
        "import ", "sql", "html", "css", "api", "interface", "type ", "script",
        "regex", "algorithm", "database", "query", "endpoint", "test"
    ]
    reasoning_keywords = [
        "explain", "why", "plan", "logic", "strategy", "compare", "analyze", "review"
    ]
    vision_keywords = ["image", "diagram", "screenshot", "ui layout", "visual", "picture"]

    if any(k in p_lower for k in code_keywords):
        return "code"
    if any(k in p_lower for k in vision_keywords):
        return "vision"
    if any(k in p_lower for k in reasoning_keywords):
        return "reasoning"
    return "fast"

def ask_openrouter(
    prompt, 
    model=None, 
    system_prompt=None, 
    file_path=None, 
    context_symbol=None,
    stream=True, 
    out_file=None, 
    clean_fences=False,
    providers=None
):
    # 1. Handle File Context Injection (Smart Pruning or Full)
    if file_path:
        context_block, status_msg = extract_smart_context(file_path, symbol=context_symbol)
        if context_block:
            prompt = context_block + "\n\n" + prompt
            print(f"[{status_msg}]", file=sys.stderr, flush=True)
        else:
            print(f"[Warning: {status_msg}]", file=sys.stderr, flush=True)

    # 2. Determine Model Priority & Friendly Aliases
    alias_map = {
        # Speed-First Models
        "router": "openrouter/free",
        "free": "openrouter/free",
        "auto": "openrouter/free",
        "fast": "google/gemma-4-26b-a4b-it:free",
        "gemma-moe": "google/gemma-4-26b-a4b-it:free",
        "gemma-26b": "google/gemma-4-26b-a4b-it:free",
        "cohere": "cohere/north-mini-code:free",
        "code": "cohere/north-mini-code:free",
        "lightning": "nvidia/nemotron-3.5-lightning:free",
        "nemotron-lightning": "nvidia/nemotron-3.5-lightning:free",
        "nex-mini": "nex-agi/nex-n2.5-mini:free",
        "liquid": "liquid/lfm-2.5-2.6b:free",
        
        # Heavy Critical Thinking & Reasoning (Large Models)
        "reasoning": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "critical": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "heavy": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "ultra": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "nemotron-ultra": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "nemotron-120b": "nvidia/nemotron-3-super-120b-a12b:free",
        "nemotron-omni": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        "inkling": "thinkingmachines/inkling:free",
        
        # Coding & Creative
        "nex": "nex-agi/nex-n2.5-pro:free",
        "nex-pro": "nex-agi/nex-n2.5-pro:free",
        "poolside": "poolside/laguna-s-2.1:free",
        "laguna": "poolside/laguna-s-2.1:free",
        "laguna-s": "poolside/laguna-s-2.1:free",
        "laguna-xs": "poolside/laguna-xs-2.1:free",
        "gemma": "google/gemma-4-31b-it:free",
        "ling": "inclusionai/ling-3.0-flash-vl:free",
    }

    cat = detect_task_category(prompt)
    live_free_pool = get_live_free_models()

    if model and model.lower() in alias_map:
        target_model = alias_map[model.lower()]
        models_to_try = [target_model] + [m for m in live_free_pool if m != target_model]
    elif model and (model in live_free_pool or ":free" in model):
        models_to_try = [model] + [m for m in live_free_pool if m != model]
    else:
        recommended = MODELS.get(cat, MODELS["fast"])
        print(f"[Smart Router: Task detected as '{cat.upper()}' -> Prioritizing {recommended[0]}]", file=sys.stderr, flush=True)
        models_to_try = recommended + [m for m in live_free_pool if m not in recommended]

    if system_prompt:
        effective_system_prompt = system_prompt
    elif cat == "reasoning":
        effective_system_prompt = DEFAULT_REASONING_SYSTEM_PROMPT
    elif cat in ("code", "fast"):
        effective_system_prompt = DEFAULT_CODING_SYSTEM_PROMPT
    else:
        effective_system_prompt = None

    messages = []
    if effective_system_prompt:
        messages.append({"role": "system", "content": effective_system_prompt})
    messages.append({"role": "user", "content": prompt})

    errors = []

    # Outer loop on models, inner loop with instant key failover & network backoff
    for m in models_to_try:
        if not m:
            continue

        for active_key in API_KEYS:
            key_masked = active_key[:10] + "..." + active_key[-4:] if len(active_key) > 14 else active_key
            headers = {
                "Authorization": f"Bearer {active_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://antigravity.google",
                "X-Title": "Antigravity OpenRouter Engine"
            }

            # Network retry loop (handles brief DNS or Wi-Fi flaps)
            max_network_retries = 2
            for attempt in range(max_network_retries):
                try:
                    # Fast provider routing: Prioritize Together, DeepInfra, Chutes, Lepton with fallback
                    provider_config = {
                        "allow_fallbacks": True
                    }
                    if providers:
                        provider_config["order"] = [p.strip() for p in providers.split(",") if p.strip()]
                    else:
                        # Default low-latency provider routing order
                        provider_config["order"] = ["Together", "DeepInfra", "Fireworks", "Chutes", "Lepton"]

                    payload = {
                        "model": m,
                        "messages": messages,
                        "temperature": 0.2,
                        "stream": stream,
                        "provider": provider_config
                    }
                    # Fast connect timeout (15s), generous read timeout (55s)
                    resp = http_session.post(
                        f"{BASE_URL}/chat/completions",
                        headers=headers,
                        json=payload,
                        timeout=(15, 55),
                        stream=stream
                    )

                    # 429 Rate limit: Switch immediately to the next key in pool
                    if resp.status_code == 429:
                        print(f"[Key {key_masked} returned 429 rate limit. Switching key...]", file=sys.stderr, flush=True)
                        errors.append(f"{m} (Key 429)")
                        break

                    # 404 / 403 / 400: Model not accessible with this account/tier, skip model
                    if resp.status_code in (404, 403):
                        errors.append(f"{m} (HTTP {resp.status_code})")
                        break

                    if resp.status_code == 200:
                        full_text = []
                        if stream:
                            print(f"[Model {m} streaming response]:\n", file=sys.stderr, flush=True)
                            for line in resp.iter_lines():
                                if not line:
                                    continue
                                line_str = line.decode('utf-8')
                                if line_str.startswith("data: "):
                                    data_part = line_str[6:].strip()
                                    if data_part == "[DONE]":
                                        break
                                    try:
                                        chunk = json.loads(data_part)
                                        delta = chunk.get("choices", [{}])[0].get("delta", {})
                                        content = delta.get("content", "")
                                        if content:
                                            print(content, end="", flush=True)
                                            full_text.append(content)
                                    except Exception:
                                        continue
                            print("\n", flush=True)
                        else:
                            data = resp.json()
                            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                            full_text.append(content)

                        full_content = "".join(full_text).strip()

                        # Check for empty or throttled response
                        if len(full_content) == 0:
                            print(f"[Warning: {m} returned empty response. Trying fallback...]", file=sys.stderr, flush=True)
                            errors.append(f"{m} (Empty response)")
                            break

                        # Optional clean code fences
                        if clean_fences or out_file:
                            full_content = strip_code_fences(full_content)

                        # Write to out file if requested
                        if out_file:
                            os.makedirs(os.path.dirname(os.path.abspath(out_file)), exist_ok=True)
                            with open(out_file, "w", encoding="utf-8") as out_f:
                                out_f.write(full_content)
                            print(f"[Direct Output Saved to: {out_file} ({len(full_content)} bytes)]", file=sys.stderr, flush=True)

                        lines_count = len(full_content.splitlines())
                        chars_count = len(full_content)
                        approx_tokens = int(chars_count / 4)
                        saved_usd = (approx_tokens / 1000.0) * EQUIVALENT_PAID_PER_1K_TOKENS

                        # Live telemetry log
                        log_path = os.path.join(os.path.dirname(__file__), "generation_stats.json")
                        stat_entry = {
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "model_used": m,
                            "key_used": key_masked,
                            "prompt_preview": prompt[:80] + ("..." if len(prompt) > 80 else ""),
                            "file_injected": file_path if file_path else None,
                            "output_file": out_file if out_file else None,
                            "lines_written": lines_count,
                            "characters": chars_count,
                            "approx_tokens_saved": approx_tokens,
                            "usd_saved": round(saved_usd, 4),
                            "cost_to_user": "$0.00 (Free Tier)"
                        }
                        try:
                            stats_history = []
                            if os.path.exists(log_path):
                                with open(log_path, "r", encoding="utf-8") as f:
                                    stats_history = json.load(f)
                            stats_history.append(stat_entry)
                            with open(log_path, "w", encoding="utf-8") as f:
                                json.dump(stats_history, f, indent=2)
                        except Exception:
                            pass

                        print(f"\n==================== [TASK LOG: OPENROUTER GENERATION COMPLETE] ====================", file=sys.stderr, flush=True)
                        print(f"  • Model Active : {m}", file=sys.stderr, flush=True)
                        print(f"  • Key Used     : {key_masked}", file=sys.stderr, flush=True)
                        print(f"  • Lines Made   : {lines_count} lines", file=sys.stderr, flush=True)
                        print(f"  • Tokens Saved : ~{approx_tokens:,} tokens", file=sys.stderr, flush=True)
                        print(f"  • Credits Saved: ~${saved_usd:.4f} USD (~₹{saved_usd * 87:.2f} INR)", file=sys.stderr, flush=True)
                        print(f"  • Actual Cost  : $0.00 (100% Free Tier)", file=sys.stderr, flush=True)
                        if out_file:
                            print(f"  • Target File  : {out_file}", file=sys.stderr, flush=True)
                        print(f"====================================================================================\n", file=sys.stderr, flush=True)

                        return {
                            "success": True,
                            "model_used": m,
                            "key_used": key_masked,
                            "lines_written": lines_count,
                            "approx_tokens_saved": approx_tokens,
                            "saved_usd": saved_usd,
                            "content": full_content
                        }

                    else:
                        errors.append(f"{m} (HTTP {resp.status_code})")
                        break

                except requests.exceptions.RequestException as e:
                    if attempt < max_network_retries - 1:
                        print(f"[Network glitch connecting to {m}: {e}. Retrying in 2s...]", file=sys.stderr, flush=True)
                        time.sleep(2)
                    else:
                        errors.append(f"{m} ({str(e)})")
                        break

    return {
        "success": False,
        "error": f"Failed to get response. Tried models: {', '.join(errors)}"
    }

# Convenient alias for direct python scripts
run_prompt = ask_openrouter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Antigravity OpenRouter Free Models Credit-Saver Runner (v2.5)")
    parser.add_argument("prompt", nargs="?", default=None, help="Prompt or instruction for the AI")
    parser.add_argument("model", nargs="?", default=None, help="Specific model alias or model name (optional)")
    parser.add_argument("--file", "-f", dest="file_path", default=None, help="Path to a file to inject as context")
    parser.add_argument("--symbol", "-s", dest="context_symbol", default=None, help="Specific function/interface to extract (Smart Context Pruner)")
    parser.add_argument("--prompt-file", "-p", dest="prompt_file", default=None, help="Path to a text file containing the prompt")
    parser.add_argument("--model", "-m", dest="flag_model", default=None, help="Specific model alias via flag")
    parser.add_argument("--providers", dest="providers", default=None, help="Comma-separated provider order (e.g. Together,DeepInfra)")
    parser.add_argument("--out", "-o", dest="out_file", default=None, help="Path to save generated output directly to a file")
    parser.add_argument("--clean", action="store_true", help="Strip markdown backticks (```) from the output")
    parser.add_argument("--status", action="store_true", help="Check status and quotas of API keys in pool")
    parser.add_argument("--savings", action="store_true", help="View total tokens and dollar credits saved")

    args = parser.parse_args()

    if args.status:
        check_keys_status()
        sys.exit(0)

    if args.savings:
        show_savings_dashboard()
        sys.exit(0)

    # Determine prompt from argument, file, or stdin
    final_prompt = args.prompt
    if args.prompt_file and os.path.exists(args.prompt_file):
        with open(args.prompt_file, "r", encoding="utf-8") as pf:
            final_prompt = pf.read()
    elif not final_prompt and not sys.stdin.isatty():
        final_prompt = sys.stdin.read()

    if not final_prompt:
        print("Error: No prompt provided. Provide prompt as argument, --prompt-file, or via stdin.", file=sys.stderr)
        print("Use --status to check keys or --savings to check tokens saved.", file=sys.stderr)
        sys.exit(1)

    chosen_model = args.flag_model or args.model
    if chosen_model == "default":
        chosen_model = None

    res = ask_openrouter(
        final_prompt,
        model=chosen_model,
        file_path=args.file_path,
        context_symbol=args.context_symbol,
        out_file=args.out_file,
        clean_fences=args.clean,
        providers=args.providers
    )
    if not res["success"]:
        print(f"\nError: {res['error']}", file=sys.stderr)
        sys.exit(1)
