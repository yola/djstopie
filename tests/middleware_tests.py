from django.test import SimpleTestCase
from django.test.client import RequestFactory
from mock import Mock, patch

from djstopie.middleware import UnsupportedBrowsersMiddleware
from django.conf import settings


class CheckBrowserMiddlewareTest(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.requested_url = '/home'
        self.request = self.factory.get(self.requested_url)
        self.response = Mock()
        self.cbmw = UnsupportedBrowsersMiddleware()

        self.ua_dict = {
            'major': 8,
            'family': 'IE'
        }

        self.patcher = patch(
            'djstopie.middleware.user_agent_parser',
            Parse=Mock(return_value={'user_agent': self.ua_dict}))
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop

    def test_redirects_an_unsupported_browser(self):
        response = self.cbmw.process_response(self.request, self.response)
        self.assertIn(settings.UNSUPPORTED_URL, response.url)

    def test_does_not_redirect_supported_browsers(self):
        self.ua_dict['major'] = 9
        response = self.cbmw.process_response(self.request, self.response)
        self.assertEqual(self.response, response)

    def test_does_not_redirect_a_whitelisted_urls(self):
        request = self.factory.get(
            path=settings.WHITELISTED_URL_PATHS[0] + '/app.js',
        )
        response = self.cbmw.process_response(request, self.response)
        self.assertEqual(self.response, response)

    def test_does_not_redirect_the_error_page(self):
        request = self.factory.get(
            path=settings.UNSUPPORTED_URL
        )
        response = self.cbmw.process_response(request, self.response)
        self.assertEqual(self.response, response)
