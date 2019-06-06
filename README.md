# Development of Software Library for Financial Time Series Forecasting
Ryzh staralsya
Bachelor’s qualifying paper «Development of a Software Library for Financial Time Series Forecasting»
The object of the study is the process of forecasting and classification in machine learning.
The aim of the study is to develop a library of financial time series forecasting.
The methods of research are object oriented analysis, software engineering
methods, data analysis methods.
In a bachelor’s qualifying paper provides an analytical review of recent publications on the financial time series forecasting. Methods of processing and classification of text data are considered. The design of the library for predicting financial values based on the analysis of text news is executed. Tools are implemented for downloading, processing and conducting computations over financial and text data.

# Motivation
Chtoby Ryzha hvalily

# Libraries
[numpy](https://www.numpy.org/)

[pandas](https://pandas.pydata.org/)

[keras](keras.io/)

[scipy](https://www.scipy.org/)

[newspaper3k](https://newspaper.readthedocs.io/en/latest/)

[BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/)

[nltk](https://www.nltk.org/)

[sklearn](https://scikit-learn.org/)

[gensim](https://radimrehurek.com/gensim/)

[pyLDAvis](https://pyldavis.readthedocs.io/en/latest/)

# Features

# Usage Example
```python
btcData = BitcoinData()
btcData.load(path='../input/ryzhbtc', filename='Bitcoin Historical Data - Investing.com.csv')
btcData.prepare()
btcData.resample(period='d')
btcData.writeToFile(path='../working', filename='btcDataresample=d.csv')
```

```python
btcPreprocessor = BitcoinPreprocessor()
btcPreprocessor.readFromFile(path='../working', filename='btcDataresample=d.csv')
btcPreprocessor.calculateDeltas(date_from = '2017-01-01', date_to='2018-12-31', news_period=3, btc_period=2)
btcPreprocessor.writeToFile(path='../working', filename='btcPreproc20180101-20180301p=2.csv')
```

```python
newsData = NewsData()
newsData.loadFromFile(path='../input/bitcointicker-articles', filename='bitcointicker.csv')
newsData.loadFromWeb(linksNumber=1000)
newsData.prepare()
newsData.writeToFile(path='../working', filename='bitcointickerNewsPrepared10000.csv')
```

```python
newsPreproc = NewsPreprocessor(data = [])
newsPreproc.readFromFile(path='../working', filename='bitcointickerNewsPrepared10000.csv')
newsPreproc.combine(date_from='2019-04-29', date_to='2019-05-13', period=3)
vec = newsPreproc.getKeywords()
```

```python
classifier = NewsBitcoinClassifier(date_from='2017-03-01', date_to='2019-02-14', news_window=6, btc_window=1)
classifier.getBTCData()
classifier.getNewsData(prepare=False, file=False, path_to='../input/ryzh-prepared-articles/bitcointickernewsprepared10000', filename_to='bitcointickerNewsPrepared10000.csv')
classifier.ensemble(classifiers_names=['RandomForest', 'GradientBoosting', 'SVC', 'SGD', 'LogisticRegression'])
```

```python
lstm = LSTMClassifier()
lstm.setData(btcData.data)
lstm.scale()
lstm.split()
lstm.classify()
```
