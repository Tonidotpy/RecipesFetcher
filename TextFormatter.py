class TextFormatter:
    # Styles
    NORMAL           = 0
    BOLD             = 1
    DIM              = 2
    ITALIC           = 3
    UNDERLINE        = 4
    NEGATIVE         = 7
    STRIKE           = 9
    DOUBLE_UNDERLINE = 21
    
    # Colors
    BLACK  = 30
    RED    = 31
    GREEN  = 32
    YELLOW = 33
    BLUE   = 34
    PURPLE = 35
    CYAN   = 36
    WHITE  = 37
   
    def Background(self, col : int) -> int:
        return col + 10
    def Bright(self, col : int) -> int:
        return col + 60
    
    # SGR terminal formatting - https://en.wikipedia.org/wiki/ANSI_escape_code
    def GetColor(self, style : int = -1, col : int = -1, colBright : bool = False, backCol : int = -1, backBright : bool = False) -> str:
        res = ""
        # Style
        if style >= 0:
            res += "\033[" + str(style) + "m"
        # Fore color
        if col >= 0:
            if colBright:
                col = self.Bright(col)
            res += "\033[" + str(col) + "m"
        # Background color
        if backCol >= 0:
            if backBright:
                backCol = self.Bright(backCol)
            res += "\033[" + str(backCol) + "m"

        return res
    
    def Format(self, strings : list, format : str) -> str:
        pass