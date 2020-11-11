Aarti Badami
Final Project
RUID #172003903
NETID: asb243

How to run test cases:

(1) from the stdin : "python compiler.py"
[will print ILOC code to console]

(2) indirection : "python compiler.py < test01.txt"
[will print ILOC code to console]

(3) compile + run in one step : "cat test01.txt | python compiler.py | ./sim"

* please note that if an error is reported, a line number will also be printed where the error occurred, please disregard this line *




PART ONE -- FULLY FUNCTIONAL
grammar does not specify precedence so 5 * 3 + 4 must be written as (5 * 3) + 4 for instance in order to be computed properly


PART TWO -- FULLY FUNCTIONAL


PART THREE -- not implemented


PART FOUR -- FULLY FUNCTIONAL
constant propagation implemented
