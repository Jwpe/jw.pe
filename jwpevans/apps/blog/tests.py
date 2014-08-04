from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.test import TestCase
from django.test.client import RequestFactory
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

        data = "payload=%7B%22content%22%3A%22%23%23+OMG%5Cn%5Cn%23%23%23+SICK%5Cn%5CnIt+works%22%2C%22created_at%22%3A%222014-08-03T13%3A19%3A39-05%3A00%22%2C%22folder_id%22%3Anull%2C%22id%22%3A402057%2C%22name%22%3A%22Test+Post%22%2C%22parent_id%22%3Anull%2C%22token%22%3Anull%2C%22updated_at%22%3A%222014-08-03T13%3A20%3A04-05%3A00%22%2C%22content_html%22%3A%22%3Ch2%3EOMG%3C%2Fh2%3E%5Cn%5Cn%3Ch3%3ESICK%3C%2Fh3%3E%5Cn%3Cp%3EIt+works%3C%2Fp%3E%22%2C%22content_html_raw%22%3A%22%3Ch2+id%3D%5C%22omg%5C%22%3EOMG%3C%2Fh2%3E%5Cn%5Cn%3Ch3+id%3D%5C%22sick%5C%22%3ESICK%3C%2Fh3%3E%5Cn%3Cp%3EIt+works%3C%2Fp%3E%22%2C%22collaborators_ready%22%3Afalse%2C%22user%22%3A%7B%22email%22%3A%22jwpevans%40gmail.com%22%2C%22id%22%3A204341%7D%7D"

        factory = RequestFactory()
        mock_request = factory.post(reverse('blog:process_draft_post'), data=data,
            content_type='application/x-www-form-urlencoded')

        response = process_draft_post(mock_request)

        self.assertEqual("http://www.jw.pe/blog/a-post", response['location'])

        blog_post_data = {"content": "## OMG\n\n### SICK\n\nIt works",
            "created_at": "2014-08-03T13:19:39-05:00",
            "folder_id": None,
            "id": 402057,
            "name": "Test Post",
            "parent_id": None,
            "token": None,
            "updated_at": "2014-08-03T13:20:04-05:00",
            "content_html": "<h2>OMG</h2>\n\n<h3>SICK</h3>\n<p>It works</p>",
            "content_html_raw": "<h2 id=\"omg\">OMG</h2>\n\n<h3 id=\"sick\">SICK</h3>\n<p>It works</p>",
            "collaborators_ready": False,
            "user": {"email": "jwpevans@gmail.com", "id": 204341}}
        mock_create_post.assert_called_once_with(data=blog_post_data)

    def test_create_post(self):

        User.objects.create(username='Jonathan')

        data = {'id': 1, 'name': "Test Post", 'content': "Wooooo"}

        post = create_post(data=data)

        self.assertEqual('Test Post', post.title)
        self.assertEqual('test-post', post.slug)
        self.assertEqual(1, post.draft_id)
        self.assertEqual("Wooooo", post.body)
        self.assertEqual("Wooooo...", post.tease)
        self.assertEqual('/blog/post/test-post/', post.get_absolute_url())
