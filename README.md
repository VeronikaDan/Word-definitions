# Word-definitions

### Goal:
This work is intended to fill a gap in the field of machine methods of writing semantic definitions. The creation of software that, using minimal data about a word, is able to quickly generate the simplest but meaningful definition, can be useful both for the development of applied lexicography and for improving the level of culture and education of users who are constantly faced with little-known words.

### How to use:
Final code is located in word_definition.py

The main function that can generate a word cloud, which describes the meaning of a word, is named "make_definition" and takes two arguments: 1) the defined word (string), 2) its contexts (array of sentences, where sentence is array of words)

This method generates two files:

1) a word cloud (png)

2) json file with words from word cloud and their significance for the cloud (dic - string : float)

### Requirements:
- multidict
- pymorphy2
- wordcloud
- matplotlib
- PyStemmer
- gensim.models.fasttext
- fastText model ('araneum_none_fasttextskipgram_300_5_2018.model' from [here](http://rusvectores.org/ru/models/)
- Levenshtein