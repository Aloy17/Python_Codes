
class Parser:
    def __init__(self, token):
        self.token = token
        self.output = []
        self.symbols = {}
        self.functions = {}
        self.position = 0
        self.current_params = []
        self.handlers = {
            "LET": self.var_declare,
            "IDENTIFIER": self.assignment,
            "OUT": self.print_stmt,
            "IN": self.input_stmt,
            "RUN": self.loop_stmt,
            "IF": self.conditional_stmt,
            "ELIF": self.conditional_stmt,
            "ELSE": self.conditional_stmt,
            "FUNC": self.func_def,
            "RETURN": self.return_stmt
        }


    def parse(self):
        while self.position < len(self.token):
            current_token = self.token[self.position]
            token_type = current_token[1]

            if token_type == "IDENTIFIER":
                if self.position + 1 < len(self.token) and self.token[self.position + 1][1] == "LPAREN":
                    handler = self.func_call
                else:
                    handler = self.assignment
            else:
                handler = self.handlers.get(token_type, self.unknown_token)

            handler(current_token)


    def var_declare(self, current_token):

        self.position += 1
        var_token = self.token[self.position]

        if var_token[1] != "IDENTIFIER":
            raise Exception("Expected identifier after 'LET'")

        var_name = var_token[0]
        self.position += 1

        if self.token[self.position][1] != "ASSIGN":
            raise Exception("Expected '=' after identifier")

        self.position += 1
        expr = self.expression(self.token[self.position])

        self.output.append(f"{var_name} = {expr.strip()}")
        self.symbols[var_name] = expr


    def assignment(self, current_token):
        var_name = current_token[0]

        if var_name not in self.symbols:
            raise Exception(f"Variable '{var_name}' not declared")

        self.position += 1
        if self.token[self.position][1] != "ASSIGN":
            raise Exception("Expected '=' after identifier")

        self.position += 1
        expr = self.expression(self.token[self.position])

        self.symbols[var_name] = expr
        self.output.append(f"{var_name} = {expr.strip()}")


    def print_stmt(self, current_token):
        self.position += 1
        if self.token[self.position][1] != "LPAREN":
            raise Exception("Expected '(' after 'OUT'")
        self.position += 1

        value = self.expression(self.token[self.position])

        if self.token[self.position][1] != "RPAREN":
            raise Exception("Expected ')' after OUT value")
        self.position += 1
        self.output.append(f"print({value})")


    def input_stmt(self, current_token):
        self.position += 1
        if self.token[self.position][1] != "IDENTIFIER":
            raise Exception("Expected variable name after IN")
        var_name = self.token[self.position][0]

        if var_name not in self.symbols:
            raise Exception(f"Variable '{var_name}' not declared. Use 'Let {var_name} = ...' first")

        self.position += 1

        if self.token[self.position][1] != "LPAREN":
            raise Exception("Expected '(' after variable name")

        self.position += 1
        next_token = self.token[self.position]

        if next_token[1] == "RPAREN":
            self.output.append(f"{var_name} = input()")
            self.position += 1

        elif next_token[1] == "STRING":
            prompt = f'"{next_token[0]}"'
            self.position += 1

            if self.token[self.position][1] != "RPAREN":
                raise Exception("Expected ')' after input prompt")
            self.output.append(f"{var_name} = input({prompt})")
            self.position += 1

        else:
            raise Exception("Invalid syntax in input statement")


    def loop_stmt(self, current_token):

        if current_token[1] != "RUN":
            raise Exception("Expected 'RUN'")
        self.position += 1
        next_token = self.token[self.position]

        if next_token[1] == "LPAREN":
            self.position += 1
            num_token = self.token[self.position]

            if num_token[1] != "NUMBER":
                raise Exception("Expected number inside Run(...)")
            loop_template = f"for _ in range({num_token[0]}):"
            self.position += 1

            if self.token[self.position][1] != "RPAREN":
                raise Exception("Expected ')' after loop count")
            self.position += 1

            if self.token[self.position][1] != "LBRACE":
                raise Exception("Expected '{' to start loop block")
            self.position += 1

            block_lines = self.block(current_token)
            self.output.append(loop_template)
            self.output.extend(["    " + line for line in block_lines])

        elif next_token[1] == "WHILE":
            self.position += 1

            if self.token[self.position][1] != "LPAREN":
                raise Exception("Expected '(' after 'while'")
            self.position += 1
            cond_str = self.condition(self.token[self.position])

            if self.token[self.position][1] != "RPAREN":
                raise Exception("Expected ')' after condition")
            self.position += 1

            if self.token[self.position][1] != "LBRACE":
                raise Exception("Expected '{' to start loop block")
            self.position += 1
            block_lines = self.block(current_token)

            self.output.append(f"while {cond_str}:")
            self.output.extend(["    " + line for line in block_lines])

        else:
            raise Exception("Expected '(' or 'while' after RUN")


    def conditional_stmt(self, current_token):

        keyword = current_token[1]
        if keyword not in ("IF", "ELIF", "ELSE"):
            raise Exception("Expected IF, ELIF, or ELSE")
        self.position += 1

        cond_str = ""
        if keyword in ("IF", "ELIF"):

            if self.token[self.position][1] != "LPAREN":
                raise Exception("Expected '(' after conditional keyword")
            self.position += 1
            cond_str = self.condition(self.token[self.position])

            if self.token[self.position][1] != "RPAREN":
                raise Exception("Expected ')' after condition")
            self.position += 1

        if self.token[self.position][1] != "LBRACE":
            raise Exception("Expected '{' to start block")
        self.position += 1
        block_lines = self.block(current_token)

        if keyword == "IF":
            self.output.append(f"if {cond_str}:")

        elif keyword == "ELIF":
            self.output.append(f"elif {cond_str}:")

        else:
            self.output.append("else:")

        for line in block_lines:
            self.output.append("    " + line)


    def func_def(self, current_token):

        if current_token[1] != "FUNC":
            raise Exception("Expected 'FUNC'")
        self.position += 1

        func_name = self.token[self.position][0]
        self.position += 1

        if self.token[self.position][1] != "LPAREN":
            raise Exception("Expected '(' after function name")
        self.position += 1
        parameters = []

        while self.token[self.position][1] != "RPAREN":

            if self.token[self.position][1] == "IDENTIFIER":
                parameters.append(self.token[self.position][0])
                self.position += 1

            elif self.token[self.position][0] == ",":
                self.position += 1

            else:
                raise Exception("Invalid token in function parameters")
        self.position += 1

        if self.token[self.position][1] != "LBRACE":
            raise Exception("Expected '{' to start function block")
        self.position += 1
        self.current_params = parameters

        block_lines = self.block(current_token)
        params = ",".join(parameters)
        self.output.append(f"def {func_name}({params}):")
        self.output.extend(["    " + line for line in block_lines])
        self.functions[func_name] = {"params": parameters, "body": block_lines}
        self.current_params = []


    def block(self, current_token):
        block_lines = []

        while self.position < len(self.token) and self.token[self.position][1] != "RBRACE":
            current_token = self.token[self.position]
            token_type = current_token[1]

            if token_type == "IDENTIFIER":

                if self.position + 1 < len(self.token) and self.token[self.position + 1][1] == "LPAREN":
                    handler = self.func_call
                else:
                    handler = self.assignment

            else:
                handler = self.handlers.get(token_type, self.unknown_token)

            old_output = self.output
            self.output = []
            handler(current_token)
            block_lines.extend(self.output)
            self.output = old_output

        if self.position < len(self.token) and self.token[self.position][1] == "RBRACE":
            self.position += 1

        if len(block_lines) == 0:
            block_lines.append("pass")

        return block_lines


    def condition(self, current_token):

        lhs = self.expression(self.token[self.position])
        op_token = self.token[self.position]
        op_map = {"EQ": "==", "NEQ": "!=", "LT": "<", "GT": ">", "LTE": "<=", "GTE": ">="}

        if op_token[1] not in op_map:
            raise Exception("Invalid operator in condition")
        op = op_map[op_token[1]]
        self.position += 1

        rhs = self.expression(self.token[self.position])

        return f"{lhs} {op} {rhs}"

    def func_call(self, current_token):
        func_name = current_token[0]

        if func_name not in self.functions:
            raise Exception(f"Function '{func_name}' not defined")
        self.position += 1

        if self.token[self.position][1] != "LPAREN":
            raise Exception("Expected '(' after function name")
        self.position += 1
        args = []

        while self.position < len(self.token) and self.token[self.position][1] != "RPAREN":
            arg_token = self.token[self.position]

            if arg_token[1] in ("NUMBER", "BOOL"):
                args.append(str(arg_token[0]))

            elif arg_token[1] == "STRING":
                args.append(f'"{arg_token[0]}"')

            elif arg_token[1] == "IDENTIFIER":

                if arg_token[0] in self.symbols or arg_token[0] in self.current_params:
                    args.append(arg_token[0])
                else:
                    raise Exception(f"Variable '{arg_token[0]}' not declared")

            else:
                raise Exception(f"Unsupported argument type: {arg_token[1]}")
            self.position += 1

            if self.position < len(self.token) and self.token[self.position][1] != "RPAREN":

                if self.token[self.position][0] != ",":
                    raise Exception("Expected ',' between function arguments")
                self.position += 1

                if self.position < len(self.token) and self.token[self.position][1] == "RPAREN":
                    raise Exception("Trailing comma not allowed in function arguments")

        if self.position >= len(self.token) or self.token[self.position][1] != "RPAREN":
            raise Exception("Expected ')' after function arguments")
        self.position += 1
        call_str = f"{func_name}({', '.join(args)})"
        self.output.append(call_str)


    def return_stmt(self, current_token):

        if current_token[1] != "RETURN":
            raise Exception("Error, expected 'give'")
        self.position += 1

        expr = self.expression(self.token[self.position])

        self.output.append(f"return {expr}")


    def expression(self, current_token):
        return self.parse_additive()

    def parse_additive(self):
        left = self.parse_multiplicative()

        while self.position < len(self.token) and self.token[self.position][1] in ("PLUS", "MINUS"):
            op = self.token[self.position][0]
            self.position += 1
            right = self.parse_multiplicative()
            left = f"{left} {op} {right}"

        return left


    def parse_multiplicative(self):
        left = self.parse_primary()

        while self.position < len(self.token) and self.token[self.position][1] in ("MULT", "DIV", "MOD"):
            op = self.token[self.position][0]
            self.position += 1
            right = self.parse_primary()
            left = f"{left} {op} {right}"

        return left


    def parse_primary(self):

        if self.position >= len(self.token):
            raise Exception("Unexpected end of expression")

        current = self.token[self.position]
        value_token, key_token = current

        if key_token == "NUMBER":
            self.position += 1
            return value_token

        elif key_token == "STRING":
            self.position += 1
            return f'"{value_token}"'

        elif key_token == "BOOL":
            self.position += 1
            return value_token

        elif key_token == "IDENTIFIER":

            if self.position + 1 < len(self.token) and self.token[self.position + 1][1] == "LPAREN":
                return self.parse_function_call()

            else:
                if value_token not in self.symbols and value_token not in self.current_params:
                    raise Exception(f"Variable '{value_token}' not declared")
                self.position += 1
                return value_token

        elif key_token == "LPAREN":
            self.position += 1
            expr = self.parse_additive()

            if self.position >= len(self.token) or self.token[self.position][1] != "RPAREN":
                raise Exception("Expected ')' after expression")
            self.position += 1
            return f"({expr})"

        else:
            raise Exception(f"Unexpected token in expression: {key_token}")

    def parse_function_call(self):
        func_name = self.token[self.position][0]

        if func_name not in self.functions:
            raise Exception(f"Function '{func_name}' not defined")
        self.position += 1

        if self.token[self.position][1] != "LPAREN":
            raise Exception("Expected '(' after function name")
        self.position += 1

        args = []

        while self.position < len(self.token) and self.token[self.position][1] != "RPAREN":
            arg_expr = self.parse_additive()
            args.append(arg_expr)

            if self.position < len(self.token) and self.token[self.position][1] != "RPAREN":
                if self.token[self.position][0] != ",":
                    raise Exception("Expected ',' between function arguments")
                self.position += 1
                if self.position < len(self.token) and self.token[self.position][1] == "RPAREN":
                    raise Exception("Trailing comma not allowed in function arguments")

        if self.position >= len(self.token) or self.token[self.position][1] != "RPAREN":
            raise Exception("Expected ')' after function arguments")
        self.position += 1

        return f"{func_name}({', '.join(args)})"


    def unknown_token(self, current_token):
        raise Exception(f"Unknown token {current_token}")


#Test
token = [
    ('Let', 'LET'),
    ('x', 'IDENTIFIER'),
    ('=', 'ASSIGN'),
    ('0', 'NUMBER'),
    ('Run', 'RUN'),
    ('while', 'WHILE'),
    ('(', 'LPAREN'),
    ('x', 'IDENTIFIER'),
    ('<', 'LT'),
    ('3', 'NUMBER'),
    (')', 'RPAREN'),
    ('{', 'LBRACE'),
    ('out', 'OUT'),
    ('(', 'LPAREN'),
    ('x', 'IDENTIFIER'),
    (')', 'RPAREN'),
    ('x', 'IDENTIFIER'),
    ('=', 'ASSIGN'),
    ('x', 'IDENTIFIER'),
    ('+', 'PLUS'),
    ('1', 'NUMBER'),
    ('}', 'RBRACE')
]

parser = Parser(token)
parser.parse()
print(parser.output)