# map for variable lookup : map(key=variable, value=data type)

import sys
import re

next = None
input = ""
start = 0
symtable = {}
memory = {}
AST = []
instructions = None
next_reg = 1
next_label = 1
offset_num = 0
level = 0
while_flag = 0
for_flag = 0
if_flag = 0


class Node:
  def __init__(self, dtype, value):
    self.dtype = dtype
    self.value = value
    self.left = None
    self.right = None
    self.data = (self.dtype, self.value) # for printing tree

def Program():
  MainP()
  # print "input : ", input

def MainP():
  # scan first two words
  scan()
  start_stmt = next
  scan()
  start_stmt += ' ' + next

  if start_stmt == "def main":
    VarDecls()
    Stmts([])

    # delete this
    # for root in AST:
    #  print "-----------"
    #  print_tree(root)
    #  print "-----------"
    # after finished

    if next != 'end':
      print "line 51"
      error(1) # checking for end token

  else:
    print "line ", 55
    error(1)

def VarDecls():
  scan()
  if next == "int" or next == "bool":
    VarDecl()
    scan()
    if next == ";":
      VarDecls()
    else:
      print "line ", 67
      error(1)

  else: # eps case
    return

def VarDecl():
  global offset_num
  var_type = Type()
  scan()
  var_name = next
  # valid var name check
  if (not var_name[0].isalpha()) or (not var_name.isalnum()):
    print "line ", 80
    error(1)
  symtable[var_name] = var_type
  memory[var_name] = [level, offset_num, None] # level, offset, value
  offset_num += 4

def Type():
  return next

def Stmts(temp_arr):

  head = Stmt()
  if (if_flag == 0) and (while_flag == 0) and (for_flag == 0): AST.append(head)
  else: temp_arr.append(head)
  scan()
  if next == ';':
    scan()
    if next == "end" or next == "else":
      return temp_arr
    else:
      return Stmts(temp_arr)
  else:
    print "line ", 105
    error(1)

def Stmt():
  if next == "print":
    return Print()
  elif next == "while":
    return WHILE()
  elif next == "if":
    return IF()
  elif next == "for":
    return FOR()
  else:
    if next[0].isalpha():
      return Assign()
    else:
      print "line ", 121
      error(1)

def WHILE():
  global while_flag
  head = Node("ctrlflow", "while")
  scan()
  if next != "(":
    print "line 129"
    error(1)
  scan()
  head.left = Expr()
  if head.left.dtype != "bool": error(2)
  scan()
  if next != ")":
    print "line 136"
    error(1)

  scan()
  if next != "do":
    print "line 141"
    error(1)
  scan()
  while_flag += 1
  head.right = Stmts([])
  while_flag -= 1 # reset flag
  return head

def IF():
  global if_flag
  global start
  head = Node("ctrlflow", "ifelse")
  scan()
  if next != "(":
    print "line 155"
    error(1)
  scan()
  head.left = Node("ctrlflow", "if")
  head.left.left = Expr()
  if head.left.left.dtype != "bool": error(2)
  scan()
  if next != ")":
    print "line 162"
    error(1)
  scan()
  if next != "do":
    print "line 166"
    error(1)
  scan()
  if_flag += 1
  head.left.right = Stmts([])
  if next == "end":
    head.right = None
    if_flag -= 1
    return head

  else: # else case
    scan()
    head.right = Node("ctrlflow", "else")
    head.right.left = Stmts([])
    if_flag -= 1
    return head


def FOR():
  global for_flag
  head = Node("ctrlflow", "for")
  scan()
  if next != "(":
    print "line 191"
    error(1)
  scan()
  head.left = []
  head.left.append(Stmt()) # Stmt
  scan()
  if next != ";": # first semicolon
    print "line 198"
    error(1)
  scan()
  head.left.append(Expr()) # Expr
  if head.left[1].dtype != "bool": error(2)
  scan()
  if next != ";": # second semicolon
    print "line 204"
    error(1)
  scan()
  head.left.append(Stmt()) # Stmt
  scan()
  if next != ")":
    print "line 210"
    error(1)
  scan()
  if next != "do":
    print "line 214"
    error(1)
  scan()
  for_flag += 1
  head.right = Stmts([])
  for_flag -= 1 # reset flag
  return head


def Assign():
  var_name = next
  if var_name not in symtable.keys():
    print "line ", 226
    error(3)
  left = Node(symtable[var_name], var_name)
  scan()
  if next == "=":
    head = Node('assign', None)
    scan()
    right = Expr()
    head.left = left
    head.right = right

    # type checking
    if head.left.dtype != head.right.dtype:
      print "line ", 239
      error(4)

    return optimize(head)
    #return head

  else:
    print "line ", 245
    error(1)

def Print():
  scan()
  if next == '(':
    scan()
    print_val = next
    head = Node('print', None)
    if print_val in symtable.keys():
      left = Node(symtable[print_val], print_val)
    else:
      print "line ", 257
      error(3)

    scan()
    if next != ')':
      print "line ", 262
      error(1)
  else:
    print "line ", 265
    error(1)

  head.left = left
  return head

def Expr():
  global next
  ops = ['&', '|', '^', '+', '-', '*', '/', '<', '<', '>', '>', '=', '!']

  if next == '!':
    scan()
    left = Expr()
    head = Node('bool', '^')
    head.left = left
    head.right = Node('bool', 'true')

    if not TypeMatch(head, left, head.right):
      print "line ", 283
      error(4)
    else: return head  
  
  elif next == '(':
    scan()
    head = Expr()
    scan()
    if next != ')':
      print "line ", 292
      error(1)

    while look_ahead() in ops:
      left = head
      scan()
      head = BinOp()
      scan()
      right = Expr()
      head.left = left
      head.right = right

      if not TypeMatch(head, left, right):
        print "line ", 305
        error(4)

    return head

  elif next == ')':
    return

  else:
    if look_ahead() in ops: # E Op E
      if next[0].isalpha() and next != "true" and next != "false":
        left = Id()
      else: left = Const()
      scan()
      head = BinOp()
      scan()
      right = Expr()

      head.left = left
      head.right = right

      if not TypeMatch(head, left, right):
        print "line ", 327
        error(4)
      else:
        return head

    elif next[0].isalpha() and (not (next == "true" or next == "false")): # ID
      return Id()

    elif next[-1].isdigit() or next == "true" or next == "false": # Const
      return Const()

    else:
      print "line ", 341
      error(1)

def TypeMatch(head, left, right):
  if head.value == "+" or head.value == "-" or head.value == "*" or head.value == "/":
    if left.dtype != "int" or right.dtype != "int": return False
    else: return True

  elif head.value == "&&" or head.value == "||" or head.value == "^":
    if left.dtype != "bool" or right.dtype != "bool": return False
    else: return True

  elif head.value == "<" or head.value == "<=" or head.value == ">" or head.value == ">=":
    if left.dtype != "int" or right.dtype != "int": return False
    else: return True

  elif head.value == "==" or head.value == "!=":
    if left.dtype != right.dtype: return False
    else: return True

  else:
    error(5)

def BinOp():
  bool_ops = ['&&', '||', '^', '<', '<=', '>=', '>', '==', '!=']
  int_ops = ['+', '-', '*', '/']

  if (next not in bool_ops) and (next not in int_ops):
    print "line ", 371
    error(1)
  else:
    if next in bool_ops: return Node('bool', next)
    else: return Node('int', next)

def Id():
  # checking if valid id
  if (not next[0].isalpha()) or (not next.isalnum()) or (next == 'int') or (next == 'bool'):
    print "line ", 380
    error(1)
  else:
    # creating node
    var_name = next
    if var_name not in symtable.keys():
      print "line ", 386
      print "next : ", next
      error(3) # undeclared variable
    else: return Node(symtable[var_name], var_name)

def Const():
  # checking if valid const
  if next.isdigit():
    if int(next) < 0:
      print "line ", 395
      error(1)
  else:
    if next != 'true' and next != 'false':
      print "line ", 399
      error(1)

  # creating node
  if next == 'true' or next == 'false': return Node('bool', next)
  else: return Node('int', next)

def error(n):
  if n == 1:
    sys.stdout.write("syntax error\n")
    sys.exit(1)
  elif n == 2:
    sys.stdout.write("exception\n")
    sys.exit(1)
  elif n == 3:
    sys.stdout.write("error: variable undeclared\n")
    sys.exit(1)
  elif n == 4:
    sys.stdout.write("error: type mismatch\n")
    sys.exit(1)
  else:
    sys.stdout.write("ERROR:%i, SOURCE:%s\n" % (n, input))
    sys.exit(1)

def scan():
  global next
  global start
  temp_word = ""
  char = input[start]
  tokens = ['!', '(', ')', ';', '&&', '||', '^', '+', '-', '*',
  '/', '<', '<=', '>=', '>', '==', '!=']  

  while char == ' ':
    start += 1
    char = input[start]

  if char in tokens:
    if (char == "<" or char == ">" or char == "!") and (input[start+1] == "="):
      next = char + input[start+1]
      start += 2
      return  
    else:
      next = char
      start += 1
      return

  while (start < len(input)) and (char not in tokens) and (char != ' '):
    temp_word += char
    start += 1
    if start == len(input): break # edge case
    char = input[start]

  next = temp_word  

def load_input():
  global input
  for line in sys.stdin:
    input += re.sub(r"\s+", " ", line)
  input = input[:-1]

def look_ahead():
  i = 0
  next_tok = input[start+i]
  while next_tok == ' ':
    i += 1
    next_tok = input[start+i]

  return next_tok

def print_tree(root):
  queue = []
  queue.append([root, 0])

  while len(queue) != 0:
    curr_node = queue.pop(0)
    curr_level = curr_node[1]
    print_val = str(curr_node[0].data)
    while curr_node[1] > 0:
      print_val = "\t" + print_val
      curr_node[1] -= 1

    print print_val

    # push children
    if curr_node[0].value == "while":
      queue.append([curr_node[0].left, (curr_level+1)])
      arr = curr_node[0].right
      for item in arr:
        queue.append([item, (curr_level+1)])

    elif curr_node[0].value == "for":
      arr_left = curr_node[0].left
      for item in arr_left:
        queue.append([item, (curr_level+1)])
      arr_right = curr_node[0].right
      for item in arr_right:
        queue.append([item, (curr_level+1)])

    elif curr_node[0].value == "ifelse":
      expression = curr_node[0].left.left
      queue.append([expression, (curr_level+1)])
      arr_if = curr_node[0].left.right
      for item in arr_if:
        queue.append([item, (curr_level+1)])
      if curr_node[0].right != None:
        arr_else = curr_node[0].right.left
        for item in arr_else:
          queue.append([item, (curr_level+1)])

    else:
      if curr_node[0].left != None:
        queue.append([curr_node[0].left, (curr_level+1)])
      if curr_node[0].right != None:
        queue.append([curr_node[0].right, (curr_level+1)])


def optimize(head):
  
  if ConstExpr(head.right):
    right_dtype = head.right.dtype
    right_value = str(Eval(head.right))
    # convert to str
    if right_value == "True": right_value = "true"
    elif right_value == "False": right_value = "false"
    elif right_value.isdigit(): right_value = str(right_value)
    else: error(1)

    head.right = Node(right_dtype, right_value)
    return head
  else:
    return head

def ConstExpr(node):
  # base case
  if node.right == None and node.left == None:
    if node.value == "true" or node.value == "false" or node.value.isdigit():
      return True
    else: return False
  else: # recursive case
    return (ConstExpr(node.left) and ConstExpr(node.right))

def Eval(node):
  ops = ["+", "-", "*", "/", "<", "<=", ">", ">=", "&&", "||", "^", "==", "!="]

  if node.value in ops:
    op = node.value
    value1 = Eval(node.left)
    value2 = Eval(node.right)

    # operator calculations
    if op == "+": return (value1 + value2)
    elif op == "-": return (value1 - value2)
    elif op == "*": return (value1 * value2)
    elif op == "/": return (value1 / value2)
    elif op == "<":
      if value1 < value2: return True
      else: return False
    elif op == "<=":
      if value1 <= value2: return True
      else: return False
    elif op == ">":
      if value1 > value2: return True
      else: return False
    elif op == ">=":
      if value1 >= value2: return True
      else: return False
    elif op == "&&":
      if value1 and value2: return True
      else: return False
    elif op == "||":
      if value1 or value2: return True
      else: return False
    elif op == "^":
      if (value1 == True and value2 == False) or (value1 == False and value2 == True):
        return True
      else: return False
    elif op == "==":
      if value1 == value2: return True
      else: return False
    elif op == "!=":
      if value1 != value2: return True
      else: return False
    else:
      error(1)

  elif node.value == "true":
    return True
  elif node.value == "false":
    return False
  elif node.value.isdigit():
    return int(node.value)
  else:
    return error(1)


# ASSEMBLY CODE GENERATOR ------------------------
def IDENT(node):
  if node.value[0].isalpha(): return True
  else: return False

def CONST(node):
  if node.value.isdigit(): return True
  elif node.value == "true" or node.value == "false": return True
  else: return False

def assembly_code_driver():
  global instructions
  global next_reg
  num_trees = len(AST)
  instructions = []

  instructions.append("L0:")
  instructions.append("\tloadI 0 => r0")
  for i in range(num_trees): # generates code sets for each AST
    assembly_code(AST[i])

def NextRegister():
  global next_reg
  output = "r" + str(next_reg)
  next_reg += 1
  return output

def NextLabel():
  global next_label
  output = "L" + str(next_label)
  next_label += 1
  return output

def emit(command, reg1, reg2, result):
  if command == "\toutput":
    return (command + " " + reg1)
  elif reg2 == None:
    return (command + " " + reg1 + " => " + result)
  elif command == "\tstoreAI":
    return (command + " " + reg1 + " => " + reg2 + ", " + result)
  else:
    return (command + " " + reg1 + ", " + reg2 + " => " + result)

def base(node): # may change when functions are introduced
  var_name = node.value
  return "r0" # str(memory[var_name][0]) # [level, offset]

def offset(node):
  var_name = node.value
  return str(memory[var_name][1]) # [level, offset]

def op_code(op):
  if op == '+':
    return "\tadd"
  elif op == '-':
    return "\tsub"
  elif op == '*':
    return "\tmult"
  elif op == '/':
    return "\tdiv"
  elif op == '&&':
    return "\tand"
  elif op == '||':
    return "\tor"
  elif op == '^':
    return "\txor"
  elif op == '<':
    return "\tcmp_LT"
  elif op == '<=':
    return "\tcmp_LE"
  elif op == '==':
    return "\tcmp_EQ"
  elif op == '!=':
    return "\tcmp_NE"
  elif op == '>=':
    return "\tcmp_GE"
  elif op == '>':
    return "\tcmp_GT"
  elif op == "assign":
    return "\tstore"
  else:
    error(5)



# ret type : register (where result stored)
def assembly_code(node):
  ops = ['+', '-', '*', '/', '&&', '||', '^', '<', 
  '<=', '==', '!=', '>=', '>']
  global next_reg

  if node.dtype == "assign":
    offset_num = offset(node.left)
    val_to_store = assembly_code(node.right)
    instruction = emit("\tstoreAI", val_to_store, base(node), offset_num)
    instructions.append(instruction)
    next_reg = 1

  elif node.dtype == "print":
    t1 = offset(node.left)
    instruction = emit("\toutput", t1, None, None)
    instructions.append(instruction)

  elif node.value == "while":
    L1 = NextLabel()
    instructions.append(("\tbr " + L1))
    instructions.append(("\n" + L1 + ":"))
    cmp_reg = assembly_code(node.left)
    L2 = NextLabel()
    L3 = NextLabel()
    instructions.append(("\tcbr " + cmp_reg + " => " + L2 + ", " + L3))
    instructions.append(("\n" + L2 + ":"))
    for subnode in node.right: # loads all instructions inside loop
      assembly_code(subnode)
    instructions.append(("\tbr " + L1))

    instructions.append(("\n" + L3 + ":"))
    return

  elif node.value == "for":
    L1 = NextLabel()
    assembly_code(node.left[0])
    instructions.append(("\tbr " + L1))
    instructions.append(("\n" + L1 + ":"))
    cmp_reg = assembly_code(node.left[1])
    L2 = NextLabel()
    L3 = NextLabel()
    instructions.append(("\tcbr " + cmp_reg + " => " + L2 + ", " + L3))
    instructions.append(("\n" + L2 + ":"))
    for subnode in node.right:
      assembly_code(subnode)
    assembly_code(node.left[2])
    instructions.append(("\tbr " + L1))

    instructions.append(("\n" + L3 + ":"))
    return

  elif node.value == "ifelse":
    if node.right != None: # if, else case
      L1 = NextLabel()
      instructions.append(("\tbr " + L1))
      instructions.append(("\n" + L1 + ":"))
      cmp_reg = assembly_code(node.left.left)
      L2 = NextLabel()
      L3 = NextLabel()
      L4 = NextLabel()
      instructions.append(("\tcbr " + cmp_reg + " => " + L2 + ", " + L3))

      instructions.append(("\n" + L2 + ":"))
      for subnode in node.left.right: # if
        assembly_code(subnode)
      instructions.append(("\tbr " + L4))

      instructions.append(("\n" + L3 + ":"))
      for subnode in node.right.left: # else
        assembly_code(subnode)
      instructions.append(("\tbr " + L4))

      instructions.append(("\n" + L4 + ":"))
      return

    else: # if case
      L1 = NextLabel()
      instructions.append(("\tbr " + L1))
      instructions.append(("\n" + L1 + ":"))
      cmp_reg = assembly_code(node.left.left)
      L2 = NextLabel()
      L3 = NextLabel()
      instructions.append(("\tcbr " + cmp_reg + " => " + L2 + ", " + L3))
      
      instructions.append(("\n" + L2 + ":"))
      for subnode in node.left.right: # if
        assembly_code(subnode)
      instructions.append(("\tbr " + L3))
      instructions.append(("\n" + L3 + ":"))
      return

  elif node.value in ops: # OP
    t1 = assembly_code(node.left)
    t2 = assembly_code(node.right)
    result = NextRegister()
    instruction = emit(op_code(node.value), t1, t2, result)
    instructions.append(instruction)
    return result

  elif CONST(node): # NUM or BOOL
    if node.value.isdigit():
      result = NextRegister()
      instruction = emit("\tloadI", node.value, None, result)
      instructions.append(instruction)
      return result
    elif node.value == "true":
      result = NextRegister()
      instruction = emit("\tloadI", "1", None, result)
      instructions.append(instruction)
      return result
    elif node.value == "false":
      result = NextRegister()
      instruction = emit("\tloadI", "0", None, result)
      instructions.append(instruction)
      return result
    else: error(5)

  elif IDENT(node): # IDENT
    t1 = base(node)
    t2 = offset(node)
    result = NextRegister()
    instruction = emit("\tloadAI", t1, t2, result)
    instructions.append(instruction)
    return result

  else:
    error(5)


def main():
  load_input()
  Program()
  assembly_code_driver()
  global instructions

  # strip extra label at end
  if instructions[-1][-1] == ":":
    instructions = instructions[:-1]

  # print memory
  # for i in range(len(instructions)):
    # print "------"
    # print "set ", i
    #for string in instructions[i]:
    #  print string
    # print "----------"

  for string in instructions:
    print string


if __name__ == "__main__":
  main()

