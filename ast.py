import abc
import tok


# abstract class for Abstract Syntax Tree
class AST(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def eval(self):
        raise NotImplemented()

class BinOp(AST):
    def __init__(self, left: AST, op: tok.Token, right: AST):
        self.left = left
        self.token = op
        self.right = right

    def eval():
        raise NotImplemented()

class Num(AST):
    def __init__(self, token: tok.Token):
        self.token = token
    
    def eval(self):
        return self.token.value

class BinOp_PLUS(BinOp):
    def __init__(self, left: AST, right: AST):
        super().__init__(left, tok.Token(tok.PLUS, '+'), right)

    def eval(self):
        return self.left.eval() + self.right.eval()

class BinOp_MINUS(BinOp):
    def __init__(self, left: AST, right: AST):
        super().__init__(left, tok.Token(tok.MINUS, '-'), right)

    def eval(self):
        return self.left.eval() - self.right.eval()

class BinOp_MUL(BinOp):
    def __init__(self, left: AST, right: AST):
        super().__init__(left, tok.Token(tok.MUL, '*'), right)

    def eval(self):
        return self.left.eval() * self.right.eval()

class BinOp_DIV(BinOp):
    def __init__(self, left: AST, right: AST):
        super().__init__(left, tok.Token(tok.DIV, '/'), right)

    def eval(self):
        return self.left.eval() / self.right.eval()

class BinOp_POW(BinOp):
    def __init__(self, left: AST, right: AST):
        super().__init__(left, tok.Token(tok.POW, '**'), right)

    def eval(self):
        return self.left.eval() ** self.right.eval()