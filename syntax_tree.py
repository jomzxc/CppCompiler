# syntax_tree.py

class Node:
    def __init__(self, lineno=None, lexpos=None):
        self.lineno = lineno
        self.lexpos = lexpos

class Program(Node):
    def __init__(self, declarations):
        super().__init__()
        self.declarations = declarations

class FunctionDefinition(Node):
    def __init__(self, return_type, name, params, body):
        super().__init__()
        self.return_type = return_type
        self.name = name
        self.params = params
        self.body = body

class Parameter(Node):
    def __init__(self, param_type, name):
        super().__init__()
        self.param_type = param_type
        self.name = name

class Block(Node):
    def __init__(self, statements):
        super().__init__()
        self.statements = statements

class Declaration(Node):
    def __init__(self, data_type, name, initializer):
        super().__init__()
        self.data_type = data_type
        self.name = name
        self.initializer = initializer

class Assignment(Node):
    def __init__(self, lvalue, rvalue):
        super().__init__()
        self.lvalue = lvalue
        self.rvalue = rvalue

class ReturnStatement(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

class IfStatement(Node):
    def __init__(self, condition, then_block, else_block):
        super().__init__()
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class ForStatement(Node):
    def __init__(self, init, condition, increment, body):
        super().__init__()
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body

class WhileStatement(Node):
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body

class BinaryExpression(Node):
    def __init__(self, op, left, right):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right

class Identifier(Node):
    def __init__(self, name, lineno=None, lexpos=None): # Modified to accept lineno and lexpos
        super().__init__(lineno, lexpos)
        self.name = name

class Literal(Node):
    def __init__(self, type, value, lineno=None, lexpos=None): # Modified to accept lineno and lexpos
        super().__init__(lineno, lexpos)
        self.type = type
        self.value = value

class EmptyStatement(Node):
    def __init__(self):
        super().__init__()

class CallExpression(Node):
    def __init__(self, callee, arguments):
        super().__init__()
        self.callee = callee
        self.arguments = arguments