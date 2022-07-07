#scanner
import re
import Chario
import Token

class Scanner:
    REGEX = [
        ('NEWLINE', r'\n'),
        ('WHITESPACE', r'\s+'),
        ('THRU', r'[\.][\.]'),
        ('EXPO', r'[\*][\*]'),
        ('AND', r'and'),
        ('OR', r'or'),
        ('GETS', r':='),
        ('COLON', r':'),
        ('COMMA', r','),
        ('PERIOD',r'[\.]'),
        ('GE', r'>='),
        ('GT', r'>'),
        ('LE', r'<='),
        ('LT', r'<'),
        ('NE', r'/='),
        ('EQ', r'='),
        ('PLUS', r'\+'),
        ('MINUS', r'\-'),
        ('DIV', r'\/'),
        ('MUL', r'\*'),
        ('L_PAR', r'\('),
        ('R_PAR', r'\)'),
        ('LBRACK', r'\['),
        ('RBRACK', r'\]'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('IS',r'is'),
        ('IN', r'\bin\b'),
        ('OUT', r'out'),
        ('NOT', r'not'),
        ('OF', r'of'),
        ('ELSIF', r'elsif'),
        ('ELSE', r'else'),
        ('THEN', r'then'),
        ('MOD', r'mod'),
        ('LOOP', r'loop'),
        ('TYPE', r'type'),
        ('WHILE', r'while'),
        ('BEGIN', r'begin'),
        ('END', r'end'),
        ('PROC', r'procedure'),
        ('ARRAY', r'array'),
        ('CONST', r'constant'),
        ('NULL', r'null'),
        ('RANGE', r'range'),
        ('EXIT', r'exit'),
        ('SEMI', r';'),
        ('WHEN', r'when'),
        ('INT', r'[0-9]+'),
        ('CHAR', r'\'[a-zA-Z_]\w*\''),
        ('ID', r'[A-Za-z][A-Za-z0-9_]*')
    ]

    regs = ['(%s)' % reg for token, reg in REGEX]

    p = re.compile('|'.join(regs))
    tokenList = []
    wordList = []
    index = 0

    def tokenize(self, s):
        loc = 0
        match = self.p.match(s, loc)
        while match:
            token = match.groups()
            loc = match.end()

            for num in range(len(token)):
                if token[num] != None:
                    self.tokenList.append(self.REGEX[num][0])
                    break

            match = self.p.match(s, loc)
        return self.tokenList


    def wordRet(self,s):
        loc = 0
        match = self.p.match(s, loc)
        while match:
            token = match.groups()
            loc = match.end()

            for num in range(len(token)):
                if token[num] != None:
                    self.wordList.append(token[num])
                    break

            match = self.p.match(s, loc)
        return self.wordList


    def selectToken(self):
        return self.tokenList[self.index]


    def nextToken(self):
        index = index + 1
        return self.tokenList[self.index]