"""Journal markdown behavior moved into its own module by PR 13."""
import unittest

from render_md import md2html


class MdTest(unittest.TestCase):
    def test_inline(self):
        got = md2html("See **bold** and `code` plus [[Wiki]] and <tag> &")
        expect = "<p>See <strong>bold</strong> and <code>code</code> plus Wiki and &lt;tag&gt; &amp;</p>"
        assert got == expect

    def test_paragraph_joins_lines(self):
        assert md2html("one\ntwo") == "<p>one two</p>"

    def test_heading_quote_rule(self):
        assert md2html("### Title") == "<h4>Title</h4>"
        assert md2html("> note") == "<blockquote>note</blockquote>"
        assert md2html("---") == "<hr>"

    def test_list_and_blank_line(self):
        assert md2html("- a\n* b") == "<ul><li>a</li><li>b</li></ul>"
        assert md2html("  - a\n\nnext") == "<ul><li>a</li></ul><p>next</p>"

    def test_empty(self):
        assert md2html("") == ""
        assert md2html("\n") == ""
