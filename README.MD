# Swiftly Programming Language

Swiftly is a lightweight scripting language designed for learning, scripting, and automation. It features a Python-like syntax with Ruby-style flexibility and is interpreted through a custom parser and virtual machine built in Python.

---

## ✨ Features

### ✅ Variables
Declare variables using `let`:

```swiftly
let x = 10
let name = "Swiftly"
```

### ✅ Arithmetic
Supports basic arithmetic operations:

```swiftly
let total = 5 + 2 * 3
let ratio = 10 / 2
let mod = 10 % 3
```

### ✅ Comparison & Logical Operators
Swiftly supports:

- `==`, `!=`, `<`, `<=`, `>`, `>=`
- `and`, `or`, `not`

```swiftly
if x == 0 or not y > 2 {
  print("Condition met")
}
```

### ✅ Functions
Define reusable functions with parameters:

```swiftly
func greet(name) {
  print("Hello, " + name)
}

greet("Eddy")
```

Supports recursive functions and return values:

```swiftly
func factorial(n) {
  if n == 0 {
    return 1
  } else {
    return n * factorial(n - 1)
  }
}

print(factorial(5))  # Output: 120
```

### ✅ Control Flow

#### If / Else

```swiftly
if x < 10 {
  print("Small")
} else {
  print("Large")
}
```

#### While Loops

```swiftly
let i = 0
while i < 5 {
  print(i)
  i = i + 1
}
```

### ✅ Native Functions

- `print(...)`: Output values to console.

---

## 🧱 Under the Hood

Swiftly is built with:

- **Lark**: For parsing custom grammar
- **Custom AST Transformer**: Converts parse tree to Swiftly AST
- **Interpreter**: Executes AST node-by-node

---

## 📦 Example Program

```swiftly
let x = 5

func factorial(n) {
  if n == 0 {
    return 1
  } else {
    return n * factorial(n - 1)
  }
}

print(factorial(x))
```

---

## 🚧 Planned Features

- Class declarations (`class`, `init`, etc.)
- Modules / imports
- Arrays and Sets
- File I/O
- Error handling (try/catch)
- Package system for native libraries

---

## 🛠️ How to Run

```bash
python run_swiftly.py program.swiftly
```

Make sure you have the `swiftly_lark.txt` grammar file and your interpreter modules set up.

---

## 🧑‍💻 Author

Created by Eddy Chery.  
Interpreter and grammar handcrafted in Python.