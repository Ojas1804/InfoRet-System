from BooleanOperator import or_operator, and_operator, not_operator
from Conversion import InfixToPostfix
import re
from ExtendedBinaryRetrieval import BiwordIndex
from InverseIndex import InverseIndex
from Soundex import Soundex


# preprocess query and solve the boolean expression
class Query:
    def __init__(self, query):
        self.query = query
        self.ebr = BiwordIndex()
        self.ebr.get_posting_list()
        self.biword_index = self.ebr.index
        self.inv_index = InverseIndex()
        self.inv_index.get_posting_list()
        self.index = self.inv_index.index
        self.last_file = self.index[list(self.index.keys())[-1]][-1]


    # preprocess the query
    def preprocess_query(self):
        self.query = self.query.lower()
        self.query = re.sub(r'(?<=[\[{(])\s+|\s+(?=[\]})])', '', self.query)
        self.query = self.query.replace('(', '( ')
        self.query = self.query.replace(')', ' )')


    # solve the boolean expression
    def process_query(self):
        self.preprocess_query()
        infix = InfixToPostfix(self.query) # convert query to postfix
        postfix = infix.convert()
        boolean_operators = ['and', 'or', 'not']
        query_tokens = []

        # solve postfix boolean expression
        for p in postfix:
            if p not in boolean_operators:
                q = p.split('-')
                # print(q)
                if len(q) == 1:  # search in normal inverted index
                    if p in self.index:
                        query_tokens.append(self.index[p])
                else:  # If len(q) > 1 then it is a biword
                    str = ""
                    biwords = []
                    for i in range(len(q)-1):
                        str += q[i]
                        str += ' '
                        str += q[i+1]
                        biwords.append(str)
                        str = ""
                        
                    biword_and = []
                    for str in biwords:
                        if str in self.biword_index:
                            biword_and.append(self.ebr.search(str))
                    biword_res = []
                    if len(biword_and) == 1:
                        biword_res.append(biword_and.pop())
                    else:
                        while(len(biword_and) > 1):
                            biword_and.append(and_operator(biword_and.pop(), biword_and.pop()))
                        biword_res.append(biword_and.pop())
                    query_tokens.append(biword_res.pop())
            else:
                if p == 'not':
                    term = query_tokens.pop()
                    operator = 'not'
                    query_tokens.append(self.solve(term, operator))
                else:
                    term = []
                    term.append(query_tokens.pop())
                    term.append(query_tokens.pop())
                    operator = p
                    query_tokens.append(self.solve(term, operator))
        return query_tokens[0]


    def solve(self, term, operator):
        if operator == 'or':
            return or_operator(term[0], term[1])
        elif operator == 'and':
            return and_operator(term[0], term[1])
        else:
            return not_operator(term, self.last_file)

    
    def soundex_query(self, soundex_index):
        self.preprocess_query()
        infix = InfixToPostfix(self.query) # convert query to postfix
        postfix = infix.convert()
        boolean_operators = ['and', 'or', 'not']
        query_tokens = []
        soundex = Soundex()

        # solve postfix boolean expression
        for p in postfix:
            if p not in boolean_operators:
                q = p.split('-')
                if len(q) == 1:  # search in normal inverted index
                    p_s = soundex.getSoundex(p)
                    query_tokens.append(soundex_index[p_s])
            else:
                if p == 'not':
                    term = query_tokens.pop()
                    operator = 'not'
                    query_tokens.append(self.solve(term, operator))
                else:
                    term = []
                    term.append(query_tokens.pop())
                    term.append(query_tokens.pop())
                    operator = p
                    query_tokens.append(self.solve(term, operator))
        return query_tokens[0]