# djstoppy


## Features

* Redirects unsupported browsers to a custom error page
* Separately redirects IE browsers in compatibility mode

## Installation and configuration

djstoppy requires a tuple of `UNSUPPORTED_BROWSERS` and `COMPATIBILITY_MODE_BROWSERS`
to be configured in the projets `settings.py` file. In addition it also requires
an `UNSUPPORTED_URL` and `COMPATIBILITY_URL` to be configures; these urls are
used to redirect the user to a custom error page.

Here is an example of a configured `setting.py` file:

```python
COMPATIBILITY_URL = 'compatibility-mode'
UNSUPPORTED_URL = 'unsupported-browser'

COMPATIBILITY_MODE_BROWSERS = (
    'MSIE 7.0',
    'MSIE 8.0'
)

UNSUPPORTED_BROWSERS = (
    'MSIE 6.0',
    'MSIE 6.1',
    'MSIE 7.0',
    'MSIE 8.0'
)

```

The last step is setting up the middleware itself. **NB**: The compatibility mode
middleware should be listed before the unsupported browser middleware.

```python
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    ...
    'djstoppy.middleware.CompatibilityModeMiddleware',
    'djstoppy.middleware.UnsupportedBrowsersMiddleware'
)
```
