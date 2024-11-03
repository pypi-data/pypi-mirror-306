import unittest

from minigrammar.string_parser_iterator import StringParserIterator
from minigrammar.language_settings import LanguageSettings
from minigrammar.parsing import *
from minigrammar.exceptions import *


class ParsingEither(unittest.TestCase):

    def test_case_digest_everything_successfully(self):
        @exact_match("10")
        class Number10(LanguageSettings): pass

        @exact_match("Hello")
        class Hello(LanguageSettings): pass

        @either([Hello.get_id(), Number10.get_id()])
        class Number10OrHello(LanguageSettings): pass

        iterator = StringParserIterator("Hello")
        Number10OrHello(iterator)
        self.assertEqual(None, iterator.peek())

    def test_case_digest_everything_successfully2(self):
        @exact_match("10")
        class Number10(LanguageSettings): pass

        @exact_match("Hello")
        class Hello(LanguageSettings): pass

        @either([Hello.get_id(), Number10.get_id()])
        class Number10OrHello(LanguageSettings): pass

        iterator = StringParserIterator("10")
        Number10OrHello(iterator)
        self.assertEqual(None, iterator.peek())

    def test_case_no_case_matches(self):
        @exact_match("10")
        class Number10(LanguageSettings): pass

        @exact_match("Hello")
        class Hello(LanguageSettings): pass

        @either([Hello.get_id(), Number10.get_id()])
        class Number10OrHello(LanguageSettings): pass

        iterator = StringParserIterator("XX")
        with self.assertRaises(CannotParseException):
            Number10OrHello(iterator)
        self.assertEqual("X", iterator.peek())


if __name__ == '__main__':
    unittest.main()
