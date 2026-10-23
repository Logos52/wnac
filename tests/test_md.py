"""Journal markdown behavior moved into its own module by PR 13."""
import unittest

from render_md import md2html


class MdTest(unittest.TestCase):
    def test_inline(self):
        got = md2html("See **bold** and `code` plus [[Wiki]] and <tag> &")
        self.assertEqual(
            got,
            "<p>See <strong>bold</strong> and <code>code</code> plus Wiki and &lt;tag&gt; &amp;</p>",
        )

    def test_paragraph_joins_lines(self):
        self.assertEqual(md2html("one\ntwo"), "<p>one two</p>")

    def test_heading_quote_rule(self):
        self.assertEqual(md2html("### Title"), "<h4>Title</h4>")
        self.assertEqual(md2html("> note"), "<blockquote>note</blockquote>")
        self.assertEqual(md2html("---"), "<hr>")

    def test_list_and_blank_line(self):
        self.assertEqual(md2html("- a\n* b"), "<ul><li>a</li><li>b</li></ul>")
        self.assertEqual(md2html("  - a\n\nnext"), "<ul><li>a</li></ul><p>next</p>")

    def test_empty(self):
        self.assertEqual(md2html(""), "")
        self.assertEqual(md2html("\n"), "")
