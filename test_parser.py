from unittest import TestCase
import unittest
from lexer import lexer, tokens
from parser import parser
from semantic import semantic_analyzer
from syntax_tree import *

class ParserTest(unittest.TestCase):
    code_snippets = [
        """int add(int a, int b) { return a + b; }""",
        """int main() { int x; x = 10; return x; }""",
        """float pi = 3.14f;""",
        """void check(int num) { if (num > 0) { return; } }""",
        """int sum() { int total = 0; for (int i = 0; i < 5; i = i + 1) { total = total + i; } return total; }""",
        """int decrement(int n) { while (n > 0) { n = n - 1; } return n; }""",
        """int process() { int a = 5; int b = 10; return a * b; }""",
        """bool compare(int x, float y) { return x > y; }""",
        """int main() { int count = 0; for (int j = 0; j < 3; j = j + 1) { if (j > 1) { count = count + 1; } } return count; }""",
        """int main() { y = 5; return y; }""", # Semantic error: y not declared
        """int main() { int z = true; return z; }""", # Semantic error: type mismatch
        """double average(int a, float b) { return (a + b) / 2.0; }""",
        """char initial = 'A';""",
        """bool flag = false;""",
        """int main() { int a = 10; int b = a + 5; return b; }""",
        """float area(float radius) { return 3.14f * radius * radius; }""",
        """void print_value(int val) { return; }""",
        """int factorial(int n) { if (n <= 1) { return 1; } else { return n * factorial(n - 1); } }""", # Assuming recursion is handled (parser level)
        """int main() { int i = 0; while (i < 10) { i = i + 1; } return i; }""",
        """bool is_even(int num) { if (num % 2 == 0) { return true; } else { return false; } }""",
        """int main() { int x = 5; x = 7; return x; }""", # Testing update
        """int main() { int a; a = 10; if (a > 5) { int b = 20; return b; } return 0; }""", # Block scope
        """int main() { for (int i = 0; i < 2; i = i + 1) { int local = i * 2; } return 0; }""", # Block scope of for loop
        """int main() { int x = 10; int y = x / 2; return y; }""",
        """int main() { int a = 5; int b = a * (3 + 2); return b; }""",
        """bool check_range(int val) { return val > 0 && val < 10; }""",
        """int main() { int x = 5; bool result = x == 5; return result; }""",
        """int main() { int a = 10; int b = 5; bool res = a != b; return res; }""",
        """int main() { float f = 2.5f; double d = 3.7; return d; }""",
        """int main() { double val = 10; float res = val; return 0; }""", # Semantic error: double to float
        """int main() { char c = 65; return c; }""", # Implicit conversion int to char (if allowed by your rules)
        """int main() { bool b = 1; return b; }""", # Implicit conversion int to bool (if allowed)
        """int main() { int x = 10; if (x) { return 1; } else { return 0; } }""", # Using int as boolean condition (if allowed)
        """int main() { bool flag = true; if (flag) { return 5; } return 0; }""",
        """void do_nothing() { }""",
        """int main() { int a = 5; a = a + 1; return a; }""",
        """int main() { int x = -5; return x; }""",
        """int main() { return 1 + 2 * 3 - 4 / 2; }""", # Complex arithmetic expression
        """bool logical_op(bool a, bool b) { return a && !b; }""", # Assuming ! is not implemented, using AND and comparison
        """int main() { int a = 5; return (a > 3) && (a < 10); }""",
        """int main() { int x = 0; while (x < 3) { x = x + 1; int inner = x * 2; } return x; }""", # Block scope in while
        """int main() { for (int i = 0; i < 2; i = i + 1) { if (i > 0) { return 1; } } return 0; }""", # Nested control flow
        """int identity(int k) { return k; }""",
        """int main() { int val = identity(10); return val; }""", # Assuming function calls will be implemented later (parser level)
        """int main() { return; }""", # Error: return in main should return int
        """void main() { return 0; }""", # Error: main should return int
        """int func() { int a = 10; return; }""", # Error: non-void function should return a value
        """int main(int argc) { return 0; }""", # Error: main should have no parameters
        """int main() { int x = 5; int x = 10; return x; }""", # Semantic error: redeclaration
        """int main() { return unknown_var; }""", # Semantic error: unknown variable
        """int main() { int a = 5; return a + true; }""", # Semantic error: type mismatch in addition
        """void setValue(int val) { x = val; }""", # Semantic error: x not declared in scope
    ]

    def test_add_function(self):
        code = self.code_snippets[0]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_main_function_simple(self):
        code = self.code_snippets[1]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_float_declaration(self):
        code = self.code_snippets[2]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_void_function_if(self):
        code = self.code_snippets[3]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_sum_function_for_loop(self):
        code = self.code_snippets[4]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_decrement_function_while_loop(self):
        code = self.code_snippets[5]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_process_function_multiple_declarations(self):
        code = self.code_snippets[6]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_compare_function_mixed_types(self):
        code = self.code_snippets[7]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_main_function_complex_control_flow(self):
        code = self.code_snippets[8]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_semantic_error_undeclared_variable(self):
        code = self.code_snippets[9]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 1)
        self.assertIn("Semantic Error: 'y' not declared before use.", errors[0])

    def test_semantic_error_type_mismatch(self):
        code = self.code_snippets[10]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 1)
        self.assertIn("Semantic Error: Type mismatch in declaration of 'z'. Expected 'int', got 'bool'.", errors[0])

    def test_average_function_mixed_types(self):
        code = self.code_snippets[11]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_char_declaration(self):
        code = self.code_snippets[12]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_bool_declaration(self):
        code = self.code_snippets[13]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_main_function_arithmetic(self):
        code = self.code_snippets[14]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_area_function_float(self):
        code = self.code_snippets[15]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_void_function_return(self):
        code = self.code_snippets[16]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_factorial_function_recursive(self):
        code = self.code_snippets[17]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_main_function_while(self):
        code = self.code_snippets[18]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_is_even_function_bool_return(self):
        code = self.code_snippets[19]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_main_function_assignment_update(self):
        code = self.code_snippets[20]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_main_function_if_block_scope(self):
        code = self.code_snippets[21]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_main_function_for_block_scope(self):
        code = self.code_snippets[22]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_main_function_division(self):
        code = self.code_snippets[23]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_main_function_complex_arithmetic(self):
        code = self.code_snippets[24]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_check_range_function_logical_and(self):
        code = self.code_snippets[25]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_main_function_equality_comparison(self):
        code = self.code_snippets[26]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_main_function_inequality_comparison(self):
        code = self.code_snippets[27]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_main_function_double_declaration(self):
        code = self.code_snippets[28]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_semantic_error_double_to_float_assignment(self):
        code = self.code_snippets[29]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 1)
        self.assertIn("Semantic Error: Type mismatch in declaration of 'res'. Expected 'float', got 'double'.", errors[0])

    def test_main_function_implicit_int_to_char(self):
        code = self.code_snippets[30]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_semantic_error_implicit_int_to_bool(self):
        code = self.code_snippets[31]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 1)
        self.assertIn("Semantic Error: Type mismatch in declaration of 'b'. Expected 'bool', got 'int'.", errors[0])

    def test_semantic_error_int_as_bool_condition(self):
        code = self.code_snippets[32]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 1)
        self.assertIn("Semantic Error: If condition must be boolean, got 'int'.", errors[0])

    def test_main_function_if_true(self):
        code = self.code_snippets[33]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_void_function_no_return(self):
        code = self.code_snippets[34]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_main_function_increment(self):
        code = self.code_snippets[35]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_main_function_negative_int(self):
        code = self.code_snippets[36]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_main_function_complex_arithmetic_expr(self):
        code = self.code_snippets[37]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_logical_op_function_and_not_implemented(self):
        code = self.code_snippets[38]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0) # Assuming '!' is not a token, so it will likely parse as an error or differently

    def test_main_function_logical_and_comparison(self):
        code = self.code_snippets[39]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_main_function_while_block_scope(self):
        code = self.code_snippets[40]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_main_function_nested_if_in_for(self):
        code = self.code_snippets[41]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_identity_function(self):
        code = self.code_snippets[42]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0)

    def test_main_function_with_identity_call_parser_level(self):
        code = self.code_snippets[43]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 0) # Assuming function calls are parsed

    def test_semantic_error_return_in_main_no_value(self):
        code = self.code_snippets[44]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 1)
        self.assertIn("Semantic Error: Non-void function 'main' must return a value.", errors[0])

    def test_semantic_error_void_main_returns_int(self):
        code = self.code_snippets[45]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 1)
        self.assertIn("Semantic Error: Function 'main' must have return type 'int'.", errors[0])

    def test_semantic_error_non_void_func_no_return(self):
        code = self.code_snippets[46]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 1)
        self.assertIn("Semantic Error: Non-void function 'func' must return a value.", errors[0])

    def test_semantic_error_main_function_with_parameters(self):
        code = self.code_snippets[47]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 1)
        self.assertIn("Semantic Error: Function 'main' should not have parameters.", errors[0])

    def test_semantic_error_redeclaration(self):
        code = self.code_snippets[48]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 1)
        self.assertIn("Semantic Error: 'x' already declared.", errors[0])

    def test_semantic_error_unknown_variable(self):
        code = self.code_snippets[49]
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        print(errors)
        self.assertEqual(len(errors), 1)
        self.assertIn("Semantic Error: 'unknown_var' not declared before use.", errors[0])

    def test_semantic_error_undeclared_variable_setValue(self):
        code = "void setValue(int val) { x = val; }"
        lexer.input(code)
        ast = parser.parse(code, lexer=lexer)
        errors = semantic_analyzer(ast)
        self.assertEqual(len(errors), 1)
        self.assertIn("Semantic Error: 'x' not declared before use.", errors[0])