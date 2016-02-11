"""Utilities for the Flask API and SQLAlchemy models."""

from dateutil import parser as datetime_parser
from dateutil.tz import tzutc

from flask.globals import _app_ctx_stack, _request_ctx_stack
from werkzeug.urls import url_parse
from werkzeug.exceptions import NotFound
from .exceptions import ValidationError


def split_url(url, method='GET'):
    """Returns the endpoint name and arguments that match a given URL.

    This is the reverse of Flask's `url_for()`.
    """
    appctx = _app_ctx_stack.top
    reqctx = _request_ctx_stack.top
    if appctx is None:
        raise RuntimeError('Attempted to match a URL without the '
                           'application context being pushed. This has to be '
                           'executed when application context is available.')

    if reqctx is not None:
        url_adapter = reqctx.url_adapter
    else:
        url_adapter = appctx.url_adapter
        if url_adapter is None:
            raise RuntimeError('Application was not able to create a URL '
                               'adapter for request independent URL matching. '
                               'You might be able to fix this by setting '
                               'the SERVER_NAME config variable.')
    parsed_url = url_parse(url)
    if parsed_url.netloc is not '' and \
            parsed_url.netloc != url_adapter.server_name:
        raise ValidationError('Invalid URL: ' + url)
    try:
        result = url_adapter.match(parsed_url.path, method)
    except NotFound:
        raise ValidationError('Invalid URL: ' + url)
    return result


def format_utc_datetime(dt):
    """Standardized UTC `str` representation for a
    `datetime.datetime.Datetime`.
    """
    if dt is None:
        return None
    else:
        return dt.isoformat() + 'Z'


def parse_utc_datetime(datetime_str):
    """Parse a date string, returning a UTC datetime object."""
    if datetime_str is not None:
        date = datetime_parser.parse(datetime_str)\
            .astimezone(tzutc())\
            .replace(tzinfo=None)
        return date
    else:
        return None