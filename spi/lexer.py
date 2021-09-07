from . import tok


class Lexer(object):
    def __init__(self, text: str):
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

    # TODO: support float
    def integer(self) -> int:
        """Return a (multidigit) integer consumed from the input."""
        result = []
        while self.current_char is not None and self.current_char.isdigit():
            result.append(self.current_char)
            self.advance()
        return int(''.join(result))

    def identifier(self) -> str:
        result = []
        while self.current_char is not None and self.current_char.isalnum():
            result.append(self.current_char)
            self.advance()
        return ''.join(result)

    def symbol(self) -> str:
        result = []
        while self.current_char is not None and not self.current_char.isspace() and not self.current_char.isalnum():
            result.append(self.current_char)
            self.advance()
        return ''.join(result)

    # TODO: improve with a Trie
    def get_next_token(self) -> tok.Token:
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return tok.Token(tok.INTEGER, self.integer())

            identifier = self.identifier()
            if identifier:  # identifier mustn't be '' or None
                token = tok.SYMBOLS.get(identifier, None)
                if token is not None:
                    return token
                else:
                    return tok.Token(tok.VAR, identifier)

            symbol = self.symbol()
            if symbol is not None:
                token = tok.SYMBOLS.get(symbol, None)
                if token is not None:
                    return token

            self.error()

        return tok.Token(tok.EOF, None)