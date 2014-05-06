from django.test import TestCase
from apps.blog.templatetags.markdown_filter import markdownify

class MarkdownTestCase(TestCase):

    def test_markdown_processor(self):

        text = "# I am a title string"

        html = markdownify(text)
        self.assertEqual("<h1>I am a title string</h1>", html)