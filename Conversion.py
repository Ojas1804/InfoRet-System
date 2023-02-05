from Stack import Stack
from Lemmatizer import lemmatize_text


# infix to postfix converter
class InfixToPostfix:
    def __init__(self, infix):
        self.infix = infix
        self.postfix = []
        self.stack = Stack()
        self.precedence = {"(": 0, "or": 1, "and": 2, "not": 3}
        self.operators = ["and", "or", "not", "(", ")"]

    def convert(self):
        temp = self.infix.split(" ")
        str = ""
        biword = [] #  join words with hyphen to make it a single word
        for t in temp:
            if t not in self.operators:
                str += t + "-"
            else:
                if str != "":
                    biword.append(str[:-1])
                biword.append(t)
                str = ""
        biword.append(str[:-1])
        if biword[-1] == "":
            biword.pop()

        str = ""
        for t in biword:
            str += t + " "
        self.infix = str[:-1]

        tokens = self.infix.split(" ")
        for token in tokens:
            if token not in self.operators:
                token = lemmatize_text(token)[0][0]
                self.postfix.append(token)
            elif token == "(":
                self.stack.push(token)
            elif token == ")":
                while self.stack.peek() != "(":
                    self.postfix.append(self.stack.pop())
                self.stack.pop()
            else:
                while not self.stack.isEmpty() and self.precedence[self.stack.peek()] >= self.precedence[token]:
                    self.postfix.append(self.stack.pop())
                self.stack.push(token)
        while not self.stack.isEmpty():
            self.postfix.append(self.stack.pop())
        return self.postfix