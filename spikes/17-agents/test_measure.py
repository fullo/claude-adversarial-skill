"""Tests for measure.py, on a real stream: the lines of run tuning-B-2 (Sonnet 5.5, medium effort)
that measure.py reads, copied as they were: the init event, every assistant message of the
coordinator, two of the sub-agents, the nine result events, and the first and last timestamped
events.

  python3 -m unittest discover -s spikes/17-agents -p test_measure.py

The expected values were read off the stream by hand. The coordinator waited for background
agents, so its stream has one result event per turn (nine); the cost in each is cumulative
(4.0052182 USD in all of them) and the last one's modelUsage covers the sub-agents too. The
largest context of the coordinator: input 2, cache read 150629, cache creation 2277 (152908).
It called the Agent tool nine times. First event 10:31:46.019Z, last 10:46:53.861Z (907.8 s).
Each message id appears more than once in the stream (one line per content block), with the same
usage: it is counted once.
"""

import json
import os
import shutil
import tempfile
import unittest

import measure

HERE = os.path.dirname(os.path.abspath(__file__))
STREAM = os.path.join(HERE, "results", "fixtures", "tuning-B-2.session.jsonl")


class RealStream(unittest.TestCase):
    def setUp(self):
        self.m = measure.from_stream(STREAM)

    def test_model(self):
        self.assertEqual(self.m["model_init"], "claude-sonnet-5-5")
        self.assertEqual(self.m["models"], ["claude-sonnet-5-5"])

    def test_cost_is_the_last_cumulative_one(self):
        self.assertEqual(self.m["result_events"], 9)
        self.assertAlmostEqual(self.m["cost_usd"], 4.0052182)
        self.assertFalse(self.m["is_error"])

    def test_duration_is_wall_time(self):
        self.assertEqual(self.m["duration_s"], 907.8)

    def test_max_context_is_main_session_only(self):
        self.assertEqual(self.m["max_context"], 2 + 150629 + 2277)
        self.assertEqual(self.m["sub_agent_messages"], 2)

    def test_messages_counted_once_per_id(self):
        self.assertEqual(self.m["main_messages"], 31)

    def test_agents(self):
        self.assertEqual(self.m["agents"], 9)

    def test_tokens(self):
        self.assertEqual(self.m["tokens"]["output_tokens"], 43057)        # main session, summed
        self.assertEqual(self.m["tokens_all"]["output_tokens"], 178219)   # every agent


class Failures(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir)

    def write(self, events):
        p = os.path.join(self.dir, "s.jsonl")
        with open(p, "w", encoding="utf-8") as f:
            f.write("\n".join(json.dumps(e) for e in events) + "\n")
        return p

    def test_no_usage_stops(self):
        p = self.write([{"type": "assistant", "message": {"id": "a", "content": []}},
                        {"type": "result", "total_cost_usd": 1}])
        with self.assertRaises(SystemExit) as c:
            measure.from_stream(p)
        self.assertIn("largest context cannot be measured", str(c.exception))

    def test_no_result_stops(self):
        p = self.write([{"type": "assistant", "message": {"id": "a", "usage": {}, "content": []}}])
        with self.assertRaises(SystemExit):
            measure.from_stream(p)

    def test_cost_not_cumulative_stops(self):
        a = {"type": "assistant", "message": {"id": "a", "usage": {}, "content": []}}
        p = self.write([a, {"type": "result", "total_cost_usd": 2}, {"type": "result", "total_cost_usd": 1}])
        with self.assertRaises(SystemExit):
            measure.from_stream(p)


class Log(unittest.TestCase):
    def test_discarded_column(self):
        d = tempfile.mkdtemp()
        try:
            p = os.path.join(d, "log.md")
            with open(p, "w", encoding="utf-8") as f:
                f.write("# Log\n\n| Role | Files | Rows returned | Rows discarded |\n|---|---|---|---|\n"
                        "| Code | a.py | 12 | 2 |\n| Tests | t.py | 5 | 0 (none) |\n\nDepartures: none.\n")
            self.assertEqual(measure.discarded(p), 2)
            self.assertIsNone(measure.discarded(os.path.join(d, "missing.md")))
        finally:
            shutil.rmtree(d)


if __name__ == "__main__":
    unittest.main()
