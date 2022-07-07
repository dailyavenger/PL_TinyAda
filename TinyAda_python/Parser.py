#parser
import Token
import Scanner
import Chario
import sys

class Parser:

    c = Chario.Chario()
    s = []
    s_index = 0
    tok = ""
    word = []
    w_index = 0
    w = ""
    addOp = set()
    mulOp = set()
    relOp = set()
    dec = set()
    stmt = set()

    def __init__(self):
        self.c = Chario.Chario.chario(Chario.Chario())
        self.s = Scanner.Scanner.tokenize(Scanner.Scanner(),self.c)
        self.initHandles()
        self.tok = self.s[self.s_index]
        self.word = Scanner.Scanner.wordRet(Scanner.Scanner(),self.c)
        self.w = self.word[self.w_index]


    def initHandles(self):
        self.addOp.add(Token.Token.PLUS)
        self.addOp.add(Token.Token.MINUS)

        self.mulOp.add(Token.Token.MUL)
        self.mulOp.add(Token.Token.DIV)
        self.mulOp.add(Token.Token.MOD)

        self.relOp.add(Token.Token.EQ)
        self.relOp.add(Token.Token.NE)
        self.relOp.add(Token.Token.LE)
        self.relOp.add(Token.Token.GE)
        self.relOp.add(Token.Token.LT)
        self.relOp.add(Token.Token.GT)

        self.dec.add(Token.Token.TYPE)
        self.dec.add(Token.Token.ID)
        self.dec.add(Token.Token.PROC)

        self.stmt.add(Token.Token.EXIT)
        self.stmt.add(Token.Token.ID)
        self.stmt.add(Token.Token.IF)
        self.stmt.add(Token.Token.LOOP)
        self.stmt.add(Token.Token.NULL)
        self.stmt.add(Token.Token.WHILE)


    def accept(self,expected,msg):
        if self.tok != Token.Token.codeToStr(Token.Token,expected):
            self.fatalError(msg)
        self.nextToken()


    def fatalError(self,msg):
        print(msg)
        sys.exit()
        raise Exception("Fatal error")


    def nextToken(self):
        if (self.w == ''):
            print("\nNo errors reported.")
        else:
            print(self.w, end='')
        self.s_index = self.s_index + 1
        if len(self.s) <= self.s_index:
            self.tok = Token.Token.codeToStr(Token.Token, Token.Token.EOF)
        else:
            self.tok = self.s[self.s_index]

        self.w_index = self.w_index + 1

        if len(self.word) <= self.w_index:
            self.w = ''
        else:
            self.w = self.word[self.w_index]

        while (self.tok == 'WHITESPACE' or self.tok == 'NEWLINE'):
            if(self.w==''):
                print("\nNo errors reported.")
            else:
                print(self.w,end='')
            self.s_index = self.s_index + 1
            if len(self.s) <= self.s_index:
                self.tok = Token.Token.codeToStr(Token.Token, Token.Token.EOF)
            else:
                self.tok = self.s[self.s_index]
            self.w_index = self.w_index + 1
            if len(self.word) <= self.w_index:
                self.w = ''
            else:
                self.w = self.word[self.w_index]


    def parse(self):
        self.subprogramBody()
        self.accept(Token.Token.EOF,"extra symbols after logical end of program")


    def subprogramBody(self):
        self.subprogramSpecification()
        self.accept(Token.Token.IS, "'is' expected")
        self.declarativePart()
        self.accept(Token.Token.BEGIN, "'begin' expected")
        self.sequenceOfStatements()
        self.accept(Token.Token.END, "'end' expected")
        if self.tok == Token.Token.codeToStr(Token.Token, Token.Token.ID):
            self.nextToken()
        self.accept(Token.Token.SEMI, "semicolon expected")


    def subprogramSpecification(self):
        self.accept(Token.Token.PROC,"'procedure' expected")
        self.accept(Token.Token.ID, "identifier expected")
        if self.tok == Token.Token.codeToStr(Token.Token,Token.Token.L_PAR):
            self.formalPart()


    def formalPart(self):
        self.accept(Token.Token.L_PAR, "'(' expected")
        self.parameterSpecification()
        while Token.Token.s2c(Token.Token,self.tok) == Token.Token.SEMI:
            self.nextToken()
            self.parameterSpecification()
        self.accept(Token.Token.R_PAR, "')' expected")


    def parameterSpecification(self):
        self.identifierList()
        self.accept(Token.Token.COLON, "':' expected")
        if (self.tok == Token.Token.codeToStr(Token.Token,Token.Token.IN)):
            self.accept(Token.Token.IN, "'in' identifier expected")
        if (self.tok == Token.Token.codeToStr(Token.Token,Token.Token.OUT)):
            self.accept(Token.Token.OUT, "'out' identifier expected")
        self.accept(Token.Token.ID, "identifier expected")


    def declarativePart(self):
        while Token.Token.s2c(Token.Token,self.tok) in self.dec:
            self.basicDeclaration()


    def basicDeclaration(self):
        if self.tok ==  Token.Token.codeToStr(Token.Token,Token.Token.ID) :
            self.numberOrObjectDeclaration()
        elif self.tok == Token.Token.codeToStr(Token.Token,Token.Token.TYPE):
            self.typeDeclaration()
        elif self.tok == Token.Token.codeToStr(Token.Token,Token.Token.PROC):
            self.subprogramBody()
        else:
            self.fatalError("error in declaration part")


    def numberOrObjectDeclaration(self):
        self.identifierList()
        self.accept(Token.Token.COLON, "':' expected")
        if (self.tok == Token.Token.codeToStr(Token.Token,Token.Token.CONST)):
            self.nextToken()
            self.accept(Token.Token.GETS, "':=' expected")
            self.expression()

        else:
            self.typeDefinition()
        self.accept(Token.Token.SEMI, "semicolon expected")


    def typeDeclaration(self):
        self.accept(Token.Token.TYPE, "'type' expected")
        self.accept(Token.Token.ID, "identifier expected")
        self.accept(Token.Token.IS, "'is' expected")
        self.typeDefinition()
        self.accept(Token.Token.SEMI, "semicolon expected")


    def typeDefinition(self):

        if self.tok == Token.Token.codeToStr(Token.Token,Token.Token.ARRAY):
            self.arrayTypeDefinition()
        elif self.tok == Token.Token.codeToStr(Token.Token,Token.Token.L_PAR):
            self.enumerationTypeDefinition()
        elif self.tok == Token.Token.codeToStr(Token.Token,Token.Token.RANGE):
            self.range()
        elif self.tok == Token.Token.codeToStr(Token.Token,Token.Token.ID):
            self.accept(Token.Token.ID, "identifier expected")
        else:
            self.fatalError("error in type definition")


    def enumerationTypeDefinition(self):
        self.accept(Token.Token.L_PAR, "'(' expected")
        self.identifierList()
        self.accept(Token.Token.R_PAR, "')' expected")


    def arrayTypeDefinition(self):
        self.accept(Token.Token.ARRAY, "'array' expected")
        self.accept(Token.Token.L_PAR, "'(' expected")
        self.index()
        while (Token.Token.s2c(Token.Token,self.tok) == Token.Token.COMMA):
            self.nextToken()
            self.index()
        self.accept(Token.Token.R_PAR, "')' expected")
        self.accept(Token.Token.OF, "'of' expected")
        self.accept(Token.Token.ID, "identifier expected")


    def index(self):
        if (Token.Token.s2c(Token.Token,self.tok) == Token.Token.RANGE):
            self.range()
        elif (Token.Token.s2c(Token.Token,self.tok) == Token.Token.ID):
            self.nextToken()
        else:
            self.fatalError("error in index type")


    def range(self):
        self.accept(Token.Token.RANGE, "'range' expected")
        self.expression()
        self.accept(Token.Token.THRU, "'..' expected")
        self.expression()


    def identifierList(self):
        self.accept(Token.Token.ID, "identifier expected")
        while (self.tok == Token.Token.codeToStr(Token.Token,Token.Token.COMMA)):
            self.nextToken()
            self.accept(Token.Token.ID, "identifier expected")


    def sequenceOfStatements(self):
        self.statement()
        while (Token.Token.s2c(Token.Token,self.tok) in self.stmt):
            self.statement()


    def statement(self):
        if Token.Token.s2c(Token.Token,self.tok) == Token.Token.ID:
            self.assignmentOrCallStatement()
        elif Token.Token.s2c(Token.Token,self.tok) == Token.Token.EXIT:
            self.exitStatement()
        elif Token.Token.s2c(Token.Token,self.tok) == Token.Token.IF:
            self.ifStatement()
        elif Token.Token.s2c(Token.Token,self.tok) == Token.Token.NULL:
            self.nullStatement()
        elif Token.Token.s2c(Token.Token,self.tok) == Token.Token.WHILE or Token.Token.s2c(Token.Token,self.tok) == Token.Token.LOOP:
            self.loopStatement()
        else:
            self.fatalError("error in statement")


    def nullStatement(self):
        self.accept(Token.Token.NULL, "'null' expected")
        self.accept(Token.Token.SEMI, "semicolon expected")


    def loopStatement(self):
        if (Token.Token.s2c(Token.Token,self.tok) == Token.Token.WHILE):
            self.nextToken()
            self.condition()

        self.accept(Token.Token.LOOP, "'loop' expected")
        self.sequenceOfStatements()
        self.accept(Token.Token.END, "'end' expected")
        self.accept(Token.Token.LOOP, "'loop' expected")
        self.accept(Token.Token.SEMI, "semicolon expected")


    def ifStatement(self):
        self.accept(Token.Token.IF, "'if' expected")
        self.condition()
        self.accept(Token.Token.THEN, "'then' expected")
        self.sequenceOfStatements()
        while (self.tok == Token.Token.ELSIF):
            self.nextToken()
            self.condition()
            self.accept(Token.Token.THEN, "'then' expected")
            self.sequenceOfStatements()

        if (self.tok == Token.Token.ELSE):
            self.nextToken()
            self.sequenceOfStatements()

        self.accept(Token.Token.END, "'end' expected")
        self.accept(Token.Token.IF, "'if' expected")
        self.accept(Token.Token.SEMI, "semicolon expected")


    def exitStatement(self):
        self.accept(Token.Token.EXIT, "'exit' expected")
        if (self.tok == Token.Token.WHEN):
            self.nextToken()
            self.condition()
        self.accept(Token.Token.SEMI, "semicolon expected")


    def assignmentOrCallStatement(self):
        self.name()
        if (Token.Token.s2c(Token.Token,self.tok) == Token.Token.GETS):
            self.nextToken()
            self.expression()

        self.accept(Token.Token.SEMI, "semicolon expected")


    def condition(self):
        self.expression()


    def expression(self):
        self.relation()
        if (Token.Token.s2c(Token.Token,self.tok) == Token.Token.AND):
            while (Token.Token.s2c(Token.Token,self.tok) == Token.Token.AND):
                self.nextToken()
                self.relation()

        elif (Token.Token.s2c(Token.Token,self.tok) == Token.Token.OR):
            while (Token.Token.s2c(Token.Token,self.tok) == Token.Token.OR):
                self.tok = self.s.nextToken()
                self.relation()


    def relation(self):
        self.simpleExpression()
        while Token.Token.s2c(Token.Token,self.tok) in self.relOp:
            self.nextToken()
            self.simpleExpression()


    def simpleExpression(self):
        if Token.Token.s2c(Token.Token,self.tok) in self.addOp:
            self.nextToken()
        self.term()
        while Token.Token.s2c(Token.Token,self.tok) in self.addOp:
            self.nextToken()
            self.term()


    def term(self):
        self.factor()
        while Token.Token.s2c(Token.Token,self.tok) in self.mulOp:
            self.nextToken()
            self.factor()


    def factor(self):
        if (Token.Token.s2c(Token.Token,self.tok) == Token.Token.NOT):
            self.nextToken()
            self.primary()
        else:
            self.primary()
            if (Token.Token.s2c(Token.Token,self.tok) == Token.Token.EXPO):
                self.nextToken()
                self.primary()


    def primary(self):
        if Token.Token.s2c(Token.Token,self.tok) == Token.Token.INT or Token.Token.s2c(Token.Token,self.tok) == Token.Token.CHAR:
            self.nextToken()
        elif Token.Token.s2c(Token.Token,self.tok) == Token.Token.ID:
            self.name()
        elif Token.Token.s2c(Token.Token,self.tok) == Token.Token.L_PAR:
            self.nextToken()
            self.expression()
            self.accept(Token.Token.R_PAR, "')' expected")
        else:
            self.fatalError("error in primary")


    def name(self):
        self.accept(Token.Token.ID, "identifier expected")
        if (Token.Token.s2c(Token.Token,self.tok) == Token.Token.L_PAR):
            self.indexedComponent()


    def indexedComponent(self):
        self.nextToken()
        self.expression()
        while (Token.Token.s2c(Token.Token,self.tok) == Token.Token.COMMA):
            self.nextToken()
            self.expression()
        self.accept(Token.Token.R_PAR, "')' expected")
