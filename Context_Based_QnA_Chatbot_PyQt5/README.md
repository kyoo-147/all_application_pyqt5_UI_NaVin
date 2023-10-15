# Context_Based_QnA_Chatbot_PyQt5
- Question answering Chatbot craeted by using PyQt5 tools, for questions related to particular context 
- Transformaers archetecture used to ceate this bot 
- leaveraged the use of NLP pipeline from Hugging Face


## Content
  * [Visuals](#Visuals)
  * [Context](#Context)
  * [PyQt5 Framework Design](#PyQt5_Framework_Design)
  * [Directory Tree](#directory-tree)
  * [Am I missing Something?](#Am-I-missing-Something?)


## Visuals



[<img target="_blank" src="https://i.imgur.com/Rx9nN7t.png" width=500 height=400>]


## Context
- Here wiki page of Elon Musk is taken as a context to be feed to the transfomers 
- Other contexts such as Books or any other liturature can be given as context , to build QnA bot 

[<img target="_blank" src="https://i.imgur.com/gVj7M10.png" width=400 height=200>]



## Installation
-Install all dependancies using following command after cloning [cloning](https://www.howtogeek.com/451360/how-to-clone-a-github-repository/) the repository:
```bash
pip install -r requirements.txt
```
- One needs PyQt5 to be installed to run QnA framework
- this can be installed through .exe file cant be attached because of big size . (please do contact if ypu need this file)  

## PyQt5 Framework Design
- Basic Framework is Designed using t Designer 
- Themes and Styles are added using Setsyle 

[![]<img target="_blank" src="https://i.imgur.com/H0TXELG.png " width=400 height=300>](https://doc.qt.io/qt-5/qtdesigner-manual.html)




## Directory Tree 
```
├── context.py
├── TransformerQandA.py
├── Askme_Qt_app.py
├── README.md
├── model.pkl
├── requirements.txt
```

- model.pkl is not copied to repo , as size is to huge 
- Please run TransformerQandA.py in your local machine first to get model.pkl 


## Technologies Used

![](https://forthebadge.com/images/badges/made-with-python.svg)

[<img target="_blank" src="https://i.imgur.com/J37eDG4.png" width=170>](https://pypi.org/project/PyQt5/)
[<img target="_blank" src="https://i.imgur.com/zWRUuCJ.jpg" width=170>](https://shecancode.io/huggingface-company-page)
[<img target="_blank" src="https://i.imgur.com/3TWKJ0S.png" width=170>](https://pytorch.org/) 


## Am I missing Something?

- **Nothing is impossible!**
- please open an [issue](https://github.com/kudeore/Context_Based_QnA_Chatbot_PyQt5/issues) and lets make it better together 
- *Bug reports, feature requests, patches, and well-wishes are always welcome.* :heavy_exclamation_mark:
