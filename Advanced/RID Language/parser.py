from logging import exception


class Parser:
    def __init__(self,token):
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
            handler = self.handlers.get(token_type,self.unknown_token)
            handler(current_token)

    def var_declare(self,current_token):
        self.position+=1
        var_token = self.token[self.position]

        if var_token[1] == "IDENTIFIER":
            var_name = var_token[0]
            self.position+=1
            assign_token = self.token[self.position]

            if assign_token[1] == "ASSIGN":
                self.position+=1
                value_token = self.token[self.position]

                if value_token[1] in ("NUMBER","STRING","BOOL"):
                    value = value_token[0]
                    if value_token[1] == "STRING":
                        value = f'"{value}"'
                    self.output.append(f'{var_name} = {value}')
                    self.symbols[var_name] = value
                    self.position += 1
                else:
                    raise Exception("Invalid value type in declaration")
            else:
                raise Exception("Expected '=' after identifier")
        else:
            raise Exception("Expected identifier after 'let'")


    def assignment(self,current_token):
        var_name = current_token[0]

        if var_name in self.symbols:
            self.position+=1
            assign_token = self.token[self.position]

            if assign_token[1] == "ASSIGN":
                self.position+=1
                value_token = self.token[self.position]

                if value_token[1] in ("NUMBER","BOOL"):
                    value = value_token[0]
                elif value_token[1] == "STRING":
                    value = f'"{value_token[0]}"'
                elif value_token[1] == "IDENTIFIER":
                    if value_token[0] in self.symbols:
                        value = value_token[0]
                    else:
                        raise Exception(f"Variable '{value_token[0]}' not declared")
                else:
                    raise Exception("Unsupported value type for assignment")
                self.symbols[var_name] = value
                self.output.append(f"{var_name} = {value}")
                self.position+=1
        else:
            raise Exception(f"Variable '{var_name}' not declared")

    def print_stmt(self,current_token):
            self.position+=1
            paren_token = self.token[self.position]

            if paren_token[1] == "LPAREN":
                self.position+=1
                value_token = self.token[self.position]

                if value_token[1] in ("NUMBER","BOOL"):
                    value = value_token[0]

                elif value_token[1] == "STRING":
                    value = f'"{value_token[0]}"'

                elif value_token[1] == "IDENTIFIER":
                    if value_token[0] in self.symbols:
                        value = value_token[0]
                    else:
                        raise Exception("Error, undefined variable")
                else:
                    raise Exception("Unexpected datatype")

                self.output.append(f'print({value})')
                self.position+=1

                paren_token = self.token[self.position]
                if paren_token[1] == "RPAREN":
                    self.position+=1
                else:
                    raise Exception("Error, syntax incomplete")

    def input_stmt(self, current_token):
        var_name = current_token[0]
        self.position += 1

        if self.token[self.position][1] != "LPAREN":
            raise Exception("Expected '(' after 'in'")

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
            raise Exception("Expected 'Run'")

        self.position += 1
        next_token = self.token[self.position]

        if next_token[1] == "LPAREN":
            self.position += 1
            num_token = self.token[self.position]

            if num_token[1] != "NUMBER":
                raise Exception("Expected number inside Run(..)")

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

            cond = self.condition(self.token[self.position])
            self.position += 1

            if self.token[self.position][1] != "RPAREN":
                raise Exception("Expected ')' after while condition")
            self.position += 1

            if self.token[self.position][1] != "LBRACE":
                raise Exception("Expected '{' to start loop block")
            self.position += 1

            block_lines = self.block(current_token)
            self.output.append(f"while {cond}:")
            self.output.extend(["    " + line for line in block_lines])

        else:
            raise Exception("Expected '(' or 'while' after 'Run'")

    def block(self,current_token):
       pass

    def conditional_stmt(self,current_token):

        keyword = current_token[1]
        if keyword not in ("IF", "ELIF", "ELSE"):
            raise Exception("Expected 'agar', 'ya_fir', or 'warna'")

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
        if current_token[1] == "FUNC":
            self.position += 1
            func_name = self.token[self.position][0]
            self.position += 1

            paren_token = self.token[self.position]

            if paren_token == "LPAREN":
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

                paren_token = self.token[self.position]

                if paren_token[1] == "LBRACE":
                    block_lines = self.block(paren_token)
                    params = ",".join(parameters)
                    self.output.append(f"def {func_name}({params}):")
                    self.output.extend(["    " + line for line in block_lines])
                else:
                    raise Exception("Expected '{' to start function block")
            else:
                raise Exception("Expected '(' after function name")
        else:
            raise Exception("Expected 'func'")

    def func_call(self,current_token):
        pass

    def return_stmt(self,current_token):
        pass

    def expression(self,current_token):
        pass

    def term(self,current_token):
        pass

    def condition(self,current_token):
        pass

    def param_list(self,current_token):
        pass

    def arg_list(self,current_token):
        pass

    def unknown_token(self,current_token):
        pass

token = [('Run', 'RUN'), ('(', 'LPAREN'), ('3', 'NUMBER'), (')', 'RPAREN'), ('{', 'LBRACE'), ('out', 'OUT'), ('(', 'LPAREN'), ('Hey', 'STRING'), (')', 'RPAREN'), ('}', 'RBRACE')]

parser = Parser(token)

parser.parse()
print(parser.symbols)
print(parser.output)