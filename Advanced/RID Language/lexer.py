KEYWORDS = {
    "Let": "LET",
    "out": "OUT",
    "in": "IN",
    "Run": "RUN",
    "while": "WHILE",
    "agar": "IF",
    "ya_fir": "ELIF",
    "warna": "ELSE",
    "func": "FUNC",
    "give": "RETURN",
    "True": "BOOL",
    "False": "BOOL"
}

OPERATORS = {
    "=": "ASSIGN",
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULT",
    "/": "DIV",
    "%": "MOD",
    "==": "EQ",
    "!=": "NEQ",
    "<": "LT",
    ">": "GT",
    "<=": "LTE",
    ">=": "GTE"
}

DELIMITERS = {
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE"
}

TOKEN_TYPES = [
    "IDENTIFIER",   # variable or function names
    "NUMBER",       # integer or float
    "STRING"        # text inside quotes
]





def get_keyword_token(word):
    return KEYWORDS.get(word, "IDENTIFIER")

def lex(words):
    position = 0
    tokens = []

    while position < len(words):
        char = words[position]

        if char.isspace():
            position+=1

        elif char in DELIMITERS:
            tokens.append((char,DELIMITERS[char]))
            position+=1

        elif char in OPERATORS:
            if position+1<len(words) and (char + words[position+1]) in OPERATORS:
                tokens.append((char + words[position+1],OPERATORS[char + words[position+1]]))
                position+=2
            else:
                tokens.append((char,OPERATORS[char]))
                position+=1

        elif char.isalpha():
            current = ""
            while position < len(words) and (words[position].isalpha() or words[position] == "_"):
                current+=words[position]
                position+=1

            if current in KEYWORDS:
                tokens.append((current,KEYWORDS[current]))
            else:
                tokens.append((current,"IDENTIFIER"))

        elif char == '"':
            position+=1
            current = ""
            while position < len(words) and words[position] != '"':
                current+=words[position]
                position+=1
            position+=1
            tokens.append((current,"STRING"))

        elif char.isdigit():
            current = ""
            dot_count = 0
            while position < len(words) and (words[position].isdigit() or words[position] == "."):
                if words[position] == ".":
                    dot_count+=1
                    if dot_count > 1:
                        break
                current+=words[position]
                position+=1
            tokens.append((current,"NUMBER"))

        elif char == "~":
            position+=1
            while position<len(words) and words[position]!="~":
                position+=1
            position+=1

        else:
            position+=1

    return tokens

