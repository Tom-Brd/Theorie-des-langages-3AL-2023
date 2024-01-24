
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftANDORnonassocGREATERLESSleftPLUSMINUSleftTIMESDIVIDEAND ASSIGN BOOL CHAR CHARCHAIN COMMA DECREASE DECREMENT DIVIDE ELSE ELSEIF EQUALS FALSE FALSE FLOAT FOR FUNCTION GREATER GREATEREQUALS IF INCREASE INCREMENT INT LBRACKET LCURLYBRACKET LESS LESSEQUALS LPAREN MINUS MULTI_COMMENT NAME NOTEQUALS NUMBER OR PLUS PRINT RBRACKET RCURLYBRACKET RETURN RPAREN SCAN SEMICOLON SIMPLE_COMMENT STRING TIMES TOAMSCAN TRUE TRUE VOID WHILEstart : blocbloc : bloc statement SEMICOLON\n            | statement SEMICOLON\n            | bloc SIMPLE_COMMENT\n            | SIMPLE_COMMENT\n            | bloc MULTI_COMMENT\n            | MULTI_COMMENTstatement : FUNCTION RETURNTYPE NAME LPAREN PARAMS RPAREN LCURLYBRACKET bloc RCURLYBRACKET\n                | FUNCTION RETURNTYPE NAME LPAREN RPAREN LCURLYBRACKET bloc RCURLYBRACKETPARAMS : TYPE NAME\n                | TYPE NAME COMMA PARAMSstatement : PRINT LPAREN expression RPAREN\n        | PRINT LPAREN CHARCHAIN RPARENstatement : IF LPAREN expression RPAREN LCURLYBRACKET bloc RCURLYBRACKET\n        | IF LPAREN expression RPAREN LCURLYBRACKET bloc RCURLYBRACKET ELSE LCURLYBRACKET bloc RCURLYBRACKETstatement : WHILE LPAREN expression RPAREN LCURLYBRACKET bloc RCURLYBRACKETstatement : FOR LPAREN statement SEMICOLON expression SEMICOLON statement RPAREN LCURLYBRACKET bloc RCURLYBRACKETstatement : TOAMSCAN LPAREN NAME RPARENstatement : NAME ASSIGN SCAN LPAREN RPARENARRAYELEMENT : expression\n                    | expression COMMA ARRAYELEMENTstatement : TYPE NAME ASSIGN expression\n        | TYPEARRAY NAME ASSIGN LBRACKET RBRACKET\n        | TYPEARRAY NAME ASSIGN LBRACKET ARRAYELEMENT RBRACKET\n        | NAME ASSIGN expression\n        | NAME ASSIGN LBRACKET RBRACKET\n        | NAME ASSIGN LBRACKET ARRAYELEMENT RBRACKETexpression : expression MINUS expression\n\t\t\t\t| expression DIVIDE expression\n\t\t\t\t| expression PLUS expression\n\t\t\t\t| expression TIMES expressionexpression : LPAREN expression RPARENexpression : NUMBERexpression : BOOLEANexpression : NAMEFUNCPARAMS : expression\n                | expression COMMA FUNCPARAMSexpression : NAME LPAREN RPAREN\n        | NAME LPAREN FUNCPARAMS RPARENstatement : NAME LPAREN RPAREN\n        | NAME LPAREN FUNCPARAMS RPARENTYPE : INT\n            | FLOAT\n            | CHAR\n            | STRING\n            | BOOLTYPEARRAY : TYPE LBRACKET RBRACKETRETURNTYPE : TYPE\n            | VOIDstatement : RETURN expression\n        | RETURN statement\n        | RETURNBOOLEAN : TRUE\n                | FALSEexpression : CHARCHAINexpression : expression AND expression\n                | expression OR expression\n                | expression GREATER expression\n                | expression LESS expression\n                | expression EQUALS expression\n                | expression NOTEQUALS expression\n                | expression GREATEREQUALS expression\n                | expression LESSEQUALS expressionstatement : NAME INCREMENT\n                | NAME DECREMENT\n                | NAME INCREASE expression\n                | NAME DECREASE expression'
    
_lr_action_items = {'SIMPLE_COMMENT':([0,2,4,5,22,23,24,51,125,126,132,136,137,140,141,146,152,153,154,155,],[4,22,-5,-7,-4,-6,-3,-2,4,4,4,22,22,4,22,22,4,4,22,22,]),'MULTI_COMMENT':([0,2,4,5,22,23,24,51,125,126,132,136,137,140,141,146,152,153,154,155,],[5,23,-5,-7,-4,-6,-3,-2,5,5,5,23,23,5,23,23,5,5,23,23,]),'FUNCTION':([0,2,4,5,15,22,23,24,37,51,125,126,132,136,137,138,140,141,146,152,153,154,155,],[6,6,-5,-7,6,-4,-6,-3,6,-2,6,6,6,6,6,6,6,6,6,6,6,6,6,]),'PRINT':([0,2,4,5,15,22,23,24,37,51,125,126,132,136,137,138,140,141,146,152,153,154,155,],[8,8,-5,-7,8,-4,-6,-3,8,-2,8,8,8,8,8,8,8,8,8,8,8,8,8,]),'IF':([0,2,4,5,15,22,23,24,37,51,125,126,132,136,137,138,140,141,146,152,153,154,155,],[9,9,-5,-7,9,-4,-6,-3,9,-2,9,9,9,9,9,9,9,9,9,9,9,9,9,]),'WHILE':([0,2,4,5,15,22,23,24,37,51,125,126,132,136,137,138,140,141,146,152,153,154,155,],[10,10,-5,-7,10,-4,-6,-3,10,-2,10,10,10,10,10,10,10,10,10,10,10,10,10,]),'FOR':([0,2,4,5,15,22,23,24,37,51,125,126,132,136,137,138,140,141,146,152,153,154,155,],[11,11,-5,-7,11,-4,-6,-3,11,-2,11,11,11,11,11,11,11,11,11,11,11,11,11,]),'TOAMSCAN':([0,2,4,5,15,22,23,24,37,51,125,126,132,136,137,138,140,141,146,152,153,154,155,],[12,12,-5,-7,12,-4,-6,-3,12,-2,12,12,12,12,12,12,12,12,12,12,12,12,12,]),'NAME':([0,2,4,5,13,14,15,16,17,18,19,20,22,23,24,25,26,27,28,29,32,33,34,35,36,37,38,44,51,56,68,69,71,72,73,74,75,76,77,78,79,80,81,82,84,86,92,97,100,118,123,125,126,132,136,137,138,140,141,146,152,153,154,155,],[7,7,-5,-7,39,41,47,-42,-43,-44,-45,-46,-4,-6,-3,52,-48,-49,53,53,53,53,53,53,53,7,67,53,-2,53,53,-47,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,133,53,7,7,7,7,7,7,7,7,7,7,7,7,7,]),'RETURN':([0,2,4,5,15,22,23,24,37,51,125,126,132,136,137,138,140,141,146,152,153,154,155,],[15,15,-5,-7,15,-4,-6,-3,15,-2,15,15,15,15,15,15,15,15,15,15,15,15,15,]),'INT':([0,2,4,5,6,15,22,23,24,37,51,85,125,126,132,136,137,138,140,141,142,146,152,153,154,155,],[16,16,-5,-7,16,16,-4,-6,-3,16,-2,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,]),'FLOAT':([0,2,4,5,6,15,22,23,24,37,51,85,125,126,132,136,137,138,140,141,142,146,152,153,154,155,],[17,17,-5,-7,17,17,-4,-6,-3,17,-2,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,]),'CHAR':([0,2,4,5,6,15,22,23,24,37,51,85,125,126,132,136,137,138,140,141,142,146,152,153,154,155,],[18,18,-5,-7,18,18,-4,-6,-3,18,-2,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,]),'STRING':([0,2,4,5,6,15,22,23,24,37,51,85,125,126,132,136,137,138,140,141,142,146,152,153,154,155,],[19,19,-5,-7,19,19,-4,-6,-3,19,-2,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,]),'BOOL':([0,2,4,5,6,15,22,23,24,37,51,85,125,126,132,136,137,138,140,141,142,146,152,153,154,155,],[20,20,-5,-7,20,20,-4,-6,-3,20,-2,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,]),'$end':([1,2,4,5,22,23,24,51,],[0,-1,-5,-7,-4,-6,-3,-2,]),'SEMICOLON':([3,15,21,30,31,42,43,45,46,47,48,49,50,53,55,57,60,61,66,88,91,93,94,98,99,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,121,122,127,128,130,134,139,143,144,147,151,156,157,],[24,-52,51,-64,-65,-50,-51,-33,-34,-35,-55,-53,-54,-35,-25,-40,-66,-67,97,-26,-41,-12,-13,-18,-22,-28,-29,-30,-31,-56,-57,-58,-59,-60,-61,-62,-63,-32,-38,-38,-19,-27,138,-23,-39,-39,-24,-14,-16,-9,-8,-15,-17,]),'RCURLYBRACKET':([4,5,22,23,24,51,136,137,141,146,154,155,],[-5,-7,-4,-6,-3,-2,143,144,147,151,156,157,]),'VOID':([6,],[27,]),'ASSIGN':([7,39,41,47,],[28,68,70,28,]),'LPAREN':([7,8,9,10,11,12,15,28,29,32,33,34,35,36,44,47,52,53,54,56,68,71,72,73,74,75,76,77,78,79,80,81,82,84,86,92,97,100,123,],[29,34,35,36,37,38,44,44,44,44,44,44,44,44,44,84,85,86,87,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,]),'INCREMENT':([7,47,],[30,30,]),'DECREMENT':([7,47,],[31,31,]),'INCREASE':([7,47,],[32,32,]),'DECREASE':([7,47,],[33,33,]),'LBRACKET':([13,16,17,18,19,20,28,70,],[40,-42,-43,-44,-45,-46,56,100,]),'RPAREN':([15,29,30,31,42,43,45,46,47,48,49,50,53,55,57,58,59,60,61,62,63,64,65,67,83,84,85,86,87,88,91,93,94,98,99,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,119,120,121,122,124,128,130,133,134,139,143,144,145,147,148,151,156,157,],[-52,57,-64,-65,-50,-51,-33,-34,-35,-55,-53,-54,-35,-25,-40,91,-36,-66,-67,93,94,95,96,98,113,114,117,119,121,-26,-41,-12,-13,-18,-22,-28,-29,-30,-31,-56,-57,-58,-59,-60,-61,-62,-63,-32,-38,130,131,-38,134,-19,-27,-37,-23,-39,-10,-39,-24,-14,-16,150,-9,-11,-8,-15,-17,]),'NUMBER':([15,28,29,32,33,34,35,36,44,56,68,71,72,73,74,75,76,77,78,79,80,81,82,84,86,92,97,100,123,],[45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,]),'CHARCHAIN':([15,28,29,32,33,34,35,36,44,56,68,71,72,73,74,75,76,77,78,79,80,81,82,84,86,92,97,100,123,],[48,48,48,48,48,63,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,]),'TRUE':([15,28,29,32,33,34,35,36,44,56,68,71,72,73,74,75,76,77,78,79,80,81,82,84,86,92,97,100,123,],[49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,]),'FALSE':([15,28,29,32,33,34,35,36,44,56,68,71,72,73,74,75,76,77,78,79,80,81,82,84,86,92,97,100,123,],[50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,]),'SCAN':([28,],[54,]),'RBRACKET':([40,45,46,48,49,50,53,56,89,90,100,101,102,103,104,105,106,107,108,109,110,111,112,113,119,129,134,135,],[69,-33,-34,-55,-53,-54,-35,88,122,-20,128,-28,-29,-30,-31,-56,-57,-58,-59,-60,-61,-62,-63,-32,-38,139,-39,-21,]),'MINUS':([42,45,46,47,48,49,50,53,55,59,60,61,62,63,64,65,83,90,99,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,127,130,134,],[71,-33,-34,-35,-55,-53,-54,-35,71,71,71,71,71,-55,71,71,71,71,71,-28,-29,-30,-31,71,71,71,71,71,71,71,71,-32,-38,-38,71,-39,-39,]),'DIVIDE':([42,45,46,47,48,49,50,53,55,59,60,61,62,63,64,65,83,90,99,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,127,130,134,],[72,-33,-34,-35,-55,-53,-54,-35,72,72,72,72,72,-55,72,72,72,72,72,72,-29,72,-31,72,72,72,72,72,72,72,72,-32,-38,-38,72,-39,-39,]),'PLUS':([42,45,46,47,48,49,50,53,55,59,60,61,62,63,64,65,83,90,99,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,127,130,134,],[73,-33,-34,-35,-55,-53,-54,-35,73,73,73,73,73,-55,73,73,73,73,73,-28,-29,-30,-31,73,73,73,73,73,73,73,73,-32,-38,-38,73,-39,-39,]),'TIMES':([42,45,46,47,48,49,50,53,55,59,60,61,62,63,64,65,83,90,99,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,127,130,134,],[74,-33,-34,-35,-55,-53,-54,-35,74,74,74,74,74,-55,74,74,74,74,74,74,-29,74,-31,74,74,74,74,74,74,74,74,-32,-38,-38,74,-39,-39,]),'AND':([42,45,46,47,48,49,50,53,55,59,60,61,62,63,64,65,83,90,99,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,127,130,134,],[75,-33,-34,-35,-55,-53,-54,-35,75,75,75,75,75,-55,75,75,75,75,75,-28,-29,-30,-31,-56,-57,-58,-59,75,75,75,75,-32,-38,-38,75,-39,-39,]),'OR':([42,45,46,47,48,49,50,53,55,59,60,61,62,63,64,65,83,90,99,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,127,130,134,],[76,-33,-34,-35,-55,-53,-54,-35,76,76,76,76,76,-55,76,76,76,76,76,-28,-29,-30,-31,-56,-57,-58,-59,76,76,76,76,-32,-38,-38,76,-39,-39,]),'GREATER':([42,45,46,47,48,49,50,53,55,59,60,61,62,63,64,65,83,90,99,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,127,130,134,],[77,-33,-34,-35,-55,-53,-54,-35,77,77,77,77,77,-55,77,77,77,77,77,-28,-29,-30,-31,77,77,None,None,77,77,77,77,-32,-38,-38,77,-39,-39,]),'LESS':([42,45,46,47,48,49,50,53,55,59,60,61,62,63,64,65,83,90,99,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,127,130,134,],[78,-33,-34,-35,-55,-53,-54,-35,78,78,78,78,78,-55,78,78,78,78,78,-28,-29,-30,-31,78,78,None,None,78,78,78,78,-32,-38,-38,78,-39,-39,]),'EQUALS':([42,45,46,47,48,49,50,53,55,59,60,61,62,63,64,65,83,90,99,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,127,130,134,],[79,-33,-34,-35,-55,-53,-54,-35,79,79,79,79,79,-55,79,79,79,79,79,-28,-29,-30,-31,-56,-57,-58,-59,79,79,79,79,-32,-38,-38,79,-39,-39,]),'NOTEQUALS':([42,45,46,47,48,49,50,53,55,59,60,61,62,63,64,65,83,90,99,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,127,130,134,],[80,-33,-34,-35,-55,-53,-54,-35,80,80,80,80,80,-55,80,80,80,80,80,-28,-29,-30,-31,-56,-57,-58,-59,80,80,80,80,-32,-38,-38,80,-39,-39,]),'GREATEREQUALS':([42,45,46,47,48,49,50,53,55,59,60,61,62,63,64,65,83,90,99,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,127,130,134,],[81,-33,-34,-35,-55,-53,-54,-35,81,81,81,81,81,-55,81,81,81,81,81,-28,-29,-30,-31,-56,-57,-58,-59,81,81,81,81,-32,-38,-38,81,-39,-39,]),'LESSEQUALS':([42,45,46,47,48,49,50,53,55,59,60,61,62,63,64,65,83,90,99,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,127,130,134,],[82,-33,-34,-35,-55,-53,-54,-35,82,82,82,82,82,-55,82,82,82,82,82,-28,-29,-30,-31,-56,-57,-58,-59,82,82,82,82,-32,-38,-38,82,-39,-39,]),'COMMA':([45,46,48,49,50,53,59,90,101,102,103,104,105,106,107,108,109,110,111,112,113,119,133,134,],[-33,-34,-55,-53,-54,-35,92,123,-28,-29,-30,-31,-56,-57,-58,-59,-60,-61,-62,-63,-32,-38,142,-39,]),'LCURLYBRACKET':([95,96,117,131,149,150,],[125,126,132,140,152,153,]),'ELSE':([143,],[149,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'start':([0,],[1,]),'bloc':([0,125,126,132,140,152,153,],[2,136,137,141,146,154,155,]),'statement':([0,2,15,37,125,126,132,136,137,138,140,141,146,152,153,154,155,],[3,21,43,66,3,3,3,21,21,145,3,21,21,3,3,21,21,]),'TYPE':([0,2,6,15,37,85,125,126,132,136,137,138,140,141,142,146,152,153,154,155,],[13,13,26,13,13,118,13,13,13,13,13,13,13,13,118,13,13,13,13,13,]),'TYPEARRAY':([0,2,15,37,125,126,132,136,137,138,140,141,146,152,153,154,155,],[14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,]),'RETURNTYPE':([6,],[25,]),'expression':([15,28,29,32,33,34,35,36,44,56,68,71,72,73,74,75,76,77,78,79,80,81,82,84,86,92,97,100,123,],[42,55,59,60,61,62,64,65,83,90,99,101,102,103,104,105,106,107,108,109,110,111,112,59,59,59,127,90,90,]),'BOOLEAN':([15,28,29,32,33,34,35,36,44,56,68,71,72,73,74,75,76,77,78,79,80,81,82,84,86,92,97,100,123,],[46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,]),'FUNCPARAMS':([29,84,86,92,],[58,115,120,124,]),'ARRAYELEMENT':([56,100,123,],[89,129,135,]),'PARAMS':([85,142,],[116,148,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('start -> bloc','start',1,'p_start','interpreter.py',121),
  ('bloc -> bloc statement SEMICOLON','bloc',3,'p_bloc','interpreter.py',132),
  ('bloc -> statement SEMICOLON','bloc',2,'p_bloc','interpreter.py',133),
  ('bloc -> bloc SIMPLE_COMMENT','bloc',2,'p_bloc','interpreter.py',134),
  ('bloc -> SIMPLE_COMMENT','bloc',1,'p_bloc','interpreter.py',135),
  ('bloc -> bloc MULTI_COMMENT','bloc',2,'p_bloc','interpreter.py',136),
  ('bloc -> MULTI_COMMENT','bloc',1,'p_bloc','interpreter.py',137),
  ('statement -> FUNCTION RETURNTYPE NAME LPAREN PARAMS RPAREN LCURLYBRACKET bloc RCURLYBRACKET','statement',9,'p_statement_function','interpreter.py',151),
  ('statement -> FUNCTION RETURNTYPE NAME LPAREN RPAREN LCURLYBRACKET bloc RCURLYBRACKET','statement',8,'p_statement_function','interpreter.py',152),
  ('PARAMS -> TYPE NAME','PARAMS',2,'p_params','interpreter.py',160),
  ('PARAMS -> TYPE NAME COMMA PARAMS','PARAMS',4,'p_params','interpreter.py',161),
  ('statement -> PRINT LPAREN expression RPAREN','statement',4,'p_statement_expr','interpreter.py',169),
  ('statement -> PRINT LPAREN CHARCHAIN RPAREN','statement',4,'p_statement_expr','interpreter.py',170),
  ('statement -> IF LPAREN expression RPAREN LCURLYBRACKET bloc RCURLYBRACKET','statement',7,'p_statement_if','interpreter.py',175),
  ('statement -> IF LPAREN expression RPAREN LCURLYBRACKET bloc RCURLYBRACKET ELSE LCURLYBRACKET bloc RCURLYBRACKET','statement',11,'p_statement_if','interpreter.py',176),
  ('statement -> WHILE LPAREN expression RPAREN LCURLYBRACKET bloc RCURLYBRACKET','statement',7,'p_statement_while','interpreter.py',184),
  ('statement -> FOR LPAREN statement SEMICOLON expression SEMICOLON statement RPAREN LCURLYBRACKET bloc RCURLYBRACKET','statement',11,'p_statement_for','interpreter.py',189),
  ('statement -> TOAMSCAN LPAREN NAME RPAREN','statement',4,'p_statement_toamScan','interpreter.py',195),
  ('statement -> NAME ASSIGN SCAN LPAREN RPAREN','statement',5,'p_statement_scan','interpreter.py',200),
  ('ARRAYELEMENT -> expression','ARRAYELEMENT',1,'p_expression_array_element','interpreter.py',205),
  ('ARRAYELEMENT -> expression COMMA ARRAYELEMENT','ARRAYELEMENT',3,'p_expression_array_element','interpreter.py',206),
  ('statement -> TYPE NAME ASSIGN expression','statement',4,'p_statement_assign','interpreter.py',214),
  ('statement -> TYPEARRAY NAME ASSIGN LBRACKET RBRACKET','statement',5,'p_statement_assign','interpreter.py',215),
  ('statement -> TYPEARRAY NAME ASSIGN LBRACKET ARRAYELEMENT RBRACKET','statement',6,'p_statement_assign','interpreter.py',216),
  ('statement -> NAME ASSIGN expression','statement',3,'p_statement_assign','interpreter.py',217),
  ('statement -> NAME ASSIGN LBRACKET RBRACKET','statement',4,'p_statement_assign','interpreter.py',218),
  ('statement -> NAME ASSIGN LBRACKET ARRAYELEMENT RBRACKET','statement',5,'p_statement_assign','interpreter.py',219),
  ('expression -> expression MINUS expression','expression',3,'p_expression_binop_operations','interpreter.py',227),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression_binop_operations','interpreter.py',228),
  ('expression -> expression PLUS expression','expression',3,'p_expression_binop_operations','interpreter.py',229),
  ('expression -> expression TIMES expression','expression',3,'p_expression_binop_operations','interpreter.py',230),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','interpreter.py',235),
  ('expression -> NUMBER','expression',1,'p_expression_number','interpreter.py',240),
  ('expression -> BOOLEAN','expression',1,'p_expression_boolean','interpreter.py',245),
  ('expression -> NAME','expression',1,'p_expression_name','interpreter.py',250),
  ('FUNCPARAMS -> expression','FUNCPARAMS',1,'p_expression_funcparams','interpreter.py',256),
  ('FUNCPARAMS -> expression COMMA FUNCPARAMS','FUNCPARAMS',3,'p_expression_funcparams','interpreter.py',257),
  ('expression -> NAME LPAREN RPAREN','expression',3,'p_expression_call_function','interpreter.py',265),
  ('expression -> NAME LPAREN FUNCPARAMS RPAREN','expression',4,'p_expression_call_function','interpreter.py',266),
  ('statement -> NAME LPAREN RPAREN','statement',3,'p_statement_call_function','interpreter.py',274),
  ('statement -> NAME LPAREN FUNCPARAMS RPAREN','statement',4,'p_statement_call_function','interpreter.py',275),
  ('TYPE -> INT','TYPE',1,'p_type_definition','interpreter.py',283),
  ('TYPE -> FLOAT','TYPE',1,'p_type_definition','interpreter.py',284),
  ('TYPE -> CHAR','TYPE',1,'p_type_definition','interpreter.py',285),
  ('TYPE -> STRING','TYPE',1,'p_type_definition','interpreter.py',286),
  ('TYPE -> BOOL','TYPE',1,'p_type_definition','interpreter.py',287),
  ('TYPEARRAY -> TYPE LBRACKET RBRACKET','TYPEARRAY',3,'p_return_type_array','interpreter.py',292),
  ('RETURNTYPE -> TYPE','RETURNTYPE',1,'p_return_type','interpreter.py',297),
  ('RETURNTYPE -> VOID','RETURNTYPE',1,'p_return_type','interpreter.py',298),
  ('statement -> RETURN expression','statement',2,'p_return_statement','interpreter.py',303),
  ('statement -> RETURN statement','statement',2,'p_return_statement','interpreter.py',304),
  ('statement -> RETURN','statement',1,'p_return_statement','interpreter.py',305),
  ('BOOLEAN -> TRUE','BOOLEAN',1,'p_boolean_definition','interpreter.py',313),
  ('BOOLEAN -> FALSE','BOOLEAN',1,'p_boolean_definition','interpreter.py',314),
  ('expression -> CHARCHAIN','expression',1,'p_expression_charchain','interpreter.py',319),
  ('expression -> expression AND expression','expression',3,'p_expression_binop_bool','interpreter.py',324),
  ('expression -> expression OR expression','expression',3,'p_expression_binop_bool','interpreter.py',325),
  ('expression -> expression GREATER expression','expression',3,'p_expression_binop_bool','interpreter.py',326),
  ('expression -> expression LESS expression','expression',3,'p_expression_binop_bool','interpreter.py',327),
  ('expression -> expression EQUALS expression','expression',3,'p_expression_binop_bool','interpreter.py',328),
  ('expression -> expression NOTEQUALS expression','expression',3,'p_expression_binop_bool','interpreter.py',329),
  ('expression -> expression GREATEREQUALS expression','expression',3,'p_expression_binop_bool','interpreter.py',330),
  ('expression -> expression LESSEQUALS expression','expression',3,'p_expression_binop_bool','interpreter.py',331),
  ('statement -> NAME INCREMENT','statement',2,'p_expression_incr_decr','interpreter.py',336),
  ('statement -> NAME DECREMENT','statement',2,'p_expression_incr_decr','interpreter.py',337),
  ('statement -> NAME INCREASE expression','statement',3,'p_expression_incr_decr','interpreter.py',338),
  ('statement -> NAME DECREASE expression','statement',3,'p_expression_incr_decr','interpreter.py',339),
]
