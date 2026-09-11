#!/usr/bin/env python3
"""
The one place this repository knows anything about the Prometheus graph engine.

WHY A SEPARATE MODULE
---------------------
Prometheus is proprietary and lives outside this repository
(`Z:\\_dev-ssd\\prometheus\\prometheus-graph-engine`). It is never vendored, and the
submission export ships none of it. Confining every import, path and
vendor-shaped assumption to this file means:

  * `srq4_experiment.py` stays runnable by an assessor who has scenarios A-C, the
    shipped per-brand CSVs and an OpenAI key, and no engine at all. Importing
    this module is allowed to fail; scenarios D and E then report `unavailable`
    rather than taking the harness down with them.
  * When the vendor moves a symbol, one file breaks, and it breaks loudly here
    instead of silently mid-run.

WHAT D AND E ARE
----------------
The ladder's second half, on a DIFFERENT orchestrator:

    D_prometheus_data        = B_llm_data, run through Prometheus instead of the hosted
                          Code Interpreter. The agent writes and runs its own
                          code against the same series.
    E_prometheus_model  = C_llm_model, run through Prometheus. The agent is told the
                          dedicated model's forecast is authoritative.

D -> E is therefore the SAME intervention as B -> C, on a production agent rather
than a bare API loop. Agreement between the two is a materially stronger claim
than either alone; disagreement is itself a finding about orchestrator coupling.

THE ARCHITECTURE, AND WHY IT IS NOT WHAT THE PLAN ASSUMED (F45)
---------------------------------------------------------------
Prometheus is TWO agents, not one:

  * the conversational agent, whose only data verb is `invoke_prometheus_coder`;
  * a nested coder agent owning all five data tools -- `run_sql`,
    `inspect_schema`, `distinct_values`, `sample_rows`, `execute_code`.

That tool list is hardcoded at module scope in the vendor's
`prometheus_coder.py`, NOT passed through `ProjectDeps`. So DEC-D-SNAPSHOT's
"register the project without the SQL tools" is not achievable by configuration,
and achieving it by edit would make D a fork of Prometheus rather than
Prometheus -- which would forfeit the entire ecological-validity argument that
justifies running D at all.

WHAT WE DO INSTEAD, AND THE HONEST LIMIT OF IT
-----------------------------------------------
The vendor exposes `extra_coder_guardrails` through the LangGraph `configurable`
dict, documented in their own types as "Eval/runtime-only context appended to
coder tasks (not in prod prompts)". It is an eval seam, used here for an eval.

We inject the brand series through it, and instruct the coder to work from that
series alone.

  * **Asserted:** D received exactly the series B received, the model is pinned
    to the same dated snapshot, and no code in the vendor tree was modified.
  * **NOT asserted:** that the agent was *incapable* of issuing SQL.
  * **Measured:** `sql_calls` in every trace. The tool calls are visible in the
    returned message history, so a run that touched the warehouse is DETECTED,
    not assumed away, and `_classify_engine_run` fails it. This is stronger
    evidence than a filtered tool list, because it is observed per run rather
    than configured once and trusted.

Reported in the limitations as written, not softened.

USAGE
    from prometheus_bridge import available, run_prometheus
    ok, why = available()
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Where the engine lives
# ---------------------------------------------------------------------------
# NOT a PATHS.py constant: PATHS.py describes THIS repository's tiers, and the
# engine is a different product that an assessor will not have. Overridable so a
# machine that keeps it elsewhere needs no edit.
_DEFAULT_ENGINE = Path(r"Z:\_dev-ssd\prometheus\prometheus-graph-engine\graph-engine")
ENGINE_DIR = Path(os.environ.get("PROMETHEUS_ENGINE_DIR", _DEFAULT_ENGINE))

# ---------------------------------------------------------------------------
# THE TWO INTERPRETERS -- why D and E run in a subprocess
# ---------------------------------------------------------------------------
# The environments are DISJOINT and neither can be made to satisfy both sides:
#
#   thesis .venv   Python 3.14   xgboost, lightgbm, sklearn   -- no engine
#   engine .venv   Python 3.13   langgraph, pydantic-ai, e2b  -- no xgboost
#
# Verified 2026-09-10: importing the engine from the thesis venv dies on
# `No module named 'azure.storage'`, and importing xgboost from the engine venv
# dies likewise. Scenario E needs BOTH -- the engine to orchestrate, the trained
# booster to forecast.
#
# Merging them is the wrong fix. The engine pins Python 3.13 and a large
# dependency set that this thesis does not control and must not perturb; a
# thesis result that depended on having modified the vendor's environment would
# be neither reproducible nor honest.
#
# So the process boundary IS the fix, and it buys three things beyond mere
# compatibility:
#   * the vendor's imports never enter the harness process, so `srq4_experiment`
#     stays importable by an assessor with no engine at all;
#   * a crash inside the engine cannot take down a paid experiment mid-run;
#   * for Scenario E, the parent evaluates the trained model and passes the
#     PAYLOAD in, so the child never needs xgboost -- which is what makes the
#     split work rather than merely tolerable.
_DEFAULT_PY = ENGINE_DIR / ".venv" / "Scripts" / "python.exe"
if not _DEFAULT_PY.is_file():                       # POSIX layout
    _DEFAULT_PY = ENGINE_DIR / ".venv" / "bin" / "python"
ENGINE_PYTHON = Path(os.environ.get("PROMETHEUS_ENGINE_PYTHON", _DEFAULT_PY))

# True when this process IS the engine-side worker (set by the parent).
IN_WORKER = os.environ.get("SRQ4_ENGINE_WORKER") == "1"

# The vendor's own default coder reasoning effort is "low" (their comment records
# it as 2.3x faster with identical accuracy on their eval suite). Scenarios A-C
# run "medium". Left to default, D and E would differ from B and C by BOTH the
# orchestrator and the reasoning budget -- two variables, so the D->E vs B->C
# comparison would not be attributable.
#
# Pinned to match A-C. Set PROMETHEUS_CODER_REASONING_EFFORT before import to
# override deliberately; the value actually in force is recorded in every trace.
CODER_REASONING_EFFORT = os.environ.get("PROMETHEUS_CODER_REASONING_EFFORT", "medium")
os.environ["PROMETHEUS_CODER_REASONING_EFFORT"] = CODER_REASONING_EFFORT

# The vendor caps the coder loop at UsageLimits(request_limit=40). Mirrored here
# so the harness can report the ceiling it ran under rather than a remembered one.
CODER_REQUEST_LIMIT = 40

# The engine's default per-invoke timeout is 300s. A Prometheus analysis turn
# runs a nested agent with a 40-request budget against a live sandbox, which
# routinely exceeds that; a timeout would be recorded as a scenario failure when
# it is really a harness setting. Raised, and the value in force is traced.
INVOKE_TIMEOUT_S = float(os.environ.get("SRQ4_ENGINE_TIMEOUT_S", "1800"))

_graph = None
_import_error: str | None = None


def _prefixed(model: str) -> str:
    """pydantic-ai model id with an explicit provider prefix."""
    return model if ":" in model else f"openai:{model}"


# ---------------------------------------------------------------------------
# Availability
# ---------------------------------------------------------------------------
def available() -> tuple[bool, str]:
    """(ok, reason). Never raises -- a missing engine is a normal state.

    Import is attempted once and the outcome cached, because importing the
    vendor package builds agents and reads prompt files: expensive, and not
    something to repeat per run.
    """
    global _graph, _import_error
    if _graph is not None:
        return True, "engine loaded"
    if _import_error is not None:
        return False, _import_error

    if not ENGINE_DIR.is_dir():
        _import_error = f"engine not found at {ENGINE_DIR}"
        return False, _import_error

    # config/loader.py reads the PARENT of graph-engine/ for its .env (F42).
    # Checked here because the failure is otherwise a pydantic validation error
    # naming a field, which does not point at the missing file.
    if not (ENGINE_DIR.parent / ".env").is_file():
        _import_error = (f"no .env at {ENGINE_DIR.parent} -- the engine reads the "
                         "PARENT directory, not graph-engine/ (F42)")
        return False, _import_error

    # ENVIRONMENT must be set BEFORE the first import: config/loader.py raises on
    # missing feature groups (Gemini, Logfire, Twilio) for any value other than
    # local/dev, and get_config() caches into a module global on first access, so
    # setting it afterwards is too late. We hold none of those credentials and
    # need none of those features.
    os.environ.setdefault("ENVIRONMENT", "local")

    sys.path.insert(0, str(ENGINE_DIR))
    try:
        from langgraph.checkpoint.memory import InMemorySaver
        from data_agents.projects.prometheus.prometheus import prometheus_graph

        # A CHECKPOINTER IS REQUIRED, and this is not optional plumbing.
        # The graph's last node is `user_input_node`, which calls LangGraph's
        # interrupt() -- that interrupt is what makes one turn terminate rather
        # than looping back into the agent. interrupt() cannot work without a
        # checkpointer, so a graph compiled bare (as `prometheus.py:70` does for
        # the module-level `prometheus` handle) fails at invoke, not at compile.
        #
        # In-memory, not the production Postgres saver: a scenario run is ONE
        # turn and must not inherit state from any other run. Persisting
        # checkpoints across runs would let one observation's context reach the
        # next, which is precisely the contamination the fresh-container rule
        # protects Scenario B from.
        _graph = prometheus_graph.compile(checkpointer=InMemorySaver())
        return True, "engine loaded"
    except Exception as e:                      # noqa: BLE001 -- any failure is "unavailable"
        _import_error = f"{type(e).__name__}: {str(e)[:200]}"
        return False, _import_error


# ---------------------------------------------------------------------------
# Reading a finished run
# ---------------------------------------------------------------------------
def _answer_text(state) -> str:
    """The prose the engine would have shown a user.

    `message_to_human` is a Message of parts; only text parts are scored. An
    image part is a chart, which the scoring path cannot read and must not
    silently treat as an empty answer.
    """
    msg = (state or {}).get("message_to_human")
    if msg is None:
        return ""
    parts = getattr(msg, "parts", None) or []
    out = []
    for p in parts:
        t = getattr(p, "text", None)
        if t:
            out.append(t)
    return "\n".join(out)


def _tool_calls(state) -> list[str]:
    """Every tool name the nested coder invoked, in order.

    This is the evidence that makes the DEC-D-SNAPSHOT limit checkable rather
    than assumed. The vendor accumulates the coder's messages into
    `nested_agent_messages` specifically so a caller can inspect them.

    Read defensively: pydantic-ai part classes vary by version, and a rename
    upstream must degrade to "no calls observed" -- which `_classify_engine_run`
    treats as a REASON TO FAIL a scenario-D run, never as a pass. A silent
    empty list is exactly the F21-class failure this project keeps hitting, so
    the absence of evidence is not read as evidence of absence.
    """
    names: list[str] = []
    for m in (state or {}).get("nested_agent_messages") or []:
        for part in (getattr(m, "parts", None) or []):
            n = getattr(part, "tool_name", None)
            if n:
                names.append(str(n))
    return names


def _code_written(state) -> list[str]:
    """The SOURCE the nested coder executed, in order.

    Scenario B's code blocks are cached in full, so B's method is auditable.
    D's were not: the run recorded `['execute_code'] * 4` and discarded what was
    in them (2026-09-11). On the one comparison where both arms write code, only
    one could be read.

    Same defensive posture as `_tool_calls`: arguments vary in shape by
    pydantic-ai version, so every access degrades to "nothing captured" rather
    than raising. An empty list here is NOT used to fail a run -- `_tool_calls`
    already carries that duty, and duplicating it would fail D for a vendor
    rename in a field that is documentary rather than evidential.
    """
    out: list[str] = []
    for m in (state or {}).get("nested_agent_messages") or []:
        for part in (getattr(m, "parts", None) or []):
            if getattr(part, "tool_name", None) != "execute_code":
                continue
            a = getattr(part, "args", None)
            if isinstance(a, str):
                out.append(a)
                continue
            if isinstance(a, dict):
                for k in ("code", "source", "python", "script"):
                    if isinstance(a.get(k), str):
                        out.append(a[k])
                        break
    return out


def _usage_from(state) -> dict:
    """Token usage, if the engine surfaced it.

    The graph does not promise usage in its state, so this may legitimately
    return zeros. Recorded as `usage_reported: False` rather than passed off as
    a measurement of zero -- D and E cost money whatever this says, and the
    billing endpoint is the ground truth for the reported figure (as it already
    is for A-C's container charge).
    """
    tot = {"tokens_in": 0, "tokens_out": 0, "tokens_cached_in": 0,
           "tokens_reasoning": 0}
    seen = False
    for m in ((state or {}).get("nested_agent_messages") or []) + \
             ((state or {}).get("messages") or []):
        u = getattr(m, "usage", None)
        if u is None:
            continue
        seen = True
        tot["tokens_in"] += getattr(u, "input_tokens", 0) or getattr(u, "request_tokens", 0) or 0
        tot["tokens_out"] += getattr(u, "output_tokens", 0) or getattr(u, "response_tokens", 0) or 0
    return tot, seen


_SQL_TOOLS = ("run_sql", "inspect_schema", "distinct_values", "sample_rows")


def classify_engine_run(calls: list[str], answer: str, err: str | None,
                        require_code: bool, expect_calls: bool = True) -> tuple[str, dict]:
    """Scenario-D/E outcome, from observed evidence only.

    Returns (verdict, evidence). `ok` is the ONLY passing verdict, and it
    requires positive evidence rather than the absence of a complaint --
    the discipline F21 exists to enforce.

    `expect_calls` is False for Scenario E, where making NO tool call is the
    correct behaviour. E's forecast is computed in the parent and handed to the
    engine in its prompt, because the trained booster needs xgboost and the
    vendor interpreter does not have it (F46). The engine's job is to report and
    interpret that payload, so an empty tool list is compliance, not silence.

    Measured 2026-09-11: E was classified `no_evidence` on a run where it had
    reported the model's figures exactly -- forecast, interval, confidence tier
    and WMAPE all correct, and identical to Scenario C's. The rule was right for
    D and wrong for E, and applying one rule to both scenarios is what hid it.

    What replaces the tool call as E's evidence is NOT weaker: the parent
    already asserts `payload_complete` before dispatching, and already overrides
    the result with the model's own number. So E is verified on the payload it
    injected rather than on a call it was never supposed to make.
    """
    ev = {"sql_calls": [c for c in calls if c in _SQL_TOOLS],
          "code_calls": sum(1 for c in calls if c == "execute_code"),
          "all_calls": calls}
    if err:
        return "code_error", ev
    # A warehouse query means the run did not read the snapshot it was given, so
    # it is not comparable to B and cannot be pooled with D. Excluded loudly.
    if ev["sql_calls"]:
        return "warehouse_access", ev
    if not calls and expect_calls:
        # Either the coder was never invoked, or the vendor renamed the part
        # attribute this reads. Both mean the run is unverifiable, and an
        # unverifiable run is not a passing run.
        #
        # Guarded by `expect_calls` so this stays a real check for D while not
        # failing E for behaving correctly. Note it still fires for E if the
        # vendor renames the attribute AND E is later asked to call a tool --
        # the guard narrows the rule, it does not remove it.
        return "no_evidence", ev
    if require_code and not ev["code_calls"]:
        return "no_code", ev
    if not (answer or "").strip():
        return "no_forecast", ev
    return "ok", ev


# ---------------------------------------------------------------------------
# Invocation
# ---------------------------------------------------------------------------
def run_prometheus(user_message: str, coder_context: str, model: str,
                   timeout_s: float | None = None) -> dict:
    """One turn through the engine. Returns a plain dict; never raises.

    `coder_context` is injected via the vendor's documented eval seam
    (`extra_coder_guardrails` -> `ProjectDeps.runtime_coder_context`), which is
    prepended to the coder's brief. Nothing in the vendor tree is modified.

    Both models are pinned explicitly. The vendor's ProjectDeps carries the
    FLOATING alias "gpt-5.5"; DEC-VENDOR requires the dated snapshot, and an
    alias silently re-points, which would break reproducibility mid-study. The
    override is the same mechanism the vendor's own evals use.
    """
    ok, why = available()
    if not ok:
        return {"error": f"engine unavailable: {why}", "answer": "",
                "state": None, "elapsed_s": 0.0}
    timeout_s = INVOKE_TIMEOUT_S if timeout_s is None else timeout_s

    from schemas.message_models import Message, TextPart   # noqa: PLC0415

    state_in = {
        "latest_user_message": Message(parts=[TextPart(type="text", text=user_message)]),
        "messages": [],
        "message_to_human": None,
        "images_generated": [],
        "nested_agent_messages": [],
        # Named so a run is identifiable in any vendor-side log, and so two
        # concurrent runs cannot be confused for one another.
        "conversation_id": f"srq4-{int(time.time() * 1000)}",
        # user_id is DELIBERATELY ABSENT. The project sets use_memory=True, so a
        # user_id makes the graph call the Hindsight memory service and build a
        # cross-conversation memory context. That would carry information
        # between observations -- a brand forecast remembered into the next
        # brand's run -- which breaks the independence every repeat assumes.
        # Omitted, the graph logs a warning and skips the call.
        "graph_name": "prometheus_pydantic",
    }
    config = {"configurable": {
        "extra_coder_guardrails": coder_context,
        # The `openai:` prefix is explicit. The vendor sets a bare "gpt-5.5",
        # which pydantic-ai still resolves but only through a deprecated
        # legacy-prefix path that emits a DeprecationWarning -- and would raise
        # outright under `-W error`. Being explicit also keeps the pin readable.
        "main_agent_model": _prefixed(model),
        "coder_model": _prefixed(model),
        "thread_id": state_in["conversation_id"],
    }}

    t0 = time.perf_counter()

    async def _go():
        state, err = None, None
        try:
            state = await asyncio.wait_for(_graph.ainvoke(state_in, config),
                                           timeout=timeout_s)
        except Exception as e:                              # noqa: BLE001
            err = f"{type(e).__name__}: {str(e)[:300]}"
            # Read the checkpoint even on failure: a run that timed out has
            # very likely created a sandbox, and that is exactly the case where
            # forgetting to kill it leaks one.
            try:
                snap = await _graph.aget_state(config)
                state = getattr(snap, "values", None)
            except Exception:                               # noqa: BLE001
                state = None
        killed = await _kill_sandbox(state)
        return state, err, killed

    # The graph is async. asyncio.run() builds and tears down its own loop, so
    # the harness stays synchronous and D/E slot into the same run loop as
    # A/B/C without colouring the caller.
    import asyncio                                          # noqa: PLC0415
    try:
        state, err, killed = asyncio.run(_go())
    except Exception as e:                                  # noqa: BLE001
        return {"error": f"{type(e).__name__}: {str(e)[:300]}", "answer": "",
                "state": None, "sandbox_killed": None,
                "elapsed_s": round(time.perf_counter() - t0, 2)}

    return {"error": err, "answer": "" if err else _answer_text(state),
            "state": state, "sandbox_killed": killed,
            "elapsed_s": round(time.perf_counter() - t0, 2)}


async def _kill_sandbox(state) -> str | None:
    """Kill the E2B sandbox a run created. Returns its id, or None.

    TWO reasons, and the second is the one that matters for the results.

    1. Cost and hygiene: an unkilled sandbox bills until it times out.
    2. **Contamination.** The engine reuses `state["code_interpreter_id"]`
       across turns, and the coder's kernel keeps `df`, `df_1`, `df_2`... alive
       in it. A sandbox surviving into another observation would let one brand's
       DataFrame be visible while forecasting another -- silently, and it would
       look like unusually good performance rather than like a bug.

       Scenario B gets a fresh container per call by construction
       (`container: auto`). D and E must match that, or the arms are not
       comparable.

    Failure to kill is reported, never raised: the forecast is already produced,
    and losing a scored run to a teardown error would be the wrong trade.
    """
    sid = (state or {}).get("code_interpreter_id")
    if not sid:
        return None
    try:
        from e2b_code_interpreter import AsyncSandbox   # noqa: PLC0415
        sandbox = await AsyncSandbox.connect(sid)
        await sandbox.kill()
    except Exception:                                   # noqa: BLE001
        return f"{sid} (kill failed)"
    return sid


# ---------------------------------------------------------------------------
# Parent side: dispatch one run into the engine interpreter
# ---------------------------------------------------------------------------
def engine_available() -> tuple[bool, str]:
    """(ok, reason) as seen from the HARNESS process. Never raises.

    Checks the engine interpreter can actually import the graph, by asking it.
    Cheap (one subprocess, no API call), and it fails here rather than
    mid-experiment. Cached for the process lifetime.
    """
    global _engine_probe
    if _engine_probe is not None:
        return _engine_probe
    if not ENGINE_DIR.is_dir():
        _engine_probe = (False, f"engine not found at {ENGINE_DIR}")
        return _engine_probe
    if not ENGINE_PYTHON.is_file():
        _engine_probe = (False, f"engine interpreter not found at {ENGINE_PYTHON}")
        return _engine_probe
    if not (ENGINE_DIR.parent / ".env").is_file():
        _engine_probe = (False, f"no .env at {ENGINE_DIR.parent} -- the engine reads "
                                "the PARENT directory, not graph-engine/ (F42)")
        return _engine_probe
    r = _dispatch({"op": "probe"}, timeout_s=180)
    _engine_probe = (bool(r.get("ok")), str(r.get("reason") or r.get("error") or "?"))
    return _engine_probe


_engine_probe: tuple[bool, str] | None = None


def _dispatch(request: dict, timeout_s: float) -> dict:
    """Run one request in the engine interpreter and return its JSON reply.

    The request goes in on stdin and the reply comes back on the LAST line of
    stdout. Not the whole of stdout: importing the engine prints integration
    warnings, and the sandbox may print anything at all. Parsing the last line
    keeps a chatty dependency from corrupting the result -- and the rest of
    stdout is kept as `stdout_log`, because for Scenario D the code the agent
    ran is qualitative evidence, not noise.
    """
    import subprocess                                       # noqa: PLC0415
    env = dict(os.environ)
    env["SRQ4_ENGINE_WORKER"] = "1"
    env.setdefault("ENVIRONMENT", "local")
    env["PROMETHEUS_CODER_REASONING_EFFORT"] = CODER_REASONING_EFFORT
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        p = subprocess.run([str(ENGINE_PYTHON), str(Path(__file__).resolve())],
                           input=json.dumps(request), capture_output=True,
                           text=True, encoding="utf-8", errors="replace",
                           timeout=timeout_s, cwd=str(ENGINE_DIR), env=env)
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"engine subprocess exceeded {timeout_s}s"}
    except Exception as e:                                  # noqa: BLE001
        return {"ok": False, "error": f"{type(e).__name__}: {str(e)[:200]}"}

    lines = [ln for ln in (p.stdout or "").splitlines() if ln.strip()]
    for ln in reversed(lines):
        if ln.lstrip().startswith("{"):
            try:
                out = json.loads(ln)
                out["stdout_log"] = "\n".join(lines[:-1])[-4000:]
                return out
            except json.JSONDecodeError:
                continue
    return {"ok": False,
            "error": f"engine subprocess returned no JSON (rc={p.returncode})",
            "stderr": (p.stderr or "")[-1500:], "stdout_log": "\n".join(lines)[-2000:]}


def call_engine(user_message: str, coder_context: str, model: str,
                timeout_s: float | None = None) -> dict:
    """One scenario run through Prometheus, from the harness process.

    This is the ONLY function scenarios D and E call. Never raises: an
    unavailable engine is a recorded outcome, not a crashed experiment.
    """
    ok, why = engine_available()
    if not ok:
        return {"error": f"engine unavailable: {why}", "answer": "",
                "calls": [], "elapsed_s": 0.0, "usage_reported": False}
    t = INVOKE_TIMEOUT_S if timeout_s is None else timeout_s
    r = _dispatch({"op": "run", "user_message": user_message,
                   "coder_context": coder_context, "model": model,
                   "timeout_s": t},
                  # A margin over the in-graph timeout, so the graph's own
                  # timeout fires first and returns a usable partial record
                  # rather than the parent killing it and learning nothing.
                  timeout_s=t + 120)
    r.setdefault("calls", [])
    r.setdefault("answer", "")
    r.setdefault("elapsed_s", 0.0)
    return r


def engine_fingerprint() -> dict:
    """What was actually run, for the trace.

    Read from the vendor module rather than restated, so it cannot drift from
    the engine that produced the answer -- the generated-artefact-provenance
    rule applied to a configuration rather than a number.
    """
    fp = {"engine_dir": str(ENGINE_DIR),
          "coder_reasoning_effort": CODER_REASONING_EFFORT,
          "coder_request_limit": CODER_REQUEST_LIMIT}
    try:
        from data_agents.projects.prometheus.prometheus import (  # noqa: PLC0415
            prometheus_project_deps as d)
        fp["vendor_main_agent_model"] = d.main_agent_model
        fp["vendor_coder_model"] = d.coder_model
        fp["vendor_tool_names"] = list(d.tool_names)
        fp["agent_name"] = d.agent_name
    except Exception as e:                                  # noqa: BLE001
        fp["fingerprint_error"] = str(e)[:150]
    return fp


# ---------------------------------------------------------------------------
# Worker entry point -- runs under the ENGINE interpreter
# ---------------------------------------------------------------------------
def _worker() -> int:
    """Read one request from stdin, print one JSON reply as the last stdout line."""
    req = json.loads(sys.stdin.read() or "{}")
    op = req.get("op")

    if op == "probe":
        ok, why = available()
        out = {"ok": ok, "reason": why}
        if ok:
            out["fingerprint"] = engine_fingerprint()
        print(json.dumps(out, default=str))
        return 0

    if op == "run":
        r = run_prometheus(req["user_message"], req["coder_context"],
                           req["model"], req.get("timeout_s"))
        state = r.pop("state", None)
        usage, seen = _usage_from(state)
        calls = _tool_calls(state)
        print(json.dumps({"ok": r["error"] is None, "answer": r["answer"],
                          "error": r["error"], "elapsed_s": r["elapsed_s"],
                          "sandbox_killed": r.get("sandbox_killed"),
                          "calls": calls, "usage": usage,
                          "usage_reported": seen,
                          "code_written": _code_written(state),
                          "fingerprint": engine_fingerprint()}, default=str))
        return 0

    print(json.dumps({"ok": False, "error": f"unknown op {op!r}"}))
    return 2


def _selftest() -> int:
    """Free check that the engine can be reached. Sends no request to any model."""
    print(f"engine dir:     {ENGINE_DIR}")
    print(f"engine python:  {ENGINE_PYTHON}")
    print(f"harness python: {sys.executable}")
    print(f"coder effort:   {CODER_REASONING_EFFORT} (A-C run 'medium')")
    print(f"invoke timeout: {INVOKE_TIMEOUT_S}s")
    ok, why = engine_available()
    print(f"\nengine reachable: {ok} -- {why}")
    if ok:
        r = _dispatch({"op": "probe"}, timeout_s=180)
        fp = r.get("fingerprint") or {}
        print(f"  vendor main model: {fp.get('vendor_main_agent_model')}")
        print(f"  vendor coder model: {fp.get('vendor_coder_model')}")
        tools = fp.get("vendor_tool_names") or []
        sql = [t for t in tools if t in _SQL_TOOLS]
        print(f"  conversational tools: {len(tools)}")
        print(f"  SQL tools on the conversational agent: {sql or 'none (F45)'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(_worker() if IN_WORKER else _selftest())
