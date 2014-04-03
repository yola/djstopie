from django.test import TestCase
from django.test.client import RequestFactory
from mock import Mock, patch

from djstoppy.middleware import UnsupportedBrowsersMiddleware, CompatibilityModeMiddleware
from django.conf import settings



class CompatibilityModeTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.requested_url = '/home'
        self.request = self.factory.get(self.requested_url)
        self.response = Mock()
        self.cmw = CompatibilityModeMiddleware()

    def test_redirects_ie7_compatiblity_mode(self):
        ie7Compat = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; Trident/7.0; .NET4.0E; .NET4.0C)'
        self.request.META['HTTP_USER_AGENT'] = ie7Compat
        response = self.cmw.process_response(self.request, self.response)
        self.assertIn(settings.COMPATIBILITY_URL, response.url)

    def test_redirects_ie8_compatiblity_mode(self):
        ie8Compat = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.3; Trident/7.0; .NET4.0E; .NET4.0C)'
        self.request.META['HTTP_USER_AGENT'] = ie8Compat
        response = self.cmw.process_response(self.request, self.response)
        self.assertIn(settings.COMPATIBILITY_URL, response.url)

    def test_ie_browser_not_in_compatibitly_mode_are_not_redirected(self):
        ie11 = 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0)'
        self.request.META['HTTP_USER_AGENT'] = ie11
        response = self.cmw.process_response(self.request, self.response)
        self.assertEqual(self.response, response)

    def test_redirect_to_next_url_after_compatibility_mode_is_off(self):
        ie11 = 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0)'
        self.request.META['HTTP_USER_AGENT'] = ie11
        url = settings.COMPATIBILITY_URL + '?next=/home'
        self.request = self.factory.get(url)
        response = self.cmw.process_response(self.request, self.response)
        self.assertEqual(response.url, '/home')


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
