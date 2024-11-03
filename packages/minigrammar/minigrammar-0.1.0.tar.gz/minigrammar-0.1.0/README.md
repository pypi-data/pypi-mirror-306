# MiniGrammar

A parser-generation library that makes use of python metaprogramming to inject the parsing-logic 
into user defined AST-classes. All the user has to do is to decorate the classes in the codebase
with the provided decorators. Such decorators will inject into the classes a constructor (`__init__`) and
a list of parsed elements (`elems`), wich will be accessible for every instance of the classes.

---

Consider the following grammar:
```g4
expression
    : sum
    | mul
    | wrapped_expression
    | num
    | var
    ;

wrapped_expression: '(' expression ')'
sum: expression PLUS expression;
mul: expression STAR expression;
var: ID;
num: INT;
```

This grammar is left-recursive, so it will cause the parser to loop forever. But we can 
change it in such a way to avoid this problem by refactoring it as follows:

```g4
expression
    : addend ((PLUS addend)*) 
    ;

addend
    : factor ((STAR factor)*) 
    ;

factor
    : num
    | var
    | wrapped_expression
    ;

wrapped_expression: '(' expression ')'
var: ID;
num: INT;
```

Then, for every grammar rule we define a python class that will end up being used to build the **AST** itself. For instance,
let's consider the class `WrappedExpression`

```python
@chain([rid("OpenParen"), rid("Expression"), rid("ClosedParen")])
class WrappedExpression(MathSettings):
    def __repr__(self):
        return " ( " + self.elems[1].__repr__() + " ) "

@exact_match("(")
class OpenParen(MathSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@exact_match(")")
class ClosedParen(MathSettings):
    def __repr__(self):
        return self.elems[0].__repr__()
```

This class has also a way to be printed in the console. The user can add method for evaluating the expression or to serialize it in multiple ways
and so on. Possibilities are limitless, feel free to explore with your creativity as long as the grammar is not left-recursive and as long as 
regex are non-prefix. The whole example has being uploaded in `MiniGrammar/examples/math_demo.py`.