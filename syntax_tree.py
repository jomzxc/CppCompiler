# syntax_tree.py
class Node:
    def __repr__(self):
        return self.__class__.__name__

class Program(Node):
    def __init__(self, declarations):
        self.declarations = declarations

    def __repr__(self):
        return f"Program(declarations={self.declarations})"

class FunctionDefinition(Node):
    def __init__(self, return_type, name, params, body):
        self.return_type = return_type
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionDefinition(return_type='{self.return_type}', name='{self.name}', params={self.params}, body={self.body})"

class Parameter(Node):
    def __init__(self, param_type, name):
        self.param_type = param_type
        self.name = name

    def __repr__(self):
        return f"Parameter(type='{self.param_type}', name='{self.name}')"

class Block(Node):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block(statements={self.statements})"

class Declaration(Node):
    def __init__(self, data_type, name, initializer):
        self.data_type = data_type
        self.name = name
        self.initializer = initializer

    def __repr__(self):
        return f"Declaration(type='{self.data_type}', name='{self.name}', initializer={self.initializer})"

class Assignment(Node):
    def __init__(self, lvalue, rvalue):
        self.lvalue = lvalue
        self.rvalue = rvalue

    def __repr__(self):
        return f"Assignment(lvalue='{self.lvalue}', rvalue={self.rvalue})"

class ReturnStatement(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"ReturnStatement(value={self.value})"

class IfStatement(Node):
    def __init__(self, condition, then_block, else_block):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def __repr__(self):
        return f"IfStatement(condition={self.condition}, then_block={self.then_block}, else_block={self.else_block})"

class ForStatement(Node):
    def __init__(self, init, condition, increment, body):
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body

    def __repr__(self):
        return f"ForStatement(init={self.init}, condition={self.condition}, increment={self.increment}, body={self.body})"

class WhileStatement(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileStatement(condition={self.condition}, body={self.body})"

class BinaryExpression(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinaryExpression(op='{self.op}', left={self.left}, right={self.right})"

class Literal(Node):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Literal(type='{self.type}', value={self.value})"

class Identifier(Node):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier(name='{self.name}')"

class EmptyStatement(Node):
    def __repr__(self):
        return "EmptyStatement()"

class CallExpression(Node):
    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments

    def __repr__(self):
        return f"CallExpression(callee={self.callee}, arguments={self.arguments})"