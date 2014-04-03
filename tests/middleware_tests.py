from django.test import TestCase
from django.test.client import RequestFactory
from mock import Mock, patch

from djstopie.middleware import UnsupportedBrowsersMiddleware
from django.conf import settings


class CheckBrowserTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.requested_url = '/home'
        self.request = self.factory.get(self.requested_url)
        self.response = Mock()
        self.cbmw = UnsupportedBrowsersMiddleware()

    def test_redirect_unsupported_browser(self):
        self.request.META['HTTP_USER_AGENT'] = 'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)'
        response = self.cbmw.process_response(self.request, self.response)
        self.assertIn(settings.UNSUPPORTED_URL, response.url)

    def test_IE_8_redirects_to_unsupported_browser(self):
        self.request.META['HTTP_USER_AGENT'] = 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)'
        response = self.cbmw.process_response(self.request, self.response)
        self.assertIn('unsupported-browser', response.url)

    def test_supported_browsers_are_not_redirected(self):
        ie11 = 'Mozilla/4.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)'
        self.request.META['HTTP_USER_AGENT'] = ie11
        response = self.cbmw.process_response(self.request, self.response)
        self.assertEqual(self.response, response)
