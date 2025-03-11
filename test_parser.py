from unittest import TestCase
import unittest
from lexer import lexer, tokens
from parser import parser

class ParserTest(unittest.TestCase):
    def test_empty_program(self):
        code = ""
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('program', None), result)

    def test_function_no_params(self):
        code = "int main() {}"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('program', [('function', 'int', 'main', [], ('block', []))]), result)

    def test_function_with_no_params(self):
        code = "void foo(){}"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('program', [('function', 'void', 'foo', [], ('block', []))]), result)

    def test_function_with_params(self):
        code = "int add(int a, int b) {}"
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(
            ('program', [('function', 'int', 'add', [('param', 'int', 'a'), ('param', 'int', 'b')], ('block', []))]), result)

    def test_block_in_function(self):
        code = """
        int main(){
             { int x; }
        }
        """
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('program', [('function', 'int', 'main', [], ('block', [('block', [('declare', 'int', 'x', None)])]))]), result)

    def test_full_program(self):
        code = """
        int main() {
            int x = 5;
            x = x + 3;
            return x;
        }
        """
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('program', [('function', 'int', 'main', [], ('block', [('declare', 'int', 'x', ('number', 5)), ('assign', 'x', ('binop', '+', ('id', 'x'),('number', 3))),('return', ('id', 'x'))]))]), result)

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

    def test_full_program_with_while(self):
        code = """
        int main() {
            int x = 5;
            x = x + 3;
            while (x < 10) {
                x = x * 2;
            }
            return x;
        }
        """
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('program', [('function', 'int', 'main', [], ('block', [('declare', 'int', 'x', ('number', 5)), ('assign', 'x', ('binop', '+', ('id', 'x'),('number', 3))), ('while_loop', ('binop', '<', ('id', 'x'), ('number', 10)), ('block', [('assign', 'x', ('binop', '*', ('id', 'x'), ('number', 2)))])) ,('return', ('id', 'x'))]))]), result)

    def test_complex_expression(self):
        code = """
       int main() {
           int x = (5 + 2) * 3;
           return x;
       }
       """
        result = parser.parse(code, lexer=lexer)
        self.assertEqual(('program', [('function', 'int', 'main', [], ('block', [('declare', 'int', 'x', ('binop', '*', ('binop', '+', ('number', 5), ('number', 2)), ('number', 3))), ('return', ('id', 'x'))]))]), result)