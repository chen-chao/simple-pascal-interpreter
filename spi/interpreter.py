from . import astree
from .lexer import Lexer
from . import tok

# rules:
# factor: INTEGER | variable
# value: factor | paren | (PLUS | MINUS) value
# paren: LPAREN expr RPAREN
# power: value (POW value)*
# mul: power ((MUL | DIV) power)*
# addition: mul ((PLUS | MINUS) mul)*
# expr: additon

# pascal rules
# program: compound_block DOT
# compound_block = BEGIN block END
# block: statements | statements SEMI block
# statements: empty | assignment | compound_block
# assignment: variable ASSIGN expr
# variable: id
# empty: 
# expr： see above

class Interpreter:
    def __init__(self, lexer: Lexer):
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
        print('current token: ', self.current_token, ' required token: ', token_type)

        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def integer(self) -> astree.AST:
        """Return an INTEGER token value.

        factor : INTEGER
        """
        token = self.current_token
        self.eat(tok.INTEGER)
        return astree.Num(token)
        
    def variable(self) -> astree.AST:
        token = self.current_token
        self.eat(tok.VAR)
        return astree.Variable(token)

    def assignment(self) -> astree.AST:
        """Return an assignment AST
        
        assignment: variable ASSIGN expr
        """
        var = self.variable()
        self.eat(tok.ASSIGN)
        expr = self.expr()
        return astree.Assign(var, expr)

    def value(self) -> astree.AST:
        """value parser / interpreter.
        value: factor | paren
        """
        if self.current_token.type == tok.INTEGER:
            return self.integer()

        if self.current_token.type == tok.VAR:
            return self.variable()

        if self.current_token.type == tok.LPAREN:
            return self.paren()
        
        if self.current_token.type == tok.PLUS:
            self.eat(tok.PLUS)
            return astree.UnaryOp_PLUS(self.value())

        if self.current_token.type == tok.MINUS:
            self.eat(tok.MINUS)
            return astree.UnaryOp_MINUS(self.value())

    def paren(self) -> astree.AST:
        """Parenthesis parser / interpreter.
        paren: LPAREN term1 RPAREN
        term1: addition
        """
        self.eat(tok.LPAREN)
        result = self.addition()
        self.eat(tok.RPAREN)           
        return result

    def power(self) -> astree.AST:
        """Power parser / interpreter
        power: value (POW value)*
        """
        result = self.value()
        while self.current_token.type == tok.POW:
            self.eat(tok.POW)
            result = astree.BinOp_POW(result, self.value())

        return result

    def mul(self) -> astree.AST:
        """Arithmetic expression parser / interpreter.

        mul: value ((MUL | DIV) value)*
        """ 

        result = self.power()

        while self.current_token.type in (tok.MUL, tok.DIV):
            token = self.current_token
            if token.type == tok.MUL:
                self.eat(tok.MUL)
                result = astree.BinOp_MUL(result, self.power())
            elif token.type == tok.DIV:
                self.eat(tok.DIV)
                result = astree.BinOp_DIV(result, self.power())

        return result

    def addition(self) -> astree.AST:
        """Arithmetic expression parser / interpreter.

        addition: mul ((PLUS | MINUS) mul)*
        """
        result = self.mul()

        while self.current_token.type in (tok.PLUS, tok.MINUS):
            token = self.current_token
            if token.type == tok.PLUS:
                self.eat(tok.PLUS)
                result = astree.BinOp_PLUS(result, self.mul())
            elif token.type == tok.MINUS:
                self.eat(tok.MINUS)
                result = astree.BinOp_MINUS(result, self.mul())

        return result

    def expr(self) -> astree.AST:
        result = self.addition()
        return result

    def program(self) -> astree.AST:
        result = self.compound_block()
        self.eat(tok.DOT)
        self.eat(tok.EOF)
        return result

    def compound_block(self) -> astree.AST:
        self.eat(tok.BEG)
        result = self.block()
        self.eat(tok.END)
        return result

    def block(self) -> astree.AST:
        result = self.statements()
        while self.current_token.type == tok.SEMI:
            self.eat(tok.SEMI)
            next = self.statements()
            result = astree.Sequence(result, next)
        return result

    def statements(self) -> astree.AST:
        if self.current_token.type == tok.BEG:
            return self.compound_block()
        if self.current_token.type == tok.VAR:
            return self.assignment()
        else:
            return self.empty()

    def empty(self) -> astree.AST:
        return astree.Empty()
