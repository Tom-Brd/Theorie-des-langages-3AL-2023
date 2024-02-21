# -----------------------------------------------------------------------------
# calc.py
#
# Expressions arithmétiques sans variables
# -----------------------------------------------------------------------------
from project.toam.others.genereTreeGraphviz2 import printTreeGraph

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
    'len': 'LEN',
    'import': 'IMPORT',
}

tokens = [
             'NUMBER', 'MINUS',
             'PLUS', 'TIMES', 'DIVIDE',
             'LPAREN', 'RPAREN', 'LCURLYBRACKET', 'RCURLYBRACKET', "LBRACKET", "RBRACKET",
             'AND', 'OR', 'COMMA', 'SEMICOLON', 'NAME', 'ASSIGN', 'GREATER', 'LESS', 'EQUALS', 'NOTEQUALS',
             'GREATEREQUALS', 'LESSEQUALS',
             'INCREMENT', 'DECREMENT', 'INCREASE', 'DECREASE',
             'TRUE', 'FALSE', 'AMPERSAND',
             "CHARCHAIN", "SIMPLE_COMMENT", "MULTI_COMMENT"
         ] + list(reserved.values())

# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLYBRACKET = r'\{'
t_RCURLYBRACKET = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_AND = r'&&'
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
t_AMPERSAND = r'&'


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
    # t.value = t.value.strip('"')
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
    # printTreeGraph(p[1])
    evalSyntax(p[1])
    global runtime_stack
    runtime_stack = [{}]
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


def p_statement_import(p):
    '''statement : IMPORT CHARCHAIN'''
    p[0] = ('import', p[2])


def p_statement_function(p):
    '''statement : FUNCTION RETURNTYPE NAME LPAREN PARAMS RPAREN LCURLYBRACKET bloc RCURLYBRACKET
                | FUNCTION RETURNTYPE NAME LPAREN RPAREN LCURLYBRACKET bloc RCURLYBRACKET'''
    if len(p) == 10:
        p[0] = ('function', p[2], p[3], p[5], p[8])
    else:
        p[0] = ('function', p[2], p[3], 'empty_params', p[7])


def p_type_params(p):
    '''TYPEPARAM : ARRAYTYPE
                | TYPE'''
    p[0] = p[1]


def p_params(p):
    '''PARAMS : TYPEPARAM NAME
                | TYPEPARAM NAME COMMA PARAMS'''
    if len(p) == 3:
        p[0] = ('params', p[1], p[2])
    else:
        p[0] = ('params', p[1], p[2], p[4])


def p_statement_expr(p):
    '''statement : PRINT LPAREN expression RPAREN
        | PRINT LPAREN CHARCHAIN RPAREN'''
    p[0] = ('print', p[3])


def p_statement_add_array(p):
    '''statement : NAME LBRACKET RBRACKET ASSIGN expression
        | TIMES NAME LBRACKET RBRACKET ASSIGN expression'''
    if len(p) == 6:
        p[0] = ('add_array', p[1], p[5])
    else:
        p[0] = ('add_array_by_reference', p[2], p[6])


def p_expr_len_array(p):
    '''expression : LEN LPAREN expression RPAREN'''
    p[0] = ('len_array', p[3])


def p_statement_if(p):
    '''statement : IF LPAREN expression RPAREN LCURLYBRACKET bloc RCURLYBRACKET
        | IF LPAREN expression RPAREN LCURLYBRACKET bloc RCURLYBRACKET ELSE LCURLYBRACKET bloc RCURLYBRACKET'''
    if len(p) == 8:
        p[0] = ('if', p[3], p[6])
    else:
        p[0] = ('if', p[3], p[6], p[10])


def p_statement_while(p):
    '''statement : WHILE LPAREN expression RPAREN LCURLYBRACKET bloc RCURLYBRACKET'''
    p[0] = ('while', p[3], p[6])


def p_statement_for(p):
    '''statement : FOR LPAREN statement SEMICOLON expression SEMICOLON statement RPAREN LCURLYBRACKET bloc RCURLYBRACKET'''
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
        | TIMES NAME ASSIGN expression
        | NAME ASSIGN expression'''
    if len(p) == 5:  # type + assign
        if p[1] == '*':
            p[0] = ('assign_by_reference', p[2], p[4])
        else:
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


def p_array_declaration(p):
    '''statement : ARRAYTYPE NAME ASSIGN array_values
                   | ARRAYTYPE NAME
                   | ARRAYTYPE NAME ASSIGN FUNCCALL
                   '''
    if len(p) == 5:
        if p[4][0] == 'array_values':
            p[0] = ('declare', p[1], p[2], p[4])
        else:
            p[0] = ('declare', p[1], p[2], ('func', p[4]))
    else:
        p[0] = ('declare', p[1], p[2], 'empty_array')


def p_array_values(p):
    '''array_values : array_values COMMA array_values
                    | LBRACKET values RBRACKET
                    | LBRACKET RBRACKET'''
    if len(p) == 4:
        if p[2][0] == 'values':
            p[0] = ('array_values', p[2])
        else:
            # we are in the case array_values COMMA array_values
            p[0] = ('array_values', p[1], p[3])
    else:
        p[0] = ('array_values', 'empty_array')


def p_values(p):
    '''values : values COMMA expression
              | expression'''
    if len(p) == 4:
        p[0] = ('values', p[1], p[3])
    else:
        p[0] = ('values', p[1])


def p_set_array_value(p):
    '''statement : NAME LBRACKET expression RBRACKET ASSIGN expression
                | TIMES NAME LBRACKET expression RBRACKET ASSIGN expression
    '''
    if len(p) == 7:
        p[0] = ('set_array_value_at_index', p[1], p[3], p[6])
    else:
        p[0] = ('set_array_value_at_index_by_reference', p[2], p[4], p[7])


def p_get_array_value(p):
    '''expression : NAME LBRACKET expression RBRACKET
                | TIMES NAME LBRACKET expression RBRACKET'''
    if len(p) == 5:
        p[0] = ('get_array_value_at_index', p[1], p[3])
    else:
        p[0] = ('get_array_value_at_index_by_reference', p[2], p[4])


def p_expression_funcparams(p):
    '''FUNCPARAMS : expression
                | expression COMMA FUNCPARAMS'''
    if len(p) == 2:
        p[0] = ('funcparams', p[1])
    else:
        p[0] = ('funcparams', p[3], p[1])


def expr_to_call_function(p):
    '''expression: FUNCCALL'''
    p[0] = p[1]


def p_funccall(p):
    '''FUNCCALL : NAME LPAREN RPAREN
        | NAME LPAREN FUNCPARAMS RPAREN'''
    if len(p) == 4:
        p[0] = ('call_function', p[1])
    else:
        p[0] = ('call_function', p[1], p[3])


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
            | BOOL
            | TYPE TIMES'''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]


def p_array_type_definition(p):
    '''ARRAYTYPE : INT LBRACKET RBRACKET
            | FLOAT LBRACKET RBRACKET
            | CHAR LBRACKET RBRACKET
            | STRING LBRACKET RBRACKET
            | BOOL LBRACKET RBRACKET
            | ARRAYTYPE TIMES'''
    if len(p) == 4:
        p[0] = p[1] + p[2] + p[3]
    else:
        p[0] = p[1] + p[2]


def p_return_type(p):
    '''RETURNTYPE : TYPE
            | ARRAYTYPE
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


def p_expression_reference(p):
    '''expression : AMPERSAND NAME'''
    p[0] = ('reference', p[2])


def p_expression_dereference(p):
    '''expression : TIMES NAME'''
    p[0] = ('dereference', p[2])


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


def eval_array_values(t):
    if type(t) is tuple:
        if t[0] == 'values':
            if len(t) == 2:
                return [evalExpr(t[1])]
            else:
                return eval_array_values(t[1]) + [evalExpr(t[2])]
    return []


def evalExpr(t):
    # print('eval de ', t)
    if type(t) is str:
        if t[0] == '"':
            return t.strip('"')
        if exist_in_scope(t):
            return get_variable(t)
        else:
            return get_function(t)
    if type(t) is bool:
        return t
    if type(t) is float:
        return t
    if type(t) is int:
        return t
    if type(t) is tuple:
        match t[0]:
            case 'reference':
                if exist_in_scope(t[1]):
                    return get_address_of_variable(t[1])
                else:
                    exit(f"TOAM ERROR : La variable '{t[1]}' n'est pas déclarée")
            case 'dereference':
                if exist_in_scope(t[1]):
                    return get_variable_by_address(get_variable(t[1]))
                else:
                    exit(f"TOAM ERROR : La variable '{t[1]}' n'est pas déclarée")
            case 'len_array':
                if t[1][0] == 'dereference':
                    array = get_variable_by_address(get_variable(t[1][1]))
                    if type(array) is not list:
                        exit(f"TOAM ERROR : La variable '{array}' n'est pas un tableau")
                    else:
                        return len(array)
                if exist_in_scope(t[1]):
                    if type(get_variable(t[1])) is not list:
                        exit(f"TOAM ERROR : La variable '{t[1]}' n'est pas un tableau")
                    else:
                        return len(get_variable(t[1]))
            case 'get_array_value_at_index_by_reference':
                array = get_variable_by_address(evalExpr(t[1]))
                index = evalExpr(t[2])
                if type(array) is not list:
                    exit(f"TOAM ERROR : La variable '{t[1]}' n'est pas un tableau")
                if type(index) is not int:
                    exit(f"TOAM ERROR : L'index d'accès doit être un entier")
                if index >= len(array):
                    exit(f"TOAM ERROR : L'index d'accès doit être inférieur à la taille du tableau")
                return array[index]
            case 'get_array_value_at_index':
                # p[0] = ('get_array_value_at_index', p[1], p[3])
                array = get_variable(t[1])
                index = evalExpr(t[2])
                if type(array) is not list:
                    exit(f"TOAM ERROR : La variable '{t[1]}' n'est pas un tableau")
                if type(index) is not int:
                    exit(f"TOAM ERROR : L'index d'accès doit être un entier")
                if index >= len(array):
                    exit(f"TOAM ERROR : L'index d'accès doit être inférieur à la taille du tableau")
                return array[index]
            case 'funcparams':
                if len(t) == 2:
                    return evalExpr(t[1])
                else:
                    return evalExpr(t[2]), evalExpr(t[1])
            case 'call_function':
                if len(t) == 3:
                    return call_function(evalExpr(t[1]), evalExpr(t[2]))
                else:
                    return call_function(evalExpr(t[1]), None)
            case '+':
                first = evalExpr(t[1])
                second = evalExpr(t[2])
                if type(first) is str and type(second) is not str:
                    return first + str(second)
                if type(second) is str and type(first) is not str:
                    return second + str(first)
                return first + second
            case '*':
                return evalExpr(t[1]) * evalExpr(t[2])
            case '-':
                return evalExpr(t[1]) - evalExpr(t[2])
            case '/':
                if t[2] == 0:
                    exit("TOAM ERROR : Division par 0 impossible")
                return evalExpr(t[1]) / evalExpr(t[2])
            case '&&':
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
        if exist_in_scope(t):
            debug("t is a variable")
            return getType(get_variable(t)) is typeExpected
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
                elif not exist_in_scope(sub):
                    debug(runtime_stack)
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
            if not exist_in_scope(t):
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
                if exist_in_scope(t[2]):
                    exit(f"TOAM ERROR : Variable '{t[2]}' déjà déclarée")
                else:
                    if evalExprSyntax(t[3], getType(t[1])):
                        define_variable(t[2], t[1])
                        debug(f"scopeSyntaxVariables = {runtime_stack}")
                    else:
                        exit(f"TOAM ERROR : Type incorrect dans la déclaration : '{t[1]}'")
            # t[1] = name
            # t[2] = value
            case 'print':
                if type(t[1]) is str:
                    if t[1][0] != '"':
                        if not exist_in_scope(t[1]):
                            exit(f"TOAM ERROR : Variable '{t[1]}' non déclarée ")
                else:
                    evalSyntaxPrint(t[1])
            case 'scan':
                if not exist_in_scope(t[1]):
                    exit(f"TOAM ERROR : Variable '{t[1]}' non déclarée ")
            case 'assign':
                if exist_in_scope(t[1]):
                    debug(f"evalExprSyntax : t[2] = {t[2]}")
                    debug(f"evalExprSyntax : getType(tempVariables[t[1]]) = "
                          f"{getType(get_variable(t[1]))}")
                    debug(f"evalExprSyntax : scopeSyntaxVariables = {runtime_stack}")
                    if not evalExprSyntax(t[2], getType(get_variable(t[1]))):
                        exit(f"TOAM ERROR : Type incorrect dans l'affectation : {get_variable(t[1])}")
                else:
                    exit(f"TOAM ERROR : Variable '{t[1]}' non déclarée")
            case 'while':
                create_scope()
                if evalExprSyntax(evalSyntaxCondition(t[1]), bool):
                    create_scope()
                    evalSyntax(t[2])
                    exit_scope()
                exit_scope()
            case 'for':
                create_scope()
                evalSyntax(t[1])
                if evalExprSyntax(evalSyntaxCondition(t[2]), bool):
                    create_scope()
                    evalSyntax(t[4])
                    evalSyntax(t[3])
                    exit_scope()
                exit_scope()
            case 'if':
                create_scope()
                if evalExprSyntax(evalSyntaxCondition(t[1]), bool):
                    create_scope()
                    evalSyntax(t[2])
                    exit_scope()
                if len(t) == 4:
                    create_scope()
                    evalSyntax(t[3])
                    exit_scope()
                exit_scope()
            case 'bloc':
                evalSyntax(t[1])
                evalSyntax(t[2])
            case 'start':
                evalSyntax(t[1])


def evalInst(t):
    if type(t) is tuple:
        match t[0]:
            case 'import':
                evalInst(toamImport(t[1]))
            case 'return':
                if t[1] == "empty":
                    return "empty"
                return evalExpr(t[1])
            case 'call_function_void':
                if len(t) == 3:
                    return call_function(evalExpr(t[1]), evalExpr(t[2]))
                else:
                    return call_function(evalExpr(t[1]), None)
            case 'function':
                # t[0] = function
                # t[1] = return type
                # t[2] = name
                # t[3] = tuple de paramètres
                # t[4] = bloc d'instruction
                functions[t[2]] = (t[1], t[3], t[4])
            case 'add_array_by_reference':
                if exist_in_scope(t[1]):
                    array = get_variable_by_address(get_variable(t[1]))
                    if type(array) is not list:
                        exit(f"TOAM ERROR : La variable '{t[1]}' n'est pas un tableau")
                    else:
                        array.append(evalExpr(t[2]))
                        # set_variable(t[1], array)
            case 'add_array':
                if exist_in_scope(t[1]):
                    if type(get_variable(t[1])) is not list:
                        exit(f"TOAM ERROR : La variable '{t[1]}' n'est pas un tableau")
                    else:
                        array = get_variable(t[1])
                        array.append(evalExpr(t[2]))
                        # set_variable(t[1], array)
            case 'set_array_value_at_index_by_reference':
                array = get_variable_by_address(evalExpr(t[1]))
                index = evalExpr(t[2])
                value = evalExpr(t[3])
                if type(array) is not list:
                    exit(f"TOAM ERROR : La variable '{t[1]}' n'est pas un tableau")
                if type(index) is not int:
                    exit(f"TOAM ERROR : L'index d'accès doit être un entier")
                if index >= len(array):
                    exit(f"TOAM ERROR : L'index d'accès doit être inférieur à la taille du tableau")
                array[index] = value
            case 'set_array_value_at_index':
                # p[0] = ('set_array_value_at_index', p[1], p[3], p[6])
                array = get_variable(t[1])
                index = evalExpr(t[2])
                value = evalExpr(t[3])
                if type(array) is not list:
                    exit(f"TOAM ERROR : La variable '{t[1]}' n'est pas un tableau")
                if type(index) is not int:
                    exit(f"TOAM ERROR : L'index d'accès doit être un entier")
                if index >= len(array):
                    exit(f"TOAM ERROR : L'index d'accès doit être inférieur à la taille du tableau")
                array[index] = value
                set_variable(t[1], array)
            case 'declare':
                if type(t[3]) is tuple and t[3][0] == "array_values":
                    define_variable(t[2], eval_array_values(t[3][1]))
                elif type(t[3]) is tuple and t[3][0] == 'func':
                    define_variable(t[2], evalExpr(t[3][1]))
                else:
                    define_variable(t[2], evalExpr(t[3]))
            case 'assign':
                set_variable(t[1], evalExpr(t[2]))
            case 'assign_by_reference':
                set_variable_by_address(evalExpr(t[1]), evalExpr(t[2]))
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
                    result = evalExpr(t[1])
                    if type(result) is str:
                        result = result.strip('"')
                    toamPrint(result)
            case 'scan':
                typ = type(get_variable(t[1]))
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
                precedent_scope_is_global = isInGlobalScope()
                if precedent_scope_is_global:
                    debug("-> LEAVING GLOBAL SCOPE")
                    setInGlobalScope(False)
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
                if precedent_scope_is_global:
                    debug("-> RETURNING TO GLOBAL SCOPE\n")
                    setInGlobalScope(True)
                if result is not None:
                    return result
            case 'while':
                precedent_scope_is_global = isInGlobalScope()
                if precedent_scope_is_global:
                    debug("-> LEAVING GLOBAL SCOPE\n")
                    setInGlobalScope(False)
                create_scope()
                while evalExpr(t[1]):
                    create_scope()
                    evalInst(t[2])
                    exit_scope()
                exit_scope()
                if precedent_scope_is_global:
                    debug("-> RETURNING TO GLOBAL SCOPE\n")
                    setInGlobalScope(True)
            case 'for':
                precedent_scope_is_global = isInGlobalScope()
                if precedent_scope_is_global:
                    debug("-> LEAVING GLOBAL SCOPE\n")
                    setInGlobalScope(False)
                create_scope()
                evalInst(t[1])
                while evalExpr(t[2]):
                    create_scope()
                    evalInst(t[4])
                    evalInst(t[3])
                    exit_scope()
                exit_scope()
                if precedent_scope_is_global:
                    debug("-> RETURNING TO GLOBAL SCOPE\n")
                    setInGlobalScope(True)
            case 'bloc':
                for stmt in t[1:]:
                    result = evalInst(stmt)
                    if result is not None or result == "empty":
                        return result
            case 'start':
                evalInst(t[1])


import ply.yacc as yacc

functions = {}

global_scope = {}
runtime_stack = [{}]

functions_stack = []

is_global_scope = True
is_in_function = False


class Value:
    def __init__(self, value):
        self.value = value


def createFunctionStack():
    functions_stack.append([{}])


def exitFunctionStack():
    functions_stack.pop()


def setInGlobalScope(boolean):
    global is_global_scope
    is_global_scope = boolean


def isInGlobalScope():
    global is_global_scope
    return is_global_scope


# ('funcparams', ('funcparams', ('funcparams', 4), ('reference', 'tab')), 6)
# TODO : Gérer + de 3 paramètres et les références
def declare_variables_function(parameters, call_params):
    if type(call_params) is tuple:
        define_variable(parameters[2], call_params[0])
    else:
        define_variable(parameters[2], call_params)

    if len(parameters) == 3:
        return
    return declare_variables_function(parameters[3], call_params[1])


def call_function(name, call_params):
    if name in functions:

        called_function = functions[name]

        return_type = called_function[0]
        parameters = called_function[1]
        instructions = called_function[2]

        precedent_scope_is_global = isInGlobalScope()
        if precedent_scope_is_global:
            debug("-> LEAVING GLOBAL SCOPE")
            setInGlobalScope(False)
        """
        ON ENTRE DANS UNE FONCTION:
            - Est ce que la fonction est appellée depuis une fonction ?
                Oui : 
                    - On ne fait rien
                Non : 
                    - On set isInFunction à True au début
                    - On pense à mettre isInFunction à False à la fin
        """
        precedent_scope_is_function = isInFunction()
        if not precedent_scope_is_function:
            debug("-> ENTERING FUNCTIONS SCOPE LIST")
            setIsInFunction(True)
        createFunctionStack()
        create_scope()
        if type(parameters) is tuple:
            declare_variables_function(parameters, call_params)
        result = evalInst(instructions)
        exit_scope()
        exitFunctionStack()
        if not precedent_scope_is_function:
            debug("-> LEAVING FUNCTIONS SCOPE LIST")
            setIsInFunction(False)
        if precedent_scope_is_global:
            debug("-> RETURNING TO GLOBAL SCOPE")
            setInGlobalScope(True)
        return result
    exit(f"TOAM ERROR : La fonction '{name}' n'existe pas")


def get_function(name):
    if name in functions:
        return name
    # exit(f"TOAM ERROR : La fonction '{name}' n'existe pas")


def isInFunction():
    global is_in_function
    return is_in_function


def setIsInFunction(boolean):
    global is_in_function
    is_in_function = boolean


def create_scope():
    if isInFunction():
        functions_stack[-1].append({})
    else:
        runtime_stack.append({})


def exit_scope():
    if isInFunction():
        functions_stack[-1].pop()
    else:
        runtime_stack.pop()


def exist_in_scope(name):
    if isInFunction():
        for scope in reversed(functions_stack[-1]):
            if name in scope:
                return True
    for scope in reversed(runtime_stack):
        if name in scope:
            return True
    return name in global_scope


def update_in_scope(stack, name, value):
    for scope in reversed(stack):
        if name in scope:
            scope[name].value = value
            return True
    return False


def define_variable(name, value):
    if isInGlobalScope():
        global_scope[name] = Value(value)
    elif isInFunction():
        functions_stack[-1][-1][name] = Value(value)
    else:
        runtime_stack[-1][name] = Value(value)


def get_address_of_var_in_global_scope(name):
    if name in global_scope:
        return id(global_scope[name])
    exit(f"Variable non définie: {name}")


def get_address_of_variable(name):
    if isInGlobalScope():
        return get_address_of_var_in_global_scope(name)
    elif isInFunction():
        for scope in reversed(functions_stack[-1]):
            if name in scope:
                return id(scope[name])
    else:
        for scope in reversed(runtime_stack):
            if name in scope:
                return id(scope[name])
    return get_address_of_var_in_global_scope(name)


def set_variable_by_address(address, value):
    if isInFunction():
        for scope in reversed(functions_stack[-1]):
            for objValue in scope.values():
                if id(objValue) == address:
                    objValue.value = value
                    return

    for objValue in global_scope.values():
        if id(objValue) == address:
            objValue.value = value
            return

    for scope in reversed(runtime_stack):
        for objValue in scope.values():
            if id(objValue) == address:
                objValue.value = value
                return


def set_variable(name, value):
    if name in global_scope or isInGlobalScope():
        global_scope[name].value = value
    elif isInFunction():
        if not update_in_scope(functions_stack[-1], name, value):
            functions_stack[-1][-1][name].value = value
    else:
        if not update_in_scope(runtime_stack, name, value):
            runtime_stack[-1][name].value = value


def get_variable_name_by_address(address):
    for name, valueObj in global_scope.items():
        if id(valueObj) == address:
            return name
    for stack in functions_stack:
        for scope in reversed(stack):
            for name, valueObj in scope.items():
                if id(valueObj) == address:
                    return name
    for scope in reversed(runtime_stack):
        for name, valueObj in scope.items():
            if id(valueObj) == address:
                return name
    error(f"Variable non définie sur l'adresse: {address}")
    exit(1)


def get_variable(name):
    if isInGlobalScope():
        return get_var_in_global_scope(name)
    elif isInFunction():
        for scope in reversed(functions_stack[-1]):
            if name in scope:
                return scope[name].value
    else:
        for scope in reversed(runtime_stack):
            if name in scope:
                return scope[name].value
    return get_var_in_global_scope(name)


def get_variable_by_address(address):
    for valueObj in global_scope.values():
        if id(valueObj) == address:
            return valueObj.value
    for stack in functions_stack:
        for scope in reversed(stack):
            for valueObj in scope.values():
                if id(valueObj) == address:
                    return valueObj.value
    for scope in reversed(runtime_stack):
        for valueObj in scope.values():
            if id(valueObj) == address:
                return valueObj.value
    error(f"Variable non définie sur l'adresse: {address}")
    exit(1)


def get_var_in_global_scope(name):
    if name in global_scope:
        return global_scope[name].value
    exit(f"Variable non définie: {name}")


precedence = (
    ('left', 'AND', 'OR'),
    ('nonassoc', 'GREATER', 'LESS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

DEBUG = False

yacc.yacc()


def toam(path):
    s = open(path, "r").read()
    yacc.parse(s)


def toamImport(path):
    s = open(path.strip("\""), "r").read()
    return yacc.parse(s)
