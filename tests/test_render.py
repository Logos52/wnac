"""Page assembly from the renderer split in PR 13."""
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from render import main, page
from tests.support import JOURNAL, NOW, render_at, sample_data, sample_ins, write_case


class RenderTest(unittest.TestCase):
    def setUp(self):
        self.dest = tempfile.mkdtemp(prefix="wnac-render-")
        self.prev = os.environ.pop("WNAC_JOURNAL", None)

    def tearDown(self):
        if self.prev is None:
            os.environ.pop("WNAC_JOURNAL", None)
        else:
            os.environ["WNAC_JOURNAL"] = self.prev

    def test_inlines_tokens_data_insights_and_journal(self):
        spec = {"data": sample_data(), "ins": sample_ins(), "journal": JOURNAL}
        html, stale = render_at(self.dest, spec)
        self.assertFalse(stale)
        self.assertIn(".dialwrap", html)
        self.assertIn("--pace-under", html)
        self.assertIn(json.dumps(spec["data"]), html)
        self.assertIn(json.dumps(spec["ins"]), html)
        self.assertIn("<strong>Kept</strong>", html)
        self.assertIn("Sample note", html)
        self.assertIn(NOW.strftime("%b %d, %Y %H:%M"), html)
        self.assertNotIn("/*DATA*/", html)
        self.assertNotIn("/*STAMP*/", html)

    def test_script_has_no_comments(self):
        spec = {"data": {"accounts": [], "transactions": []}, "ins": {}}
        html, _stale = render_at(self.dest, spec)
        start = html.find("<script>")
        script = html[start:html.find("</script>", start)]
        self.assertNotIn("//", script)
        self.assertNotIn("/*", script)

    def test_dated_entries_accept_either_dash(self):
        text = "\n## 2026-01-04 — Sample note\n\n**Kept** the plan\n\n## 2026-02-01 - Next\n\nplain\n"
        spec = {"data": sample_data(), "ins": sample_ins(), "journal": text}
        html, _stale = render_at(self.dest, spec)
        self.assertIn("Next", html)
        self.assertIn("<p>plain</p>", html)

    def test_missing_journal_stays_empty(self):
        spec = {
            "data": sample_data(),
            "ins": sample_ins(),
            "config": {"journal_path": os.path.join(self.dest, "missing.md")},
        }
        html, _stale = render_at(self.dest, spec)
        self.assertIn("const JOURNAL = [];", html)

    def test_env_journal_overrides_config(self):
        spec = {"data": sample_data(), "ins": sample_ins(), "journal": JOURNAL}
        write_case(self.dest, spec)
        other = os.path.join(self.dest, "other.md")
        with open(other, "w") as handle:
            handle.write("\n## 2026-03-03 - From env\n\nenved\n")
        os.environ["WNAC_JOURNAL"] = other
        html, _stale = page(self.dest, NOW)
        self.assertIn("From env", html)
        self.assertNotIn("Sample note", html)

    def test_stale_warning_and_status_line(self):
        spec = {"data": sample_data(), "ins": sample_ins(), "stale": True}
        write_case(self.dest, spec)
        err, out = io.StringIO(), io.StringIO()
        with redirect_stderr(err), redirect_stdout(out):
            main(self.dest, NOW)
        with open(os.path.join(self.dest, "dashboard.html")) as handle:
            html = handle.read()
        note = " — ANALYSIS OUT OF DATE: data.json is newer than insights.json, run analyze.py"
        self.assertIn(note, html)
        self.assertEqual(
            err.getvalue(),
            "WARNING: data.json is newer than insights.json — run analyze.py before render.py, "
            "or the dashboard shows stale analysis\n",
        )
        self.assertTrue(out.getvalue().startswith("wrote dashboard.html ("))
        self.assertTrue(out.getvalue().endswith(" bytes) — open it in a browser\n"))
