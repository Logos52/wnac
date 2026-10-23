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
        assert self.report["error"] is None
        assert not self.report["mountError"]

    def test_money_and_sidebar_accounts(self):
        assert self.report["money"]["pos"] == "$1,500"
        assert self.report["money"]["neg"] == "-$400"
        assert self.report["money"]["zero"] == "$0"
        names = [row["name"] for row in self.report["accounts"]]
        assert names == ["Sample Checking", "Sample Card"]
        assert self.report["accounts"][0]["bal"] == "$1,500"
        assert self.report["accounts"][1]["bal"] == "-$400"
        assert rgb(self.report["accounts"][0]["dot"]) == (102, 170, 247)
        assert rgb(self.report["accounts"][1]["dot"]) == (245, 133, 87)

    def test_hero_net_flex_and_paydown(self):
        hero = "\n".join(self.report["hero"])
        assert "$1,100" in hero
        assert "Assets $1,500" in hero
        assert "Debts $400" in hero
        assert "$60 spent" in hero
        assert "$40 under" in hero
        assert "25%" in hero
        assert "$400 left" in hero
        assert "~4 mo at $100/mo" in hero
        assert "net worth $1,100" in self.report["acctView"]

    def test_follow_the_line_colors(self):
        strokes = [stroke.lower() for stroke in self.report["strokes"]]
        assert strokes == ["#00bb36", "#f5a623", "#ed8001", "#ed8001", "#f3241a"]

    def test_categories_top_seven_and_full_view(self):
        rows = "\n".join(self.report["catRows"])
        assert "Groceries" in rows
        assert "$5 uncategorized" in rows
        assert "2 to review" in rows
        assert "Fees" not in rows
        view = "\n".join(self.report["catView"])
        assert "Fees" in view
        assert "Uncategorized" not in view

    def test_recent_chips_and_escaped_payee(self):
        assert "COFFEE" in self.report["recent"][0]["text"]
        assert "Coffee" in self.report["recent"][0]["raw"]
        assert "REVIEW" in self.report["recent"][1]["text"]
        assert "review" in self.report["recent"][1]["raw"]
        assert rgb(self.report["recent"][2]["color"]) == (0, 187, 54)
        tx = "\n".join(self.report["txRows"])
        assert "<b>Odd</b>" in tx
        assert "Opening" not in tx

    def test_recurrings_need_three_months(self):
        recur = "\n".join(self.report["recurRows"])
        assert "Cafe 99" in recur
        assert "3 mo" in recur
        assert "-$5" in recur
        assert "Grocery Mart" not in recur

    def test_journal_view_and_stamp(self):
        assert "Sample note" in self.report["journal"]
        assert "<strong>Kept</strong>" in self.report["journalHtml"]
        assert NOW.strftime("%b %d, %Y %H:%M") in self.report["stamp"]

    def test_insight_chips(self):
        assert "Sample narrative for the public test." in self.report["insight"]
        assert "AI blend" in self.report["insight"]
        assert "2 to review" in self.report["insight"]
        assert "on track" in self.report["insight"]

    def test_show_view_switches_nav(self):
        assert self.report["navActive"] == "dashboard"
        assert self.report["views"]["view-transactions"] == "none"
        assert self.report["views"]["view-dashboard"] == ""
        assert self.report["afterClick"]["tx"] == ""
        assert self.report["afterClick"]["dash"] == "none"
        assert self.report["afterClick"]["active"]
        assert not self.report["afterClick"]["dashActive"]

    def test_pace_color_and_mount_error(self):
        assert self.report["pace"]["z"] == "#00BB36"
        assert self.report["pace"]["n"] == "#00BB36"
        assert self.report["pace"]["m"] == "#ed8001"
        assert self.report["pace"]["h"] == "#f3241a"
        assert self.err["mountError"]
        assert self.err["pace"]["z"] == "#00BB36"
