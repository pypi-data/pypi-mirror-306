import unittest

from minigrammar.string_parser_iterator import StringParserIterator
from minigrammar.language_settings import LanguageSettings
from minigrammar.parsing import *
from minigrammar.exceptions import *


class ParsingRepeating(unittest.TestCase):

    def test_case_ok_packed(self):
        @exact_match("10")
        class Number10(LanguageSettings): pass

        @repeating(Number10.get_id(), None, None, ',', True, False)
        class Numbers(LanguageSettings): pass

        iterator = StringParserIterator("10,10,10")
        Numbers(iterator)
        self.assertEqual(None, iterator.peek())

    def test_case_ok_well_far_apart(self):
        @exact_match("10")
        class Number10(LanguageSettings): pass

        @repeating(Number10.get_id(), None, None, ',', True, False)
        class Numbers(LanguageSettings): pass

        iterator = StringParserIterator("10 , 10 , 10")
        Numbers(iterator)
        self.assertEqual(None, iterator.peek())

    def test_case_ok_mixed(self):
        @exact_match("10")
        class Number10(LanguageSettings): pass

        @repeating(Number10.get_id(), None, None, ',', True, False)
        class Numbers(LanguageSettings): pass

        iterator = StringParserIterator(" 10 ,10,10")
        Numbers(iterator)
        self.assertEqual(None, iterator.peek())


    def test_case_mismatch_defaulted_to_sequence_of_zero_elems_ok(self):
        @exact_match("10")
        class Number10(LanguageSettings): pass

        @repeating(Number10.get_id(), None, None, ',', True, False)
        class Numbers(LanguageSettings): pass

        iterator = StringParserIterator("XX, 10")
        Numbers(iterator)
        self.assertEqual("X", iterator.peek())

    def test_case_mismatch_defaulted_to_sequence_of_zero_elems_err(self):
        @exact_match("10")
        class Number10(LanguageSettings): pass

        @repeating(Number10.get_id(), 5, None, ',', True, False)
        class Numbers(LanguageSettings): pass

        iterator = StringParserIterator("XX, 10")
        with self.assertRaises(CannotParseException):
            Numbers(iterator)
        self.assertEqual("X", iterator.peek())

    def test_case_too_many_elements(self):
        @exact_match("10")
        class Number10(LanguageSettings): pass

        @repeating(Number10.get_id(), 1, 3, ',', True, False)
        class Numbers(LanguageSettings): pass

        iterator = StringParserIterator("10, 10, 10, 10")
        with self.assertRaises(CannotParseException):
            Numbers(iterator)
        self.assertEqual("1", iterator.peek())

    def test_case_trailing_used_partially_ok_parsed_prefix(self):
        @exact_match("10")
        class Number10(LanguageSettings): pass

        @repeating(Number10.get_id(), None, None, ',', True, False)
        class Numbers(LanguageSettings): pass

        iterator = StringParserIterator("10, 10, 10, XX, ")
        Numbers(iterator)
        self.assertEqual("X", iterator.peek())

    def test_case_not_used_but_expected(self):
        @exact_match("10")
        class Number10(LanguageSettings): pass

        @repeating(Number10.get_id(), None, None, ',', True, True)
        class Numbers(LanguageSettings): pass

        iterator = StringParserIterator("10, 10, 10, 10 ")
        with self.assertRaises(CannotParseException):
            Numbers(iterator)
        self.assertEqual("1", iterator.peek())


    def test_case_trailing_used_but_not_allowed(self):
        @exact_match("10")
        class Number10(LanguageSettings): pass

        @repeating(Number10.get_id(), None, None, ',', False, False)
        class Numbers(LanguageSettings): pass

        iterator = StringParserIterator("10, 10, 10, 10, ")
        with self.assertRaises(CannotParseException):
            Numbers(iterator)
        self.assertEqual("1", iterator.peek())


if __name__ == '__main__':
    unittest.main()
