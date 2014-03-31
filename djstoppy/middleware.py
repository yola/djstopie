import urllib

from django.conf import settings
from django.shortcuts import redirect
from languish import prefix_language


def append_next_url(self, url, next):
    next_url = urllib.quote_plus(next)
    if url == next:
        return url

    return url + '?next=' + next_url



class CompatibilityModeMiddleware:
    """Inspects user agent strings to see if an Internet Explorer browser
    is running in compatiblity mode and redirect to a compatibitly compatablity
    mode error page"""

    redirect = redirect
    append_next_url = append_next_url

    def process_response(self, request, response):

        # skip over static assets
        if request.path.startswith(settings.STATIC_URL):
            return response


        requested_url = request.get_full_path()
        next_url = request.GET.get('next', '/')
        error_page = prefix_language(settings.COMPATIBILITY_URL)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        is_error_page = request.path in error_page
        unsupported_mode = self._is_unsupported_compatiblity_mode(user_agent)
        is_trident = user_agent.find('Trident') != -1


        if unsupported_mode and is_trident and not is_error_page:
            return self.redirect(self.append_next_url(error_page, requested_url))

        elif (request.GET.get('next') and is_error_page and
                not unsupported_mode):
            return self.redirect(next_url)

        return response


    def _is_unsupported_compatiblity_mode(self, user_agent):
        for mode in settings.COMPATIBILITY_MODE_BROWSERS:
            if mode in user_agent:
                return True

        return False



class CheckBrowserMiddleware:
    """Check settings for unsupported browser strings and redirect user
    to an unsupported browsers page"""

    redirect = redirect
    append_next_url = append_next_url

    def process_response(self, request, response):

        # skip over static assets
        if request.path.startswith(settings.STATIC_URL):
            return response

        requested_url = request.get_full_path()
        next_url = request.GET.get('next', '/')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        unsupported_browser = self._is_browser_unsupported(user_agent)
        error_page = prefix_language(settings.UNSUPPORTED_URL)
        is_error_page = request.path in error_page


        if unsupported_browser and not is_error_page:
            return self.redirect(self.append_next_url(error_page, requested_url))

        elif (request.GET.get('next') and is_error_page and
                not unsupported_browser):
            return self.redirect(next_url)

        return response


    def _is_browser_unsupported(self, user_agent):
        for version in settings.UNSUPPORTED_BROWSERS:
            if version in user_agent:
                return True

        return False
