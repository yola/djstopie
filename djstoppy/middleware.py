import urllib

from django.conf import settings
from django.shortcuts import redirect
from languish import prefix_language
from ua_parser import user_agent_parser


class CompatibilityModeMiddleware:
    """Redirects IE browsers in compatibility mode to error page"""

    def process_response(self, request, response):

        # skip over static assets
        if request.path.startswith(settings.STATIC_URL):
            return response

        requested_url = request.get_full_path()
        error_page = prefix_language(settings.COMPATIBILITY_URL)
        is_error_page = request.path in error_page

        user_agent = request.META.get('HTTP_USER_AGENT', '')
        user_agent_dict = user_agent_parser.Parse(user_agent)
        unsupported_mode = self._unsupported_compatiblity_mode(user_agent_dict)

        if unsupported_mode and not is_error_page:
            return self.redirect(self._append_next_url(error_page, requested_url))

        elif request.GET.get('next') and is_error_page:
            return self._redirect_back_to_original_url(request)

        return response


    def _unsupported_compatiblity_mode(self, user_agent):
        version = user_agent['user_agent']['major']
        is_trident = 'Trident' in user_agent['string']
        is_ie = user_agent['user_agent']['family'] == 'IE'

        unsupported_version = version in settings.COMPATIBILITY_MODE_BROWSERS

        return unsupported_version and is_trident and is_ie


    def _append_next_url(self, url, next):
        next_url = urllib.quote_plus(next)
        if url == next:
            return url

        return url + '?next=' + next_url

    def _redirect_back_to_original_url(self, request):
        next_url = request.GET.get('next')
        return self.redirect(next_url)



class UnsupportedBrowsersMiddleware:
    """Redirects unsupported IE browsers to error page"""

    def process_response(self, request, response):

        # skip over static assets
        if request.path.startswith(settings.STATIC_URL):
            return response

        error_page = prefix_language(settings.UNSUPPORTED_URL)
        is_error_page = request.path in error_page

        user_agent = request.META.get('HTTP_USER_AGENT', '')
        user_agent_dict = user_agent_parser.Parse(user_agent)
        unsupported_browser = self._is_browser_unsupported(user_agent_dict)


        if unsupported_browser and not is_error_page:
            return self.redirect(error_page)


        return response


    def _is_browser_unsupported(self, user_agent):
        version = user_agent['user_agent']['major']
        is_ie = user_agent['user_agent']['family'] == 'IE'

        return version in settings.UNSUPPORTED_BROWSERS and is_ie
