#token

class Token:

    AND = 0
    ARRAY = 1
    BEGIN = 2
    CHAR = 3
    COLON = 4
    COMMA = 5
    CONST = 6
    DIV = 7
    ELSE = 8
    ELSIF = 9
    END = 10
    EOF = 11
    EQ = 12
    ERROR = 13
    EXIT = 14
    EXPO = 15
    GE = 16
    GETS = 17
    GT = 18
    ID = 19
    IF = 20
    IN = 21
    INT = 22
    IS = 23
    LE = 24
    LT = 25
    LOOP = 26
    L_PAR = 27
    MINUS = 28
    MOD = 29
    MUL = 30
    NE = 31
    NOT = 32
    NULL = 33
    OF = 34
    OR = 35
    OUT = 36
    PLUS = 37
    PROC = 38
    R_PAR = 39
    RANGE = 40
    SEMI = 41
    THEN = 42
    THRU = 43
    TYPE = 44
    WHEN = 45
    WHILE = 46
    PERIOD = 47
    RECORD = 48

    code = 0
    integer = 0
    string = ""

    CODES = ["AND", "ARRAY", "BEGIN", "CHAR", "COLON", "COMMA", "CONST", "DIV", "ELSE", "ELSIF",
             "END", "EOF", "EQ", "ERROR", "EXIT", "EXPO", "GE", "GETS", "GT", "ID", "IF", "IN",
             "INT", "IS", "LE", "LT", "LOOP", "L_PAR", "MINUS", "MOD", "MUL", "NE", "NOT", "NULL",
             "OF", "OR", "OUT", "PLUS", "PROC", "R_PAR", "RANGE", "SEMI",
             "THEN", "THRU", "TYPE", "WHEN", "WHILE" , "PERIOD", "RECORD"]

    def codeToStr(self,code):
        return self.CODES[code]

    def s2c(self,string):
        code = 11
        index = 0
        for i in self.CODES:
            if i == string:
                code = index
            index = index + 1

        return code
