#terminal app
import Token
import Chario
import Scanner
import Parser


class TerminalApp:
    p = None

    def __init__(self):
        self.p = Parser.Parser()

        try:
            self.p.parse()

        except:
            Chario.Chario.reportErrors(Chario.Chario())


if __name__ == "__main__":

    TerminalApp()
