from interpreter import SwiftlyInterpreter

interpreter = SwiftlyInterpreter()

# ----------------------------
# Programa AST para probar

interpreter = SwiftlyInterpreter()

program = [
    {
        'type': 'class_decl',
        'name': 'Persona',
        'body': [
            {
                'type': 'function_decl',
                'name': 'init',
                'params': ['self', 'nombre'],
                'body': [
                    {
                        'type': 'assignment',
                        'target': {
                            'type': 'member_access',
                            'object': {'type': 'identifier', 'name': 'self'},
                            'method': 'nombre'
                        },
                        'value': {'type': 'identifier', 'name': 'nombre'}
                    }
                ]
            },
            {
                'type': 'function_decl',
                'name': 'saludar',
                'params': ['self'],
                'body': [
                    {
                        'type': 'function_call',
                        'name': 'print',
                        'args': [
                            {
                                'type': 'binary_op',
                                'op': '+',
                                'left': {'type': 'string', 'value': 'Hola, '},
                                'right': {
                                    'type': 'member_access',
                                    'object': {'type': 'identifier', 'name': 'self'},
                                    'method': 'nombre',
                                    'args': []
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    },
    {
        'type': 'variable_decl',
        'name': 'p',
        'value': {
            'type': 'new_instance',
            'class_name': 'Persona',
            'args': [
                {'type': 'string', 'value': 'Eddy'}
            ]
        }
    },
    {
        'type': 'method_call',
        'object': {'type': 'identifier', 'name': 'p'},
        'method': 'saludar',
        'args': []
    },
    {
        "type": "try",
        "try_block": [ ... ],
        "except_var": "error",
        "except_block": [ ... ]
    }
]

for stmt in program:
    interpreter.eval(stmt)