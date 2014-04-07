from django.conf import settings
from django.shortcuts import redirect
from ua_parser import user_agent_parser


class UnsupportedBrowsersMiddleware:
    """Redirects unsupported IE browsers to error page"""

    def process_response(self, request, response):

        static_asset = request.path.startswith(settings.STATIC_URL)
        is_error_page = self._is_error_page(request.path)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        user_agent_dict = user_agent_parser.Parse(user_agent)
        unsupported_browser = self._is_browser_unsupported(user_agent_dict)

        if unsupported_browser and not is_error_page and not static_asset:
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

        if not hasattr(settings, 'LANGUAGE_PREFIX'):
            return url

        prefix = settings.LANGUAGE_PREFIX

        if hasattr(prefix, '__call__'):
            return prefix(url)

        elif isinstance(prefix, basestring):
            return prefix + url

    def _is_error_page(self, url):
        return settings.UNSUPPORTED_URL in url
