"""
Credit-Saver Multi-Agent Swarm Orchestrator (v1.0)
Roles:
  1. Architect Agent (Nemotron Ultra 550B / Reasoning): Breaks requirements into technical specs.
  2. Coder Agent (Gemma-4 MoE / North Mini / Code): Implements clean, complete production code.
  3. Reviewer Agent (OpenRouter Smart Router): Audits code for syntax, missing imports, edge cases.
"""

import sys
import os
import json
import argparse

# Import core runner logic
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from runner import ask_openrouter, strip_code_fences

def run_agent(role_name, system_prompt, task_prompt, model_tier="router", stream=True):
    print(f"\n========================================================", file=sys.stderr)
    print(f"🤖 [AGENT ACTIVATED: {role_name.upper()}] (Tier: {model_tier})", file=sys.stderr)
    print(f"========================================================", file=sys.stderr)
    
    res = ask_openrouter(
        prompt=task_prompt,
        model=model_tier,
        system_prompt=system_prompt,
        stream=stream
    )
    if not res.get("success"):
        raise RuntimeError(f"Agent {role_name} failed: {res.get('error')}")
    return res["content"].strip()

def run_multi_agent_pipeline(user_prompt, out_file=None, clean=True):
    print(f"\n🚀 Initiating Multi-Agent Swarm for Task: \"{user_prompt}\"", file=sys.stderr)

    # -------------------------------------------------------------
    # AGENT 1: ARCHITECT (System Design & Specs)
    # -------------------------------------------------------------
    architect_system = (
        "You are an Elite Software Architect. Your job is to analyze the user request and produce "
        "a concise technical architecture spec: 1. Component hierarchy / state shape. 2. Edge cases. "
        "3. Required helper functions. Keep it concise, practical, and directly actionable for a developer."
    )
    architect_task = f"Plan and architect this feature request:\n\n{user_prompt}"
    architecture_spec = run_agent("Architect", architect_system, architect_task, model_tier="reasoning")

    # -------------------------------------------------------------
    # AGENT 2: CODER (Implementation)
    # -------------------------------------------------------------
    coder_system = (
        "You are a Senior Principal Developer. Given a technical specification, generate clean, complete, "
        "production-ready, self-contained code. Do NOT leave placeholders, TODOs, or conversational chatter. "
        "Return pure code ready to execute."
    )
    coder_task = (
        f"Original User Request: {user_prompt}\n\n"
        f"Technical Architecture Plan by Architect:\n{architecture_spec}\n\n"
        "Now implement the complete production code meeting all requirements."
    )
    generated_code = run_agent("Developer", coder_system, coder_task, model_tier="code")

    # -------------------------------------------------------------
    # AGENT 3: REVIEWER & QA AUDITOR (Self-Correction & Linting)
    # -------------------------------------------------------------
    reviewer_system = (
        "You are an expert QA and Code Auditor. Your job is to inspect the provided code for: "
        "1. Uninstalled third-party imports (replace with native equivalents or standard SVG/CSS). "
        "2. Syntax errors, missing brackets, or unhandled null/undefined cases. "
        "3. Output ONLY the final perfected, working code with any bugs fixed. No markdown chit-chat."
    )
    reviewer_task = (
        f"Inspect and polish this generated code:\n\n{generated_code}\n\n"
        "Verify imports, safety, and correctness. Output the final refined code directly."
    )
    final_polished_code = run_agent("Reviewer & QA", reviewer_system, reviewer_task, model_tier="router")

    if clean:
        final_polished_code = strip_code_fences(final_polished_code)

    if out_file:
        os.makedirs(os.path.dirname(os.path.abspath(out_file)), exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(final_polished_code)
        print(f"\n[Multi-Agent Final Output Successfully Saved to: {out_file}]", file=sys.stderr)

    return {
        "architecture": architecture_spec,
        "raw_code": generated_code,
        "final_code": final_polished_code
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Credit-Saver Multi-Agent Swarm Orchestrator")
    parser.add_argument("prompt", help="Feature request or goal for the agent team")
    parser.add_argument("--out", "-o", dest="out_file", default=None, help="Save final code to file")
    parser.add_argument("--no-clean", action="store_true", help="Do not strip markdown backticks")

    args = parser.parse_args()
    run_multi_agent_pipeline(args.prompt, out_file=args.out_file, clean=not args.no_clean)
