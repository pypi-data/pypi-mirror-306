import sys
from minigrammar import *


class JsonSettings(LanguageSettings):

    @classmethod
    def ignore_characters(cls, char):
        return char == ' ' or char == '\t' or char == '\r'


rid = JsonSettings.get_id_of_rule_assuming_in_same_module


@either([rid("Array"), rid("Value"), rid("Object")])
class Json(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@chain([rid("OpenSquareBracket"), rid("MultipleArrayElems"), rid("ClosedSquareBracket")])
class Array(JsonSettings):
    def __repr__(self):
        return "[" + self.elems[1].__repr__() + "]"


@chain([rid("OpenCurlyBracket"), rid("MultipleObjectFields"), rid("ClosedCurlyBracket")])
class Object(JsonSettings):
    def __repr__(self):
        return "{" + self.elems[1].__repr__() + "}"


@repeating(rid("Json"), None, None, ',', False, False)
class MultipleArrayElems(LanguageSettings):
    def __repr__(self):
        return self.elems.__repr__()[1:-1]


@repeating(rid("ObjectField"), None, None, ',', False, False)
class MultipleObjectFields(LanguageSettings):
    def __repr__(self):
        return self.elems.__repr__()[1:-1]


@chain([rid("StringLiteral"), rid("Colon"), rid("Json")])
class ObjectField(LanguageSettings):
    def __repr__(self):
        return self.elems[0].__repr__() + " : " + self.elems[2].__repr__()


@either([rid("StringLiteral"), rid("FloatingPointLiteral"), rid("IntegerLiteral"), rid("BooleanLiteral"),
         rid("NullLiteral")])
class Value(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@regex_pattern(r'^"(?:[^"\\]|\\.)*"$')
class StringLiteral(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__()[1:-1]


@exact_match("null")
class NullLiteral(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@regex_pattern(r'^\d+$')
class IntegerLiteral(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@regex_pattern(r'^\d*\.\d+$')
class FloatingPointLiteral(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@regex_pattern(r'true|false')
class BooleanLiteral(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@exact_match("[")
class OpenSquareBracket(LanguageSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@exact_match("]")
class ClosedSquareBracket(LanguageSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@exact_match("{")
class OpenCurlyBracket(LanguageSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@exact_match("}")
class ClosedCurlyBracket(LanguageSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@exact_match(":")
class Colon(LanguageSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as file:
        iterator = FileParserIterator(file)
        json = Json(iterator)
        print(json)
