import lexer
import interpreter

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        l = lexer.Lexer(text)
        i = interpreter.Interpreter(l)
        result = i.program().eval()
        print(result)


if __name__ == '__main__':
    main()
