#!/usr/bin/env python
# coding: utf-8

# In[39]:


from collections import defaultdict
import os
import re
import csv
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
import sys


# In[40]:


pathin='/home/akku/Desktop/english-corpora'
os.mkdir('english-corpora-cleaned')
#pathout='/home/akku/Desktop/english-corpora-processed'
pathout='/home/akku/Desktop/english-corpora-cleaned'


# In[46]:


#Global dic to store (word: {docID,freq})
all_unique_word_dict = {}#Its dict of dict,to store all unique words with  doc_id's containing them.
doc_matrix=[]#lst of dictionaries,where each dictionary storing word and there correspnding frequencies
doc_list=[]#Stores all doc_ids
dict_freq={} #storing frequency of word in dictionary
dict_idf={} #storing idf_value of every document
length_per_doc=[] #storing doc length
corpus_size=0 #total_files
boolean_dict={} #bool_dictionary
dict_queries={}#Stores


# <h4>Q1-Corpus_cleaning</h4>

# In[47]:


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


# In[101]:


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

    
    
    
    
    
    
    


# <h6>processing query</h6> 

# In[48]:


# taking input from command line
query_name=sys.argv[1]


# In[49]:


def filter_query():
    f=open(query_name, 'rb')
    sen = f.readlines()
    for line in sen:
            l=line.strip()
            str_val = l.decode('UTF-8') 
            temp=str_val.split("\t")
            dict_queries[temp[0]]=temp[1]
    print(dict_queries)
    clean_query()
    f.close()
   
    
       


# In[50]:


def clean_query():
    for item in dict_queries:
        sen=dict_queries[item]
        sen=replace_occur(sen)
        sen=remove_spaces(sen)
        sen=remove_unicode(sen)
        sen=remove_links(sen)
        sen=remove_code(sen)
        sen=remove_wiki(sen)
        sen=remove_punc(sen)
        sen=remove_spaces(sen)
        query=tokeizing(sen)
        query=word_tokenize(query[1:-1])
        dict_queries[item]=query


# In[51]:


filter_query()


# <h6>Boolean Retrieval Model</h6>

# <p>(I)Creating Inverted Index</p>

# In[52]:


#creating dictiontionary to count each word frequency of each text file

def create_index (filename):
        index = defaultdict(int)
        with open(pathout+'/'+filename,'r+')as fin:
            for line in fin:
                for word in line.split(): 
                    index[word]+=1;
            create_inverted_index(index,filename)#creating dictionary of linked_list.
            length_per_doc.append(len(index))
            doc_matrix.append(index)
         
         


# In[53]:


#Making a List_linked for each word and storing all the nodes

def create_inverted_index(index,filename):
    #Initialzing dic with all unique words
    for item in index:
        try:
            all_unique_word_dict[item][(str(filename).replace('.txt',''))]=index[item]
        except:
            all_unique_word_dict[item]={}
            all_unique_word_dict[item][(str(filename).replace('.txt',''))]=index[item]
           
   


# In[54]:


# Accessing each and every file from corpus

for filename in os.listdir(pathout):
    #Creating list of all filenames
    doc_list.append(str(filename).replace('.txt',''))
    # create inverted index
    create_index(filename)
    corpus_size+=1


# In[55]:


f=open('inverted_index_dict.pkl', 'wb') 
pickle.dump( all_unique_word_dict, f)
f.close()
     
f=open('length_per_doc.pkl', 'wb')
pickle.dump(length_per_doc, f)
f.close()
       
f=open('dict_matrix.pkl', 'wb')
pickle.dump(doc_matrix, f)
f.close()
       

f=open('inverted_index_dict.pkl', 'rb')
loaded_inverted_index_dict = pickle.load(f)
f.close()
f=open('length_per_doc.pkl', 'rb')
loaded_length_per_doc = pickle.load(f)
f.close()
f=open('dict_matrix.pkl', 'rb') 
loaded_dict_matrix = pickle.load(f)
f.close()


# In[58]:


len(loaded_inverted_index_dict)


# In[59]:


def process_query(query,zero_and_1_of_all_words):
    for j in range(len(query)-1):
        try:
            l1=zero_and_1_of_all_words[0]
            l2=zero_and_1_of_all_words[1]

            op = [w1 & w2 for (w1,w2) in zip(l1,l2)]
            
            zero_and_1_of_all_words.remove(l1)
            zero_and_1_of_all_words.remove(l2)
            zero_and_1_of_all_words.insert(0,op)

        except:
            print("Wrong sequence of Boolean Operator !!!")
    
    files = []    
    val = zero_and_1_of_all_words[0]
    cnt = 0
    for index in val:
        if index == 1:
            files.append(doc_list[cnt])
        cnt = cnt+1
    
    return files[:5]


# In[60]:


def boolean_list_creation(different_words):
    zero_and_1 = []
    zero_and_1_of_all_words = []
    for word in different_words:
        if word.lower() in loaded_inverted_index_dict:
            zero_and_1 = [0] * corpus_size
            t=loaded_inverted_index_dict[word]
            for item in t:
                temp=doc_list.index((str(item)))
                zero_and_1[temp] = 1
            zero_and_1_of_all_words.append(zero_and_1)
        else:
            print(word," word absent")
    return process_query(different_words,zero_and_1_of_all_words)


# In[61]:


#function to create boolean_retrieval_file
def check_boolean_retrieval():
    boolean_list=[]
    for item in dict_queries:
        test=boolean_list_creation(dict_queries[item])
        for i in test:
            boolean_list.append([item,1,i,1])
        file=open('boolean.txt','w')
        f=csv.writer(file)
        f.writerows(boolean_list)
           
     
    


# In[62]:


check_boolean_retrieval()


# <h4>Implementing TF-IDF using Cosing similarity</h4>

# In[63]:


def cosine_tf_idf(query):
    lq=len(query)
    tf={}
    arr=np.zeros((lq+1,corpus_size))
    for i in range(lq):
        try:
            tf[query[i]]+=1
        except:
            tf[query[i]]=1
            
        tempx = loaded_inverted_index_dict[query[i]]
        
        for item in tempx:
            temp=item
            temp2=doc_list.index((str(temp)))
            arr[i][temp2]=(tempx[item])
            arr[-1][temp2]+=arr[i][temp2]**2
    return query_vector(tf,lq,arr)


# In[64]:


def query_vector(tf,q_len,arr):
    square_query=0
    for item in tf:
        tf[item]=tf[item]*(np.log(corpus_size/len(loaded_inverted_index_dict[item]))) #need to handle this case when item is not in dict
        square_query+=tf[item]**2
     
    array_q=np.zeros(q_len)
    
    m=0
    for k in tf:
        array_q[m]=tf[k]
        m=m+1
    
    return similarity_check_tf_df(q_len,array_q,arr)    


# In[65]:


def similarity_check_tf_df(q_len,array_q,arr):
    score_doc={}
    for i in range(corpus_size):
        st=0
        for j in range(q_len):
            st+=(arr[j][i]*array_q[j])
        score_doc[doc_list[i]]=st
    score_doc = {k: v for k, v in sorted(score_doc.items(), key=lambda x: x[1],reverse=True)}
    return score_doc

    


# In[66]:


def check_tf_idf():
    tf_df_list=[]
    for item in dict_queries:
        test=list(cosine_tf_idf(dict_queries[item]).keys())[:5]
        for i in test:
            tf_df_list.append([item,1,i,1])
            file=open('tf_df.txt','w')
            f=csv.writer(file)
            f.writerows(tf_df_list)
            #print(tf_df_list)


# In[67]:


check_tf_idf()


# <h4>Implementation of BM25</h4>

# In[68]:


#calculating avg_doc_len value
avg_doc_len_ = sum(loaded_length_per_doc) / corpus_size


# In[69]:


#search for query 
def check_query(query):
    scores = {}
    for index in range(corpus_size):
        scores[doc_list[index]]=check_score(query, index)
    return scores


# In[70]:


#Function calculating score of each document
def check_score(query, index,k1=1.2,b=0.75):
        score = 0.0

        doc_len =loaded_length_per_doc[index]
        #print("doc : ",doc_len)
        freq = loaded_dict_matrix[index]
        #print("fre : ",frequencies)
        for term in query:
            
            #print('1')
            if term not in freq:
                continue
            
            count=len(loaded_inverted_index_dict[term])
            fr = freq[term]
            idf_val=np.log(1 + (corpus_size - count + 0.5) / (count + 0.5))
            num = idf_val * fr * (k1 + 1)
            deno = fr + k1 * (1 - b + b * doc_len / avg_doc_len_)
            score += (num / deno)

        return score


# In[71]:


def check_bm25_system():
    BM25_list=[]
    for item in dict_queries:
        score=check_query(dict_queries[item])
        score=dict(sorted(score.items(), key=lambda item: item[1],reverse=True))
        BM25=list(score.keys())[:5]
        for i in BM25:
            BM25_list.append([item,1,i,1])
            file=open('BM25.txt','w')
            f=csv.writer(file)
            f.writerows(BM25_list)
            #print(BM25_list)
    


# In[72]:


check_bm25_system()

        


# In[ ]:




