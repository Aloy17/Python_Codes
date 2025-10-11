program        → statement* ;

statement      → var_decl
               | print_stmt
               | input_stmt
               | assignment
               | loop_stmt
               | conditional_stmt
               | func_def
               | func_call ;

var_decl       → "Let" IDENTIFIER "=" expression ;

assignment     → IDENTIFIER "=" expression ;

print_stmt     → "out" "(" expression ")" ;

input_stmt     → IDENTIFIER "=" "in" "("? STRING? ")"? ;

expression → term (("+" | "-" | "*" | "/" | "%") term)*

term           → NUMBER
               | STRING
               | IDENTIFIER
               | "(" expression ")" ;

loop_stmt → "Run" "(" expression ")" block         ; fixed-count
           | "Run" "while" "(" condition ")" block ; conditional


conditional_stmt → "agar" "(" condition ")" block
                   ("ya_fir" "(" condition ")" block)*
                   ("warna" block)? ;


condition      → expression ( "==" | "!=" | "<" | ">" | "<=" | ">=" ) expression ;

func_def       → "func" IDENTIFIER "(" param_list? ")" block ;

param_list     → IDENTIFIER ("," IDENTIFIER)* ;

func_call      → IDENTIFIER "(" arg_list? ")" ;

arg_list       → expression ("," expression)* ;

block          → "{" statement* "}" ;

return_stmt    → "give" expression ;
