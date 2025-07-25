from lark import Transformer, v_args

@v_args(inline=True)
class SwiftlyTransformer(Transformer):
    def start(self, *items):
        return list(items)

    def variable_decl(self, *items):
        return {"type": "variable_decl", "name": str(items[0]), "value": items[1]}

    def assignment(self, *items):
        return {"type": "assignment", "target": items[0], "value": items[1]}

    def function_decl(self, *items):
        name = str(items[0])
        params = items[1] if isinstance(items[1], list) else []
        body = items[-1]
        return {"type": "function_decl", "name": name, "params": params, "body": body}

    def class_decl(self, *items):
        name = str(items[0])
        parent = str(items[1]) if len(items) == 3 else None
        body = items[-1]
        return {"type": "class_decl", "name": name, "parent": parent, "body": body}

    def if_stmt(self, *items):
        condition = items[0]
        then_branch = items[1]
        else_branch = items[2] if len(items) > 2 else None
        return {"type": "if_stmt", "condition": condition, "then": then_branch, "else": else_branch}

    def while_stmt(self, *items):
        return {"type": "while_stmt", "condition": items[0], "body": items[1]}

    def for_stmt(self, *items):
        return {"type": "for_stmt", "var": str(items[0]), "iterable": items[1], "body": items[2]}

    def return_stmt(self, *items):
        return {"type": "return_stmt", "value": items[0] if items else None}

    def expression_stmt(self, expr):
        return expr

    def block(self, *items):
        return list(items)

    def param_list(self, *items):
        return [str(i) for i in items]

    def arg_list(self, *items):
        return list(items)

    def number(self, *items):
        return {"type": "number", "value": float(items[0]) if '.' in str(items[0]) else int(items[0])}

    def string(self, token):
        s = str(token)
        if s.startswith('"') and s.endswith('"'):
            s = s[1:-1]
        return {"type": "string", "value": s}

    def var(self, *items):
        return {"type": "var", "name": str(items[0])}

    def member_access(self, *items):
        if not items:
            return None
        result = items[0]
        for member in items[1:]:
            result = {"type": "member_access", "object": result, "method": str(member)}
        return result

    def call(self, *items):
        if len(items) == 1:
            return items[0]
        obj = items[0]
        args = items[1] if len(items) > 1 else []

        # If the call target is a member access (obj.method), extract method name
        if obj.get("type") == "member_access":
            method_name = obj["method"]
            return {"type": "method_call", "object": obj["object"], "method": method_name, "args": args}

        # Otherwise, it's a plain function call
        return {"type": "function_call", "name": obj["name"], "args": args}


    def array_literal(self, *items):
        return {"type": "array", "elements": items}

    def set_literal(self, *items):
        return {"type": "set", "elements": items}

    def true(self, _): return {"type": "bool", "value": True}
    def false(self, _): return {"type": "bool", "value": False}
    def null(self, _): return {"type": "null", "value": None}

    # Binary operators
    def add(self, *items): return {"type": "add", "left": items[0], "right": items[1]}
    def sub(self, *items): return {"type": "sub", "left": items[0], "right": items[1]}
    def mul(self, *items): return {"type": "mul", "left": items[0], "right": items[1]}
    def div(self, *items): return {"type": "div", "left": items[0], "right": items[1]}
    def mod(self, *items): return {"type": "mod", "left": items[0], "right": items[1]}

    def eq_op(self, *items): return {"type": "eq", "left": items[0], "right": items[1]}
    def neq_op(self, *items): return {"type": "neq", "left": items[0], "right": items[1]}
    def lt_op(self, *items): return {"type": "lt", "left": items[0], "right": items[1]}
    def le_op(self, *items): return {"type": "le", "left": items[0], "right": items[1]}
    def gt_op(self, *items): return {"type": "gt", "left": items[0], "right": items[1]}
    def ge_op(self, *items): return {"type": "ge", "left": items[0], "right": items[1]}

    def or_op(self, *items): return {"type": "or", "left": items[0], "right": items[1]}
    def and_op(self, *items): return {"type": "and", "left": items[0], "right": items[1]}

    def not_op(self, *items): return {"type": "not", "value": items[0]}
    def neg(self, *items): return {"type": "neg", "value": items[0]}

    def try_stmt(self, *items):
        return {
            "type": "try",
            "try_block": items[0],
            "error_var": items[1].value,
            "catch_block": items[2],
        }

    def raise_stmt(self, *items):
        return {
            "type": "raise",
            "value": items[0],
        }
    
    def dict_literal(self, *pairs):
        return {
            "type": "dict_literal",
            "pairs": list(pairs)
        }

    def pair(self, key, value):
        return {"key": key, "value": value}