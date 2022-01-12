import pytest

from h.util import markdown


class TestRender:
    def test_it_renders_markdown(self):
        actual = markdown.render("_emphasis_ **bold**")
        assert actual == "<p><em>emphasis</em> <strong>bold</strong></p>\n"

    def test_it_ignores_math_block(self):
        actual = markdown.render("$$1 + 1 = 2$$")
        assert actual == "<p>$$1 + 1 = 2$$</p>\n"

    def test_it_ignores_inline_math(self):
        actual = markdown.render(r"Foobar \(1 + 1 = 2\)")
        assert actual == "<p>Foobar \\(1 + 1 = 2\\)</p>\n"

    @pytest.mark.parametrize(
        "text",
        [
            '<p><a href="mailto:foo@example.net">example</a></p>',  # Don't add rel and target attrs to mailto: links
            '<p><a title="foobar">example</a></p>',
            '<p><a href="https://example.org" rel="nofollow noopener" target="_blank" title="foobar">example</a></p>',
            "<blockquote>Foobar</blockquote>",
            "<p><code>foobar</code></p>",
            "<p><em>foobar</em></p>",
            "<hr>",
            "<h1>foobar</h1>",
            "<h2>foobar</h2>",
            "<h3>foobar</h3>",
            "<h4>foobar</h4>",
            "<h5>foobar</h5>",
            "<h6>foobar</h6>",
            '<p><img src="http://example.com/img.jpg"></p>',
            '<p><img src="/img.jpg"></p>',
            '<p><img alt="foobar" src="/img.jpg"></p>',
            '<p><img src="/img.jpg" title="foobar"></p>',
            '<p><img alt="hello" src="/img.jpg" title="foobar"></p>',
            "<ol><li>foobar</li></ol>",
            "<p>foobar</p>",
            "<pre>foobar</pre>",
            "<p><strong>foobar</strong></p>",
            "<ul><li>foobar</li></ul>",
        ],
    )
    def test_it_allows_markdown_html(self, text):
        # HTML tags that Markdown can output are allowed through unsanitized.
        assert markdown.render(text) == text

    @pytest.mark.parametrize(
        "text,expected",
        [
            ("<script>evil()</script>", "&lt;script&gt;evil()&lt;/script&gt;"),
            (
                '<a href="#" onclick="evil()">foobar</a>',
                '<p><a href="#" rel="nofollow noopener" target="_blank">foobar</a></p>\n',
            ),
            (
                '<a href="#" onclick=evil()>foobar</a>',
                '<p><a href="#" rel="nofollow noopener" target="_blank">foobar</a></p>\n',
            ),
            (
                "<a href=\"javascript:alert('evil')\">foobar</a>",
                "<p><a>foobar</a></p>\n",
            ),
            (
                '<img src="/evil.jpg" onclick="evil()">',
                '<p><img src="/evil.jpg"></p>\n',
            ),
            ("<img src=\"javascript:alert('evil')\">", "<p><img></p>\n"),
        ],
    )
    def test_it_escapes_evil_html(self, text, expected):
        assert markdown.render(text) == expected

    def test_it_adds_target_blank_and_rel_nofollow_to_links(self):
        actual = markdown.render('<a href="https://example.org">Hello</a>')
        expected = '<p><a href="https://example.org" rel="nofollow noopener" target="_blank">Hello</a></p>\n'

        assert actual == expected
