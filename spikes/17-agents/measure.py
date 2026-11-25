#!/usr/bin/env python3
"""The measures of one run, from the event stream of its session (launcher.md, point 6).

  python3 measure.py RUNS/L-B-1                # reads out/session.jsonl and out/log.md
  python3 measure.py --json RUNS/L-B-1

Measures:
  cost_usd        total cost the session reports at its end (sub-agents included); the stream
                  has one result event per turn of the main session (a coordinator that waits
                  for background agents has several) and the cost in each is cumulative
  tokens          token usage of the main session: the sum over the result events
  tokens_all      token usage of every agent, sub-agents included: modelUsage of the last result
  max_context     largest input + cache read + cache creation over the assistant messages of the
                  main session (not of the sub-agents); usage is counted once per message id
  duration_s      wall time from the first to the last timestamped event of the stream
  api_duration_s  duration_api_ms of the last result (cumulative, all agents, may overlap)
  agents          Task/Agent tool calls made by the main session
  discarded       rows the coordinator discarded, summed from the table of out/log.md whose
                  header has a column named like "discarded"; None when there is no such table
  models          every model id seen on assistant messages, main session and sub-agents

Stops with a message when the stream does not report usage per message: the largest context
cannot be estimated by eye.
"""

import argparse
import datetime
import json
import os
import re
import sys

AGENT_TOOLS = ("Task", "Agent")


def events(path):
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as e:
                    raise SystemExit(f"{path}:{n}: not JSON ({e})")


def context_of(usage):
    return (usage.get("input_tokens") or 0) + (usage.get("cache_read_input_tokens") or 0) \
        + (usage.get("cache_creation_input_tokens") or 0)


def wall(stamps):
    if len(stamps) < 2:
        return None
    t = [datetime.datetime.fromisoformat(x.replace("Z", "+00:00")) for x in (min(stamps), max(stamps))]
    return round((t[1] - t[0]).total_seconds(), 1)


def from_stream(path):
    results, init, stamps = [], None, []
    main_ctx = {}          # message id -> context, main session only
    agent_calls = set()
    models = set()
    sub_messages = 0
    for e in events(path):
        t = e.get("type")
        if e.get("timestamp"):
            stamps.append(e["timestamp"])
        if t == "system" and e.get("subtype") == "init" and init is None:
            init = e
        elif t == "assistant":
            m = e.get("message") or {}
            model = m.get("model")
            if model and model != "<synthetic>":
                models.add(model)
            if e.get("parent_tool_use_id"):
                sub_messages += 1
                continue
            usage = m.get("usage")
            if usage is None:
                raise SystemExit(f"{path}: an assistant message of the main session has no usage: "
                                 "the largest context cannot be measured")
            mid = m.get("id") or e.get("uuid")
            main_ctx[mid] = max(main_ctx.get(mid, 0), context_of(usage))
            for block in m.get("content") or []:
                if block.get("type") == "tool_use" and block.get("name") in AGENT_TOOLS:
                    agent_calls.add(block.get("id"))
        elif t == "result":
            results.append(e)
    if not results:
        raise SystemExit(f"{path}: no result event: the session did not end")
    if not main_ctx:
        raise SystemExit(f"{path}: no assistant message of the main session")
    result = results[-1]
    keys = ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens", "output_tokens")
    tokens = {k: sum((r.get("usage") or {}).get(k) or 0 for r in results) for k in keys}
    mu = result.get("modelUsage") or {}
    camel = {"input_tokens": "inputTokens", "cache_read_input_tokens": "cacheReadInputTokens",
             "cache_creation_input_tokens": "cacheCreationInputTokens", "output_tokens": "outputTokens"}
    tokens_all = {k: sum((m.get(c) or 0) for m in mu.values()) for k, c in camel.items()} if mu else None
    costs = [r.get("total_cost_usd") for r in results if r.get("total_cost_usd") is not None]
    if costs != sorted(costs):
        raise SystemExit(f"{path}: the cost of the result events is not cumulative: {costs}")
    return {
        "model_init": init.get("model") if init else None,
        "models": sorted(models),
        "is_error": any(bool(r.get("is_error")) for r in results),
        "stop_reason": result.get("stop_reason"),
        "result_events": len(results),
        "cost_usd": result.get("total_cost_usd"),
        "tokens": tokens,
        "tokens_all": tokens_all,
        "max_context": max(main_ctx.values()),
        "main_messages": len(main_ctx),
        "sub_agent_messages": sub_messages,
        "duration_s": wall(stamps),
        "api_duration_s": round((result.get("duration_api_ms") or 0) / 1000, 1),
        "num_turns": sum(r.get("num_turns") or 0 for r in results),
        "agents": len(agent_calls),
    }


def discarded(log_path):
    """Sum of the 'discarded' column of the first markdown table that has one; None if none."""
    if not os.path.exists(log_path):
        return None
    tables, cur = [], []
    for line in open(log_path, encoding="utf-8").read().splitlines() + [""]:
        s = line.strip()
        if s.startswith("|"):
            cur.append([c.strip() for c in s.strip("|").split("|")])
        elif cur:
            tables.append(cur)
            cur = []
    for rows in tables:
        col = next((i for i, c in enumerate(rows[0]) if "discard" in c.lower()), None)
        if col is None:
            continue
        total = 0
        for cells in rows[1:]:
            if all(set(c) <= set("-: ") for c in cells):
                continue  # the separator row
            m = re.match(r"\d+", cells[col]) if col < len(cells) else None
            total += int(m.group()) if m else 0
        return total
    return None


def measure(run):
    out = from_stream(os.path.join(run, "out", "session.jsonl"))
    out["discarded"] = discarded(os.path.join(run, "out", "log.md"))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("run", help="the folder of one run (RUNS/<case>-<mode>-<n>)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    m = measure(a.run)
    if a.json:
        print(json.dumps(m, indent=1))
    else:
        for k, v in m.items():
            print(f"{k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
