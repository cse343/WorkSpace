import re
import math

class TokenType: # regex ifadeler icin wrapper olustur
    def __init__(self, _name, _regex):
        self.name = _name
        self.regex = _regex
        
    def checkRegex(self, text):
        return re.match(self.regex,text)
    
class Token:
    def __init__(self, match, T):
        self.match = match # regex matchi
        self.type = T # ve tipini tut

class Tokenizer:
    def __init__(self):
        self.token_type_list = [] 
        # bu tokenizer tarafindan taninabilecek token tiplerinin listesi

    def addTokenType(self, _name, _regex):
        """ Token tipi ekle """
        self.token_type_list.append( TokenType(_name, _regex))

    def tokenize(self, text):
        _text = text
        token_list = []
        while len(_text) > 0:
            isMatch = False
            for token_type in self.token_type_list: # her token type icin itere et
                # iki token tipi arasinda oncelik tanimi yapmak icin birini
                # listeye daha once eklemeniz yeterli
                match = token_type.checkRegex(_text) 
                if match:
                    isMatch = True
                    token_list.append( Token(match, token_type) ) # yeni token ekle
                    _text = _text[match.end():] # texti guncelle match uzunlugu kadar 
                    break
            if not isMatch:
                break
        us= []
        for tok in token_list:
            us.append([tok.type.name,tok.match.group()])
        return us
            
    
# dosya okuma
fp = open("code.py", "r")
_text = ""
for line in fp:
    _text = _text + line

tk = Tokenizer() # tokenizer obje olustur

Identifier = Tokenizer()


tk.addTokenType("Op", r"\s+")
tk.addTokenType("Op",r'\[' )
tk.addTokenType("Op", r'\]' )
tk.addTokenType("Id", r'^[_a-zA-Z][a-zA-Z_0-9]*')
tk.addTokenType("Op", r"\(")
tk.addTokenType("Op", r'\)' )
tk.addTokenType("Op", r'\{')
tk.addTokenType("Op", r'\}')
tk.addTokenType("Op", r',' )
tk.addTokenType("Op", r'\:')
tk.addTokenType("Op", r'\.')
tk.addTokenType("Op", r'-|\+|\*\*?|\/|\%|==?|<[<=]?|>[=>]?')
tk.addTokenType("Op", r'#.*')
tk.addTokenType("Op", r'[0-9]*\.[0-9]+|[0-9]+\.[0-9]*')
tk.addTokenType("Op", r'[0-9]+')
tk.addTokenType("Op", r'".*?"')
tk.addTokenType("Op", r'@')
tk.addTokenType("Op", r'\'' )
tk.addTokenType("Op", r'\|' )
tk.addTokenType("Op", r'\\' )

uu=tk.tokenize(_text)

ide=0
op=0
a=[]
b=[]
for i in uu:
    if(i[0] == 'Id'):
        ide+=1
        if(a.count(i[1]) == 0):
            a.append(i[1])
    else:
        op+=1
        if(b.count(i[1]) == 0):
            b.append(i[1])

print len(a),ide,len(b),op




Unique_identifier = len(a)
Unique_operator = len(b)
Halstead_Program_Length = (Unique_identifier*math.log(Unique_identifier,2)) 
+ (Unique_operator*math.log(Unique_operator,2))
print "Halstead's Length : ", Halstead_Program_Length
