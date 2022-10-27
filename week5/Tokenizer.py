import jieba

class Tokenizer:
    def __init__(self,chars,coding,PAD=0):
        self.coding=coding
        self.chars=chars
        self.PAD=PAD
        self.chardict = {}
        self.chardict['PAD']=0
        count = 1
        for char in chars:
            if coding == 'c':
                for i in range(len(char)):
                    if char[i] not in self.chardict.keys():
                        self.chardict[char[i]] = count
                        count+=1
            if coding == 'w':
                wordcutlist = jieba.lcut(char)
                for word in wordcutlist:
                    if word not in self.chardict.keys():
                        self.chardict[word] = count
                        count+=1

    def tokenize(self,sentence):
        if self.coding == 'w':
            wordcutlist = jieba.lcut(sentence)
        if self.coding == 'c':
            wordcutlist=[]
            leng = len(sentence)
            for i in range(leng):
                if sentence[i] != ' ':
                    wordcutlist.append(sentence[i])
        return wordcutlist

    def encode(self,list_of_chars):
        list_of_numbers=[]
        for char in list_of_chars:
            list_of_numbers.append(self.chardict[char])
        return list_of_numbers

    def trim(self,tokens,seq_len):
        if len(tokens) > seq_len:
            del tokens[seq_len:]
        while True:
            if len(tokens) < seq_len:
                tokens.append(self.PAD)
            else:
                break

    def decode(self,tokens):
        charlist=[]
        for i in range(len(tokens)):
            char = [k for k, v in self.chardict.items() if v == tokens[i]][0]
            if char == 'PAD':
                char = '[PAD]'
            charlist.append(char)
            sentence=''.join(charlist)
        return sentence

    def encode_all(self,seq_len):
        all_number=[]
        for char in self.chars:
            tokens=self.encode(self.tokenize(char))
            self.trim(tokens,seq_len)
            all_number.append(tokens)
        return all_number