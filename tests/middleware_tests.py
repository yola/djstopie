from django.test import SimpleTestCase
from django.test.client import RequestFactory
from mock import Mock

from djstopie.middleware import UnsupportedBrowsersMiddleware
from django.conf import settings


class CheckBrowserMiddlewareTest(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.requested_url = '/home'
        self.request = self.factory.get(self.requested_url)
        self.response = Mock()
        self.cbmw = UnsupportedBrowsersMiddleware()

        self.IE8 = 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)'

    def test_redirects_an_unsupported_browser(self):
        self.request.META['HTTP_USER_AGENT'] = 'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)'
        response = self.cbmw.process_response(self.request, self.response)
        self.assertIn(settings.UNSUPPORTED_URL, response.url)

    def test_redirects_IE_8_to_unsupported_browser_page(self):
        self.request.META['HTTP_USER_AGENT'] = self.IE8
        response = self.cbmw.process_response(self.request, self.response)
        self.assertIn('unsupported-browser', response.url)

    def test_does_not_redirect_supported_browsers(self):
        ie11 = 'Mozilla/4.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)'
        self.request.META['HTTP_USER_AGENT'] = ie11
        response = self.cbmw.process_response(self.request, self.response)
        self.assertEqual(self.response, response)

    def test_does_not_redirect_a_whitelisted_urls(self):
        self.request.META['HTTP_USER_AGENT'] = self.IE8
        url = settings.WHITELISTED_URL_PATHS[0] + '/app.js'
        new_request = self.request = self.factory.get(url)
        response = self.cbmw.process_response(new_request, self.response)
        self.assertEqual(self.response, response)

    def test_does_not_redirect_the_error_page(self):
        self.request.META['HTTP_USER_AGENT'] = self.IE8
        url = settings.UNSUPPORTED_URL
        new_request = self.request = self.factory.get(url)
        response = self.cbmw.process_response(new_request, self.response)
        self.assertEqual(self.response, response)
