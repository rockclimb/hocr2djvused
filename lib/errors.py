# encoding=UTF-8

# Copyright © 2009-2019 Jakub Wilk <jwilk@jwilk.net>
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

from __future__ import print_function

class MalformedOcrOutput(Exception):

    def __init__(self, message):
        Exception.__init__(self,
            'malformed OCR output: {msg}'
            .format(msg=message)
        )

class MalformedHocr(MalformedOcrOutput):

    def __init__(self, message):
        Exception.__init__(self,
            'malformed hOCR document: {msg}'
            .format(msg=message)
        )

EXIT_FATAL = 1

__all__ = [
    'MalformedOcrOutput',
    'MalformedHocr',
    'EXIT_FATAL',
]

# vim:ts=4 sts=4 sw=4 et
