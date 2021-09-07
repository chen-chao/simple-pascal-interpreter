# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER = 'INTEGER'
PLUS, MINUS, MUL, DIV, POW = 'PLUS', 'MINUS', 'MUL', 'DIV', 'POW'
LPAREN, RPAREN = 'LPAREN', 'RPAREN'
EOF = 'EOF'
BEG, END = 'BEGIN', 'END'
DOT, SEMI, ASSIGN = 'DOT', 'SEMI', 'ASSIGN'
SEQ, IF, WHILE, FOR = 'SEQ', 'IF', 'WHILE', 'FOR'
VAR = 'VAR'

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, MUL, DIV, or EOF
        self.type = type
        # token value: non-negative integer value, '*', '/', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


SYMBOLS = {
    "BEGIN": Token(BEG, BEG),
    'END': Token(END, END),
    'IF': Token(IF, IF),
    'WHILE': Token(WHILE, WHILE),
    'FOR': Token(FOR, FOR),
    '+': Token(PLUS, '+'),
    '-': Token(MINUS, '-'),
    '*': Token(MUL, '*'),
    '**': Token(POW, '**'),
    '/': Token(DIV, '/'),
    '.': Token(DOT, '.'),
    ';': Token(SEMI, ';'),
    '(': Token(LPAREN, '('),
    ')': Token(RPAREN, ')'),
    ':=': Token(ASSIGN, ':=')
}