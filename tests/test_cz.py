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

from unittest import TestCase

from num2words import num2words

TEST_CASES_CARDINAL = (
    (100, "sto"),
    (101, "sto jedna"),
    (110, "sto deset"),
    (115, "sto patnáct"),
    (123, "sto dvacet tři"),
    (1000, "tisíc"),
    (1001, "tisíc jedna"),
    (2012, "dva tisíce dvanáct"),
    (10.02, "deset celá nula dva"),
    (15.007, "patnáct celá nula nula sedm"),
    (12519.85, "dvanáct tisíc pětset devatenáct celá osmdesát pět"),
    (123.50, "sto dvacet tři celá pět"),
    (
        1234567890,
        "miliarda dvěstě třicet čtyři miliony pětset šedesát sedm tisíc osmset devadesát",
    ),
    (
        215461407892039002157189883901676,
        "dvěstě patnáct quintillionů čtyřista šedesát jedna kvadriliard "
        "čtyřista sedm kvadrilionů osmset devadesát dva triliardy třicet "
        "devět trilionů dva biliardy sto padesát sedm bilionů sto "
        "osmdesát devět miliard osmset osmdesát tři miliony "
        "devětset jedna tisíc šestset sedmdesát šest",
    ),
    (
        719094234693663034822824384220291,
        "sedmset devatenáct quintillionů devadesát "
        "čtyři kvadriliardy dvěstě třicet čtyři "
        "kvadriliony šestset devadesát tři triliardy "
        "šestset šedesát tři triliony třicet čtyři biliardy osmset "
        "dvacet dva biliony osmset dvacet čtyři "
        "miliardy třista osmdesát čtyři miliony dvěstě dvacet "
        "tisíc dvěstě devadesát jedna",
    ),
)

TEST_CASES_ORDINAL = (
    # ones
    (0, "nultý"),
    (3, "třetí"),
    (5, "pátý"),
    # teens
    (15, "patnáctý"),
    # tens
    (10, "desátý"),
    (20, "dvacátý"),
    (25, "dvacátý pátý"),
    # hundreds
    (100, "stý"),
    (105, "stý pátý"),  # hundreds + ones
    (110, "stý desátý"),  # hundreds + tens
    (115, "stý patnáctý"),  # hundreds + teens
    (120, "stý dvacátý"),  # hundreds + tens
    (125, "stý dvacátý pátý"),  # hundreds + tens + ones
    (200, "dvoustý"),
    (225, "dvoustý dvacátý pátý"),
    # thousands
    (1000, "tisící"),
    (1005, "tisící pátý"),
    (1010, "tisící desátý"),
    (1015, "tisící patnáctý"),
    (1020, "tisící dvacátý"),
    (1025, "tisící dvacátý pátý"),
    (1100, "tisící stý"),
    (1200, "tisící dvoustý"),
    (2000, "dvou tisící"),
    (5000, "pátý tisící"),
    (10000, "desátý tisící"),
    (13000, "třináctý tisící"),
    (20000, "dvacátý tisící"),
    (100000, "stý tisící"),
    (200000, "dvoustý tisící"),
    (223000, "dvoustý dvacátý tří tisící"),
    # millions
    (10**6, "miliontý"),
    (100 * 10**6, "stý miliontý"),
    (223 * 10**6, "dvoustý dvacátý tří miliontý"),
    (10**6 + 21, "miliontý dvacátý první"),
    (10**6 + 1000, "miliontý tisící"),
    (10**6 + 2000, "miliontý dvou tisící"),
    # higher orders
    (10**9, "miliardtý"),
    (10**12, "biliontý"),
)


class Num2WordsCZTest(TestCase):
    def test_cardinal(self):
        for input_number, expected_phrase in TEST_CASES_CARDINAL:
            self.assertEqual(
                expected_phrase, num2words(input_number, lang="cz", to="cardinal")
            )

    def test_to_ordinal(self):
        for input_number, expected_phrase in TEST_CASES_ORDINAL:
            self.assertEqual(
                expected_phrase, num2words(input_number, lang="cz", to="ordinal")
            )

    def test_currency(self):
        self.assertEqual(
            "deset euro, nula centů",
            num2words(10.0, lang="cz", to="currency", currency="EUR"),
        )
        self.assertEqual(
            "jedna koruna, nula haléřů",
            num2words(1.0, lang="cz", to="currency", currency="CZK"),
        )
        self.assertEqual(
            "tisíc dvěstě třicet čtyři euro, padesát šest centů",
            num2words(1234.56, lang="cz", to="currency", currency="EUR"),
        )
        self.assertEqual(
            "tisíc dvěstě třicet čtyři koruny, padesát šest haléřů",
            num2words(1234.56, lang="cz", to="currency", currency="CZK"),
        )
        self.assertEqual(
            "sto jedna euro a jedenáct centů",
            num2words(101.11, lang="cz", to="currency", currency="EUR", separator=" a"),
        )
        self.assertEqual(
            "sto jedna korun a dvacet jedna haléřů",
            num2words(101.21, lang="cz", to="currency", currency="CZK", separator=" a"),
        )
        self.assertEqual(
            "mínus dvanáct tisíc pětset devatenáct euro, 85 centů",
            num2words(-12519.85, lang="cz", to="currency", cents=False),
        )
        self.assertEqual(
            "sto dvacet tři koruny a padesát haléřů",
            num2words(123.50, lang="cz", to="currency", currency="CZK", separator=" a"),
        )
        self.assertEqual(
            "devatenáct euro, 50 centů",
            num2words(19.50, lang="cz", to="currency", cents=False),
        )
