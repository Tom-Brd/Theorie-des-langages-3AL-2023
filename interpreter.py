# -----------------------------------------------------------------------------
# calc.py
#
# Expressions arithmétiques sans variables
# -----------------------------------------------------------------------------
from genereTreeGraphviz2 import printTreeGraph

reserved = {
    'print': 'PRINT',
    'toamScan': 'TOAMSCAN',
    'scan': 'SCAN',
    'if': 'IF',
    'else if': 'ELSEIF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'string': 'STRING',
    'bool': 'BOOL',
    'true': 'TRUE',
    'false': 'FALSE'
}

tokens = [
             'NUMBER', 'MINUS',
             'PLUS', 'TIMES', 'DIVIDE',
             'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
             'AND', 'OR', 'SEMICOLON', 'NAME', 'ASSIGN', 'GREATER', 'LESS', 'EQUALS', 'NOTEQUALS',
             'INCREMENT', 'DECREMENT', 'INCREASE', 'DECREASE',
             'TRUE', 'FALSE',
             "CHARCHAIN", "SIMPLE_COMMENT", "MULTI_COMMENT",
         ] + list(reserved.values())

# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_AND = r'&'
t_OR = r'\|'
t_SEMICOLON = r';'
t_ASSIGN = r'='
t_GREATER = r'>'
t_LESS = r'<'
t_EQUALS = r'=='
t_NOTEQUALS = r'!='
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


def t_CHARCHAIN(t):
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

def toamPrint(string):
    print("TOAM PRINT : ", string)
def debug(string):
    if DEBUG:
        print("TOAM DEBUG : ", string)

def error(string):
    print("TOAM ERROR : ", string)

def p_start(p):
    'start : bloc'
    p[0] = ('START', p[1])
    print('Arbre de dérivation = ', p[0])
    printTreeGraph(p[1])
    evalSyntax(p[1])
    evalInst(p[1])


def p_bloc(p):
    '''bloc : bloc statement SEMICOLON
            | statement SEMICOLON
            | bloc SIMPLE_COMMENT
            | SIMPLE_COMMENT
            | bloc MULTI_COMMENT
            | MULTI_COMMENT'''
    if len(p) == 4:
        p[0] = ('bloc', p[1], p[2])
    else:
        if p[1] == '//' or p[1] == '/*':
            p[0] = p[0]
        else:
            p[0] = ('bloc', p[1], 'empty')


def p_statement_expr(p):
    '''statement : PRINT LPAREN expression RPAREN
        | PRINT LPAREN CHARCHAIN RPAREN'''
    p[0] = ('print', p[3])


def p_statement_if(p):
    '''statement : IF LPAREN expression RPAREN LBRACKET bloc RBRACKET
        | IF LPAREN expression RPAREN LBRACKET bloc RBRACKET ELSE LBRACKET bloc RBRACKET'''
    if len(p) == 8:
        p[0] = ('if', p[3], p[6])
    else:
        p[0] = ('if', p[3], p[6], p[10])


def p_statement_while(p):
    '''statement : WHILE LPAREN expression RPAREN LBRACKET bloc RBRACKET'''
    p[0] = ('while', p[3], p[6])


def p_statement_for(p):
    '''statement : FOR LPAREN statement SEMICOLON expression SEMICOLON statement RPAREN LBRACKET bloc RBRACKET'''
    print(p[3], p[5], p[7], p[10])
    p[0] = ('for', p[3], p[5], p[7], p[10])


def p_statement_toamScan(p):
    '''statement : TOAMSCAN LPAREN NAME RPAREN'''
    p[0] = ('scan', p[3])


def p_statement_scan(p):
    '''statement : NAME ASSIGN SCAN LPAREN RPAREN'''
    p[0] = ('scan', p[1])


def p_statement_assign(p):
    '''statement : TYPE NAME ASSIGN expression
        | NAME ASSIGN expression'''
    if len(p) == 5:  # type + assign
        p[0] = ('declare', p[1], p[2], p[4])  # type ; name ; value
    else:  # re assign
        p[0] = ('assign', p[1], p[3])  # name ; value


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

def p_expression_boolean(p):
    'expression : BOOLEAN'
    p[0] = bool(p[1])

def p_expression_name(p):
    'expression : NAME'
    # p[0] = names[p[1]]
    p[0] = p[1]


def p_type_definition(p):
    '''TYPE : INT
            | FLOAT
            | CHAR
            | STRING
            | BOOL'''
    p[0] = p[1]

def p_boolean_definition(p):
    '''BOOLEAN : TRUE
                | FALSE'''
    p[0] = p[1]

def p_expression_charchain(p):
    'expression : CHARCHAIN'
    p[0] = p[2]


def p_expression_binop_bool(p):
    '''expression : expression AND expression
                | expression OR expression
                | expression GREATER expression
                | expression LESS expression
                | expression EQUALS expression
                | expression NOTEQUALS expression'''
    p[0] = (p[2], p[1], p[3])


def p_expression_incr_decr(p):
    '''statement : NAME INCREMENT
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
    print(p)
    print("Syntax error at '%s'" % p.value)


def evalExpr(t):
    # print('eval de ', t)
    if type(t) is str: return variables[t]
    if type(t) is int: return t
    if type(t) is tuple:
        match t[0]:
            case '+':
                return evalExpr(t[1]) + evalExpr(t[2])
            case '*':
                return evalExpr(t[1]) * evalExpr(t[2])
            case '-':
                return evalExpr(t[1]) - evalExpr(t[2])
            case '/':
                if t[2] == 0:
                    exit("TOAM ERROR : Division par 0 impossible")
                return evalExpr(t[1]) / evalExpr(t[2])
            case '&':
                return evalExpr(t[1]) & evalExpr(t[2])
            case '|':
                return evalExpr(t[1]) | evalExpr(t[2])
            case '>':
                return evalExpr(t[1]) > evalExpr(t[2])
            case '<':
                return evalExpr(t[1]) < evalExpr(t[2])
            case '==':
                return evalExpr(t[1]) == evalExpr(t[2])
            case '!=':
                return evalExpr(t[1]) != evalExpr(t[2])
            case _:
                return
    return 'UNK'


def getType(expectedType):
    match expectedType:
        case 'int':
            return int
        case 'float':
            return float
        case 'char':
            return str
        case 'string':
            return str
        case 'bool':
            return bool


def isTypeCorrect(expectedType, value):
    return type(value) is getType(expectedType)


def evalExprSyntax(t, typeExpected, tempVariables):
    debug(f"t = {t}")
    debug(f"typeExpected = {typeExpected}")
    if type(t) is str:
        debug("t is a string")

        if t in tempVariables:
            debug("t is a variable")
            return getType(tempVariables[t]) is typeExpected
        else:
            exit(f"TOAM ERROR : La variable '{t}' n'est pas déclarée")
    if type(t) is typeExpected:
        return True
    if type(t) is tuple:
        debug(f"t is a tuple : {t}")
        if t[0] == '/' and t[2] == 0:
            exit("TOAM ERROR : Division par 0 impossible")
        return evalExprSyntax(t[1], typeExpected, tempVariables) and evalExprSyntax(t[2], typeExpected, tempVariables)
    return False


knownOperators = ['+', '-', '*', '/', '&&', '||', '>', '<', '==', '!=', '++', '--', '+=', '-=']


def evalSyntaxCondition(condition, syntaxVariables):
    debug("On est passé dans evalSyntaxCondition")
    debug(f"Condition = {condition}")
    if type(condition) is tuple:
        for sub in condition:
            debug(f"sub = {sub}")
            if type(sub) is str:
                debug("sub is str")
                if sub in knownOperators:
                    debug("sub is knownOperator")
                    continue
                elif sub not in syntaxVariables:
                    print(syntaxVariables)
                    exit(f"TOAM ERROR : Variable '{sub}' non déclarée dans la condition")
            else:
                debug("sub is not str")
                return evalSyntaxCondition(sub, syntaxVariables)
    return True

def evalSyntaxPrint(t, tempVariables):
    # t = 1
    # print("test");
    # print(1 + y);
    # ('+', 1, 'y')
    if type(t) is str:
        if t not in knownOperators:
            if t not in tempVariables:
                exit(f"TOAM ERROR : Variable '{t}' non déclarée ")
    elif type(t) is tuple:
        for sub in t:
                evalSyntaxPrint(sub, tempVariables)

def evalSyntax(t):
    if type(t) is tuple:
        match t[0]:
            # t[1] = type
            # t[2] = name
            # t[3] = value
            case 'declare':
                if t[2] in tempVariables:
                    exit(f"TOAM ERROR : Variable '{t[2]}' déjà déclarée")
                else:
                    if evalExprSyntax(t[3], getType(t[1]), tempVariables):
                        tempVariables[t[2]] = t[1]
                        debug(f"tempVariables = {tempVariables}")
                    else:
                        exit(f"TOAM ERROR : Type incorrect dans la déclaration : '{t[1]}'")
            # t[1] = name
            # t[2] = value
            case 'print':
                if type(t[1]) is str:
                    if t[1][0] != '"':
                        if t[1] not in tempVariables:
                            exit(f"TOAM ERROR : Variable '{t[1]}' non déclarée ")
                else:
                    evalSyntaxPrint(t[1], tempVariables)
            case 'scan':
                # scan or toamScan
                if t[1] in tempVariables:
                    evalExprSyntax(t[2], getType(tempVariables[t[1]]), tempVariables)
            case 'assign':
                if t[1] in tempVariables:
                    debug(f"evalExprSyntax : t[2] = {t[2]}")
                    debug(f"evalExprSyntax : getType(tempVariables[t[1]]) = {getType(tempVariables[t[1]])}")
                    debug(f"evalExprSyntax : tempVariables = {tempVariables}")
                    if not evalExprSyntax(t[2], getType(tempVariables[t[1]]), tempVariables):
                        exit(f"TOAM ERROR : Type incorrect dans l'affectation : {tempVariables[t[1]]}")
                else:
                    exit(f"TOAM ERROR : Variable '{t[1]}' non déclarée")
            case 'while':
                if evalExprSyntax(evalSyntaxCondition(t[1], tempVariables), bool, tempVariables):
                    evalSyntax(t[2])
            case 'bloc':
                evalSyntax(t[1])
                evalSyntax(t[2])
            case 'start':
                evalSyntax(t[1])


def evalInst(t):
    if type(t) is tuple:
        match t[0]:
            case 'declare':
                variables[t[2]] = evalExpr(t[3])
            case 'assign':
                variables[t[1]] = evalExpr(t[2])
            case 'print':
                if type(t[1]) is str:
                    if t[1] in variables:
                        toamPrint(variables[t[1]])
                    else:
                        toamPrint(t[1])
                else:
                    toamPrint(evalExpr(t[1]))
            case 'scan':
                variables[t[1]] = input()
            case 'if':
                if evalExpr(t[1]):
                    evalInst(t[2])
                else:
                    if len(t) == 4:
                        evalInst(t[3])
            case 'while':
                while evalExpr(t[1]):
                    evalInst(t[2])
            case 'for':
                evalInst(t[1])
                while evalExpr(t[2]):
                    evalInst(t[4])
                    evalInst(t[3])
            case 'bloc':
                evalInst(t[1])
                evalInst(t[2])
            case 'start':
                evalInst(t[1])


import ply.yacc as yacc


variables = {}
tempVariables = {}

precedence = (
    ('left', 'AND', 'OR'),
    ('nonassoc', 'GREATER', 'LESS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

DEBUG = False

yacc.yacc()

s = open("prog.toam", "r").read()
yacc.parse(s)