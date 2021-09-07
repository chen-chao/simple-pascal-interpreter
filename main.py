import lexer
import interpreter

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
        l = lexer.Lexer(text)
        i = interpreter.Interpreter(l)
        result = i.expr().eval()
        print(result)


if __name__ == '__main__':
    main()