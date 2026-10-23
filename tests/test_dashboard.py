"""Browser behavior of the dashboard script embedded by PR 13."""
import os
import tempfile
import unittest

from tests.support import JOURNAL, NOW, render_at, run_probe, sample_data, sample_ins


def rgb(value):
    value = (value or "").strip().lower()
    if value.startswith("#") and len(value) == 7:
        return tuple(int(value[i:i + 2], 16) for i in (1, 3, 5))
    if value.startswith("rgb(") and value.endswith(")"):
        return tuple(int(part.strip()) for part in value[4:-1].split(","))
    raise AssertionError(value)


class DashboardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prev = os.environ.pop("WNAC_JOURNAL", None)
        dest = tempfile.mkdtemp(prefix="wnac-dash-")
        spec = {"data": sample_data(), "ins": sample_ins(), "journal": JOURNAL}
        html, _stale = render_at(dest, spec)
        cls.report = run_probe(html)
        err_html, _stale = render_at(dest + "-err", {"data": sample_data(), "ins": {}})
        cls.err = run_probe(err_html)

    @classmethod
    def tearDownClass(cls):
        if cls.prev is None:
            os.environ.pop("WNAC_JOURNAL", None)
        else:
            os.environ["WNAC_JOURNAL"] = cls.prev

    def test_probe_ran(self):
        self.assertIsNone(self.report["error"])
        self.assertFalse(self.report["mountError"])

    def test_money_and_sidebar_accounts(self):
        self.assertEqual(self.report["money"]["pos"], "$1,500")
        self.assertEqual(self.report["money"]["neg"], "-$400")
        self.assertEqual(self.report["money"]["zero"], "$0")
        self.assertEqual(
            [row["name"] for row in self.report["accounts"]],
            ["Sample Checking", "Sample Card"],
        )
        self.assertEqual(self.report["accounts"][0]["bal"], "$1,500")
        self.assertEqual(self.report["accounts"][1]["bal"], "-$400")
        self.assertEqual(rgb(self.report["accounts"][0]["dot"]), (102, 170, 247))
        self.assertEqual(rgb(self.report["accounts"][1]["dot"]), (245, 133, 87))

    def test_hero_net_flex_and_paydown(self):
        hero = "\n".join(self.report["hero"])
        self.assertIn("$1,100", hero)
        self.assertIn("Assets $1,500", hero)
        self.assertIn("Debts $400", hero)
        self.assertIn("$60 spent", hero)
        self.assertIn("$40 under", hero)
        self.assertIn("25%", hero)
        self.assertIn("$400 left", hero)
        self.assertIn("~4 mo at $100/mo", hero)
        self.assertIn("net worth $1,100", self.report["acctView"])

    def test_follow_the_line_colors(self):
        self.assertEqual(
            [stroke.lower() for stroke in self.report["strokes"]],
            ["#00bb36", "#f5a623", "#ed8001", "#ed8001", "#f3241a"],
        )

    def test_categories_top_seven_and_full_view(self):
        rows = "\n".join(self.report["catRows"])
        self.assertIn("Groceries", rows)
        self.assertIn("$5 uncategorized", rows)
        self.assertIn("2 to review", rows)
        self.assertNotIn("Fees", rows)
        view = "\n".join(self.report["catView"])
        self.assertIn("Fees", view)
        self.assertNotIn("Uncategorized", view)

    def test_recent_chips_and_escaped_payee(self):
        self.assertIn("COFFEE", self.report["recent"][0]["text"])
        self.assertIn("Coffee", self.report["recent"][0]["raw"])
        self.assertIn("REVIEW", self.report["recent"][1]["text"])
        self.assertIn("review", self.report["recent"][1]["raw"])
        self.assertEqual(rgb(self.report["recent"][2]["color"]), (0, 187, 54))
        tx = "\n".join(self.report["txRows"])
        self.assertIn("<b>Odd</b>", tx)
        self.assertNotIn("Opening", tx)

    def test_recurrings_need_three_months(self):
        recur = "\n".join(self.report["recurRows"])
        self.assertIn("Cafe 99", recur)
        self.assertIn("3 mo", recur)
        self.assertIn("-$5", recur)
        self.assertNotIn("Grocery Mart", recur)

    def test_journal_view_and_stamp(self):
        self.assertIn("Sample note", self.report["journal"])
        self.assertIn("<strong>Kept</strong>", self.report["journalHtml"])
        self.assertIn(NOW.strftime("%b %d, %Y %H:%M"), self.report["stamp"])

    def test_insight_chips(self):
        self.assertIn("Sample narrative for the public test.", self.report["insight"])
        self.assertIn("AI blend", self.report["insight"])
        self.assertIn("2 to review", self.report["insight"])
        self.assertIn("on track", self.report["insight"])

    def test_show_view_switches_nav(self):
        self.assertEqual(self.report["navActive"], "dashboard")
        self.assertEqual(self.report["views"]["view-transactions"], "none")
        self.assertEqual(self.report["views"]["view-dashboard"], "")
        self.assertEqual(self.report["afterClick"]["tx"], "")
        self.assertEqual(self.report["afterClick"]["dash"], "none")
        self.assertTrue(self.report["afterClick"]["active"])
        self.assertFalse(self.report["afterClick"]["dashActive"])

    def test_pace_color_and_mount_error(self):
        self.assertEqual(self.report["pace"]["z"], "#00BB36")
        self.assertEqual(self.report["pace"]["n"], "#00BB36")
        self.assertEqual(self.report["pace"]["m"], "#ed8001")
        self.assertEqual(self.report["pace"]["h"], "#f3241a")
        self.assertTrue(self.err["mountError"])
        self.assertEqual(self.err["pace"]["z"], "#00BB36")
