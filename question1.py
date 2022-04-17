#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from collections import defaultdict
import os
import re
import pandas as pd
import numpy as np
import pickle
import string
import nltk
import unidecode
from nltk import word_tokenize
from nltk.stem import PorterStemmer
nltk.download('stopwords') 
from nltk.corpus import stopwords
import time


# In[ ]:


pathin='english-corpora'
os.mkdir('english-corpora-cleaned')
pathout='english-corpora-cleaned'


# In[ ]:


<h4>Q1-Corpus_cleaning</h4>


# In[ ]:


# Replacing all the occurrences of \n,,\\,\t with a space.
def replace_occur(sen):
    sen = sen.replace('\\n', ' ').replace('\n', ' ').replace('\t',' ').replace('\\', ' ').replace('. com', '.com')
    return sen
def remove_spaces(sen):
    # Remove_whitespace
    pat = re.compile(r'\s+') 
    Without_space = re.sub(pat, ' ', sen)
    # There are some instances where there is no space after '?' & ')', So I am replacing these with one space so that It will not consider two words as one token.
    sen = Without_space.replace('?', ' ? ').replace(')', ') ')
    return sen
def remove_unicode(sen):
    # Unidecode() - It takes unicode data & tries to represent it to ASCII characters. 
    sen = unidecode.unidecode(sen)
    return sen
def remove_links(sen):
    # Remove links
    remove_https = re.sub(r'http\S+', '', sen)
    sen = re.sub(r"\ [A-Za-z]*\.com", " ", remove_https)
    return sen
def remove_code(sen):
    # Remove Code
    sen=re.sub(r' {[^}]*}','',sen)
    return sen
def remove_wiki(sen):
    # Remove wikipedia references 
    sen = re.sub("\[[0-9]+\]", ' ', sen)
    return sen
def remove_punc(sen):
    # removing punctuations
    sen = re.sub('[%s]' % re.escape(string.punctuation), ' ', sen)
    return sen
def tokeizing(sen):
    # The code for removing stopwords
    stpwrd = stopwords.words('english') 
    stpwrd = set(stpwrd)
    # repr() function actually gives the precise information about the string
    sen = repr(sen)
    # Text without stopwords
    clean_StopWords = [word for word in word_tokenize(sen) if word.lower() not in stpwrd]
    # Convert list of tokens_without_stopwords to String type.
    words_string = ' '.join(clean_StopWords)    
    
    tokens_words = nltk.word_tokenize(words_string)
    ps = PorterStemmer()
    
    word_list = nltk.word_tokenize(words_string)
    sen = ' '.join([ps.stem(w) for w in word_list])
    
    return sen 


# In[ ]:


# Executing aboue functions on each file of corpus
for filename in os.listdir(pathin):
    with open(pathin+'/'+filename,'r')as fin, open(pathout+'/'+filename,'w') as fout:
        sen=fin.read()
        sen=replace_occur(sen)
        sen=remove_spaces(sen)
        sen=remove_unicode(sen)
        sen=remove_links(sen)
        sen=remove_code(sen)
        sen=remove_wiki(sen)
        sen=remove_punc(sen)
        sen=remove_spaces(sen)
        sen=tokeizing(sen)
        fout.writelines(sen)

