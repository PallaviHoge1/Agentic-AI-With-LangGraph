# src/utils/llm_client.py
"""
Flexible Ollama caller.

Tries, in order:
  1. Python 'ollama' package (if installed and compatible).
  2. CLI: ollama run MODEL --prompt "..."
  3. CLI: ollama run MODEL (feed prompt to stdin)

This file decodes CLI output as UTF-8 to avoid Windows UnicodeDecodeError.
"""

import os
import shlex
import subprocess
from typing import Optional

MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
CLI_TIMEOUT = 60  # seconds


def _try_python_package(prompt: str, max_tokens: int = 512, temperature: float = 0.0) -> Optional[str]:
    try:
        import ollama  # type: ignore
    except Exception:
        return None

    try:
        # Many versions of the ollama package expose different APIs.
        # We'll attempt a couple of common call patterns and be tolerant.
        # 1) Ollama client with generate(...)
        if hasattr(ollama, "Ollama"):
            client = ollama.Ollama()
            if hasattr(client, "generate"):
                resp = client.generate(model=MODEL, prompt=prompt, max_tokens=max_tokens, temperature=temperature)
                # resp may be dict-like or string
                if isinstance(resp, dict):
                    return resp.get("text") or resp.get("content") or str(resp)
                return str(resp)
            # try chat-like API
            if hasattr(client, "chat"):
                resp = client.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
                if isinstance(resp, dict):
                    return resp.get("text") or resp.get("content") or str(resp)
                return str(resp)
        # 2) Some package exposes top-level generate(...)
        if hasattr(ollama, "generate"):
            resp = ollama.generate(model=MODEL, prompt=prompt, max_tokens=max_tokens, temperature=temperature)
            if isinstance(resp, dict):
                return resp.get("text") or resp.get("content") or str(resp)
            return str(resp)

    except Exception:
        # If python package exists but API differs, just bail to CLI fallback.
        return None

    return None


def _run_cli_with_prompt(prompt: str) -> Optional[str]:
    """
    Try: ollama run MODEL --prompt "PROMPT"
    """
    # quote model and prompt properly
    model_quoted = shlex.quote(MODEL)
    # escape double quotes inside prompt
    safe_prompt = prompt.replace('"', '\\"')
    cmd = f'ollama run {model_quoted} --prompt "{safe_prompt}"'
    try:
        completed = subprocess.run(cmd, shell=True, capture_output=True, timeout=CLI_TIMEOUT)
        stdout = completed.stdout.decode("utf-8", errors="ignore").strip()
        stderr = completed.stderr.decode("utf-8", errors="ignore").strip()
        if completed.returncode == 0 and stdout:
            return stdout
        # If the CLI returns JSON or extra text, return stdout if present, else raise later
        if stdout:
            return stdout
        if stderr and "unknown command" in stderr.lower():
            # indicates this CLI form is not supported
            return None
        return None
    except Exception:
        return None


def _run_cli_with_stdin(prompt: str) -> Optional[str]:
    """
    Try: echo "PROMPT" | ollama run MODEL
    or: ollama run MODEL  (send prompt to stdin)
    """
    cmd = ["ollama", "run", MODEL]
    try:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate(input=prompt.encode("utf-8"), timeout=CLI_TIMEOUT)
        out_text = stdout.decode("utf-8", errors="ignore").strip()
        err_text = stderr.decode("utf-8", errors="ignore").strip()
        if proc.returncode == 0 and out_text:
            return out_text
        # If returncode non-zero but stdout has something, still return it
        if out_text:
            return out_text
        # Otherwise return None so caller can try other fallbacks or raise
        return None
    except Exception:
        return None


def call_llm(prompt: str) -> str:
    """
    Main entry point to call the local Ollama model.
    Tries python package first, then two CLI forms. Raises RuntimeError if all fail.
    """
    # 1) Try python package
    try:
        res = _try_python_package(prompt)
        if res:
            return res.strip()
    except Exception:
        pass

    # 2) Try CLI with --prompt
    res = _run_cli_with_prompt(prompt)
    if res:
        return res.strip()

    # 3) Try CLI by feeding prompt to stdin
    res = _run_cli_with_stdin(prompt)
    if res:
        return res.strip()

    # If we reached here, nothing worked — produce a helpful error.
    # Provide diagnostics: is 'ollama' on PATH? is model pulled?
    raise RuntimeError(
        "Could not call Ollama. Tried python package and common CLI forms.\n"
        "- Ensure 'ollama' is installed and on your PATH.\n"
        "- Ensure the model is pulled, e.g. `ollama pull llama3.2:3b` or set OLLAMA_MODEL env var.\n"
        "- You can test manually in a terminal:\n"
        "    ollama run llama3.2:3b --prompt \"Hello\"\n"
        "  or\n"
        "    ollama run llama3.2:3b   (then type/paste prompt and press Ctrl-D)\n"
        f"- Current OLLAMA_MODEL={MODEL}"
    )
