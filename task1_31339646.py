#!/usr/bin/env python
# coding: utf-8

# <div class="alert alert-block alert-success">
#     
# # FIT5196 Task 1 in Assessment 1
# #### Student Name: Rohan Singh
# #### Student ID: 31339646
# 
# Date: 17-04-2023
# 
# 
# Libraries used:
# * re (for regular expression, installed and imported) 
# * pandas (for data manipulation) 
#     
# </div>

# <div class="alert alert-block alert-danger">
#     
# ## Table of Contents
# 
# </div>    
# 
# [1. Introduction](#Intro) <br>
# [2. Importing Libraries](#libs) <br>
# [3. Examining Patent Files](#examine) <br>
# [4. Loading and Parsing Files](#load) <br>
# $\;\;\;\;$[4.1. Defining Regular Expressions](#Reg_Exp) <br>
# $\;\;\;\;$[4.2. Reading Files](#Read) <br>
# $\;\;\;\;$[4.3. Whatever else](#latin) <br>
# [5. Writing to CSV/JSON File](#write) <br>
# $\;\;\;\;$[5.1. Verification - using the sample files](#test_xml) <br>
# [6. Summary](#summary) <br>
# [7. References](#Ref) <br>

# -------------------------------------

# <div class="alert alert-block alert-warning">
# 
# ## 1.  Introduction  <a class="anchor" name="Intro"></a>
#     
# </div>

# This assessment regards extracting data from semi-sctuctured text files. The dataset contained 500 `.txt` files which included various information about user reviews. In particular, ....

# -------------------------------------

# <div class="alert alert-block alert-warning">
#     
# ## 2.  Importing Libraries  <a class="anchor" name="libs"></a>
#  </div>

# The only permitted packages to be used in this assessment are imported in the following. They are used to fulfill the following tasks:
# 
# * **re:** to define and use regular expressions
# * **pandas:** ...

# In[ ]:


import re
import pandas as pd


# In[ ]:


from google.colab import drive
drive.mount('/content/drive')


# -------------------------------------

# -------------------------------------

# <div class="alert alert-block alert-warning"> 
# 
# ## 3.  Loading and Parsing Files <a class="anchor" name="load"></a>
# 
# </div>

# In this section, the files are parsed and processed. First of all, appropriate regular expressions are defined to extract desired information when reading the files. ....

# In[ ]:


f = open("31339646.txt", "r").read()


# -------------------------------------

# <div class="alert alert-block alert-info">
#     
# ### 3.1. Defining Regular Expressions <a class="anchor" name="Reg_Exp"></a>

# Defining correct regular expressions is crucial in extracting desired information from the text efficiently. ...

# In[ ]:


#This code is used to create a list of all entries by matching all the starting and ending of each xml file in the text.
entries = re.findall(r'<\?xml version="1\.0" encoding="UTF-8"\?>.*?<\/us-patent-grant>', f, re.DOTALL)


# Each item in the list will be a string that contains the entire XML document, including the XML declaration at the beginning and the root element at the end.

# In[ ]:


x= re.findall(r"US[A-Z1][A-Z0-9]\d{6}", f)
l = []
for x1 in x:
    if x1 not in l:
        l.append(x1)


# This regular expression is looking for a string that starts with "US", followed by one uppercase letter or the number 1, followed by another uppercase letter or a digit from 0 to 9, and ends with exactly six digits. The next part of the code is used to create a new list l that contains only the unique elements from an existing list x.

# In[ ]:


y = re.findall(r"<invention-title id.+>(.+)<\/invention-title>", f)
for index, t in enumerate(y):
    if '&#x2018;' and '&#x2019;' in t: 
        t = t.replace('&#x2018;',"\'")
        t = t.replace('&#x2019;',"\'")
        y[index] = t


# This pattern looks for a string that starts with <invention-title id, followed by any number of characters (denoted by the .+), then a >, then a string that ends with </invention-title>. After that if t contains both the two Unicode characters then they are replaced with a \ using the replace method. The updated string t is then assigned to the original list y at the current index using the y[index] = t syntax.

# In[ ]:


e = re.findall(f'<application-reference appl-type="([a-z]+)">', f)
for index,p in enumerate(e):
    if p == "utility":
        e4 = re.search('<kind>B(.)<\/kind>',entries[index])
        #if p is utility then we search the entry of same index as application to get the kind value of B1 or B2 
        if e4[1] == '2':
            #if the kind value is B2 then we print the following code
            e[index] = "Utility Patent Grant (with a published application) issued on or after January 2, 2001."
        else:
            #else the kind value is B1 and we print the following code
            e[index] = "Utility Patent Grant (no published application)"
    elif p == "design":
        e[index] = "Design Patent"
    elif p == "reissue":
        e[index] = "Reissue Patent"
    elif p == "plant":
        e5 = re.search('<kind>B(.)<\/kind>',entries[index])
        #if p is plant then we search the entry of same index as application to get the kind value of B1 or B2 
        if e5[1] == '2':
            #if the kind value is B2 then we print the following code
            e[index] = "Plant Patent Grant (with a published application) issued on or after January 2, 2001"
        else:
            #else the kind value is B1 and we print the following code
            e[index] = "Plant Patent Grant (no published application)"


# This regular expression matches a this pattern within an XML file where the application-reference tag has an attribute appl-type with a value consisting of one or more lowercase letters. The () in the regular expression indicate a capturing group that is used to extract this lowercase letter string.

# In[ ]:





# In[ ]:


b = re.findall("<number-of-claims>(.+)<\/number-of-claims>",f)


# Here we use the following regex to find the total number of claims by matching the number of claims tags the extracting it internal value using a group and assinging the list of value into a variable. 
# 

# In[ ]:


h1 = re.findall(f"<inventors>.*?<\/inventors>",f,re.DOTALL)


# Here we use the following regex to find all the inventors lists in the xml file by matching the starting and closing of the inventors tags and assigning it into a variable h1

# In[ ]:


inventor = []
for h4 in h1:
    h2 = re.findall(r"<inventor .*?<\/inventor>",h4,re.DOTALL)
    inventor.append(h2)


# This code extracts all instances of the inventor tag from a list of inventors and stores them into a list called inventor

# In[ ]:


last_first = []
#initalizing intitial lists
last_first1 = []
for h5 in inventor:
    last_first1 = []
    for h6 in h5:
        h3 = re.findall(r"<last-name>(.+)<\/last-name>\n<first-name>(.+)<\/first-name>", h6, re.DOTALL)
        last_first1.append(h3)
    last_first.append(last_first1)


# The outer loop iterates through each <inventor> tag extracted from the patent file by the previous code. The inner loop iterates through each <inventor> tag's name fields, and extracts the last and first name using regex pattern. The extracted names for each <inventor> tag are then appended to the last_first1 list. Finally, the last_first1 list is appended to the last_first list, which contains the names of all inventors for the patent.

# In[ ]:


last_first4 = []
for i2 in last_first:
    last_first3 = []
    for i3 in i2:
        last_first2 = []
        for i4 in i3:
            print(i4[1] +' ' + i4[0])
            i5 = i4[1] +' ' + i4[0]
            last_first2.append(i5)
        last_first3.append(last_first2)    
    last_first4.append(last_first3)  


# This code initializes an empty list last_first4, then loops through each element i2 in the last_first list. For each i2, it initializes an empty list last_first3, then loops through each element i3 in i2. For each i3, it initializes an empty list last_first2, then loops through each element i4 in i3. For each i4, it concatenates the second element in the string which is the first name with a space and the first element which is the last name), and appends the resulting string i5 to last_first2. Finally, it appends last_first2 to last_first3 and last_first3 to last_first4. The resulting last_first4 list will contain the first and last names of all inventors, with each name represented as a string.

# In[ ]:


citations = []
for e in entries:
    citation = re.findall(r"<us-references-cited>.*?<\/us-references-cited>", e, re.DOTALL)
    citations.append(citation)


# for each entry of xml in the txt file we match the us reference cited tags to get the citaions in a list

# In[ ]:


examiner = []
for c1 in citations:
    if not c1:
        examiner.append(0)
    else:    
        for c2 in c1:
            c10 = re.findall(r"cited by examiner",c2)
            examiner.append(len(c10))


# Here we create a list called examiner that will contain the number of times each patent in citations has been cited by an examiner. We first check if c1 is empty or not, if c1 is empty, it means that the patent has not been cited by anyone, so examiner will append 0. Otherwise, it will loop through each citation c2 for that patent in c1. It will then search for the string "cited by examiner" in c2 using the re.findall() function and store the matches in c10. The length of c10 gives the number of times that the patent has been cited by an examiner, which is then appended to the examiner list.

# In[ ]:


applicant = []
for c1 in citations:
    if not c1:
        applicant.append(0)
    else:    
        for c2 in c1:
            c10 = re.findall(r"cited by applicant",c2)
            applicant.append(len(c10))


# Here we use the same logic as before to create a list called applicant that will contain the number of times each patent in citations has been cited by an applicant. We first check if c1 is empty or not, if c1 is empty, it means that the patent has not been cited by anyone, so applicant will append 0. Otherwise, it will loop through each citation c2 for that patent in c1. It will then search for the string "cited by applicant" in c2 using the re.findall() function and store the matches in c10. The length of c10 gives the number of times that the patent has been cited by an applicant, which is then appended to the applicant list.

# In[ ]:


claims = re.findall(r'<claims id="claims">.*?<\/claims>', f, re.DOTALL)


# Here we match all the claim id tags in the entire text and store them in a list called claims to extract the each claims text for each xml.

# In[ ]:


claims_all = []
for t6 in claims:
    cl = []
    t5 = re.sub(r'<.*?>','',t6)
    alll = re.sub('\n','',t5)
    cl.append(alll)
    claims_all.append(cl)


# Here iternate through the claims list and remove all the html tags and new line characters from it and append it into a new list called claims_all

# In[ ]:


abstracts = []
for c50 in entries:
    c52 = re.findall(r'<abstract id="abstract">.*?</abstract>',c50,re.DOTALL)
    abstracts.append(c52)


# Here iternate through all the entries to match all the abstracts and extract it

# In[ ]:


all_abstracts = []
for c60 in abstracts:
    if not c60:
        all_abstracts.append("NA")
    else:    
        for c61 in c60:
            c62 = re.sub(r'<.*?>','',c61)
            c63 = re.sub('\n','',c62)
            all_abstracts.append(c63)


# In this code we iternate through the list of abstracts we stored in the variable abstracts before and clean up the text by removing HTML tags and newlines using the regular expressions. The cleaned-up text is then appended to the list all_abstracts.

# -------------------------------------

# <div class="alert alert-block alert-warning"> 
# 
# ## 4.  Writing to CSV/JSON File <a class="anchor" name="write"></a>
# 
# </div>

# In[ ]:


#Here we define a dictionary by giving the keys as the name of columns we will need in our dataframe and the list of all values we extracted above as the column values.
uy= {'grant_id': l, 'patent_title': y, 'kind': e, 'number_of_claims': b, 'inventors': last_first4, 'citations_applicant_count': applicant, 'citations_examiner_count': examiner, 'claims_text': claims_all, 'abstract': all_abstracts}
df1 = pd.DataFrame(uy)
df1


# After defining the dictionary we define a dataframe df1 with the dictionary uy as the data and print the data to check it.

# In[ ]:


df1.to_csv("task1_31339646.csv",index=False)


# The following command generates and writes the contents of a pandas DataFrame object df1 to a CSV (Comma-Separated Values) file named "task1_31339646.csv" without including row index values in the file. The first argument "task1_31339646.csv" is the file name and path where the CSV file will be saved. The second argument index=False specifies that row indexes should not be included in the saved CSV file. 

# TO JSON GENERSTOR FILE

# In[ ]:


dict_json = {}
for n1 in range(150):
    dict_json[df1.loc[n1][0]] = { 'patent_title' : df1.loc[n1][1], 'kind': df1.loc[n1][2], 'number_of_claims': df1.loc[n1][3], 'inventors': df1.loc[n1][4], 'citations_applicant_count': df1.loc[n1][5], 'citations_examiner_count': df1.loc[n1][6], 'claims_text': df1.loc[n1][7], 'abstract': df1.loc[n1][8] }    
x67 = str(dict_json)


# Here we define a nested dictionary dict_json and store the patent names as the main key of it and the other attributes as the values of their keys respectively in the same format as the sample output json file. So, the code reads data from a DataFrame df1 which contains information about patents, and creates a dictionary of dictionaries that stores various attributes of each patent. The resulting dict_json dictionary is then serialized to a JSON format using the str function and storing it into the variable x67 as a string.

# In[ ]:


f3 = re.sub(r"'",'"',x67)
f4 = re.sub(r'"s',"'s",f3)
file1 = open('task1_31339646.json',"a+")
file1.write(f4)
file1.close()


# We then take the string x67 we created in the last step and substitute the ' ' with " " for the names of the attributes as given in the sample output json file. We then create a new file 'task1_31339646.json' and write this string to it to get our json file.

# -------------------------------------

# <div class="alert alert-block alert-info">
#     
# ### 5.1. Verification of the Generated CSV/JSON File <a class="anchor" name="test_xml"></a>

# ....

# -------------------------------------

# <div class="alert alert-block alert-warning"> 
# 
# ## 6. Summary <a class="anchor" name="summary"></a>
# 
# </div>

# ....

# -------------------------------------

# <div class="alert alert-block alert-warning"> 
# 
# ## 7. References <a class="anchor" name="Ref"></a>
# 
# </div>

# 
# 
# [1]<a class="anchor" name="ref-2"></a> Why do I need to add DOTALL to python regular expression to match new line in raw string, https://stackoverflow.com/questions/22610247, Accessed 30/08/2022.
# 
# ....
# 

# ## --------------------------------------------------------------------------------------------------------------------------
