#!/usr/bin/env python
# coding: utf-8

# In[1]:


#pip install transformers


# In[2]:


#pip install nlp


# In[8]:


#pip install torch


# In[3]:


from transformers import pipeline


# In[4]:


nlp = pipeline("question-answering")


# In[10]:


from context import context


# In[16]:


import pickle


# In[22]:


#print(model(question="What was scholl grade of abdul kalam?", context=context)['answer'])


# In[55]:


def pred(input_text):
    return (nlp(question=input_text, context=context)['answer'])
     
    


# In[40]:


#pred("What was scholl grade of abdul kalam?")


# In[57]:


pickle.dump(pred, open('model.pkl','wb'))


# In[58]:


#predict = pickle.load(open('model.pkl','rb'))


# In[59]:


#predict("what was abdul kalams fathers name?")


# In[ ]:




