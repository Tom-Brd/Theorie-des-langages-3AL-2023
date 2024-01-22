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
    'void': 'VOID',
    'true': 'TRUE',
    'false': 'FALSE',
    'function': 'FUNCTION',
    'return': 'RETURN',
}

tokens = [
             'NUMBER', 'MINUS',
             'PLUS', 'TIMES', 'DIVIDE',
             'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
             'AND', 'OR', 'COMMA', 'SEMICOLON', 'NAME', 'ASSIGN', 'GREATER', 'LESS', 'EQUALS','NOTEQUALS', 'GREATEREQUALS', 'LESSEQUALS',
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
t_COMMA = r','
t_SEMICOLON = r';'
t_ASSIGN = r'='
t_GREATER = r'>'
t_LESS = r'<'
t_GREATEREQUALS = r'>='
t_LESSEQUALS = r'<='
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
    # evalSyntax(p[1])
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


def p_statement_function(p):
    '''statement : FUNCTION RETURNTYPE NAME LPAREN PARAMS RPAREN LBRACKET bloc RBRACKET'''
    p[0] = ('function', p[2], p[3], p[5], p[8])


def p_params(p):
    '''PARAMS : TYPE NAME
                | TYPE NAME COMMA PARAMS'''
    if len(p) == 3:
        p[0] = ('params', p[1], p[2])
    else:
        p[0] = ('params', p[1], p[2], p[4])


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


def p_expression_funcparams(p):
    '''FUNCPARAMS : expression
                | expression COMMA FUNCPARAMS'''

    if len(p) == 2:
        p[0] = ('funcparams', p[1])
    else:
        p[0] = ('funcparams', p[3], p[1])


def p_expression_call_function(p):
    '''expression : NAME LPAREN RPAREN
        | NAME LPAREN FUNCPARAMS RPAREN'''
    if len(p) == 4:
        p[0] = ('call_function', p[1])
    else:
        p[0] = ('call_function', p[1], p[3])


def p_statement_call_function(p):
    '''statement : NAME LPAREN RPAREN
        | NAME LPAREN FUNCPARAMS RPAREN'''
    if len(p) == 4:
        p[0] = ('call_function_void', p[1])
    else:
        p[0] = ('call_function_void', p[1], p[3])


def p_type_definition(p):
    '''TYPE : INT
            | FLOAT
            | CHAR
            | STRING
            | BOOL'''
    p[0] = p[1]


def p_return_type(p):
    '''RETURNTYPE : TYPE
            | VOID'''
    p[0] = p[1]


def p_return_statement(p):
    '''statement : RETURN expression
        | RETURN statement
        | RETURN'''
    if len(p) == 3:
        p[0] = ('return', p[2])
    else:
        p[0] = ('return', 'empty')


def p_boolean_definition(p):
    '''BOOLEAN : TRUE
                | FALSE'''
    p[0] = p[1]


def p_expression_charchain(p):
    'expression : CHARCHAIN'
    p[0] = p[1]


def p_expression_binop_bool(p):
    '''expression : expression AND expression
                | expression OR expression
                | expression GREATER expression
                | expression LESS expression
                | expression EQUALS expression
                | expression NOTEQUALS expression
                | expression GREATEREQUALS expression
                | expression LESSEQUALS expression'''
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
    if type(t) is str:
        if t[0] == '"':
            return t
        if exist_in_scope(t):
            return get_variable(t)
        else:
            return get_function(t)
    if type(t) is int:
        return t
    if type(t) is tuple:
        match t[0]:
            case 'funcparams':
                if len(t) == 2:
                    return evalExpr(t[1])
                else:
                    return evalExpr(t[2]), evalExpr(t[1])
            case 'call_function':
                return call_function(evalExpr(t[1]), evalExpr(t[2]))
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
            case '>=':
                return evalExpr(t[1]) >= evalExpr(t[2])
            case '<=':
                return evalExpr(t[1]) <= evalExpr(t[2])
            case '==':
                debug(get_variable(t[1]))
                debug("type of t[1] = " + str(type(t[1])))
                debug("type of t[2] = " + str(type(t[2])))
                debug("t[1] = " + str(get_variable(t[1])))
                debug("t[2] = " + str(t[2]))
                debug("evalExpr(t[1]) = " + str(evalExpr(t[1])))
                debug("evalExpr(t[2]) = " + str(evalExpr(t[2])))
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


def evalExprSyntax(t, typeExpected):
    debug(f"t = {t}")
    debug(f"typeExpected = {typeExpected}")
    if type(t) is typeExpected:
        return True
    if type(t) is str:
        debug("t is a string")
        if exist_in_syntax_scope(t):
            debug("t is a variable")
            return getType(get_syntax_variable(t)) is typeExpected
        else:
            exit(f"TOAM ERROR : La variable '{t}' n'est pas déclarée")
    if type(t) is tuple:
        debug(f"t is a tuple : {t}")
        if t[0] == '/' and t[2] == 0:
            exit("TOAM ERROR : Division par 0 impossible")
        return evalExprSyntax(t[1], typeExpected) and evalExprSyntax(t[2], typeExpected)
    return False


knownOperators = ['+', '-', '*', '/', '&&', '||', '>', '<', '==', '!=', '++', '--', '+=', '-=', '>=', '<=']


def evalSyntaxCondition(condition):
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
                elif not exist_in_syntax_scope(sub):
                    debug(syntax_analysis_variables_scope_stack)
                    exit(f"TOAM ERROR : Variable '{sub}' non déclarée dans la condition")
            else:
                debug("sub is not str")
                return evalSyntaxCondition(sub)
    return True


def evalSyntaxPrint(t):
    # t = 1
    # print("test");
    # print(1 + y);
    # ('+', 1, 'y')
    if type(t) is str:
        if t not in knownOperators:
            if not exist_in_syntax_scope(t):
                exit(f"TOAM ERROR : Variable '{t}' non déclarée ")
    elif type(t) is tuple:
        for sub in t:
            evalSyntaxPrint(sub)


def evalSyntax(t):
    if type(t) is tuple:
        match t[0]:
            # t[1] = type
            # t[2] = name
            # t[3] = value
            case 'declare':
                if exist_in_syntax_scope(t[2]):
                    exit(f"TOAM ERROR : Variable '{t[2]}' déjà déclarée")
                else:
                    if evalExprSyntax(t[3], getType(t[1])):
                        set_syntax_variable(t[2], t[1])
                        debug(f"scopeSyntaxVariables = {syntax_analysis_variables_scope_stack}")
                    else:
                        exit(f"TOAM ERROR : Type incorrect dans la déclaration : '{t[1]}'")
            # t[1] = name
            # t[2] = value
            case 'print':
                if type(t[1]) is str:
                    if t[1][0] != '"':
                        if not exist_in_syntax_scope(t[1]):
                            exit(f"TOAM ERROR : Variable '{t[1]}' non déclarée ")
                else:
                    evalSyntaxPrint(t[1])
            case 'scan':
                if not exist_in_syntax_scope(t[1]):
                    exit(f"TOAM ERROR : Variable '{t[1]}' non déclarée ")
            case 'assign':
                if exist_in_syntax_scope(t[1]):
                    debug(f"evalExprSyntax : t[2] = {t[2]}")
                    debug(f"evalExprSyntax : getType(tempVariables[t[1]]) = "
                          f"{getType(get_syntax_variable(t[1]))}")
                    debug(f"evalExprSyntax : scopeSyntaxVariables = {syntax_analysis_variables_scope_stack}")
                    if not evalExprSyntax(t[2], getType(get_syntax_variable(t[1]))):
                        exit(f"TOAM ERROR : Type incorrect dans l'affectation : {get_syntax_variable(t[1])}")
                else:
                    exit(f"TOAM ERROR : Variable '{t[1]}' non déclarée")
            case 'while':
                create_syntax_scope()
                if evalExprSyntax(evalSyntaxCondition(t[1]), bool):
                    create_syntax_scope()
                    evalSyntax(t[2])
                    exit_syntax_scope()
                exit_syntax_scope()
            case 'for':
                create_syntax_scope()
                evalSyntax(t[1])
                if evalExprSyntax(evalSyntaxCondition(t[2]), bool):
                    create_syntax_scope()
                    evalSyntax(t[4])
                    evalSyntax(t[3])
                    exit_syntax_scope()
                exit_syntax_scope()
            case 'if':
                create_syntax_scope()
                if evalExprSyntax(evalSyntaxCondition(t[1]), bool):
                    create_syntax_scope()
                    evalSyntax(t[2])
                    exit_syntax_scope()
                if len(t) == 4:
                    create_syntax_scope()
                    evalSyntax(t[3])
                    exit_syntax_scope()
                exit_syntax_scope()
            case 'bloc':
                evalSyntax(t[1])
                evalSyntax(t[2])
            case 'start':
                evalSyntax(t[1])


def evalInst(t):
    if type(t) is tuple:
        match t[0]:
            case 'return':
                if t[1] == "empty":
                    return "empty"
                return evalExpr(t[1])
            case 'call_function_void':
                call_function(evalExpr(t[1]), evalExpr(t[2]))
            case 'function':
                # t[0] = function
                # t[1] = return type
                # t[2] = name
                # t[3] = tuple de paramètres
                # t[4] = bloc d'instruction
                functions[t[2]] = (t[1], t[3], t[4])
            case 'declare':
                set_variable(t[2], evalExpr(t[3]))
            case 'assign':
                set_variable(t[1], evalExpr(t[2]))
            case 'print':
                if type(t[1]) is str:
                    if t[1][0] == '"':
                        chaine = t[1].strip('"')
                        toamPrint(chaine)
                    else:
                        toBePrinted = get_variable(t[1])
                        if type(toBePrinted) is str:
                            chaine = toBePrinted.strip('"')
                            toamPrint(chaine)
                        else:
                            toamPrint(get_variable(t[1]))
                else:
                    toamPrint(evalExpr(t[1]))
            case 'scan':
                typ = type(get_variable([t[1]]))
                userInput = input()
                try:
                    if typ is int:
                        set_variable(t[1], int(userInput))
                    elif typ is float:
                        set_variable(t[1], float(userInput))
                    elif typ is str:
                        set_variable(t[1], str(userInput))
                    elif typ is bool:
                        set_variable(t[1], bool(userInput))
                except ValueError:
                    exit(f"TOAM ERROR : Impossible de convertir l'entrée '{userInput}' en {typ} : (Variable {t[1]})")
            case 'if':
                create_scope()
                result = None
                debug(evalExpr(t[1]))
                if evalExpr(t[1]):
                    create_scope()
                    result = evalInst(t[2])
                    exit_scope()
                else:
                    if len(t) == 4:
                        create_scope()
                        result = evalInst(t[3])
                        exit_scope()
                exit_scope()
                if result is not None:
                    return result
            case 'while':
                create_scope()
                while evalExpr(t[1]):
                    create_scope()
                    evalInst(t[2])
                    exit_scope()
                exit_scope()
            case 'for':
                create_scope()
                evalInst(t[1])
                while evalExpr(t[2]):
                    create_scope()
                    evalInst(t[4])
                    evalInst(t[3])
                    exit_scope()
                exit_scope()
            case 'bloc':
                for stmt in t[1:]:
                    result = evalInst(stmt)
                    if result is not None or result == "empty":
                        return result
            case 'start':
                evalInst(t[1])


import ply.yacc as yacc

variables_scope_stack = [{}]
syntax_analysis_variables_scope_stack = [{}]
functions = {}


def declare_variables_function(parameters, call_params, index):
    if type(call_params) is tuple:
        set_variable(parameters[2], call_params[index])
    else:
        set_variable(parameters[2], call_params)

    if len(parameters) == 3:
        return
    return declare_variables_function(parameters[3], call_params, index + 1)


def call_function(name, call_params):
    if name in functions:

        called_function = functions[name]

        return_type = called_function[0]
        parameters = called_function[1]
        instructions = called_function[2]

        create_scope()
        declare_variables_function(parameters, call_params, 0)
        result = evalInst(instructions)
        exit_scope()
        return result
    exit(f"TOAM ERROR : La fonction '{name}' n'existe pas")


def get_function(name):
    if name in functions:
        return name
    # exit(f"TOAM ERROR : La fonction '{name}' n'existe pas")


def create_scope():
    variables_scope_stack.append({})


def exit_scope():
    variables_scope_stack.pop()


def exist_in_scope(name):
    for scope in reversed(variables_scope_stack):
        if name in scope:
            return True
    return False


def update_in_scope(name, value):
    for scope in reversed(variables_scope_stack):
        if name in scope:
            scope[name] = value
            return True
    return False


def set_variable(name, value):
    if not update_in_scope(name, value):
        variables_scope_stack[-1][name] = value


def get_variable(name):
    for scope in reversed(variables_scope_stack):
        if name in scope:
            return scope[name]
    # exit(f"Variable non définie: {name}")


def create_syntax_scope():
    syntax_analysis_variables_scope_stack.append({})


def exit_syntax_scope():
    syntax_analysis_variables_scope_stack.pop()


def exist_in_syntax_scope(name):
    for scope in reversed(syntax_analysis_variables_scope_stack):
        if name in scope:
            return True
    return False


def update_in_syntax_scope(name, value):
    for scope in reversed(syntax_analysis_variables_scope_stack):
        if name in scope:
            scope[name] = value
            return True
    return False


def set_syntax_variable(name, value):
    if not update_in_syntax_scope(name, value):
        syntax_analysis_variables_scope_stack[-1][name] = value


def get_syntax_variable(name):
    for scope in reversed(syntax_analysis_variables_scope_stack):
        if name in scope:
            return scope[name]
    exit(f"Variable non définie: {name}")


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