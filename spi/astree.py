import abc
from . import tok


global ENV
ENV = {}

# abstract class for Abstract Syntax Tree
class AST(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def eval(self):
        raise NotImplemented()

class Num(AST):
    def __init__(self, token: tok.Token):
        self.token = token
    
    def eval(self):
        return self.token.value

class Variable(AST):
    def __init__(self, token: tok.Token):
        self.token = token

    def eval(self):
        global ENV
        try:
            return ENV[self.token.value]
        except NameError:
            raise NameError(f"{self.token.value} does not exist")
    
    def __str__(self):
        return "var"

class Empty(AST):
    def eval(self):
        pass

    def __str__(self):
        return ''

class Assign(AST):
    def __init__(self, var: AST, expr: AST):
        # should be a varaible token
        self.token = tok.Token(tok.ASSIGN, tok.ASSIGN)
        self.var = var
        self.expr = expr
    
    def eval(self):
        global ENV
        result = self.expr.eval()
        ENV[self.var.token.value] = result
        return result

    def __str__(self):
        return f"{self.var} := {self.expr}"

class UnaryOp(AST):
    def __init__(self, op: tok.Token, child: AST):
        self.token = op
        self.child = child

class UnaryOp_PLUS(UnaryOp):
    def __init__(self, child: AST):
        super().__init__(tok.Token(tok.PLUS, '+'), child)
    
    def eval(self):
        return self.child.eval()

class UnaryOp_MINUS(UnaryOp):
    def __init__(self, child: AST):
        super().__init__(tok.Token(tok.MINUS, '-'), child)
    
    def eval(self):
        return -self.child.eval()

class BinOp(AST):
    def __init__(self, left: AST, op: tok.Token, right: AST):
        self.left = left
        self.token = op
        self.right = right

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

class Sequence(AST):
    def __init__(self, current: AST, next: AST):
        self.token = tok.Token(tok.SEQ, 'SEQ')
        self.current = current
        self.next = next

    def eval(self):
        if self.next is None:
            return self.current.eval()
        else:
            return self.next.eval()

class If(AST):
    def __init__(self, conditon: AST, iftrue: AST, iffalse: AST):
        # TODO: limit condition to bool
        self.token = tok.Token(tok.IF, 'IF')
        self.condition = conditon
        self.iftrue = iftrue
        self.iffalse = iffalse
    
    def eval(self):
        if self.condition.eval():
            return self.iftrue.eval()
        else:
            return self.iffalse.eval()

class While(AST):
    def __init__(self, conditon: AST, body: AST):
        # TODO: limit condition to bool
        self.token = tok.Token(tok.IF, 'WHILE')
        self.condition = conditon
        self.body = body
    
    def eval(self):
        # environment
        while self.condition.eval():
            result = self.body.eval()
        
        return result