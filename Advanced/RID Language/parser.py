class Parser:
    def __init__(self, token):
        self.token = token
        self.output = []
        self.symbols = {}
        self.transpiled_code = []
        self.position = 0
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
        value_token = self.token[self.position]
        if value_token[1] not in ("NUMBER", "STRING", "BOOL"):
            raise Exception("Invalid value type in declaration")
        value = value_token[0]
        if value_token[1] == "STRING":
            value = f'"{value}"'
        self.output.append(f"{var_name} = {value}")
        self.symbols[var_name] = value
        self.position += 1

    def assignment(self, current_token):
        var_name = current_token[0]
        if var_name not in self.symbols:
            raise Exception(f"Variable '{var_name}' not declared")
        self.position += 1
        if self.token[self.position][1] != "ASSIGN":
            raise Exception("Expected '=' after identifier")
        self.position += 1
        value_token = self.token[self.position]
        if value_token[1] in ("NUMBER", "BOOL"):
            value = value_token[0]
        elif value_token[1] == "STRING":
            value = f'"{value_token[0]}"'
        elif value_token[1] == "IDENTIFIER":
            if value_token[0] not in self.symbols:
                raise Exception(f"Variable '{value_token[0]}' not declared")
            value = value_token[0]
        else:
            raise Exception("Unsupported value type for assignment")
        self.symbols[var_name] = value
        self.output.append(f"{var_name} = {value}")
        self.position += 1

    def print_stmt(self, current_token):
        self.position += 1
        if self.token[self.position][1] != "LPAREN":
            raise Exception("Expected '(' after 'OUT'")
        self.position += 1
        value_token = self.token[self.position]
        if value_token[1] in ("NUMBER", "BOOL"):
            value = value_token[0]
        elif value_token[1] == "STRING":
            value = f'"{value_token[0]}"'
        elif value_token[1] == "IDENTIFIER":
            if value_token[0] not in self.symbols:
                raise Exception("Undefined variable")
            value = value_token[0]
        else:
            raise Exception("Unexpected datatype")
        self.position += 1
        if self.token[self.position][1] != "RPAREN":
            raise Exception("Expected ')' after OUT value")
        self.position += 1
        self.output.append(f"print({value})")

    def input_stmt(self, current_token):
        # Correctly expect an identifier after IN
        self.position += 1
        if self.token[self.position][1] != "IDENTIFIER":
            raise Exception("Expected variable name after IN")
        var_name = self.token[self.position][0]
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
        else:
            raise Exception("Only RUN with number loop supported so far")

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
        block_lines = self.block(current_token)
        params = ",".join(parameters)
        self.output.append(f"def {func_name}({params}):")
        self.output.extend(["    " + line for line in block_lines])

    def block(self, current_token):
        block_lines = []
        while self.position < len(self.token) and self.token[self.position][1] != "RBRACE":
            current_token = self.token[self.position]
            token_type = current_token[1]
            handler = self.handlers.get(token_type, self.unknown_token)
            old_output = self.output
            self.output = []
            handler(current_token)
            block_lines.extend(self.output)
            self.output = old_output
        if self.position < len(self.token) and self.token[self.position][1] == "RBRACE":
            self.position += 1
        return block_lines

    def condition(self, current_token):
        lhs_token = self.token[self.position]
        if lhs_token[1] == "IDENTIFIER":
            if lhs_token[0] not in self.symbols:
                raise Exception(f"Variable '{lhs_token[0]}' not declared")
            lhs = lhs_token[0]
        elif lhs_token[1] in ("NUMBER", "BOOL"):
            lhs = lhs_token[0]
        elif lhs_token[1] == "STRING":
            lhs = f'"{lhs_token[0]}"'
        else:
            raise Exception("Unexpected datatype in condition")
        self.position += 1
        op_token = self.token[self.position]
        op_map = {"EQ": "==", "NEQ": "!=", "LT": "<", "GT": ">", "LTE": "<=", "GTE": ">="}
        if op_token[1] not in op_map:
            raise Exception("Invalid operator in condition")
        op = op_map[op_token[1]]
        self.position += 1
        rhs_token = self.token[self.position]
        if rhs_token[1] == "IDENTIFIER":
            if rhs_token[0] not in self.symbols:
                raise Exception(f"Variable '{rhs_token[0]}' not declared")
            rhs = rhs_token[0]
        elif rhs_token[1] in ("NUMBER", "BOOL"):
            rhs = rhs_token[0]
        elif rhs_token[1] == "STRING":
            rhs = f'"{rhs_token[0]}"'
        else:
            raise Exception("Invalid RHS in condition")
        self.position += 1
        return f"{lhs} {op} {rhs}"

    def func_call(self, current_token):
        pass

    def return_stmt(self, current_token):
        pass

    def expression(self, current_token):
        pass

    def term(self, current_token):
        pass

    def param_list(self, current_token):
        pass

    def arg_list(self, current_token):
        pass

    def unknown_token(self, current_token):
        raise Exception(f"Unknown token {current_token}")


token = [
    ('Run', 'RUN'), ('(', 'LPAREN'), ('3', 'NUMBER'), (')', 'RPAREN'),
    ('{', 'LBRACE'), ('out', 'OUT'), ('(', 'LPAREN'), ('Hey', 'STRING'),
    (')', 'RPAREN'), ('}', 'RBRACE')
]

parser = Parser(token)
parser.parse()
print(parser.symbols)
print(parser.output)
