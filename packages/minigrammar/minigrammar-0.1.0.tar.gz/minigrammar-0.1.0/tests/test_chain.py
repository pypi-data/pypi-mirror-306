import unittest

from minigrammar.string_parser_iterator import StringParserIterator
from minigrammar.language_settings import LanguageSettings
from minigrammar.parsing import *
from minigrammar.exceptions import *


class ParsingChain(unittest.TestCase):

    def test_case_digest_everything_successfully(self):
        @exact_match("10")
        class Number10(LanguageSettings): pass

        @exact_match("Hello")
        class Hello(LanguageSettings): pass

        @chain([Number10.get_id(), Hello.get_id()])
        class Number10ThenHello(LanguageSettings): pass

        iterator = StringParserIterator("10Hello")
        Number10ThenHello(iterator)
        self.assertEqual(None, iterator.peek())

    def test_case_full_mismatch(self):
        @exact_match("10")
        class Number10(LanguageSettings): pass

        @exact_match("Hello")
        class Hello(LanguageSettings): pass

        @chain([Number10.get_id(), Hello.get_id()])
        class Number10ThenHello(LanguageSettings): pass

        iterator = StringParserIterator("XX")
        with self.assertRaises(CannotParseException):
            Number10ThenHello(iterator)
        self.assertEqual("X", iterator.peek())

    def test_case_full_mismatch_on_empty_string(self):
        @exact_match("10")
        class Number10(LanguageSettings): pass

        @exact_match("Hello")
        class Hello(LanguageSettings): pass

        @chain([Number10.get_id(), Hello.get_id()])
        class Number10ThenHello(LanguageSettings): pass

        iterator = StringParserIterator("")
        with self.assertRaises(CannotParseException):
            Number10ThenHello(iterator)
        self.assertEqual(None, iterator.peek())

    def test_case_full_partial_mismatch(self):
        @exact_match("10")
        class Number10(LanguageSettings): pass

        @exact_match("Hello")
        class Hello(LanguageSettings): pass

        @chain([Number10.get_id(), Hello.get_id()])
        class Number10ThenHello(LanguageSettings): pass

        iterator = StringParserIterator("10")
        with self.assertRaises(CannotParseException):
            Number10ThenHello(iterator)
        self.assertEqual("1", iterator.peek())

    def test_case_full_partial_mismatch2(self):
        @exact_match("10")
        class Number10(LanguageSettings): pass

        @exact_match("Hello")
        class Hello(LanguageSettings): pass

        @chain([Number10.get_id(), Hello.get_id()])
        class Number10ThenHello(LanguageSettings): pass

        iterator = StringParserIterator("10He")
        with self.assertRaises(CannotParseException):
            Number10ThenHello(iterator)
        self.assertEqual("1", iterator.peek())


if __name__ == '__main__':
    unittest.main()
