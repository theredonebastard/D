import BitcoinData
import BitcoinPreprocessor
import NewsData
import NewsPreprocessor

class NewsBitcoinClassifier:
    
    X = []
    
    Y = []
    
    def __init__(self, date_from, date_to, news_window, btc_window):
        self.btcData = BitcoinData()
        self.btcPreprocessor = BitcoinPreprocessor()
        self.newsData = NewsData()
        self.newsPreprocessor = NewsPreprocessor()
        
        self.date_from = date_from
        self.date_to = date_to
        self.news_window = news_window
        self.btc_window = btc_window
        
    def getBTCData(self, path='../input/ryzhbtc', filename='Bitcoin Historical Data - Investing.com.csv', period='d', attribute='Price'):
        self.btcData.load(path, filename)
        self.btcData.prepare()
#         self.btcData.resample(period)
        self.btcPreprocessor.setData(self.btcData.data)
        self.Y = self.btcPreprocessor.calculateDeltas(date_from=self.date_from, date_to=self.date_to, news_period=self.news_window, btc_period=self.btc_window)
    
    def getNewsData(self, file=True, prepare=False, write=True, linksNumber=50, path_from='../input/bitcointicker-articles', filename_from='bitcointicker.csv', path_to='../working', filename_to='bitcointickerPreparedFromFile.csv'):
        if (prepare):
            if (file):
                self.newsData.loadFromFile(path=path_from, filename=filename_from)
            else:
                self.newsData.loadFromWeb(linksNumber)
            self.newsData.prepare()
            if (write):
                self.newsData.writeToFile(path=path_to, filename=filename_to)
            self.newsPreprocessor.setData(self.newsData.preparedArticles)
        else:
            self.newsPreprocessor.readFromFile(path=path_to, filename=filename_to)
        print ('combinig...')
        self.newsPreprocessor.combine(date_from=self.date_from, date_to=self.date_to, period=self.news_window)
        print('getting keywords....')
        self.X = self.newsPreprocessor.getKeywords()
        
    def writeToFile(self):
        df = pd.DataFrame(self.X)
        df.to_csv('X.csv', index=None, mode='w')
        df = pd.DataFrame(self.Y)
        df.to_csv('Y.csv', index=None, mode='w')
    
    def readFromFile(self):
        self.X = pd.read_csv('X.csv', encoding = "ISO-8859-1")
        self.Y = pd.read_csv('Y.csv', encoding = "ISO-8859-1")
        
        
    def _RandomForestClassifier(self, n_estimators=500, max_depth=None, random_state=0, test_size=0.2, sample_weight=None, max_features=50, warm_start=True):
        print ("""
            -----------------
            | RANDOM FOREST |
            -----------------
        """)
        classifier = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state, max_features=max_features, warm_start=warm_start)
        return classifier

    def _GradientBoostingClassifier(self, n_estimators=300, learning_rate=0.8, max_depth=None, random_state=0, sample_weight=None, test_size=0.2, warm_start=True ):
        print ("""
            ---------------------
            | GRADIENT BOOSTING |
            ---------------------
        """)
        classifier = GradientBoostingClassifier(n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth, random_state=random_state, warm_start=warm_start)
        return classifier


    def _SVC(self, gamma='scale', kernel='sigmoid', test_size=0.2, random_state=0, max_iter=8):
        print ("""
            -------
            | SVC |
            -------
        """)
        classifier = svm.SVC(gamma=gamma, kernel=kernel, max_iter=max_iter)
        return classifier
    
    def _SGDClassifier(self, loss='log', penalty='elasticnet', max_iter=500, eta0=0.1, learning_rate='constant', test_size=0.2, random_state=0):
        print ("""
            -----------------
            | SGDClassifier |
            -----------------
        """)
        classifier = SGDClassifier(loss=loss, max_iter=max_iter, eta0=eta0, penalty=penalty, learning_rate=learning_rate)
        return classifier

    def _LogisticRegression(self,random_state=0, solver='lbfgs', multi_class='multinomial' ):
        print ("""
            ----------------------
            | LogisticRegression |
            ----------------------
            """)
        classifier = LogisticRegression(random_state=random_state, solver=solver, multi_class=multi_class)
        return classifier
            
    def ensemble(self, classifiers_names=['RandomForest'], voting='hard', test_size=0.2, random_state=0):
        classifiers = []
        
        if ('RandomForest' in classifiers_names):
            classifiers.append(('rf',  self._RandomForestClassifier()))
            
        if ('GradientBoosting' in classifiers_names):
            classifiers.append(('gb', self._GradientBoostingClassifier()))
            
        if ('SVC' in classifiers_names):
            classifiers.append(('svc', self._SVC()))
            
        if ('SGD' in classifiers_names):
            classifiers.append(('sgd', self._SGDClassifier()))
            
        if ('LogisticRegression' in classifiers_names):
            classifiers.append(('lr', self._LogisticRegression()))
            
        voting_classifier = VotingClassifier(estimators=classifiers, voting=voting)
        
        X_train, X_test, Y_train, Y_test = train_test_split(self.X, self.Y, test_size=test_size, random_state=random_state)
        voting_classifier.fit(X_train, Y_train)
        print('---------SCORE---------')
        print(voting_classifier.score(X_test, Y_test))
        print('---------PREDICT---------')
        self.Y_pred = voting_classifier.predict(self.X)
        print(confusion_matrix(self.Y, self.Y_pred))