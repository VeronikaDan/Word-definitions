import json, re, multidict
from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from Stemmer import Stemmer
stemmer = Stemmer('russian')
from gensim.models.fasttext import FastText
ft_model = FastText.load('araneum_none_fasttextskipgram_300_5_2018.model')
from Levenshtein import distance as lev

def read_words(file):
    res = []
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        w = line.strip('\n')
        res.append(w)
    return res
	

def write_in_json(path, data):
    f = open(path, 'w', encoding = 'utf-8')
    json.dump(data, f, indent = 2, ensure_ascii = False)
    f.close()
	

STOPS = read_words("data/stopwords.txt")

def getFrequencyDictForText(sents, w):
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}
    mx = 0

    for word in sents:
        if word not in STOPS and word != w and not have_same_root(w,word) and not word.isdigit():                
            val = tmpDict.get(word,0)
            if val + 1 > mx:
                mx = val + 1
            tmpDict[word] = val+1
    for key in tmpDict:
        fullTermsDict.add(key,tmpDict[key] / (mx*3))
    return fullTermsDict



def Cloud(w, dic):    
    wc = WordCloud(background_color="white", max_words=150)
    wc.generate_from_frequencies(dic)
    fig = plt.figure()
	
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    fig.savefig(w+'.png') 
    plt.close(fig)
    return wc.words_

def common_letters(word1, word2):
    n = 0
    i = 0
    for letter in word1:
        if i > len(word2) - 1:
            return n
        if word2[i] == letter:
            n +=1
        else:
            return n
        i += 1
    return n
	

def have_same_root(word1, word2):
    w1_stem = stemmer.stemWord(word1)
    w2_stem = stemmer.stemWord(word2)
    if w1_stem == w2_stem or lev(w1_stem, w2_stem) <= 2:
        return True
    comm = common_letters(w1_stem,w2_stem)
    if comm < 4:
        return False
    if comm > 6:
        return True
    diff = abs(len(max(w1_stem,w2_stem))-comm)        
    if diff > comm or diff > 2:
        return False
    return True

def make_definition(word, sents)	
    dic = getFrequencyDictForText(sents, word)
	ft_model.build_vocab(sents, update=True)
    ft_model.train(sents, total_examples=ft_model.corpus_count, epochs=ft_model.epochs)
    for i in ft_model.wv.most_similar(positive=[word], topn=150):
        neighbour = i[0]
        if len(neighbour)> 3 and re.match(r'[а-я]+$',neighbour) and not have_same_root(neighbour,word) and neighbour not in dic.keys():
            add = True
            for syn in dic.keys():
                if have_same_root(neighbour, syn):
                    add = False
                    break
            if add:
                dic.add(neighbour,i[1])
    definition = Cloud(word, dic)
    write_in_json(word+".json", definition)