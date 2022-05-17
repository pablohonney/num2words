# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

from __future__ import unicode_literals
from collections import namedtuple

from .base import Num2Word_Base
from .utils import get_digits, splitbyx

ZERO = ("nula",)

ONES = {
    1: ("jedna",),
    2: ("dva",),
    3: ("tři",),
    4: ("čtyři",),
    5: ("pět",),
    6: ("šest",),
    7: ("sedm",),
    8: ("osm",),
    9: ("devět",),
}

TENS = {
    0: ("deset",),
    1: ("jedenáct",),
    2: ("dvanáct",),
    3: ("třináct",),
    4: ("čtrnáct",),
    5: ("patnáct",),
    6: ("šestnáct",),
    7: ("sedmnáct",),
    8: ("osmnáct",),
    9: ("devatenáct",),
}

TWENTIES = {
    2: ("dvacet",),
    3: ("třicet",),
    4: ("čtyřicet",),
    5: ("padesát",),
    6: ("šedesát",),
    7: ("sedmdesát",),
    8: ("osmdesát",),
    9: ("devadesát",),
}

HUNDREDS = {
    1: ("sto",),
    2: ("dvěstě",),
    3: ("třista",),
    4: ("čtyřista",),
    5: ("pětset",),
    6: ("šestset",),
    7: ("sedmset",),
    8: ("osmset",),
    9: ("devětset",),
}

THOUSANDS = {
    1: ("tisíc", "tisíce", "tisíc"),  # 10^3
    2: ("milion", "miliony", "milionů"),  # 10^6
    3: ("miliarda", "miliardy", "miliard"),  # 10^9
    4: ("bilion", "biliony", "bilionů"),  # 10^12
    5: ("biliarda", "biliardy", "biliard"),  # 10^15
    6: ("trilion", "triliony", "trilionů"),  # 10^18
    7: ("triliarda", "triliardy", "triliard"),  # 10^21
    8: ("kvadrilion", "kvadriliony", "kvadrilionů"),  # 10^24
    9: ("kvadriliarda", "kvadriliardy", "kvadriliard"),  # 10^27
    10: ("quintillion", "quintilliony", "quintillionů"),  # 10^30
}


ZERO_ORDINAL = ("nultý",)

ORDINAL_FORM = 0
COMPOUNDED_FORM = 1

# (ORDINAL_FORM, COMPOUNDED_FORM)
ONES_ORDINALS = {
    1: ("první", "jeden"),
    2: ("druhý", "dvou"),
    3: ("třetí", "tří"),
    4: ("čtvrtý", "čtyr"),
    5: ("pátý", "pěti"),
    6: ("šestý", "šesti"),
    7: ("sedmý", "siedmio"),
    8: ("osmý", "osmi"),
    9: ("devátý", "devíti"),
    10: ("desátý", "deseti"),
    11: ("jedenáctý", "jedenácti"),
    12: ("dvanáctý", "dvanácti"),
    13: ("třináctý", "třinácti"),
    14: ("čtrnáctý", "čtrnácti"),
    15: ("patnáctý", "patnácti"),
    16: ("šestnáctý", "šestnácti"),
    17: ("sedmnáctý", "sedmnácti"),
    18: ("osmnáctý", "osmnácti"),
    19: ("devatenáctý", "devatenácti"),
}

# (ORDINAL_FORM, COMPOUNDED_FORM)
TWENTIES_ORDINALS = {
    2: ("dvacátý", "dvaceti"),
    3: ("třicátý", "třiceti"),
    4: ("čtyřicátý", "čtyřiceti"),
    5: ("padesátý", "padeseti"),
    6: ("šedesátý", "šedeseti"),
    7: ("sedmdesátý", "sedmdeseti"),
    8: ("osmdesátý", "osmdeseti"),
    9: ("devadesátý", "devadeseti"),
}

# (ORDINAL_FORM, COMPOUNDED_FORM)
HUNDREDS_ORDINALS = {
    1: ("stý", "sto"),
    2: ("dvoustý", "dvouset"),
    3: ("třistý", "třiset"),
    4: ("čtyřstý", "čtyřset"),
    5: ("pětistý", "pětiset"),
    6: ("šestistý", "šestiset"),
    7: ("sedmistý", "sedmiset"),
    8: ("osmistý", "osmiset"),
    9: ("devítistý", "devítiset"),
}

THOUSANDS_ORDINALS = {
    1: "tisící",  # 10^3
}

for level_, thousand_ in THOUSANDS.items():
    if level_ not in THOUSANDS_ORDINALS:
        THOUSANDS_ORDINALS[level_] = thousand_[0].rstrip("a") + "tý"


class OrdinalFragment(namedtuple('Fragment', 'n1 n2 n3 level chunk')):
    """Represent a 3-digit fragment of the ordinal number"""

    @staticmethod
    def build_fragment(level, chunk):
        return OrdinalFragment(*get_digits(chunk), level, chunk)

    def is_empty(self):
        return self.chunk == 0

    def to_words(self):
        words = []
        last_two = self.n2 * 10 + self.n1

        form = ORDINAL_FORM if self.level == 0 else COMPOUNDED_FORM

        if self.n3 > 0:
            words.append(HUNDREDS_ORDINALS[self.n3][form])

        if last_two == 0:
            pass
        elif self.level > 0 and self.chunk == 1:  # 1000 gives thousandth, not one thousandth
            pass
        elif last_two < 20:  # ones and teens
            words.append(ONES_ORDINALS[last_two][form])
        elif self.n1 == 0:  # twenties
            words.append(TWENTIES_ORDINALS[self.n2][form])
        else:  # twenties + ones
            words.append(TWENTIES_ORDINALS[self.n2][form])
            words.append(ONES_ORDINALS[self.n1][form])

        words = self.add_suffix(words)

        return words

    # concat words in higher-order fragments
    def add_suffix(self, words):
        if self.level > 0 and self.chunk != 0:
            words.append(THOUSANDS_ORDINALS[self.level])
            words = ["".join(words)]
        return words


class Num2Word_CZ(Num2Word_Base):
    CURRENCY_FORMS = {
        "CZK": (("koruna", "koruny", "korun"), ("halíř", "halíře", "haléřů")),
        "EUR": (("euro", "euro", "euro"), ("cent", "centy", "centů")),
    }

    def setup(self):
        self.negword = "mínus"
        self.pointword = "celá"

    def to_cardinal(self, number):
        n = str(number).replace(",", ".")
        if "." in n:
            left, right = n.split(".")
            leading_zero_count = len(right) - len(right.lstrip("0"))
            decimal_part = (ZERO[0] + " ") * leading_zero_count + self._int2word(
                int(right)
            )
            return "%s %s %s" % (
                self._int2word(int(left)),
                self.pointword,
                decimal_part,
            )
        else:
            return self._int2word(int(n))

    def pluralize(self, n, forms):
        if n == 1:
            form = 0
        elif 5 > n % 10 > 1 and (n % 100 < 10 or n % 100 > 20):
            form = 1
        else:
            form = 2
        return forms[form]

    # We try to keep the ordinals' structure as consistent as possible.
    # Since the 0-999 are mostly represented in separate ordinals form we try to extend the same logic to higher order numbers.
    # Thus for 20,000 we choose dvacátý tisící, not dvacetitisící.
    # Yet this approach is explicitly wrong for 2,3 and 4 which always require the compounded form (dvou tisící, not druhý tisící).
    def to_ordinal(self, number):
        self.verify_ordinal(number)

        if number == 0:
            return ZERO_ORDINAL[0]

        fragment_chunks = list(splitbyx(str(number), 3))

        fragments = []
        for i, fragment_chunk in enumerate(fragment_chunks):
            level = len(fragment_chunks) - i - 1
            fragments.append(OrdinalFragment.build_fragment(level, fragment_chunk))

        words = []
        for fragment in fragments:
            if not fragment.is_empty():
                words.extend(fragment.to_words())

        output = " ".join(words)

        return output

    def _int2word(self, n):
        if n == 0:
            return ZERO[0]

        words = []
        chunks = list(splitbyx(str(n), 3))
        i = len(chunks)
        for x in chunks:
            i -= 1

            if x == 0:
                continue

            n1, n2, n3 = get_digits(x)

            if n3 > 0:
                words.append(HUNDREDS[n3][0])

            if n2 > 1:
                words.append(TWENTIES[n2][0])

            if n2 == 1:
                words.append(TENS[n1][0])
            elif n1 > 0 and not (i > 0 and x == 1):
                words.append(ONES[n1][0])

            if i > 0:
                words.append(self.pluralize(x, THOUSANDS[i]))

        return " ".join(words)
