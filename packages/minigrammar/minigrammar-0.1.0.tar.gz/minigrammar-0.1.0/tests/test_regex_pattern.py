import unittest

from minigrammar.string_parser_iterator import StringParserIterator
from minigrammar.parsing import *
from minigrammar.exceptions import *
from minigrammar.language_settings import *


class ParsingRegexPatterns(unittest.TestCase):

    def test_case_digest_everything_successfully(self):
        @regex_pattern(r'\b-?\d+\b')
        class Integer(LanguageSettings): pass

        iterator = StringParserIterator("10")
        Integer(iterator)
        self.assertEqual(None, iterator.peek())

    def test_case_regex_mismatch_left_the_iterator_untouched(self):
        @regex_pattern(r'\b-?\d+\b')
        class Integer(LanguageSettings): pass

        iterator = StringParserIterator("XX")
        with self.assertRaises(CannotParseException):
            Integer(iterator)
        self.assertTrue("X" == iterator.peek())

    def test_case_regex_mismatch_on_empty_string_left_the_iterator_untouched(self):
        @regex_pattern(r'\b-?\d+\b')
        class Integer(LanguageSettings): pass

        iterator = StringParserIterator("")
        with self.assertRaises(CannotParseException):
            Integer(iterator)
        self.assertTrue(None == iterator.peek())

    def test_case_regex_ok_on_empty_string_left_the_iterator_untouched(self):
        @regex_pattern(r'')
        class Empty(LanguageSettings): pass

        iterator = StringParserIterator("")
        Empty(iterator)
        self.assertTrue(None == iterator.peek())

    def test_case_regex_for_string_literals(self):
        @regex_pattern(r'^"(?:[^"\\]|\\.)*"$')
        class StringLiteral(LanguageSettings): pass

        iterator = StringParserIterator('"Hello \\" World"X')
        StringLiteral(iterator)
        self.assertEqual("X", iterator.peek())


if __name__ == '__main__':
    unittest.main()
