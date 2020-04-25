# encoding=UTF-8

# Copyright © 2008-2019 Jakub Wilk <jwilk@jwilk.net>
#
# This file is part of ocrodjvu.
#
# ocrodjvu is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# ocrodjvu is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.

from __future__ import absolute_import
import re
import warnings
from six.moves import map
import six

def enhance_import_error(exception, package, homepage):
    message = str(exception)
    message += '; please install the {pkg} package'.format(pkg=package)
    message += ' <{url}>'.format(url=homepage)
    exception.args = [message]
    exception.msg = [message]

class EncodingWarning(UserWarning):
    pass

_control_characters_regex = re.compile('[{0}]'.format(''.join(
    ch for ch in map(chr, range(32))
    if ch not in u'\n\r\t'
)))

def sanitize_utf8(text):
    '''
    Replace invalid UTF-8 sequences and control characters (except CR, LF, TAB
    and space) with Unicode replacement characters.
    '''
    if isinstance(text,six.binary_type):
        try:
            text = text.decode('UTF-8')
        except UnicodeDecodeError as exc:
            text = text.decode('UTF-8', 'replace')
            message = str(exc)
            message = re.sub("^'utf8' codec can't decode ", '', message)
            warnings.warn(
                message,
                category=EncodingWarning,
                stacklevel=2,
            )
        text = text.encode('UTF-8')
    match = _control_characters_regex.search(text)
    if match:
        byte = ord(match.group())
        message = 'byte 0x{byte:02x} in position {i}: control character'.format(byte=byte, i=match.start())
        warnings.warn(
            message,
            category=EncodingWarning,
            stacklevel=2,
        )
        text = _control_characters_regex.sub(u'\N{REPLACEMENT CHARACTER}', text)
    # There are other code points that are not allowed in XML (or even: not
    # allowed in UTF-8), but which Python happily accept. However, they haven't
    # seemed to occur in real-world documents.
    # http://www.w3.org/TR/2008/REC-xml-20081126/#NT-Char
    return text

def identity(x):
    '''
    identity(x) -> x
    '''
    return x

class property(object):

    def __init__(self, default_value=None, filter=identity):
        self._private_name = '__{mod}__{id}'.format(mod=self.__module__, id=id(self))
        self._filter = filter
        self._default_value = default_value

    def __get__(self, instance, cls):
        if instance is None:
            return self
        return getattr(instance, self._private_name, self._default_value)

    def __set__(self, instance, value):
        setattr(instance, self._private_name, self._filter(value))
        return

# vim:ts=4 sts=4 sw=4 et
