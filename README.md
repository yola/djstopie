# djstopie

[![Build Status](https://travis-ci.org/yola/djstopie.png)](https://travis-ci.org/yola/djstopie)
[![Coverage Status](https://coveralls.io/repos/yola/djstopie/badge.png)](https://coveralls.io/r/yola/djstopie)
[![Latest Version](https://img.shields.io/pypi/v/djstopie.svg)](https://pypi.python.org/pypi/djstopie/)
[![Downloads](https://img.shields.io/pypi/dm/djstopie.svg)](https://pypi.python.org/pypi/djstopie/)


## Why?

Because, at some point you may need to drop an old version of IE.

![Alt man who refuses to read](http://i.minus.com/i2EAQUnIGLyXD.gif)

## Features

* Redirects unsupported IE browsers to a custom error page


## Installation and configuration

djstopie requires an integer of the `LAST_SUPPORTED_BROWSER` to be configured in
the projects `settings.py` file. In addition it also requires an `UNSUPPORTED_URL`
to be configured; this url is used to redirect the user to a custom error page.

Here is an example of a configured `setting.py` file:

```python
UNSUPPORTED_URL = '/unsupported-browser'

LAST_SUPPORTED_BROWSER = 9
```

The last step is setting up the middleware itself.

```python
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    ...
    'djstopie.middleware.UnsupportedBrowsersMiddleware'
)
```

djstopie accepts a `LANGUAGE_PREFIX`. This will prefix redirected urls,
either by a function from a given module.

djstopie can also be configured to skip over urls with a given prefix. This can
be configured by assigning a tuple of prefixes to the `WHITELISTED_URL_PATHS`
variable in the settings.py file.
