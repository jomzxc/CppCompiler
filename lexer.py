#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2025-03-11

@author: Jomzxc
"""

from ply import lex

# --- Lexer ---

tokens = (
    'TYPE', 'ID', 'INT_NUM', 'FLOAT_NUM', 'CHAR_LIT', 'DOUBLE_NUM', 'BOOL_LIT',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN',
    'EQ', 'NEQ', 'LT', 'GT', 'LEQ', 'GEQ',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMI', 'COMMA',
    'IF', 'ELSE', 'FOR', 'WHILE', 'RETURN'
)

keywords = {
    'int': 'TYPE',
    'float': 'TYPE',
    'double': 'TYPE',
    'char': 'TYPE',
    'bool': 'TYPE',
    'void': 'TYPE',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'return': 'RETURN',
}

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_EQ = r'=='
t_NEQ = r'!='
t_LT = r'<'
t_GT = r'>'
t_LEQ = r'<='
t_GEQ = r'>='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r';'
t_COMMA = r','

t_ignore = ' \t'

def t_BOOL_LIT(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'ID')
    return t

def t_FLOAT_NUM(t):
    r'\d*\.\d+'
    t.value = float(t.value)
    return t

def t_DOUBLE_NUM(t):
    r'\d*\.\d+[dD]'
    t.value = float(t.value[:-1])
    return t

def t_INT_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CHAR_LIT(t):
    r'\'.\''
    t.value = t.value[1:-1]
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()