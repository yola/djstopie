# djstoppy

## Why?

Because, at some point you may need to drop an old version of IE.

![Alt man who refuses to read](http://i.minus.com/i2EAQUnIGLyXD.gif)

## Features

* Redirects unsupported IE browsers to a custom error page
* Separately redirects IE browsers in compatibility mode

## Installation and configuration

djstoppy requires a intiger of the `LAST_SUPPORTED_BROWSER` and `LAST_SUPPORTED_MODE `
to be configured in the projets `settings.py` file. In addition it also requires
an `UNSUPPORTED_URL` and `COMPATIBILITY_URL` to be configures; these urls are
used to redirect the user to a custom error page.

Here is an example of a configured `setting.py` file:

```python
COMPATIBILITY_URL = 'compatibility-mode'
UNSUPPORTED_URL = 'unsupported-browser'

LAST_SUPPORTED_MODE = 9
LAST_SUPPORTED_BROWSER = 9

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

djstoppy also excepts an optional `LANGUAGE_PREFIX` variable. This will prefix
redirected urls, either by calling a function or by prepending a string.
