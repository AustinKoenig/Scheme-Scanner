# Scanner -- HW 1
# Austin Koenig
# Programming Languages

# pseudo enum with class for token types
class TokenType:
    NONE, ID, BOOL, INT, REAL, PUNCT, KW, ERR = ["NONE", "ID", "BOOL", "INT", "REAL", "PUNCT", "KW", "ERR"] 

# token class
class Token:
    def __init__(self, tt, val):
        self.type = tt
        self.value = val
        
    def printToken(self):
        print(self.type + ": " + str(self.value))


class Scanner:
    def __init__(self):
        self.cursor = 0
        self.input = ""
        self.initialTokens = []
        self.inLength = len(self.input)
        self.result = []
        self.kwList = ["var", "fun", "if", "else", "return",
                       "read", "write", "not", "or", "and"]   
        self.punctList = ["\(", "\)", "{", "}", ",", "\+", "-", "\*", "/",
                          "%", ":=", "!=", "<", ">", "<=", ">="]
        self.singlePunctList = ["{", "}", ",", "\\", "-", "/", "%", ":=", "!="]
        self.bslshSubset = ["(", ")", "+", "*"]
        self.preEqualSgn = ["<", ">"]
        self.preEqualSgnRestricted = [":", "!"]
        self.digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def getInput(self): # gets input line from user
        self.input = input("CODE: ")

    def checkKW(self, kw): # looks for keywords in input
        for i in range(len(kw)):
            if i + i < len(self.input):
                if self.input[i + i] != kw[i]:
                    return False
        return True

    def isLetter(self, c):
        if 65 <= ord(c) <= 90 or 97 <= ord(c) <= 122:
            return True
        return False

    def isDigit(self, c):
        if c in self.digits:
            return True
        return False

    def getLength(self):
        return len(self.input)

    def scan(self):
        print("TOKENS: ")
        for w in self.initialTokens:
            if w in self.kwList: # checking for keywords
                temp = Token(TokenType.KW, w)
                temp.printToken()
                self.result.append(temp)
                self.cursor += len(w)
            else:
                self.cursor = 0
                if w[0] == "#": # checking for boolean values
                    if self.input[1] == "t" or w[1] == "f":
                        temp = Token(TokenType.BOOL, w[0] + w[1])
                        temp.printToken()
                        self.result.append(temp)
                        self.cursor += 2 # jumping over bool token
                    else:
                        temp = Token(TokenType.ERR, self.input[self.cursor] + self.input[self.cursor + 1])
                        temp.printToken()
                        self.result.append(temp)
                        self.cursor += 2 # jumping over the error token
                elif self.isDigit(self.input[self.cursor]) or self.input[self.cursor] == ".":
                        real = False # determine whether the number is real or int
                        tempNum = "" # var to store number while scanning it
                        for i in range(len(w)):
                            # loop iterates as long as there is a next char and it is a number or a decimal
                            if self.isDigit(self.input[self.cursor]): # number case
                                tempNum += self.input[self.cursor]
                            elif self.input[self.cursor] == "." and not real: # real case (will not work if there is already a decimal)
                                tempNum += "."
                                real = True
                            else: # end of token case
                                if real and tempNum[len(tempNum) - 1] != ".":
                                    self.result.append(Token(TokenType.REAL, tempNum))
                                elif real:
                                    self.result.append(Token(TokenType.ERR, tempNum))
                                else:
                                    self.result.append(Token(TokenType.INT, tempNum))
                                initialTokens.insert(self.initialTokens.index(w) + 1, w[i:len(w) - 1]) # add unknown word to word list
                                del w[i:len(w) - 1] # delete from current word
                elif self.input[self.cursor] in self.singlePunctList: # punctuation condition
                    if self.input[self.cursor] == "\\": # checking backslash punctuation
                        if self.input[self.cursor + 1] in self.bslshSubset:
                            self.result.append(Token(TokenType.PUNCT, self.input[self.cursor] + self.input[self.cursor + 1]))
                            self.cursor += 2
                        else:
                            self.result.append(Token(TokenType.ERR, self.input[self.cursor])) # error case
                            self.cursor += 1
                    elif self.input[self.cursor] in self.preEqualSgnRestricted: # checking equal sign punctuation
                        if self.input[self.cursor + 1] == "=":
                            self.result.append(Token(TokenType.PUNCT, self.input[self.cursor] + self.input[self.cursor + 1]))
                            self.cursor += 2
                        else:
                            self.result.append(Token(TokenType.ERR, self.input[self.cursor])) # error case
                    elif self.input[self.cursor] in self.preEqualSgn: # inequality punctuation
                        if self.input[self.cursor + 1] == "=":
                            self.result.append(Token(TokenType.PUNCT, self.input[self.cursor] + self.input[self.cursor + 1]))
                            self.cursor += 2
                        else:
                            self.result.append(Token(TokenType.PUNCT, self.input[self.cursor]))
                            self.cursor += 1
                    else:
                        self.result.append(Token(TokenType.PUNCT, self.input[self.cursor])) # all other punctuation cases
                        self.cursor += 1
                elif self.isLetter(self.input[self.cursor]): # checking keywords and identifiers
                    keyword = False # keyword boolean value
                    for word in self.kwList: # running through keyword list
                        if self.checkKW(word):
                            self.result.append(Token(TokenType.KW, word))
                            self.cursor += len(word)
                            keyword = True # if a keyword matches, then add the token
                            break
                    if not keyword: # collecting identifier characters
                        tempID = self.input[self.cursor]
                        while self.cursor < len(self.input) - 1: # checking 2nd and more chars in identifier
                            if self.isLetter(self.input[self.cursor + 1]) or self.input[self.cursor + 1] in self.digits:
                                tempID += self.input[self.cursor + 1]
                                self.cursor += 1
                            else:
                                self.result.append(Token(TokenType.ID, tempID))
                                break
                if self.cursor >= self.getLength():
                    active = False
            return self.result


if __name__ == "__main__":
    s = Scanner()
    active = True # loop condition
    while active:
        s.getInput()
        if s.input == "":
            exit()
        print(s.input+"\n")
        s.initialTokens = s.input.split(" ") # splitting the words separated by spaces into a list of primarily split words
        s.scan()
        print("\n")
