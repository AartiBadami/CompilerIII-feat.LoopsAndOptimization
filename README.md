This program fully implements a compiler: parsing/tokenizing input, building an intermediate representation (AST), and generating the corresponding ILOC assembly code which is executed with the simulator.  The compiler also optimizes with constant propagation, allowing for a faster compile-time.  
  
  
--Grammar--  
< Program >   ::= < Main >  
< Main >      ::= def main < VarDecls > < Stmts > end  
< VarDecls >  ::= < VarDecl >; < VarDecls > | e  
< VarDecl >   ::= < Type > < Id >  
< Type >      ::= int | bool  
< Stmts >     ::= < Stmt >; < Stmts > | < Stmt >;  
< Stmt >      ::= < Assign > | < Print > | < While > | < If > | < For >  
< Assign >    ::= < Id > = < Expr >  
< Print >     ::= print (< Id >)  
< While >     ::= while (< Expr >) do < Stmts > end  
< If >        ::= if (< Expr >) do < Stmts> end  
                | if (< Expr >) do < Stmts > else < Stmts > end  
< For >       ::= for (< Stmt >; < Expr >; < Stmt >) do < Stmts > end  
< Expr >      ::= < Expr > < BinOp > < Expr >  
                | ! < Expr >  
                | < Id >  
                | < Const >  
                | (< Expr >)  
< BinOp >     ::= + | - | * | / | && | || | ^ | < | <= | == | != | >= | >  




--Examples--  
Sample input:  
def main  
    int sum;  
    int i;  
    sum = 0;  
    for (i = 1; i <= 10; i = i+1) do  
        sum = sum + i;  
    end;  
    print(sum);  
end  
  
Sample output:  
60  
  
  
  
--How to Run--  

(1) from the stdin : "python compiler.py"  
[will print ILOC code to console]  
  
(2) indirection : "python compiler.py < test01.txt"  
[will print ILOC code to console]  
  
(3) compile + run in one step : "cat test01.txt | python compiler.py | ./sim"  
  
* please note that if an error is reported, a line number will also be printed where the error occurred, please disregard this line *  
