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
            (binary_number, 'binary'),
            (keyword_print, 'print'),
            (identifier, 'id'),
            (space, plex.IGNORE),
        ])
        self.st = {}

    def create_scanner(self, fp):
        self.scanner = plex.Scanner(self.lexicon, fp)
        self.la, self.text = self.next_token()
    
    def next_token(self):
        return self.scanner.read()

    def parse(self, fp):
        self.create_scanner(fp)
        self.statement_list()

    def match(self, token):
        #print(token)
        if self.la == token:
            self.la, self.text = self.next_token()
        else:
            raise ParseError("Expected self.la == token in match()")

    def statement_list(self):
        if self.la == 'id' or self.la == 'print':
            self.statement()
            self.statement_list()
        elif self.la == None:
            return
        else:
            raise ParseError('Expected id or print in statement_list()')

    def statement(self):
        if self.la == 'id':
            varname = self.text
            self.match('id')
            self.match('=')
            e = self.expression()
            self.st[varname] = e
        elif self.la == 'print':
            self.match('print')
            e = self.expression()
            print('{:08b}'.format(e))
        else:
            raise ParseError('Expected id or print in statement()')

    def expression(self):
        if self.la == '(' or self.la == 'id' or self.la == 'binary':
            a = self.atom()
            while self.la == 'xor':
                self.match('xor')
                a ^= self.atom()
            if self.la == 'id' or self.la == 'print' or self.la == None or self.la == ')':
                return a
            raise ParseError('Expected xor in atom()')
        else:
            raise ParseError('Expected ( or id or binary in expression()')
   
    def atom(self):
        if self.la == '(' or self.la == 'id' or self.la == 'binary':
            t = self.term()
            while self.la == 'or':
                self.match('or')
                t |= self.term()
            if self.la == 'xor' or self.la == 'id' or self.la == 'print' or self.la == None or self.la == ')':
                return t
            raise ParseError('Expected or in atom()')
        else:
            raise ParseError('Expected ( or id or binary in atom()')

    def term(self):
        if self.la == '(' or self.la == 'id' or self.la == 'binary':
            f = self.factor()
            while self.la == 'and':
                self.match('and')
                f &= self.factor()
            if self.la == 'xor' or self.la == 'or' or self.la == 'id' or self.la == 'print' or self.la == None or self.la == ')':
                return f
            raise ParseError('Expected and in term()')
        else:
            raise ParseError('Expected ( or id or binary in term()')

    def factor(self):
        if self.la == '(':
            self.match('(')
            e = self.expression()
            self.match(')')
            return e
        elif self.la == 'id':
            varname = self.text
            self.match('id')
            if varname in self.st:
                return self.st[varname]
            raise RunError("lathos sto factor")
        elif self.la == 'binary':
            value = int(self.text, 2)
            self.match('binary')
            return value
        else:
            raise ParseError('Expected ( or id or binary in factor()')

parser = myParser()
with open('test.txt', 'r') as fp:
    parser.parse(fp)