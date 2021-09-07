# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER = 'INTEGER'
ADD, MINUS, MUL, DIV = 'ADD', 'MINUS', 'MUL', 'DIV'
LEFTP, RIGHTP = '(', ')'
EOF = 'EOF'


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


class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "3 * 5", "12 / 3 * 4", etc
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(ADD, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LEFTP, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RIGHTP, ')')

            self.error()

        return Token(EOF, None)


# rules:
# factor: INTEGER
# value: factor | parenthesis
# parenthesis: LEFTP expr RIGHTP
# multiplication: value ((MUL | DIV) value)*
# addition: multiplication ((ADD | MINUS) multiplication)*
# expr: additon
class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        print('current token: ', self.current_token)

        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """Return an INTEGER token value.

        factor : INTEGER
        """
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def value(self):
        """value parser / interpreter.
        value: factor | parenthesis
        """
        if self.current_token.type == INTEGER:
            return self.factor()

        return self.parenthesis()

    def parenthesis(self):
        """Parenthesis parser / interpreter.
        parenthesis: LEFTP term1 RIGHTP
        term1: addition
        """
        self.eat(LEFTP)
        result = self.addition()
        self.eat(RIGHTP)           
        return result

    def multiplication(self):
        """Arithmetic expression parser / interpreter.

        multiplication: value ((MUL | DIV) value)*
        """ 

        result = self.value()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.value()
            elif token.type == DIV:
                self.eat(DIV)
                result = result / self.value()

        return result

    def addition(self):
        """Arithmetic expression parser / interpreter.

        addition: multiplication ((ADD | MINUS) multiplication)*
        """
        result = self.multiplication()

        while self.current_token.type in (ADD, MINUS):
            token = self.current_token
            if token.type == ADD:
                self.eat(ADD)
                result = result + self.multiplication()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.multiplication()

        return result

    def expr(self):
        result = self.addition()
        self.eat(EOF)
        return result


def main():
    while True:
        try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()