# encoding=UTF-8

# Copyright © 2010-2019 Jakub Wilk <jwilk@jwilk.net>
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

import sys
import warnings

from tests.tools import (
    assert_equal,
    assert_is,
    assert_is_instance,
    assert_raises,
    assert_raises_regex,
)

from lib.utils import (
    EncodingWarning,
    enhance_import_error,
    identity,
    property,
    sanitize_utf8,
)

class test_enhance_import():

    @classmethod
    def setup_class(cls):
        sys.modules['nonexistent'] = None

    def test_import(self):
        with assert_raises(ImportError) as ecm:
            try:
                import nonexistent
            except ImportError as ex:
                enhance_import_error(ex, 'PyNonexistent', 'http://pynonexistent.example.net/')
                raise
            nonexistent.f()  # quieten pyflakes
        assert_equal(str(ecm.exception)[-78:],
            '; please install the PyNonexistent package <http://pynonexistent.example.net/>'
        )

class test_sanitize_utf8():

    def test_control_characters(self):
        def show(message, category, filename, lineno, file=None, line=None):
            with assert_raises_regex(EncodingWarning, '.*control character.*'):
                raise message
        s = ''.join(map(chr, range(32)))
        with warnings.catch_warnings():
            warnings.showwarning = show
            t = sanitize_utf8(s)
        assert_equal(t,
            u'\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD'
            u'\uFFFD\t\n\uFFFD\uFFFD\r\uFFFD\uFFFD'
            u'\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD'
            u'\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD'
        )

    def test_ascii(self):
        s = 'The quick brown fox jumps over the lazy dog'
        with warnings.catch_warnings():
            warnings.filterwarnings('error', category=EncodingWarning)
            t = sanitize_utf8(s)
        assert_equal(s, t)

    def test_utf8(self):
        s = 'Jeżu klątw, spłódź Finom część gry hańb'
        with warnings.catch_warnings():
            warnings.filterwarnings('error', category=EncodingWarning)
            t = sanitize_utf8(s)
        assert_equal(s, t)

    def test_non_utf8(self):
        if sys.version_info >= (3, 0):
            # non utf-8 doesn't properly make sense for Python3 I think
            return
        def show(message, category, filename, lineno, file=None, line=None):
            with assert_raises_regex(EncodingWarning, '.* invalid continuation byte'):
                raise message
        s0 = 'Jeżu klątw, spłódź Finom część gry hańb'
        good = 'ó'
        bad = good.decode('UTF-8').encode('ISO-8859-2')
        s1 = s0.replace(good, bad)
        s2 = s0.replace(good, u'\N{REPLACEMENT CHARACTER}'.encode('UTF-8'))
        with warnings.catch_warnings():
            warnings.showwarning = show
            t = sanitize_utf8(s1)
        assert_equal(s2, t)

def test_identity():
    o = object()
    assert_is(identity(o), o)

class test_property():

    @classmethod
    def setup_class(cls):
        class Dummy(object):
            eggs = property()
            ham = property(default_value=42)
        cls.Dummy = Dummy

    def test_class(self):
        eggs = self.Dummy.eggs
        ham = self.Dummy.ham
        for obj in eggs, ham:
            assert_is_instance(obj, property)

    def test_default_filter(self):
        dummy = self.Dummy()
        assert_equal(dummy.eggs, None)
        assert_equal(dummy.ham, 42)
        dummy.eggs = -4
        dummy.ham = -2
        assert_equal(dummy.eggs, -4)
        assert_equal(dummy.ham, -2)
        dummy = self.Dummy()
        assert_equal(dummy.eggs, None)
        assert_equal(dummy.ham, 42)

# vim:ts=4 sts=4 sw=4 et
