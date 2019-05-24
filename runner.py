import plex  

class ParseError (Exception):
    pass

class RunError (Exception):
    pass

class myParser:
    def __init__(self):
        space = plex.Any(' \n\t')
        symbol_xor = plex.Str('xor')
        symbol_or = plex.Str('or')
        symbol_and = plex.Str('and')
        letter = plex.Range("azAZ")
        symbol_equals = plex.Str('=')
        symbol_leftParenthesis = plex.Str('(')
        symbol_rightParenthesis = plex.Str(')')
        digit = plex.Range('01')
        identifier = letter + plex.Rep(letter|digit)
        binary_number = plex.Rep1(digit)
        keyword_print = plex.Str('print')

        self.lexicon = plex.Lexicon([
            (symbol_leftParenthesis, '('),
            (symbol_rightParenthesis, ')'),
            (symbol_xor, 'xor'),
            (symbol_or, 'or'),
            (symbol_and, 'and'),
            (symbol_equals, '='),
            (binary_number, 'BINARY'),
            (keyword_print, 'print'),
            (identifier, 'ID'),
            (space, plex.IGNORE),
        ])
        self.st = {}

    def createScanner(self, fp):
        self.scanner = plex.Scanner(self.lexicon, fp)
        self.la, self.text = self.nextToken()
    
    def nextToken(self):
        return self.scanner.read()

    def parse(self, fp):
        self.createScanner(fp)
        self.statement_list()

    def match(self, token):
        if self.la == token:
            self.la, self.text = self.nextToken()
        else:
            raise ParseError("Expected self.la == token")

    def statement_list(self):
        if self.la == 'ID' or self.la == 'print':
            self.statement()
            self.statement_list()
        elif self.la == None:
            return
        else:
            raise ParseError('Expected ID or print in statement_list')

    def statement(self):
        if self.la == 'ID':
            varname = self.text
            self.match('ID')
            self.match('=')
            e = self.expression()
            self.st[varname] = e
        elif self.la == 'print':
            self.match('print')
            e = self.expression()
            print(e)
        else:
            raise ParseError('Expected ID or print in statement')

    def expression(self):
        if self.la == '(' or self.la == 'ID' or self.la == 'BINARY':
            t = self.term()
            while self.la == '+' or self.la == '-':
                op = self.addOperation()
                t2 = self.term()
                if op == '+':
                    t += t2
                else:
                    t -= t2
            if self.la == 'ID' or self.la == 'print' or self.la == None or self.la == ')':
                return t
            raise ParseError('Expected + or - in termination')           
        else:
            raise ParseError('Expected ( or ID or FLOAT in expression')

    def term(self):
        if self.la == '(' or self.la == 'ID' or self.la == 'FLOAT':
            f = self.factor()
            while self.la == '*' or self.la == '/':
                op = self.multiplyOperation()
                t2 = self.factor()
                if op == '*':
                    f *= t2
                else:
                    f /= t2
            if self.la == '+' or self.la == '-' or self.la == 'ID' or self.la == 'print' or self.la == None or self.la == ')':
                return f
            raise ParseError('Expected + or - in termination')
        else:
            raise ParseError('Expected ( or ID or FLOAT in termination')

    def factor(self):
        if self.la == '(':
            self.match('(')
            e = self.expression()
            self.match(')')
            return e
        elif self.la == 'ID':
            varname = self.text
            self.match('ID')
            if varname in self.st:
                return self.st[varname]
            raise RunError("lathos sto factor")
        elif self.la == 'FLOAT':
            value = float(self.text)
            self.match('FLOAT')
            return value
        else:
            raise ParseError('Expected ( or ID or FLOAT')

    def addOperation(self):
        if self.la == '+':
            self.match('+')
            return('+')
        elif self.la == '-':
            self.match('-')
            return('-')
        else:
            raise ParseError('Expected + or -')

    def multiplyOperation(self):
        if self.la == '*':
            self.match('*')
            return('*')
        elif self.la == '/':
            self.match('/')
            return('/')
        else:
            raise ParseError('Expected * or /')

parser = myParser()
with open('test.txt', 'r') as fp:
    parser.parse(fp)