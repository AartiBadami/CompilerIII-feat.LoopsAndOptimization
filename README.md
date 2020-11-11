This program fully implements a compiler: parsing/tokenizing input, building an intermediate representation (AST), and generating the corresponding ILOC assembly code which is executed with the simulator.  The compiler also optimizes with constant propagation, allowing for a faster compile-time.  
  
  
--Grammar--  


--Examples--  




--How to Run--

(1) from the stdin : "python compiler.py"  
[will print ILOC code to console]  
  
(2) indirection : "python compiler.py < test01.txt"  
[will print ILOC code to console]  
  
(3) compile + run in one step : "cat test01.txt | python compiler.py | ./sim"  
  
* please note that if an error is reported, a line number will also be printed where the error occurred, please disregard this line *  
