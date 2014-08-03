from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

import json

from .templatetags.markdown_filter import markdownify
from .views import process_draft_post


class MarkdownTestCase(TestCase):

    def test_markdown_processor(self):

        text = "# I am a title string"

        html = markdownify(text)
        self.assertEqual("<h1>I am a title string</h1>", html)

    def test_process_draft_post(self):

        client = Client()

        data = json.dumps({
            'id': 1,
            'name': "Test Post",
            'content': "Wooooo"})

        request = client.post(reverse('blog:process_draft_post'), data=data,
            content_type='application/x-www-form-urlencoded')

        response = process_draft_post(request)
