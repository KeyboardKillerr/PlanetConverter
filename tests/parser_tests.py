import unittest
from unittest import *
from parser import *
from test_api import *


class ParserZSTest(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.test_source = ParserZSTestSource('test_files\\zs')

    def test_successful_parse(self):
        given = self.test_source.get_given('given_valid_1.txt')
        expected = self.test_source.get_expected('expected_1.json')
        result = ParserZS.parse(given)
        self.assertEqual(result, expected)

    def test_missing_top_line_throws_exception(self):
        given = self.test_source.get_given('given_invalid_1.txt')
        self.assertRaises(StartLineNotPresentException, ParserZS.parse, given)

    def test_missing_bottom_line_throws_exception(self):
        given = self.test_source.get_given('given_invalid_2.txt')
        self.assertRaises(EndLineNotPresentException, ParserZS.parse, given)

    def test_missing_column_throws_exception(self):
        given = self.test_source.get_given('given_invalid_3.txt')
        self.assertRaises(MissingColumnException, ParserZS.parse, given)


class EntitiesTest(TestCase):

    def test_get_water_name_codename(self):
        self.assertEqual('River', WaterNameProperty.dataframe_name())


if __name__ == '__main__':
    unittest.main()
