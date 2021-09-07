import ast
import tok

# rules:
# factor: INTEGER
# value: factor | paren | (PLUS | MINUS) value
# paren: LPAREN expr RPAREN
# power: value (POW value)*
# mul: power ((MUL | DIV) power)*
# addition: mul ((PLUS | MINUS) mul)*
# expr: additon
class Interpreter:
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

    def factor(self) -> ast.AST:
        """Return an INTEGER token value.

        factor : INTEGER
        """
        token = self.current_token
        self.eat(tok.INTEGER)
        return ast.Num(token)

    def value(self) -> ast.AST:
        """value parser / interpreter.
        value: factor | paren
        """
        if self.current_token.type == tok.INTEGER:
            return self.factor()

        if self.current_token.type == tok.LPAREN:
            return self.paren()
        
        if self.current_token.type == tok.PLUS:
            self.eat(tok.PLUS)
            return ast.UnaryOp_PLUS(self.value())

        if self.current_token.type == tok.MINUS:
            self.eat(tok.MINUS)
            return ast.UnaryOp_MINUS(self.value())

    def paren(self) -> ast.AST:
        """Parenthesis parser / interpreter.
        paren: LPAREN term1 RPAREN
        term1: addition
        """
        self.eat(tok.LPAREN)
        result = self.addition()
        self.eat(tok.RPAREN)           
        return result

    def power(self) -> ast.AST:
        """Power parser / interpreter
        power: value (POW value)*
        """
        result = self.value()
        while self.current_token.type == tok.POW:
            self.eat(tok.POW)
            result = ast.BinOp_POW(result, self.value())

        return result

    def mul(self) -> ast.AST:
        """Arithmetic expression parser / interpreter.

        mul: value ((MUL | DIV) value)*
        """ 

        result = self.power()

        while self.current_token.type in (tok.MUL, tok.DIV):
            token = self.current_token
            if token.type == tok.MUL:
                self.eat(tok.MUL)
                result = ast.BinOp_MUL(result, self.power())
            elif token.type == tok.DIV:
                self.eat(tok.DIV)
                result = ast.BinOp_DIV(result, self.power())

        return result

    def addition(self) -> ast.AST:
        """Arithmetic expression parser / interpreter.

        addition: mul ((PLUS | MINUS) mul)*
        """
        result = self.mul()

        while self.current_token.type in (tok.PLUS, tok.MINUS):
            token = self.current_token
            if token.type == tok.PLUS:
                self.eat(tok.PLUS)
                result = ast.BinOp_PLUS(result, self.mul())
            elif token.type == tok.MINUS:
                self.eat(tok.MINUS)
                result = ast.BinOp_MINUS(result, self.mul())

        return result

    def expr(self):
        result = self.addition()
        self.eat(tok.EOF)
        return result
