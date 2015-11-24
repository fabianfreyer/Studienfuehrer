
"""
adapted from http://flask.pocoo.org/snippets/63/
"""
try:
        from urllib.parse import urlparse
except ImportError:
        from urlparse import urlparse

from flask import request, url_for, redirect
from flask.ext.wtf import Form
from wtforms import TextField, HiddenField


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def get_redirect_target():
    """
    Get the redirect target from
    - GET parameter 'next'
    - the referrer
    """
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

def redirect_back(endpoint, **values):
    target = get_redirect_target()
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)


class RedirectForm(Form):
    """
    A form that securely redirects back
    """
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='index', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))

