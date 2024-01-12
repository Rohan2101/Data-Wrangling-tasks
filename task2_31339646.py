#!/usr/bin/env python
# coding: utf-8

# <div class="alert alert-block alert-danger">
# 
# # FIT5196 Task 2 in Assessment 1
#     
# #### Student Name: Rohan Singh
# #### Student ID: 31339646
# 
# Date: 17-04-2023
# 
# Environment: Jupyter Notebook
# 
# Libraries used:
# * os (for interacting with the operating system, included in Python xxxx) 
# * pandas 1.1.0 (for dataframe, installed and imported) 
# * multiprocessing (for performing processes on multi cores, included in Python 3.6.9 package) 
# * itertools (for performing operations on iterables)
# * nltk 3.5 (Natural Language Toolkit, installed and imported)
# * nltk.collocations (for finding bigrams, installed and imported)
# * nltk.tokenize (for tokenization, installed and imported)
# * nltk.stem (for stemming the tokens, installed and imported)
# 
#     </div>

# <div class="alert alert-block alert-info">
#     
# ## Table of Contents
# 
# </div>
# 
# [1. Introduction](#Intro) <br>
# [2. Importing Libraries](#libs) <br>
# [3. Examining Input File](#examine) <br>
# [4. Loading and Parsing Files](#load) <br>
# $\;\;\;\;$[4.1. Tokenization](#tokenize) <br>
# $\;\;\;\;$[4.2. Whatever else](#whetev) <br>
# $\;\;\;\;$[4.3. Finding First 200 Bigrams](#bigrams) <br>
# $\;\;\;\;$[4.4. Whatever else](#whetev1) <br>
# [5. Writing Output Files](#write) <br>
# $\;\;\;\;$[5.1. Vocabulary List](#write-vocab) <br>
# $\;\;\;\;$[5.2. Sparse Matrix](#write-sparseMat) <br>
# [6. Summary](#summary) <br>
# [7. References](#Ref) <br>

# <div class="alert alert-block alert-success">
#     
# ## 1.  Introduction  <a class="anchor" name="Intro"></a>

# This assessment concerns textual data and the aim is to extract data, process them, and transform them into a proper format. The dataset provided is in the format of a PDF file containing ....

# <div class="alert alert-block alert-success">
#     
# ## 2.  Importing Libraries  <a class="anchor" name="libs"></a>

# In this assessment, any python packages is permitted to be used. The following packages were used to accomplish the related tasks:
# 
# * **os:** to interact with the operating system, e.g. navigate through folders to read files
# * **re:** to define and use regular expressions
# * **pandas:** to work with dataframes
# * **multiprocessing:** to perform processes on multi cores for fast performance 
# ....

# In[ ]:


import os
import re
import langid
import pandas as pd
import multiprocessing
from itertools import chain
import nltk
from nltk.probability import *
from nltk.collocations import *
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import MWETokenizer
from nltk.stem import PorterStemmer
from nltk.util import ngrams
import tabula
import time
import requests
import nltk.data
from PyPDF2 import PdfReader
from functools import reduce


# In[ ]:





# -------------------------------------

# <div class="alert alert-block alert-success">
#     
# ## 3.  Examining Input File <a class="anchor" name="examine"></a>

# In[ ]:


from google.colab import drive
drive.mount('/content/drive')


# Let's examine what is the content of the file. For this purpose, .... 

# In[ ]:


df = tabula.read_pdf("31339646.pdf",pages=(1,2,3,4,5))


# The tabula.read_pdf() function is being used to read data from the PDF file named "31339646.pdf". The function reads the specified pages (1, 2, 3, 4, and 5) from the PDF file and attempts to extract tables from the pages.
# This function will return a pandas DataFrame object, which is a two-dimensional labeled data structure.

# In[ ]:


for r3 in range(5):
    for r in range(len(df[r3])):
        r1 = requests.get(df[r3].iloc[r][1],allow_redirects=True)
        open(df[r3]['filename'][r],'wb').write(r1.content)
    time.sleep(1300)    


# For each row, the code prints the value of the second column of the row, which contains the URL pointing to the pdf download file. Then the code uses the requests library to download the content of the file at the URL, the requests.get() function takes  this as input and returns a Response object that contains the content of the response received from the server. The allow_redirects=True parameter allows the function to follow any redirects that may be specified by the server.
# The content of the response is then written to a file with the name specified in the filename column of the same row. The open() function is used to open a file with the specified name in binary write mode ('wb'). The write() method is then used to write the content of the response to the file. The code then sleeps for 1300 seconds using the time.sleep() function. This is done to avoid overloading the server with too many requests in a short period of time which leads to partial downloads.
# 

# <div class="alert alert-block alert-success">
#     
# ## 4.  Loading and Parsing File <a class="anchor" name="load"></a>

# In this section we load and extract the data

# In[ ]:


text_list = []
#intializing list
for r10 in range(5):
    for r2 in range(len(df[r10])):
        reader = PdfReader(df[r10]['filename'][r2])
        number_of_pages = len(reader.pages)
        text_all = ''
        for h in range(number_of_pages):
            page = reader.pages[h]
            text = page.extract_text()
            text_all = text_all + ' ' + text
        text_list.append(text_all)
        


# Using this function we read all the text from the pdf files respectively and save them as strings in the form of a list with each element being the all text from its respective pdf. For each row it reads the PDF file and obtains the number of pages in the file. It iterates over each page in the file, extracts the text from the page using the extract_text() method, and concatenates all the text from the pages into a single string.

# In[ ]:


doc_names = []
#intializing list
for r54 in range(5):
    for r55 in range(len(df[r54])):
        r56 = re.sub('.pdf', '', df[r54]['filename'][r55])
        doc_names.append(r56)


# The following code is used to get a list of all the document names for the pdf files we downloaded before

# In[ ]:


text_list_clean = []
#intializing list
for tex in text_list:
    tex1 = re.sub(r'\x0b','ff',tex,re.DOTALL)
    tex2 = re.sub(r'\x0c','fi',tex1,re.DOTALL)
    tex3 = re.sub(r'\x0e','ffi',tex2,re.DOTALL)
    tex4 = re.sub(r'\x0f','ffl',tex3,re.DOTALL)
    tex5 = re.sub(r'\n',' ',tex4,re.DOTALL)
    tex6 = re.sub(r'-\n',' ',tex5,re.DOTALL )
    text_list_clean.append(tex6)


# The following code is used to clean the text of the unicode values which may have been not read and coverted properly by the pdf reader. So we have found the possible values of the encoding and we substitute them into the text instead of the unicode using the sub function from the re library. We also clean the new line characters from the text.

# In[ ]:


text_list1 = []
#intializing list
for v1 in text_list_clean:
    v2 = re.findall(r'Paper Body(.+) References', v1,re.DOTALL)
    for v3 in v2:
        text_list1.append(v3)


# The resulting list text_list1 contains all the text that was found between the string "Paper Body" and the string "References" in each item of the text_list_clean list.

# In[ ]:


text_abstract = []
#intializing list
for v1 in text_list_clean:
    v2 = re.findall(r'Abstract(.+)Paper Body', v1,re.DOTALL)
    for v3 in v2:
        text_abstract.append(v3)


# The resulting list text_abstract contains all the text that was found between the string "Abstract" and the string "Paper Body" in each item of the text_list_clean list.

# <div class="alert alert-block alert-warning">
#     
# ### 4.1. Tokenization <a class="anchor" name="tokenize"></a>

# Tokenization is a principal step in text processing and producing unigrams and bigrams. In this section we will be doing that

# In[ ]:


sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
#loading the ntlk pre trained data model for sentence segmentation 
for index,i20 in enumerate(text_list1):
    e2 = sent_detector.tokenize(i20.strip())
    for i, e3 in enumerate(e2):
        if e2[i][0].isupper():
            e4 = e2[i].split()
            e5 = list(e4[0])
            e5[0] = e5[0].lower()
            e5 = ''.join(e5)
            e4[0] = e5
            e2[i] =  ' '.join(e4)
    text_list1[index] = ' '.join(e2)  


# In the first line of code we load a pre-trained sentence tokenizer for English language, which is stored as a pickle file and is called punkt. We then use this tokenize the text into sentences and then check if the start of every sentence is in upper case using the isupper function and slicing the data. If it is upper then we convert it to lower case and replace its value with this. Then we just rejoin all of the tokens again to the text for each paper body in the list. 

# In[ ]:


tok_all = []
#we can get this list by using the chain command on the token_all list but we will still use this list as it saves us time as  
#compared to repeatedly chaining the token_all list. In a way this list is optional but still included.
tokens_all = []
#intializing list
tokenizer = RegexpTokenizer(r"[A-Za-z]\w+(?:[-'?]\w+)?")
for x39 in text_list1:
    tokens = tokenizer.tokenize(x39)
    tokens_all.append(tokens)
    for tok in tokens:
        tok_all.append(tok)


# We tokenize all the words in text using the regex given to us and save it in two list, one a nested list and the other a flat list. 

# <div class="alert alert-block alert-warning">
#     
# ### 4.2. Finding First 200 Bigrams and Stopword Removal<a class="anchor" name="bigrams"></a>

# One of the tasks is to find the first 200 bigrams based on frequency. These bigrams should also be included in our vocabulary list. .....

# In[ ]:


stopwords = open('stopwords_en.txt')
#loading the stopword file
stopword = []
#intializing list
for line in stopwords:
    stopword.append(line)
stopword1 = []
for x in stopword:
    y = re.sub('\n','',x)
    stopword1.append(y)


# The following code is used to load the stopword text file and clean it by removing the next line character \n and then appending it into a list stopword1 to be used later for removing stop words.

# In[ ]:


bigram_measures = nltk.collocations.BigramAssocMeasures()
bigram_finder = nltk.collocations.BigramCollocationFinder.from_words(tok_all)
top_200_bigrams = bigram_finder.nbest(bigram_measures.pmi, 200) 


# The first line creates an instance of the BigramAssocMeasures class from the nltk.collocations module. This class provides different metrics to measure the association between bigrams, such as pmi. The second line creates an instance of the BigramCollocationFinder class which is initialized with the words in the tok_all list. This class finds bigrams in the given list  of words. The third line uses the nbest() method of the BigramCollocationFinder object to find the top 200 bigrams based on their significance score. The pmi metric is used to calculate the significance score for each bigram. The resulting list top_200_bigrams contains the 200 most significant bigrams in the tok_all text. 

# In[ ]:


mwetokenizer = MWETokenizer(top_200_bigrams,separator='__')
mwe_list = []
#intializing list
for tk in tokens_all:
    mwetokenizer2 = mwetokenizer.tokenize(tk)
    mwe_list.append(mwetokenizer2)


# Having found the top 200 meaningful bigrams, we use the MWETokenizer constructor which takes two arguments: the first argument is a list of MWEs and the second argument is a separator string that is used to join the words in each MWE. We use the  top_200_bigrams which is a list of the top 200 most significant bigrams in the text obtained before and the separator argument is set to '__'.  

# The MWETokenizer object is then used to tokenize the tokens again. The tokenize() method of the MWETokenizer object is called for each word in the text, which returns a list of tokens that have been split and joined based on the MWEs. These tokenized sentences are stored in mwe_list which is a list of lists of tokens. 

# In[ ]:


stopwords_set = set(stopword1)
stopped_list = []
for x20 in mwe_list:
    stopped_tokens = [w for w in x20 if w not in stopwords_set]
    stopped_list.append(stopped_tokens)    


# Here we convert the list of stopwords to a set for faster processing and then we use list comprehension to make a new list stopped_list without the stopwords. 

# In[ ]:


to_remove = []
#intializing list
flat_list = [element for sublist in stopped_list for element in sublist]
#converting the nested list stopped_list into a flat list
for x77 in set(flat_list):
    #using set of flat_list to faster processing
    x88 = 0
    x89 = 0
    #instializing the value to 0 for every word 
    for x78 in stopped_list:
        if x77 in x78:
            x88 = x88 + 1
            #calucating the top 95% occuring words by checking in tokens of each document and adding a 1 if pressent
        if x77 not in x78:
            x89 = x89 + 1
            #calucating the rarely occuring words by checking in tokens of each document and adding a 1 if not present
    if x88 > 189:
        #190/200 = 95 so greater than 189
        to_remove.append(x77)
    if x89 > 194:
        #5/200 = 2.5 so greater than 195
        to_remove.append(x77)


# here we convert the nested list stopped_list into a flat list and iterate through its set for faster processing. We then create a list to remove to store all the token to be removed after performing our calucations. We compare each token in a set of flat list to all tokens in each document to get the token occuring in 95 or more percent of the documents and those occuring in less than 3% of the documnents. As 90/200 = 95 so greater than 189 and 5/200 = 2.5 so greater than 195. 

# In[ ]:


#intializing list
stopped_list2 = []
for x82 in stopped_list:
    stopped_list3 = []
    for x83 in x82:
        if x83 not in to_remove:
            if len(x83) > 2:
                #removing tokens which are smaller than three characters
                stopped_list3.append(x83)
    stopped_list2.append(stopped_list3)


# Here we remove the tokens we found out are to be removed in the step above we iterate through each token and append those which are not in to_remove. We also then remove the tokens which are smaller than three characters and append all of this into nested list stopped_list2 for all the token of each document. 

# In[ ]:


stemmer = PorterStemmer()
stemmed_words = []
#intializing list
for ste in stopped_list2:
    stemmed_words1 = []
    for stem in ste:
        if '__' not in stem:
            stemmed_words1.append(stemmer.stem(stem))
        else:
            stemmed_words1.append(stem)
    stemmed_words.append(stemmed_words1)        


# Here we initialize an empty list called "stemmed_words" to store the stemmed versions of the words. The outer for-loop iterates through each list in the "stopped_list2" list. The inner for-loop iterates through each word in the current list, and checks if it contains a double underscore __ using an "if" statement. If the word does not contain it it is stemmed using the PorterStemmer algorithm and added to a temporary list called "stemmed_words1". If it does contain __ then the word is not stemmed and is simply added to "stemmed_words1" as specified in the specifications.

# In[ ]:


flat_list = [element for sublist in stemmed_words for element in sublist]
flat_list = sorted(set(flat_list))


# Now we convert this nested list of tokens of each document into a flat list and then make it a set and then use sorted to convert it into a sorted list for creating the vocab file.

# Calucating Document Frequency and count vectorizer

# In[ ]:


new = []
for stemmm in stemmed_words:
    fd_2 = FreqDist(stemmm)
    #getting freqdist of each word in the respective document 
    new_1 = fd_2.most_common()
    new.append(new_1)


# For each "stemmm" list, a FreqDist object is created using the FreqDist() method, it takes a list of tokens of each document and returns a frequency distribution of the tokens, where the keys are the unique tokens and the values are the number of times each token appears in the list. The most_common() method is then called on the FreqDist object to obtain a list of tuples, where each tuple contains a token and its frequency in descending order and the list of tuples is appended to the "new" list using the append() method.

# MOST COMMON TERMS IN ABSTRACT

# In[ ]:


sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
for index,i20 in enumerate(text_abstract):
    e2 = sent_detector.tokenize(i20.strip())
    for i, e3 in enumerate(e2):
        if e2[i][0].isupper():
            e4 = e2[i].split()
            e5 = list(e4[0])
            e5[0] = e5[0].lower()
            e5 = ''.join(e5)
            e4[0] = e5
            e2[i] =  ' '.join(e4)
    text_abstract[index] = ' '.join(e2)  


# In the first line of code we load a pre-trained sentence tokenizer for English language, which is stored as a pickle file and is called punkt. We then use this tokenize the text into sentences and then check if the start of every sentence is in upper case using the isupper function and slicing the data. If it is upper then we convert it to lower case and replace its value with this. Then we just rejoin all of the tokens again to the text for each abstract in the list.

# In[ ]:


tokens_abstract = []
tokenizer = RegexpTokenizer(r"[A-Za-z]\w+(?:[-'?]\w+)?")
for x39 in text_abstract:
    tokens = tokenizer.tokenize(x39)
    tokens_abstract.append(tokens)


# We tokenize all the words using the regex give to us and tokenize each word in all the abstracts and store it into a list token abstract. 

# In[ ]:


stopwords_set = set(stopword1)
stopped_listab = []
for x20 in tokens_abstract:
    stopped_tokens = [w for w in x20 if w not in stopwords_set]
    stopped_listab.append(stopped_tokens) 


# Here we convert the list of stopwords to a set for faster processing and then we use list comprehension to make a new list stopped_list without the stopwords. 

# In[ ]:


freq_ab = []
flat_listab = [element for sublist in stopped_listab for element in sublist]
fd_2 = FreqDist(flat_listab)
new_1 = fd_2.most_common(10)
common_ab = [nw[0] for nw in new_1]
#we get a the top 10 words without the count


# We get the frequency distribution of the top ten words in the abstract and save it into a variable

# MOST COMMON TERMS IN TITLES

# In[ ]:


text_listtitle = []
for v1 in text_list_clean:
    v2 = re.findall(r'^(.+)Authored by', v1,re.DOTALL)
    for v3 in v2:
        text_listtitle.append(v3.lower())


# The resulting list text_listtitle contains all the text that was found before the string "Authored by" in each document of the text_list_clean list.

# In[ ]:


tokens_title = []
tokenizer = RegexpTokenizer(r"[A-Za-z]\w+(?:[-'?]\w+)?")
for x39 in text_listtitle:
    tokens = tokenizer.tokenize(x39)
    tokens_title.append(tokens)


# We tokenize all the words using the regex give to us and tokenize each word in all the abstracts and store it into a list tokens_title. 

# In[ ]:


stopped_listtitle = []
#removing the stop words
for x20 in tokens_title:
    stopped_tokens = [w for w in x20 if w not in stopwords_set]
    stopped_listtitle.append(stopped_tokens) 


# removing the stop words

# In[ ]:


freq_title = []
flat_listtitle = [element for sublist in stopped_listtitle for element in sublist]
fd_3 = FreqDist(flat_listtitle)
new_2 = fd_3.most_common(10)
common_tittle = [nw[0] for nw in new_2]
#we get a the top 10 words without the count


# We get the frequency distribution of the top ten words in the title and saving it into a variable

# MOST COMMON AUTHORS

# In[ ]:


text_author = []
for v1 in text_list_clean:
    v2 = re.findall(r'Authored by:(.+?)Abstract', v1,re.DOTALL)
    for v3 in v2:
        v4 = re.sub(r'\?', 'e',v3)
        text_author.append(v4)


# The resulting list text_abstract contains all the text that was found between the string "Authored by" and the string "Abstract" in each item of the text_list_clean list.

# In[ ]:


tokens_author = []
tokenizer = RegexpTokenizer(r"[A-Za-z]\w+(?:[-'?]\w+)?")
for x39 in text_author:
    tokens = tokenizer.tokenize(x39.lower())
    tokens_author.append(tokens)
flat_author = [element for sublist in tokens_author for element in sublist]    


# Tokenizing the authors and the saving as a flat list of all the tokens 

# In[ ]:


bigram_measures = nltk.collocations.BigramAssocMeasures()
bigram_finder = nltk.collocations.BigramCollocationFinder.from_words(flat_author)
top_20_bigrams = bigram_finder.nbest(bigram_measures.pmi, 10) 
top_10_authors = [nw[0].capitalize() + ' '+ nw[1].capitalize() for nw in top_20_bigrams]


# In[ ]:





# #### Whatever else <a class="anchor" name="whatev1"></a>

# <div class="alert alert-block alert-success">
#     
# ## 5. Writing Output Files <a class="anchor" name="write"></a>

# files need to be generated:
# * Vocabulary list
# * Sparse matrix (count_vectors)
# * Statistics matrix
# 
# This is performed in the following sections.

# <div class="alert alert-block alert-warning">
#     
# ### 5.1. Vocabulary List <a class="anchor" name="write-vocab"></a>

# List of vocabulary should also be written to a file, sorted alphabetically, with their reference codes in front of them. This file also refers to the sparse matrix in the next file. For this purpose, .....

# In[ ]:


x = open('tast2_31339646_vocab.txt', 'a+')
for ind,li in enumerate(flat_list):
    x99 = f'{li}:{ind}' + '\n'
    x.write(x99)
x.close()    


# The first line of the code opens the file "task2.txt" in append mode using the 'a+' flag. This mode allows data to be appended to the file if it already exists, and creates a new file if it does not. The code then uses a for-loop to iterate through a list called "flat_list" and assigns each value to the variable "li" and its index to the variable "ind". Inside the loop, a new string is created called "x99" that concatenates the value of "li" and its corresponding index. The string" is then written to the file using the write() method. Once the loop has finished iterating through all values in "flat_list", the file is closed using the close() method to ensure all data has been written to the file.

# <div class="alert alert-block alert-warning">
#     
# ### 5.2. Count Vectorizer <a class="anchor" name="write-sparseMat"></a>

# For writing sparse matrix for a paper, we firstly calculate the frequency of words for that paper ....

# In[ ]:


x2 = open('tast2_31339646_count_vectors.txt', 'a+')
for iidx,new1 in enumerate(new):
    x111 = 0
    for x999 in new1:
        if x111 == 0:
            x997 = f'\n{doc_names[iidx]}'
            x2.write(x997)
            x111 = 1
        x998 = ', ' + f'{flat_list.index(x999[0])} : {x999[1]}'
        x2.write(x998)
x2.close()    


# The code is appending the most common words and their frequencies for each document in "new" to a text file called "tast2_31339646_count_vectors.txt" in a specific format, where each entry corresponds to a document and its most common words and their frequencies.

# <div class="alert alert-block alert-warning">
#     
# ### 5.3. Most Common CSV <a class="anchor" name="write-sparseMat"></a>

# For writing overall statistics of papers, we aggregate statistics as follows......

# In[ ]:


dic = {'top_ten_terms_in_abstract' : common_ab, 'top_ten_terms': common_tittle, 'top10_authors': top_10_authors}
df5 = pd.DataFrame(dic)
df5.to_csv('task2_31339646_stats.csv',index=False)


# Here we save the three columns in the form of a dictionary and make it into a dataframe and then convert it into a csv using to csv

# -------------------------------------

# -------------------------------------

# <div class="alert alert-block alert-success">
#     
# ## 7. References <a class="anchor" name="Ref"></a>

# [1] 3. Data model,https://docs.python.org/3.9/reference/datamodel.html#object.__contains__
# 
# 

# ## --------------------------------------------------------------------------------------------------------------------------

# In[ ]:




