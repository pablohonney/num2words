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
    7: ("sedmý", "sedmi"),
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
    5: ("padesátý", "padesáti"),
    6: ("šedesátý", "šedesáti"),
    7: ("sedmdesátý", "sedmdesáti"),
    8: ("osmdesátý", "osmdesáti"),
    9: ("devadesátý", "devadesáti"),
}

# (ORDINAL_FORM, COMPOUNDED_FORM)
HUNDREDS_ORDINALS = {
    1: ("stý", "sto"),
    2: ("dvoustý", "dvouset"),
    3: ("třístý", "třiset"),
    4: ("čtyřstý", "čtyřset"),
    5: ("pětistý", "pětiset"),
    6: ("šestistý", "šestiset"),
    7: ("sedmistý", "sedmiset"),
    8: ("osmistý", "osmiset"),
    9: ("devítistý", "devítiset"),
    # a special case of inter-fragment interference, these forms do not form compounds
    11: ("jedenáctistý", None),
    12: ("dvanáctistý", None),
    13: ("třináctistý", None),
    14: ("čtrnáctistý", None),
    15: ("patnáctistý", None),
    16: ("šestnáctistý", None),
    17: ("sedmnáctistý", None),
    18: ("osmnáctistý", None),
    19: ("devatenáctistý", None),
}

THOUSANDS_ORDINALS = {
    1: "tisící",  # 10^3
}

for level_, thousand_ in THOUSANDS.items():
    if level_ not in THOUSANDS_ORDINALS:
        THOUSANDS_ORDINALS[level_] = thousand_[0].rstrip("a") + "tý"


class OrdinalFragment(namedtuple("Fragment", "n1 n2 n3 level chunk")):
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
        elif (
            self.level > 0 and self.chunk == 1
        ):  # 1000 gives thousandth, not one thousandth
            pass
        elif last_two < 20:  # ones and teens
            words.append(ONES_ORDINALS[last_two][form])
        elif self.n1 == 0:  # twenties
            words.append(TWENTIES_ORDINALS[self.n2][form])
        else:  # twenties + ones
            words.append(TWENTIES_ORDINALS[self.n2][form])
            words.append(ONES_ORDINALS[self.n1][form])

        words = self._add_thousands_suffix(words)

        return words

    def _add_thousands_suffix(self, words):
        if self.level > 0 and not self.is_empty():
            words.append(THOUSANDS_ORDINALS[self.level])
            words = [
                "".join(words)
            ]  # concat (univerbate) words in higher-order fragments
        return words


class TeenHundredthFragmentInterferenceRule:
    """
    Inter-fragment interference rule

    Without interferece 001,100 would produce 'tisící stý' (English equivalent being 'thousandth hundredth')
    Instead 001,100 should produce 'jedenáctistý' (English equivalent being 'eleven-hundredth')

    Do not apply the rule when the second fragment has more significant digits. e.g. don't apply to 011,100 or 101,100
    Apply the rule when the first fragment has less significant digits. e.g. apply to 001,123

    Given first fragment Fragment([1-9], Any, Any) and second fragment Fragment(0, 0, 1)
    The rule will produce first fragment Fragment(0, Any, Any) and second fragment TeenHundredOrdinalFragment(1[1-9]00)
    """

    class TeenHundredOrdinalFragment:
        """Special OrdinalFragment to represent the TeenHundredth value"""

        def __init__(self, first, second):
            self._first = first
            self._second = second

        def to_words(self):
            inter_fragment_teen = self._first.n1 * 10 + self._second.n3
            word = HUNDREDS_ORDINALS[inter_fragment_teen][0]
            return [word]

        def is_empty(self):
            return False

    def apply(self, fragments):
        if len(fragments) > 1:
            fragments[-1], fragments[-2] = self._apply_teen_hundredth_pattern(
                fragments[-1], fragments[-2]
            )
        return fragments

    def _apply_teen_hundredth_pattern(self, first, second):
        if (second.n3, second.n2, second.n1) == (0, 0, 1) and first.n3:
            new_second = self.TeenHundredOrdinalFragment(second, first)
            new_first = OrdinalFragment(first.n1, first.n2, 0, first.level, first.chunk)
            return new_first, new_second
        else:
            return first, second


class Num2Word_CZ(Num2Word_Base):
    CURRENCY_FORMS = {
        "CZK": (("koruna", "koruny", "korun"), ("halíř", "halíře", "haléřů")),
        "EUR": (("euro", "euro", "euro"), ("cent", "centy", "centů")),
    }

    _ORDINAL_FRAGMENT_INTERFERENCE_RULES = [TeenHundredthFragmentInterferenceRule()]

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

    def to_ordinal(self, number):
        self.verify_ordinal(number)

        if number == 0:
            return ZERO_ORDINAL[0]

        fragment_chunks = list(splitbyx(str(number), 3))
        fragments = []
        for i, fragment_chunk in enumerate(fragment_chunks):
            level = len(fragment_chunks) - i - 1
            fragments.append(OrdinalFragment.build_fragment(level, fragment_chunk))

        fragments = self._solve_fragment_interference(fragments)

        words = []
        for fragment in fragments:
            if not fragment.is_empty():
                words.extend(fragment.to_words())

        output = " ".join(words)

        return output

    # in some cases fragments may interfere with each other
    def _solve_fragment_interference(self, fragments):
        for fragment_interference_rule in self._ORDINAL_FRAGMENT_INTERFERENCE_RULES:
            fragments = fragment_interference_rule.apply(fragments)
        return fragments

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
