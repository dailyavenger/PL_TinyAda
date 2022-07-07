#parser
import Token
import Scanner
import Chario
import sys
import SymbolTable
import SymbolEntry

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


    table = [] #
    left = set() #
    right = set() #

    bigL = []

    pTable = []
    tsTable = []



    def __init__(self):
        self.c = Chario.Chario.chario(Chario.Chario())
        self.s = Scanner.Scanner.tokenize(Scanner.Scanner(),self.c)
        self.initHandles()

        ##
        self.initTable()

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

        #
        self.left.add(SymbolEntry.SymbolEntry.PARAM)
        self.left.add(SymbolEntry.SymbolEntry.VAR)

        self.right.add(SymbolEntry.SymbolEntry.CONST)
        self.right.add(SymbolEntry.SymbolEntry.PARAM)
        self.right.add(SymbolEntry.SymbolEntry.VAR)


    #
    def acceptRole(self,s,expected,msg):

        try:

            dic = False
            for i in expected:

                if s.role == i:

                    dic = True
                    break

            if not dic:
                print("\n\n [Role Error]\n\n")
        except:
            if s.role != SymbolEntry.SymbolEntry.NONE and s.role != expected:
                print("\n\n [Role Error]\n\n")




    # table initiate
    def initTable(self):
        # construct table
        self.table = SymbolTable.SymbolTable.SymbolTable(SymbolTable.SymbolTable,self.c)
        self.table.enterScope(self.table)
        entry = self.table.enterSymbol(SymbolTable.SymbolTable,"BOOLEAN",SymbolEntry.SymbolEntry.TYPE,"BOOLEAN")
        entry = self.table.enterSymbol(SymbolTable.SymbolTable,"CHAR",SymbolEntry.SymbolEntry.TYPE,"CHAR")
        entry = self.table.enterSymbol(SymbolTable.SymbolTable,"INTEGER",SymbolEntry.SymbolEntry.TYPE,"INTEGER")
        entry = self.table.enterSymbol(SymbolTable.SymbolTable,"TRUE",SymbolEntry.SymbolEntry.CONST,"TRUE")
        entry = self.table.enterSymbol(SymbolTable.SymbolTable,"FALSE",SymbolEntry.SymbolEntry.CONST,"FALSE")



    #  ent
    def enterId(self,role,value):


        entry = SymbolEntry.SymbolEntry.SymbolEntry(SymbolEntry.SymbolEntry,"",role)

        if self.tok == Token.Token.codeToStr(Token.Token,Token.Token.ID):
            entry = self.table.enterSymbol(SymbolTable.SymbolTable, self.w,role,value)

        else:
            self.fatalError("\n\n identifier expected 1")


        self.nextToken()
        return entry


   # f i n
    def findId(self):
        entry = SymbolEntry.SymbolEntry.SymbolEntry(SymbolEntry.SymbolEntry,"",0)

        if self.tok == Token.Token.codeToStr(Token.Token,Token.Token.ID):
            entry = self.table.findSymbol(self.table,self.w)

        else:
            self.fatalError("\n\n identifier expected 2")
        self.nextToken()
        return entry



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
            print(" ",end='')
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
                print("\nChecking Finished")
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

        self.tsTable.append(self.table.exitScope(self.table))

        self.printAll()


    def printAll(self):

        if len(self.pTable) > 0:
            print("\n\n[Print Function Operated]")
            print("------------------------------------")
            for i in self.pTable:
                print(i)
            print("------------------------------------")

        if len(self.tsTable) > 0:

            for i in self.tsTable:

                print(i)



    def subprogramBody(self):
        self.subprogramSpecification()

        self.accept(Token.Token.IS, "\n\n 'is' expected")

        self.declarativePart()

        self.accept(Token.Token.BEGIN, "\n\n 'begin' expected")
        self.sequenceOfStatements()
        self.accept(Token.Token.END, "\n\n 'end' expected")

        if self.tok == Token.Token.codeToStr(Token.Token, Token.Token.ID):
            entry = self.findId()
            self.acceptRole(entry, SymbolEntry.SymbolEntry.PROC, "\n\n procedure name expected")

        self.accept(Token.Token.SEMI, "\n\n semicolon expected")
        self.tsTable.append(self.table.exitScope(self.table))


    def subprogramSpecification(self):
        self.accept(Token.Token.PROC,"\n\n 'procedure' expected")
        entry = self.enterId(SymbolEntry.SymbolEntry.PROC,self.w)
        self.table.enterScope(self.table)

        if self.tok == Token.Token.codeToStr(Token.Token,Token.Token.L_PAR):
            self.formalPart()


    def formalPart(self):
        self.accept(Token.Token.L_PAR, "\n\n '(' expected")
        self.parameterSpecification()
        while Token.Token.s2c(Token.Token,self.tok) == Token.Token.SEMI:
            self.nextToken()
            self.parameterSpecification()
        self.accept(Token.Token.R_PAR, "\n\n ')' expected")


    def parameterSpecification(self):
        list = self.identifierList() 
        
        for t in list:
            t[1] = SymbolEntry.SymbolEntry.PARAM
            for k in self.table.table:
                if t[0] == k[0]:
                    k[2] = t[1]

        self.accept(Token.Token.COLON, "\n\n ':' expected")
        if (self.tok == Token.Token.codeToStr(Token.Token,Token.Token.IN)):
            self.accept(Token.Token.IN, "\n\n 'in' identifier expected")
        if (self.tok == Token.Token.codeToStr(Token.Token,Token.Token.OUT)):
            self.accept(Token.Token.OUT, "\n\n 'out' identifier expected")

        entry = self.findId()
        self.acceptRole(entry,SymbolEntry.SymbolEntry.TYPE,"\n\n type name expected")


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
            self.fatalError("\n\n error in declaration part")


    def numberOrObjectDeclaration(self):
        list = self.identifierList()
        self.accept(Token.Token.COLON, "\n\n ':' expected")

        if (self.tok == Token.Token.codeToStr(Token.Token,Token.Token.CONST)):
            for t in list:
                t[1] = SymbolEntry.SymbolEntry.CONST
                for k in self.table.table:

                    if t[0] == k[0]:
                        k[2] = t[1]

            self.nextToken()
            self.accept(Token.Token.GETS, "\n\n ':=' expected")
            ret = self.expression()

            if len(list) == 1:
                list[0][2] = ret
                for k in self.table.table:

                    if list[0][0] == k[0]:
                        k[3] = list[0][2]

        else:
            for t in list:
                t[1] = SymbolEntry.SymbolEntry.VAR
                for k in self.table.table:
                    if t[0] == k[0]:
                        k[2] = t[1]

            self.typeDefinition()
        self.accept(Token.Token.SEMI, "\n\n semicolon expected")


    def typeDeclaration(self):
        self.accept(Token.Token.TYPE, "\n\n 'type' expected")

        entry = self.enterId(SymbolEntry.SymbolEntry.TYPE,self.w)

        self.accept(Token.Token.IS, "\n\n 'is' expected")
        self.typeDefinition()
        self.accept(Token.Token.SEMI, "\n\n semicolon expected")


    def typeDefinition(self):

        if self.tok == Token.Token.codeToStr(Token.Token,Token.Token.ARRAY):
            self.arrayTypeDefinition()
        elif self.tok == Token.Token.codeToStr(Token.Token,Token.Token.L_PAR):
            self.enumerationTypeDefinition()
        elif self.tok == Token.Token.codeToStr(Token.Token,Token.Token.RANGE):
            self.range()
        elif self.tok == Token.Token.codeToStr(Token.Token,Token.Token.ID):
            entry = self.findId()
            self.acceptRole(entry,SymbolEntry.SymbolEntry.TYPE,"\n\n type name expected")
        else:
            self.fatalError("\n\n error in type definition")


    def enumerationTypeDefinition(self):
        self.accept(Token.Token.L_PAR, "\n\n '(' expected")
        list = self.identifierList()
        for t in list:
            t[1] = SymbolEntry.SymbolEntry.CONST

            for k in self.table.table:
                if t[0] == k[0]:
                    k[2] = t[1]

        self.accept(Token.Token.R_PAR, "\n\n ')' expected")


    def arrayTypeDefinition(self):
        self.accept(Token.Token.ARRAY, "\n\n 'array' expected")
        self.accept(Token.Token.L_PAR, "\n\n '(' expected")
        self.index()
        while (Token.Token.s2c(Token.Token,self.tok) == Token.Token.COMMA):
            self.nextToken()
            self.index()

        self.accept(Token.Token.R_PAR, "\n\n ')' expected")
        self.accept(Token.Token.OF, "\n\n 'of' expected")
        entry = self.findId()
        self.acceptRole(entry,SymbolEntry.SymbolEntry.TYPE,"\n\n type name expected")


    def index(self):

        if (Token.Token.s2c(Token.Token,self.tok) == Token.Token.RANGE):
            self.range()
        elif (Token.Token.s2c(Token.Token,self.tok) == Token.Token.ID):
            entry = self.findId()
            self.acceptRole(entry,SymbolEntry.SymbolEntry.TYPE,"\n\n type name expected")
        else:
            self.fatalError("\n\n error in index type")


    def range(self):
        self.accept(Token.Token.RANGE, "\n\n 'range' expected")
        self.expression()
        self.accept(Token.Token.THRU, "\n\n '..' expected")
        self.expression()


    def identifierList(self):
        self.bigL = [[self.w, 0,0]]
        list = self.enterId(0,0)
        while (self.tok == Token.Token.codeToStr(Token.Token,Token.Token.COMMA)):
            self.nextToken()
            self.bigL.append([self.w, 0,0])

            list.append(SymbolEntry.SymbolEntry,self.enterId(0,0))
        return self.bigL


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
            self.fatalError("\n\n error in statement")


    def nullStatement(self):
        self.accept(Token.Token.NULL, "\n\n 'null' expected")
        self.accept(Token.Token.SEMI, "\n\n semicolon expected")


    def loopStatement(self):
        if (Token.Token.s2c(Token.Token,self.tok) == Token.Token.WHILE):
            self.nextToken()
            self.condition()

        self.accept(Token.Token.LOOP, "\n\n 'loop' expected")
        self.sequenceOfStatements()
        self.accept(Token.Token.END, "\n\n 'end' expected")
        self.accept(Token.Token.LOOP, "\n\n 'loop' expected")
        self.accept(Token.Token.SEMI, "\n\n semicolon expected")


    def ifStatement(self):
        self.accept(Token.Token.IF, "\n\n 'if' expected")
        self.condition()
        self.accept(Token.Token.THEN, "\n\n 'then' expected")

        self.sequenceOfStatements()
        while (self.tok == Token.Token.ELSIF):
            self.nextToken()
            self.condition()
            self.accept(Token.Token.THEN, "\n\n 'then' expected")
            self.sequenceOfStatements()

        if (self.tok == Token.Token.ELSE):
            self.nextToken()
            self.sequenceOfStatements()

        self.accept(Token.Token.END, "\n\n 'end' expected")

        self.accept(Token.Token.IF, "\n\n 'if' expected")

        self.accept(Token.Token.SEMI, "\n\n semicolon expected")



    def exitStatement(self):
        self.accept(Token.Token.EXIT, "\n\n 'exit' expected")
        if (self.tok == Token.Token.WHEN):
            self.nextToken()
            self.condition()
        self.accept(Token.Token.SEMI, "\n\n semicolon expected")


    def assignmentOrCallStatement(self):
        if self.w == "print":
            self.Print()
            entry = SymbolEntry.SymbolEntry.SymbolEntry(SymbolEntry.SymbolEntry,"print",3)
            self.acceptRole(entry, SymbolEntry.SymbolEntry.PROC, "\n\n print procedure expected")
        else:
            entry = self.name()
            if (Token.Token.s2c(Token.Token, self.tok) == Token.Token.GETS):

                self.acceptRole(entry, self.left, "\n\n variable or parameter name expected")
                self.nextToken()
                ret = self.expression()

                for i in self.table.table:
                    if entry.name == i[0]:
                        i[3] = ret
            else:
                self.acceptRole(entry, SymbolEntry.SymbolEntry.PROC, "\n\n procedure expected")

        self.accept(Token.Token.SEMI, "\n\n semicolon expected")

    def Print(self):
        self.nextToken()

        if (Token.Token.s2c(Token.Token, self.tok) == Token.Token.L_PAR):
            self.nextToken()

            if Token.Token.s2c(Token.Token, self.tok) == Token.Token.INT or Token.Token.s2c(Token.Token,self.tok) == Token.Token.CHAR:
                self.pTable.append(self.w)
                self.nextToken()

            elif Token.Token.s2c(Token.Token, self.tok) == Token.Token.ID:

                exist = False

                for k in self.table.table:

                    if self.w == k[0]:
                        exist = True
                        self.pTable.append(k[3])
                        break

                if not exist:
                    print("\nID not exist")

                self.nextToken()
        else:
            print("\n\n '(' expected")
            self.nextToken()
        self.accept(Token.Token.R_PAR,"\n\n ')' expected")


    def condition(self):
        self.expression()


    def expression(self):
        ret = self.relation()
        if (Token.Token.s2c(Token.Token,self.tok) == Token.Token.AND):
            while (Token.Token.s2c(Token.Token,self.tok) == Token.Token.AND):
                self.nextToken()
                ret2 = self.relation()
                ret = (ret and ret2)
        elif (Token.Token.s2c(Token.Token,self.tok) == Token.Token.OR):
            while (Token.Token.s2c(Token.Token,self.tok) == Token.Token.OR):
                self.tok = self.s.nextToken()
                ret3 = self.relation()
                ret = (ret or ret3)
        return ret


    def relation(self):
        ret = self.simpleExpression()
        while Token.Token.s2c(Token.Token,self.tok) in self.relOp:
            op = self.w
            self.nextToken()
            ret2 = self.simpleExpression()

            if op =='<':
                ret = ret < ret2
            elif op == '<=':
                ret = ret <= ret2
            elif op == '>':
                ret = ret > ret2
            elif op == '>=':
                ret = ret >= ret2
            elif op == '=':
                ret = (ret == ret2)
            elif op == '/=':
                ret = (ret != ret2)

        return ret


    def simpleExpression(self):
        first = ""
        second = ""
        if Token.Token.s2c(Token.Token,self.tok) in self.addOp:
            first = self.w
            self.nextToken()
        ret = self.term()
        if first == '-':
            ret = -ret
        while Token.Token.s2c(Token.Token,self.tok) in self.addOp:
            second = self.w
            self.nextToken()
            ret2 = self.term()
        if second == '+':
            ret = ret + ret2
        elif second == '-':
            ret = ret - ret2
        return ret


    def term(self):
        ret = self.factor()
        while Token.Token.s2c(Token.Token,self.tok) in self.mulOp:

            op = self.w
            self.nextToken()
            ret2 = self.factor()

            if op == '*' :
                ret = ret * ret2
            elif op == '/' and ret2!=0:
                ret = ret / ret2
            else:
                ret = ret % ret2

        return ret



    def factor(self):
        ret = 0
        if (Token.Token.s2c(Token.Token,self.tok) == Token.Token.NOT):

            self.nextToken()
            ret = self.primary()

            if ret.isdigit():
                ret = - ret

        else:
            ret = self.primary()
            tmp = ret
            if not tmp.isdigit():
                for i in self.table.table:
                    if ret == i[0]:
                        ret = i[3]

            if (Token.Token.s2c(Token.Token,self.tok) == Token.Token.EXPO):
                self.nextToken()
                ret2 = self.primary()
                if not ret2.isdigit():
                    for i in self.table.table:
                        if ret2 == i[0]:
                            ret2 = i[3]
                tmp2 = ret
                for i in range(ret2-1):
                    ret = tmp2*ret

        return ret


    def primary(self):
        ret = self.w
        if Token.Token.s2c(Token.Token,self.tok) == Token.Token.INT or Token.Token.s2c(Token.Token,self.tok) == Token.Token.CHAR:
            self.nextToken()

        elif Token.Token.s2c(Token.Token,self.tok) == Token.Token.ID:
            entry = self.name()

            self.acceptRole(entry,self.right,"\n\n var,param, const name expected")

        elif Token.Token.s2c(Token.Token,self.tok) == Token.Token.L_PAR:
            self.nextToken()
            self.expression()
            self.accept(Token.Token.R_PAR, "\n\n ')' expected")
        else:
            self.fatalError("\n\n error in primary")

        return ret


    def name(self):
        entry = self.findId()
        tmpRole = entry.role
        tmpName = entry.name

        if (Token.Token.s2c(Token.Token,self.tok) == Token.Token.L_PAR):
            self.indexedComponent()

        entry.role = tmpRole
        entry.name = tmpName

        return entry


    def indexedComponent(self):
        self.nextToken()
        self.expression()
        while (Token.Token.s2c(Token.Token,self.tok) == Token.Token.COMMA):
            self.nextToken()
            self.expression()
        self.accept(Token.Token.R_PAR, "\n\n ')' expected")
