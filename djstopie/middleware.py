import urllib

from django.conf import settings
from django.shortcuts import redirect
from ua_parser import user_agent_parser

class BrowserRedirectBase:

    def prefix_language(self, url):
        prefix = settings.LANGUAGE_PREFIX

        if not prefix:
          return url

        elif hasattr(url, '__call__'):
          return prefix(url)

        elif isinstance(url, basestring):
          return prefix + url



class CompatibilityModeMiddleware(BrowserRedirectBase):
    """Redirects IE browsers in compatibility mode to error page"""


    def process_response(self, request, response):

        # skip over static assets
        if request.path.startswith(settings.STATIC_URL):
            return response

        requested_url = request.get_full_path()
        error_page = settings.COMPATIBILITY_URL
        is_error_page = error_page in request.path
        next_url = request.GET.get('next', '')

        user_agent = request.META.get('HTTP_USER_AGENT', '')
        user_agent_dict = user_agent_parser.Parse(user_agent)
        unsupported_mode = self._unsupported_compatiblity_mode(user_agent_dict)

        if unsupported_mode and not is_error_page:
            return self._redirect_to_error_page(error_page, requested_url)

        elif next_url and is_error_page:
            return self._redirect_back_to_original_url(next_url)

        return response


    def _unsupported_compatiblity_mode(self, user_agent):
        version = user_agent['user_agent']['major']
        is_trident = 'Trident' in user_agent['string']
        is_ie = user_agent['user_agent']['family'] == 'IE'

        if is_ie:
          return int(version) < settings.LAST_SUPPORTED_MODE and is_trident

        return True


    def _append_next_url(self, url, next):
        next_url = urllib.quote_plus(next)
        if url == next:
            return url

        return url + '?next=' + next_url

    def _redirect_back_to_original_url(self, next_url):
        return redirect(next_url)

    def _redirect_to_error_page(self, error_page, original_url):
        error_page = self._append_next_url(error_page, original_url)
        error_page = self.prefix_language(error_page)

        return redirect(error_page)



class UnsupportedBrowsersMiddleware(BrowserRedirectBase):
    """Redirects unsupported IE browsers to error page"""

    def process_response(self, request, response):

        # skip over static assets
        if request.path.startswith(settings.STATIC_URL):
            return response

        is_error_page = request.path in settings.UNSUPPORTED_URL

        user_agent = request.META.get('HTTP_USER_AGENT', '')
        user_agent_dict = user_agent_parser.Parse(user_agent)
        unsupported_browser = self._is_browser_unsupported(user_agent_dict)

        if unsupported_browser and not is_error_page:
            return self._redirect_to_error_page()

        return response


    def _is_browser_unsupported(self, user_agent):
        version = user_agent['user_agent']['major']
        is_ie = user_agent['user_agent']['family'] == 'IE'

        if is_ie:
          return int(version) < settings.LAST_SUPPORTED_BROWSER

        return True

    def _redirect_to_error_page(self):
        error_page = self.prefix_language(settings.UNSUPPORTED_URL)
        return redirect(error_page)
