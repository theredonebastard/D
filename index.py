import os
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import ast


from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM


from scipy.stats import zscore


import newspaper
from newspaper import Article, ArticleException

import csv

from datetime import datetime
from datetime import timedelta

from bs4 import BeautifulSoup
import json
import urllib
from urllib.request import urlopen
from urllib import request, parse
from urllib.error import HTTPError

import nltk                                         #Natural language processing tool-kit
import re
from nltk.corpus import stopwords                   #Stopwords corpus
from nltk.stem import PorterStemmer                 # Stemmer

from sklearn.feature_extraction.text import CountVectorizer          #For Bag of words
from sklearn.feature_extraction.text import TfidfVectorizer          #For TF-IDF
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import SGDClassifier,LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix






import gensim
import gensim.corpora as corpora
from gensim import models, similarities
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.models import Word2Vec 
from gensim.summarization import keywords

import pyLDAvis
import pyLDAvis.gensim  # don't skip this

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

%matplotlib inline

import NewsBitcoinClassifier
import LSTMClassifier
