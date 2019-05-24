import plex  

class ParseError (Exception):
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

    def create_scanner(self, fp):
        self.scanner = plex.Scanner(self.lexicon, fp)
        self.la, self.text = self.next_token()
    
    def next_token(self):
        return self.scanner.read()

    def parse(self, fp):
        self.create_scanner(fp)
        self.statement_list()

    def match(self, token):
        print(token)
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
            self.match('id')
            self.match('=')
            self.expression()
        elif self.la == 'print':
            self.match('print')
            self.expression()
        else:
            raise ParseError('Expected id or print in statement()')

    def expression(self):
        if self.la == '(' or self.la == 'id' or self.la == 'binary':
            self.atom()
            self.atom_tail()
        else:
            raise ParseError('Expected ( or id or binary in expression()')
    
    def atom_tail(self):
        if self.la == 'xor':
            self.match('xor')
            self.atom()
            self.atom_tail()
        elif self.la == 'id' or self.la == 'print' or self.la == None or self.la == ')':
            return
        else:
            raise ParseError('Expected xor in atom_tail()')
    
    def atom(self):
        if self.la == '(' or self.la == 'id' or self.la == 'binary':
            self.term()
            self.term_tail()
        else:
            raise ParseError('Expected ( or id or binary in term()')

    def term_tail(self):
        if self.la == 'or':
            self.match('or')
            self.term()
            self.term_tail()
        elif self.la == 'xor' or self.la == 'id' or self.la == 'print' or self.la == None or self.la == ')':
            return
        else:
            raise ParseError('Expected or in term_tail()')

    def term(self):
        if self.la == '(' or self.la == 'id' or self.la == 'binary':
            self.factor()
            self.factor_tail()
        else:
            raise ParseError('Expected ( or id or binary in term()')
    
    def factor_tail(self):
        if self.la == 'and':
            self.match('and')
            self.factor()
            self.factor_tail()
        elif self.la == 'xor' or self.la == 'or' or self.la == 'id' or self.la == 'print' or self.la == None or self.la == ')':
            return
        else:
            raise ParseError('Expected and in factor_tail()')

    def factor(self):
        if self.la == '(':
            self.match('(')
            self.expression()
            self.match(')')
        elif self.la == 'id':
            self.match('id')
        elif self.la == 'binary':
            self.match('binary')
        else:
            raise ParseError('Expected ( or id or binary in factor()')

parser = myParser()
with open('test.txt', 'r') as fp:
    parser.parse(fp)