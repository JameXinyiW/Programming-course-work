from Tokenizer import Tokenizer
from numpy import*
import matplotlib.pyplot as plt

def main():
    t=open('final_none_duplicate.txt',encoding='UTF-8')
    cont=t.readlines()
    char_list=[]
    len_list = []
    for c in cont:
        y=c.split()
        char_list.append(y[2])
        len_list.append(len(y[2]))
    #print(mean(len_list))
    len_dic={}
    for num in len_list:
        len_dic[num]=len_dic.get(num,0)+1

    '''len_dic_set=dict(sorted(len_dic.items(),key = lambda item:item[0]))
    print(len_dic_set)
    print(len(len_dic_set))
    #plt.xticks(list(len_dic.keys()))
    #plt.yticks(list(len_dic.values()))
    count=0
    s=sum(list(len_dic_set.values()))
    print(s)
    for i in range(len(len_dic_set)):
        count+=len_dic_set[i+1]
        if count/s > 0.9:
            print(i)
            break
    print(count)
    plt.bar(list(len_dic.keys()), list(len_dic.values()))
    plt.show()'''

    test_to_see=char_list[:100]
    t=Tokenizer(chars=test_to_see,coding='w',PAD=0)
    for x in t.encode_all(61):
        print(x)
    print('--------------------------')
    print(t.chardict)
    print('--------------------------')
    temp_sentence=t.tokenize(char_list[99])
    print(temp_sentence)
    print('--------------------------')
    temp_number=t.encode(temp_sentence)
    print(temp_number)
    print('--------------------------')
    t.trim(temp_number,20)
    print(temp_number)
    print(t.decode(temp_number))
    print('--------------------------')
    t.trim(temp_number,10)
    print(temp_number)
    print(t.decode(temp_number))
    print('--------------------------')
    t.trim(temp_number,7)
    print(temp_number)
    print(t.decode(temp_number))


if __name__ == '__main__':
    main()