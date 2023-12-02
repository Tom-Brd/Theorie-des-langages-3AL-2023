# -----------------------------------------------------------------------------
# calc.py
#
# Expressions arithmétiques sans variables
# -----------------------------------------------------------------------------
from TP2.genereTreeGraphviz2 import printTreeGraph

reserved = {
    'print': 'PRINT',
    'printString': 'PRINTSTRING',
    'toamScan': 'TOAMSCAN',
    'scan': 'SCAN'
}

tokens = [
             'NUMBER', 'MINUS',
             'PLUS', 'TIMES', 'DIVIDE',
             'LPAREN', 'RPAREN', 'AND', 'OR', 'SEMICOLON', 'NAME', 'EQUALS', 'GREATER', 'LESS',
             'INCREMENT', 'DECREMENT', 'INCREASE', 'DECREASE',
             "STRING", "SIMPLE_COMMENT", "MULTI_COMMENT"
         ] + list(reserved.values())

# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_AND = r'&'
t_OR = r'\|'
t_SEMICOLON = r';'
t_EQUALS = r'='
t_GREATER = r'>'
t_LESS = r'<'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_INCREASE = r'\+='
t_DECREASE = r'-='
t_SIMPLE_COMMENT = r'//.*'
t_MULTI_COMMENT = r'/\*(.|\n)*?\*/'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')
    return t


def t_STRING(t):
    r'\"[\w\W]*?\"'
    t.value = str(t.value)
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex

lex.lex()

names = {}

precedence = (
    ('left', 'AND', 'OR'),
    ('nonassoc', 'GREATER', 'LESS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)


def p_start(p):
    'start : bloc'
    p[0] = ('START', p[1])
    print('Arbre de dérivation = ', p[0])
    printTreeGraph(p[1])
    evalInst(p[1])


def p_bloc(p):
    '''bloc : statement SEMICOLON bloc
            | statement SEMICOLON
            | SIMPLE_COMMENT bloc
            | SIMPLE_COMMENT
            | MULTI_COMMENT bloc
            | MULTI_COMMENT'''
    if len(p) == 4:
        p[0] = ('bloc', p[3], p[1])
    else:
        p[0] = ('bloc', p[1], 'empty')


def p_statement_expr(p):
    '''statement : PRINT LPAREN expression RPAREN
        | PRINTSTRING LPAREN STRING RPAREN'''
    p[0] = ('print', p[3])


def p_statement_toamScan(p):
    '''statement : TOAMSCAN LPAREN NAME RPAREN'''
    p[0] = ('scan', p[3])


def p_statement_scan(p):
    '''statement : NAME EQUALS SCAN LPAREN RPAREN'''
    p[0] = ('scan', p[1])


def p_statement_assign(p):
    'statement : NAME EQUALS expression'
    p[0] = ('assign', p[1], p[3])


def p_expression_binop_operations(p):
    '''expression : expression MINUS expression
				| expression DIVIDE expression
				| expression PLUS expression
				| expression TIMES expression'''
    p[0] = (p[2], p[1], p[3])


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]


def p_expression_name(p):
    'expression : NAME'
    # p[0] = names[p[1]]
    p[0] = p[1]


def p_expression_string(p):
    'expression : STRING'
    p[0] = p[2]


def p_expression_binop_bool(p):
    '''expression : expression AND expression
                | expression OR expression
                | expression GREATER expression
                | expression LESS expression'''
    p[0] = (p[2], p[1], p[3])


def p_expression_incr_decr(p):
    '''expression : NAME INCREMENT
                | NAME DECREMENT
                | NAME INCREASE expression
                | NAME DECREASE expression'''
    match p[2]:
        case '++':
            p[0] = ('assign', p[1], ('+', p[1], 1))
        case '--':
            p[0] = ('assign', p[1], ('-', p[1], 1))
        case '+=':
            p[0] = ('assign', p[1], ('+', p[1], p[3]))
        case '-=':
            p[0] = ('assign', p[1], ('-', p[1], p[3]))


def p_error(p):
    print("Syntax error at '%s'" % p.value)


def evalExpr(t):
    print('eval de ', t)
    if type(t) is int: return t
    if type(t) is tuple:
        match t[0]:
            case '+':
                return eval(t[1]) + eval(t[2])
            case '*':
                return eval(t[1]) * eval(t[2])
            case '-':
                return eval(t[1]) - eval(t[2])
            case '/':
                return eval(t[1]) / eval(t[2])
            case '&':
                return eval(t[1]) & eval(t[2])
            case '|':
                return eval(t[1]) | eval(t[2])
            case '>':
                return eval(t[1]) > eval(t[2])
            case '<':
                return eval(t[1]) < eval(t[2])
            case _:
                return
    return 'UNK'


def evalInst(t):
    if type(t) is tuple:
        match t[0]:
            case 'assign':
                names[t[1]] = evalExpr(t[2])
            case 'print':
                print(evalExpr(t[1]))
            case 'printString':
                print(t[1])
            case 'scan':
                names[t[1]] = input()
            case 'bloc':
                evalInst(t[1])
                evalInst(t[2])
            case 'start':
                evalInst(t[1])

import ply.yacc as yacc

yacc.yacc()

s = open("test.txt", "r").read()
yacc.parse(s)
