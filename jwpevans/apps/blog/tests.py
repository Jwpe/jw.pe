from django.contrib.auth.models import User
from django.test import TestCase

import json
import mock

from .templatetags.markdown_filter import markdownify
from .views import create_post, process_draft_post


class MarkdownTestCase(TestCase):

    def test_markdown_processor(self):

        text = "# I am a title string"

        html = markdownify(text)
        self.assertEqual("<h1>I am a title string</h1>", html)

    @mock.patch('blog.views.create_post')
    def test_process_draft_post(self, mock_create_post):

        mock_post = mock.Mock()
        mock_post.get_absolute_url.return_value = "http://www.jw.pe/blog/a-post"
        mock_create_post.return_value = mock_post

        data = {'id': 1, 'name': "Test Post", 'content': "Wooooo"}

        mock_request = mock.Mock()
        mock_request.method = "POST"
        mock_request.body = json.dumps(data)

        response = process_draft_post(mock_request)

        self.assertEqual("http://www.jw.pe/blog/a-post", response['location'])

        mock_create_post.assert_called_once_with(data=data)

    def test_create_post(self):

        User.objects.create(username='Jonathan')

        data = {'id': 1, 'name': "Test Post", 'content': "Wooooo"}

        post = create_post(data=data)

        self.assertEqual('Test Post', post.title)
        self.assertEqual('test-post', post.slug)
        self.assertEqual(1, post.draft_id)
        self.assertEqual("Wooooo", post.body)
        self.assertEqual("Wooooo...", post.tease)
