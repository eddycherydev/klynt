from lark import Lark
from transformer import SwiftlyTransformer
from interpreter import SwiftlyInterpreter
from pprint import pprint

with open("swiftly_lark.txt") as f:
    swiftly_grammar = f.read()

# Crear el parser
parser = Lark(swiftly_grammar, parser='lalr', start='start', debug=True)

# Ejemplo de código Swiftly para parsear
code = """
let x = 0

func contarHasta(n) {
  while x < n {
    print(x)
    x = x + 1
  }
  return x
}

if x == 0 {
  print("Inicio en cero")
} else {
  print("No inicia en cero")
}

contarHasta(5)
"""

# Parsear el código
tree = parser.parse(code)



# Transformar el árbol en AST
transformer = SwiftlyTransformer()
ast = transformer.transform(tree)

#print("=== AST ===")

#pprint(ast)



interpreter = SwiftlyInterpreter()
for stmt in ast:
    interpreter.eval(stmt)