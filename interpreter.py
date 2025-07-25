class SwiftlyInstance:
    def __init__(self, klass, interpreter):
        self.klass = klass
        self.interpreter = interpreter
        self.fields = {}

    def get(self, name):
        if name in self.fields:
            return self.fields[name]
        method = self.klass.methods.get(name)
        if method:
            def bound_method(*args):
                return self.interpreter.call_method_on_instance(self, name, args)
            return bound_method
        raise Exception(f"Undefined property or method '{name}'")

    def set(self, name, value):
        self.fields[name] = value

class SwiftlyClass:
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods  # dict: method_name -> function node

    def instantiate(self, interpreter, args):
        instance = SwiftlyInstance(self, interpreter)
        init_method = self.methods.get('init')
        if init_method:
            interpreter.call_method_on_instance(instance, 'init', args)
        return instance

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class SwiftlyInterpreter:
    def __init__(self):
        self.env = {}
        self.classes = {}

    def eval(self, node):
        t = node['type']

        if t == 'number':
            return node['value']
        if t == 'string':
            return node['value']
        if t == 'bool':
            return node['value']
        if t == 'null':
            return None
        if t == 'var':
            name = node['name']
            if name in self.env:
                return self.env[name]
            else:
                raise Exception(f"Variable '{name}' not defined")
        if t == 'identifier':
            name = node['name']
            if name in self.env:
                return self.env[name]
            else:
                raise Exception(f"Variable '{name}' not defined")

        if t == 'variable_decl':
            value = self.eval(node['value'])
            self.env[node['name']] = value
            return None

        if t == 'assignment':
            target = node.get('target', node.get('name'))
            value = self.eval(node['value'])
            if isinstance(target, dict) and target['type'] == 'member_access':
                obj = self.eval(target['object'])
                if not isinstance(obj, SwiftlyInstance):
                    raise Exception("Can only assign properties on instances")
                prop_name = target['method']
                obj.set(prop_name, value)
                return None
            else:
                if target in self.env:
                    self.env[target] = value
                    return None
                else:
                    raise Exception(f"Variable '{target}' not defined")

        if t == 'binary_op':
            left = self.eval(node['left'])
            right = self.eval(node['right'])
            op = node['op']
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                return left / right
            elif op == '==':
                return left == right
            elif op == '!=':
                return left != right
            elif op == '<':
                return left < right
            elif op == '<=':
                return left <= right
            elif op == '>':
                return left > right
            elif op == '>=':
                return left >= right
            elif op == 'and':
                return left and right
            elif op == 'or':
                return left or right
            else:
                raise Exception(f"Unknown operator {op}")

        if t == 'array_literal':
            return [self.eval(elem) for elem in node['elements']]

        if t == 'set_literal':
            return set(self.eval(elem) for elem in node['elements'])

        if t == 'member_access':
            obj = self.eval(node['object'])
            method_or_prop = node['method']
            args = [self.eval(arg) for arg in node.get('args', [])]
            if isinstance(obj, SwiftlyInstance):
                if args:
                    return self.call_method_on_instance(obj, method_or_prop, args)
                else:
                    return obj.get(method_or_prop)
            return self.call_method(obj, method_or_prop, args)

        if t == 'method_call':
            obj = self.eval(node['object'])
            method = node['method']
            args = [self.eval(arg) for arg in node.get('args', [])]
            if isinstance(obj, SwiftlyInstance):
                return self.call_method_on_instance(obj, method, args)
            else:
                return self.call_method(obj, method, args)

        if t == 'function_call':
            func_name = node['name']
            args = [self.eval(arg) for arg in node.get('args', [])]
            if func_name == 'print':
                print(*args)
                return None
            func = self.env.get(func_name)
            if func is None:
                raise Exception(f"Function '{func_name}' not defined")
            return self.call_function(func, args)

        if t == 'function_decl':
            self.env[node['name']] = node
            return None

        if t == 'class_decl':
            name = node['name']
            methods = {}
            for method_node in node['body']:
                if method_node['type'] == 'function_decl':
                    methods[method_node['name']] = method_node
            klass = SwiftlyClass(name, methods)
            self.classes[name] = klass
            self.env[name] = klass
            return None

        if t == 'new_instance':
            class_name = node['class_name']
            klass = self.classes.get(class_name)
            if not klass:
                raise Exception(f"Class '{class_name}' not found")
            args = [self.eval(arg) for arg in node.get('args', [])]
            return klass.instantiate(self, args)

        if t == 'dict_literal':
            result = {}
            for pair in node['pairs']:
                key = self.eval(pair['key'])
                value = self.eval(pair['value'])
                result[key] = value
            return result

        # Soporte para operaciones binarias específicas
        if t == 'add':
            left = self.eval(node['left'])
            right = self.eval(node['right'])
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        if t == 'sub':
            return self.eval(node['left']) - self.eval(node['right'])
        if t == 'mul':
            return self.eval(node['left']) * self.eval(node['right'])
        if t == 'div':
            return self.eval(node['left']) / self.eval(node['right'])
        if t == 'mod':
            return self.eval(node['left']) % self.eval(node['right'])

        if t == 'if_stmt':
            condition = self.eval(node['condition'])
            if condition:
                for stmt in node['then']:
                    self.eval(stmt)
            elif 'else' in node and node['else']:
                for stmt in node['else']:
                    self.eval(stmt)
            return None

        if t == 'while_stmt':
            while self.eval(node['condition']):
                for stmt in node['body']:
                    self.eval(stmt)
            return None

        if t == 'return_stmt':
            value = self.eval(node['value']) if node.get('value') else None
            raise ReturnException(value)
        if t == 'eq':
            return self.eval(node['left']) == self.eval(node['right'])
        if t == 'neq':
            return self.eval(node['left']) != self.eval(node['right'])
        if t == 'lt':
            return self.eval(node['left']) < self.eval(node['right'])
        if t == 'le':
            return self.eval(node['left']) <= self.eval(node['right'])
        if t == 'gt':
            return self.eval(node['left']) > self.eval(node['right'])
        if t == 'ge':
            return self.eval(node['left']) >= self.eval(node['right'])
        if t == 'and':
            return self.eval(node['left']) and self.eval(node['right'])
        if t == 'or':
            return self.eval(node['left']) or self.eval(node['right'])
        if t == 'not':
            return not self.eval(node['value'])
        if t == "try":
            try:
                for stmt in node["try_block"]:
                    self.eval(stmt)
            except Exception as e:
                if "except_block" in node and node["except_block"]:
                    self.env[node["except_var"]] = str(e)
                    for stmt in node["except_block"]:
                        self.eval(stmt)
            return None

        if t == "raise":
            value = self.eval(node["value"])
            raise Exception(value)

        raise Exception(f"Unsupported node type: {t}")

    def call_method_on_instance(self, instance, method_name, args):
        method = instance.klass.methods.get(method_name)
        if not method:
            raise Exception(f"Method '{method_name}' not found in class '{instance.klass.name}'")
        local_env = {method['params'][0]: instance}
        for param, arg in zip(method['params'][1:], args):
            local_env[param] = arg
        saved_env = self.env
        self.env = {**self.env, **local_env}
        ret = None
        for stmt in method['body']:
            ret = self.eval(stmt)
        self.env = saved_env
        return ret
    
    def call_method(self, obj, method, args):
        if method in ('size', 'length'):
            if isinstance(obj, (list, set, dict)):
                return len(obj)
            raise Exception(f"Method '{method}' not supported for this type")

        if method == 'contains':
            if isinstance(obj, (list, set)):
                return args[0] in obj
            raise Exception(f"Method '{method}' not supported for this type")

        if method == 'push':
            if isinstance(obj, list):
                obj.append(args[0])
                return None
            raise Exception(f"Method '{method}' not supported for this type")

        if method == 'pop':
            if isinstance(obj, list):
                return obj.pop()
            raise Exception(f"Method '{method}' not supported for this type")

        if method == 'add':
            if isinstance(obj, set):
                obj.add(args[0])
                return None
            raise Exception(f"Method '{method}' not supported for this type")

        if method == 'remove':
            if isinstance(obj, set):
                obj.discard(args[0])
                return None
            raise Exception(f"Method '{method}' not supported for this type")

        if method == 'first':
            if isinstance(obj, list):
                return obj[0] if obj else None
            raise Exception(f"Method '{method}' not supported for this type")

        if method == 'last':
            if isinstance(obj, list):
                return obj[-1] if obj else None
            raise Exception(f"Method '{method}' not supported for this type")

        if method == 'is_empty':
            if isinstance(obj, (list, set, dict)):
                return len(obj) == 0
            raise Exception(f"Method '{method}' not supported for this type")

        if method == 'clear':
            if isinstance(obj, (list, set)):
                obj.clear()
                return None
            raise Exception(f"Method '{method}' not supported for this type")

        if method == 'keys':
            if isinstance(obj, dict):
                return list(obj.keys())
            raise Exception(f"Method '{method}' not supported for this type")

        if method == 'values':
            if isinstance(obj, dict):
                return list(obj.values())
            raise Exception(f"Method '{method}' not supported for this type")

        if method == 'items':
            if isinstance(obj, dict):
                return list(obj.items())
            raise Exception(f"Method '{method}' not supported for this type")

        if method == 'get':
            if isinstance(obj, dict):
                return obj.get(args[0], None)
            raise Exception(f"Method '{method}' not supported for this type")

        if method == 'has_key':
            if isinstance(obj, dict):
                return args[0] in obj
            raise Exception(f"Method '{method}' not supported for this type")

        raise Exception(f"Unknown method '{method}'")

    def call_function(self, func_node, args):
        local_env = {}
        for param, arg in zip(func_node['params'], args):
            local_env[param] = arg
        saved_env = self.env
        self.env = {**self.env, **local_env}
        try:
            for stmt in func_node['body']:
                self.eval(stmt)
        except ReturnException as ret:
            self.env = saved_env
            return ret.value
        self.env = saved_env
        return None
