# djstopie

## Why?

Because, at some point you may need to drop an old version of IE.

![Alt man who refuses to read](http://i.minus.com/i2EAQUnIGLyXD.gif)

## Features

* Redirects unsupported IE browsers to a custom error page


## Installation and configuration

djstopie requires an intiger of the `LAST_SUPPORTED_BROWSER` to be configured in
the projets `settings.py` file. In addition it also requires an `UNSUPPORTED_URL`
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

djstopie also excepts a `LANGUAGE_PREFIX`. This will prefix redirected urls,
either by calling a function or by prefixing a string.
