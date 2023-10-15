#!/usr/bin/env python
# coding: utf-8

# In[ ]:

#import wikipedia
#page= wikipedia.WikipediaPage(title='Elon Musk')

#context = r""" page.content """

import wikipedia
page= wikipedia.WikipediaPage(title='Elon Musk')
page= page.content

context = page