from django.conf import settings
from django.shortcuts import redirect
from django.utils.module_loading import import_string
from ua_parser import user_agent_parser

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


class UnsupportedBrowsersMiddleware(MiddlewareMixin):
    """Redirects unsupported IE browsers to error page."""

    def process_response(self, request, response):
        requested_url = request.path
        whitelisted = self._white_listed_url(requested_url)

        user_agent = request.META.get('HTTP_USER_AGENT', '')
        user_agent_dict = user_agent_parser.Parse(user_agent)
        unsupported_browser = self._is_browser_unsupported(user_agent_dict)

        if unsupported_browser and not whitelisted:
            return self._redirect_to_error_page()

        return response

    def _is_browser_unsupported(self, user_agent):
        version = user_agent['user_agent']['major']
        is_ie = user_agent['user_agent']['family'] == 'IE'

        return is_ie and int(version) < settings.LAST_SUPPORTED_BROWSER

    def _redirect_to_error_page(self):
        error_page = self._prefix_language(settings.UNSUPPORTED_URL)
        return redirect(error_page)

    def _prefix_language(self, url):
        callable_path = getattr(settings, 'LANGUAGE_PREFIX', None)

        if not callable_path:
            return url

        return import_string(callable_path)(url)

    def _white_listed_url(self, url):
        whitelisted = (settings.STATIC_URL, settings.MEDIA_URL)

        if hasattr(settings, 'WHITELISTED_URL_PATHS'):
            whitelisted = whitelisted + settings.WHITELISTED_URL_PATHS

        whitelisted = filter(None, whitelisted)

        is_whitelisted = url.startswith(whitelisted)
        is_error_page = settings.UNSUPPORTED_URL in url

        return is_whitelisted or is_error_page
