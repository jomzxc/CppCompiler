from unittest import TestCase
import unittest
from ply import yacc
from lexer import lexer, tokens
from parser import parser


class ParserTest(unittest.TestCase):
    def test_empty_program(self):
        code = ""
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('program', []), result) #Corrected

    def test_function_no_params(self):
        code = "int main() {}"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('program', [('function', 'int', 'main', [], ('block', []))]), result) #Corrected

    def test_function_with_no_params(self):
        code = "void foo(){}"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('program', [('function', 'void', 'foo', [], ('block', []))]), result) #Corrected

    def test_function_with_params(self):
        code = "int add(int a, int b) {}"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(
            ('program', [('function', 'int', 'add', [('param', 'int', 'a'), ('param', 'int', 'b')], ('block', []))]), result) #Corrected

    def test_block_in_function(self):
        code = """
        int main(){
             { int x; }
        }
        """
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(( 'program', [('function', 'int', 'main', [], ('block', [('block', [('declare', 'int', 'x', None)])]))]), result) #Corrected

    def test_declaration_statement(self):
        code = "int x;"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('declare', 'int', 'x', None), result) #Corrected

    def test_declaration_assignment(self):
        code = "int x = 5;"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('declare', 'int', 'x', ('number', 5)), result) #Corrected

    def test_return_statement(self):
        code = "return 5;"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('return', ('number', 5)), result) #Corrected

    def test_return_empty(self):
        code = "return;"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('return', []), result) #Corrected

    def test_expression_binop(self):
        code = "x + y;"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('binop', '+', ('id', 'x'), ('id', 'y')), result) #Corrected

        code = "x - y;"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('binop', '-', ('id', 'x'), ('id', 'y')), result) #Corrected

        code = "x * y;"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('binop', '*', ('id', 'x'), ('id', 'y')), result) #Corrected

        code = "x / y;"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('binop', '/', ('id', 'x'), ('id', 'y')), result) #Corrected

        code = "x == y;"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('binop', '==', ('id', 'x'), ('id', 'y')), result) #Corrected

        code = "x != y;"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('binop', '!=', ('id', 'x'), ('id', 'y')), result) #Corrected

        code = "x < y;"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('binop', '<', ('id', 'x'), ('id', 'y')), result) #Corrected

        code = "x > y;"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('binop', '>', ('id', 'x'), ('id', 'y')), result) #Corrected

        code = "x <= y;"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('binop', '<=', ('id', 'x'), ('id', 'y')), result) #Corrected

        code = "x >= y;"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('binop', '>=', ('id', 'x'), ('id', 'y')), result) #Corrected

    def test_expression_assign(self):
        code = "x = 5;"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('assign', 'x', ('number', 5)), result) #Corrected

    def test_expression_group(self):
        code = "(x + y);"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('binop', '+', ('id', 'x'), ('id', 'y')), result) #Corrected

    def test_expression_call(self):
        code = "foo(x, 5);"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('call', 'foo', [('id', 'x'), ('number', 5)]), result) #Corrected

    def test_expression_call_empty(self):
        code = "foo();"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('call', 'foo', []), result) #Corrected

    def test_expression_id(self):
        code = "x;"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('id', 'x'), result) #Corrected

    def test_expression_number(self):
        code = "5;"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('number', 5), result) #Corrected

    def test_for_loop(self):
        code = "for(int i = 0; i < 10; i = i+1){}"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('for_loop', ('declare', 'int', 'i', ('number', 0)), ('binop', '<', ('id', 'i'), ('number', 10)),
                    ('assign', 'i', ('binop', '+', ('id', 'i'), ('number', 1))), ('block', [])), result) #Corrected

    def test_while_loop(self):
        code = "while(x < 10){}"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('while_loop', ('binop', '<', ('id', 'x'), ('number', 10)), ('block', [])), result) #Corrected

    def test_full_program(self):
        code = """
        int main() {
            int x = 5;
            x = x + 3;
            return x;
        }
        """
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('program', [('function', 'int', 'main', [], ('block', [('declare', 'int', 'x', ('number', 5)), (
            'assign', 'x', ('binop', '+', ('id', 'x'), ('number', 3))), ('return', ('id', 'x'))]))]), result) #Corrected

    def test_full_program_with_for(self):
        code = """
        int main() {
            int x = 5;
            x = x + 3;
            for (int i=0; i<10; i=i+1) {
                x = x * i;
            }
            return x;
        }
        """
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('program', [('function', 'int', 'main', [], ('block', [('declare', 'int', 'x', ('number', 5)), ('assign', 'x', ('binop', '+', ('id', 'x'), ('number', 3))), ('for_loop', ('declare', 'int', 'i', ('number', 0)), ('binop', '<', ('id', 'i'), ('number', 10)), ('assign', 'i', ('binop', '+', ('id', 'i'), ('number', 1))), ('block', [('assign', 'x', ('binop', '*', ('id', 'x'), ('id', 'i')))])), ('return', ('id', 'x'))]))]), result) #Corrected