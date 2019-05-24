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
            (binary_number, 'BINARY'),
            (keyword_print, 'print'),
            (identifier, 'ID'),
            (space, plex.IGNORE),
        ])

    def createScanner(self, fp):
        self.scanner = plex.Scanner(self.lexicon, fp)
        self.la, self.text = self.nextToken()
    
    def nextToken(self):
        return self.scanner.read()

    def parse(self, fp):
        self.createScanner(fp)
        self.statement_list()

    def match(self, token):
        print(token)
        if self.la == token:
            self.la, self.text = self.nextToken()
        else:
            raise ParseError("Expected ''")

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
            self.match('ID')
            self.match('=')
            self.expression()
        elif self.la == 'print':
            self.match('print')
            self.expression()
        else:
            raise ParseError('Expected ID or print in statement')

    def expression(self):
        if self.la == '(' or self.la == 'ID' or self.la == 'BINARY':
            self.atom()
            self.atom_tail()
        else:
            raise ParseError('Expected ( or ID or BINARY in expression')
    
    def atom_tail(self):
        if self.la == 'xor':
            self.xor_operation()
            self.atom()
            self.atom_tail()
        elif self.la == 'ID' or self.la == 'print' or self.la == None or self.la == ')':
            return
        else:
            raise ParseError('Expected xor in atom_tail')
    
    def atom(self):
        if self.la == '(' or self.la == 'ID' or self.la == 'BINARY':
            self.term()
            self.term_tail()
        else:
            raise ParseError('Expected ( or ID or NUMBER in termination')

    def term_tail(self):
        if self.la == 'or':
            self.or_operation()
            self.term()
            self.term_tail()
        elif self.la == 'xor' or self.la == 'ID' or self.la == 'print' or self.la == None or self.la == ')':
            return
        else:
            raise ParseError('Expected or in term_tail')

    def term(self):
        if self.la == '(' or self.la == 'ID' or self.la == 'BINARY':
            self.factor()
            self.factor_tail()
        else:
            raise ParseError('Expected ( or ID or BINARY in termination')
    
    def factor_tail(self):
        if self.la == 'and':
            self.and_operation()
            self.factor()
            self.factor_tail()
        elif self.la == 'xor' or self.la == 'or' or self.la == 'ID' or self.la == 'print' or self.la == None or self.la == ')':
            return
        else:
            raise ParseError('Expected and factor_tail')

    def factor(self):
        if self.la == '(':
            self.match('(')
            self.expression()
            self.match(')')
        elif self.la == 'ID':
            self.match('ID')
        elif self.la == 'BINARY':
            self.match('BINARY')
        else:
            raise ParseError('Expected ( or ID or BINARY')

    def xor_operation(self):
        if self.la == 'xor':
            self.match('xor')
        else:
            raise ParseError('Expected ^')

    def or_operation(self):
        if self.la == 'or':
            self.match('or')
        else:
            raise ParseError('Expected |')

    def and_operation(self):
        if self.la == 'and':
            self.match('and')
        else:
            raise ParseError('Expected &')

parser = myParser()
with open('test.txt', 'r') as fp:
    parser.parse(fp)