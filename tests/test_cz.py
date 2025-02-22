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


# Numbers and number fragments under thousand form open composites, each component is ordinal
TEST_CASES_ORDINAL_UNDER_THOUSAND = (
    # 0-99
    (0, "nultý"),  # ones, base case
    (1, "první"),  # ones
    (11, "jedenáctý"),  # teens
    (20, "dvacátý"),  # twenties
    (21, "dvacátý první"),  # twenties + ones
    # 100-199
    (100, "stý"),  # hundred
    (101, "stý první"),  # hundred + ones
    (111, "stý jedenáctý"),  # hundred + teens
    (120, "stý dvacátý"),  # hundred + twenties
    (121, "stý dvacátý první"),  # hundred + twenties + ones
    # 200-999
    (200, "dvoustý"),  # hundreds
    (201, "dvoustý první"),  # hundreds + ones
    (211, "dvoustý jedenáctý"),  # hundreds + teens
    (220, "dvoustý dvacátý"),  # hundreds + twenties
    (221, "dvoustý dvacátý první"),  # hundreds + twenties + ones
)

# Numbers and number fragments under thousand freely combine with higher-level fragments, no interference
TEST_CASES_ORDINAL_2XXX = (
    # 1-99
    (1001, "tisící první"),  # thousand + ones
    (1011, "tisící jedenáctý"),  # thousand + teens
    (1020, "tisící dvacátý"),  # thousand + twenties
    (1021, "tisící dvacátý první"),  # thousand + twenties + ones
    # 100-199
    (2100, "dvoutisící stý"),  # thousand + hundred
    (2101, "dvoutisící stý první"),  # thousand + hundred + ones
    (2111, "dvoutisící stý jedenáctý"),  # thousand + hundred + teens
    (2120, "dvoutisící stý dvacátý"),  # thousand + hundred + twenties
    (2121, "dvoutisící stý dvacátý první"),  # thousand + hundred + twenties + ones
    # 200-999
    (2200, "dvoutisící dvoustý"),  # thousand + hundreds
    (2201, "dvoutisící dvoustý první"),  # thousand + hundreds + ones
    (2211, "dvoutisící dvoustý jedenáctý"),  # thousand + hundreds + teens
    (2220, "dvoutisící dvoustý dvacátý"),  # thousand + hundreds + twenties
    (2221, "dvoutisící dvoustý dvacátý první"),  # thousand + hundreds + twenties + ones
)
TEST_CASES_ORDINAL_001XXX_FRAGMENT_INTERFERENCE = (
    # 100-199
    (1100, "jedenáctistý"),  # thousand + hundred, instead of 'tisící stý'
    (1101, "jedenáctistý první"),  # thousand + hundred + ones, instead of 'tisící stý první'
    (1111, "jedenáctistý jedenáctý"),  # thousand + hundred + teens, instead of 'tisící stý jedenáctý'
    (1120, "jedenáctistý dvacátý"),  # thousand + hundred + twenties, instead of 'tisící stý dvacátý'
    (1121, "jedenáctistý dvacátý první"),  # thousand + hundred + twenties + ones, instead of 'tisící stý dvacátý první'
    # 200-999
    (1200, "dvanáctistý"),  # thousand + hundreds, instead of 'tisící dvoustý'
    (1201, "dvanáctistý první"),  # thousand + hundreds + ones, instead of 'tisící dvoustý první'
    (1211, "dvanáctistý jedenáctý"),  # thousand + hundreds + teens, instead of 'tisící dvoustý jedenáctý'
    (1220, "dvanáctistý dvacátý"),  # thousand + hundreds + twenties, instead of 'tisící dvoustý dvacátý'
    (1221, "dvanáctistý dvacátý první"),  # thousand + hundreds + twenties + ones, instead of 'tisící dvoustý dvacátý první'
)  # fmt: skip


# Number fragments over thousands form open composites, each component is ordinal
TEST_CASES_ORDINAL_XXX000 = (
    (1 * 1000, "tisící"),  # ones
    (2 * 1000, "dvoutisící"),  # ones
    (5 * 1000, "pětitisící"),  # ones
    (11 * 1000, "jedenáctitisící"),  # teens
    (20 * 1000, "dvacetitisící"),  # twenties
    (21 * 1000, "dvacetijedentisící"),  # twenties + ones
    # 100-199
    (100 * 1000, "stotisící"),  # hundred
    (101 * 1000, "stojedentisící"),  # hundred + ones
    (111 * 1000, "stojedenáctitisící"),  # hundred + teens
    (120 * 1000, "stodvacetitisící"),  # hundred + twenties
    (121 * 1000, "stodvacetijedentisící"),  # hundred + twenties + ones
    # 200-999
    (200 * 1000, "dvousettisící"),  # hundreds
    (201 * 1000, "dvousetjedentisící"),  # hundreds + ones
    (211 * 1000, "dvousetjedenáctitisící"),  # hundreds + teens
    (220 * 1000, "dvousetdvacetitisící"),  # hundreds + twenties
    (221 * 1000, "dvousetdvacetijedentisící"),  # hundreds + twenties + ones
)


TEST_CASES_ORDINAL_MILLIONS = (
    (10**6, "miliontý"),
    (100 * 10**6, "stomiliontý"),
    (223 * 10**6, "dvousetdvacetitřímiliontý"),
    # higher orders
    (10**9, "miliardtý"),
    (10**12, "biliontý"),
)

TEST_CASES_ORDINAL_REGRESSION = (
    # tří with long i
    (300, "třístý"),
    # compounded tens in range 10-40 use the cardinal genitive form
    (10 * 1000, "desetitisící"),
    (40 * 1000, "čtyřicetitisící"),
    # compounded tens in range 50-90 use the ordinal form
    (50 * 1000, "padesátitisící"),
    (90 * 1000, "devadesátitisící"),
)

TEST_CASES_ORDINAL = (
    TEST_CASES_ORDINAL_UNDER_THOUSAND
    + TEST_CASES_ORDINAL_2XXX
    + TEST_CASES_ORDINAL_001XXX_FRAGMENT_INTERFERENCE
    + TEST_CASES_ORDINAL_XXX000
    + TEST_CASES_ORDINAL_MILLIONS
    + TEST_CASES_ORDINAL_REGRESSION
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
