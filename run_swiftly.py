from lark import Lark
from transformer import SwiftlyTransformer
from interpreter import SwiftlyInterpreter

with open("swiftly_lark.txt") as f:
    grammar = f.read()

parser = Lark(grammar, parser='lalr', start='start')

with open("src/program.klynt") as f:
    code = f.read()

tree = parser.parse(code)
transformer = SwiftlyTransformer()
ast = transformer.transform(tree)

interpreter = SwiftlyInterpreter()
for stmt in ast:
    interpreter.eval(stmt)