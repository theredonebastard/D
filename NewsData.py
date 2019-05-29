class NewsData:
    
    links = []
    articles = []
    preparedArticles = []
    

    def loadFromFile(self, path='', filename=''):
        articles = pd.read_csv(path + '/' + filename, encoding = "ISO-8859-1")
        for index, article in articles.iterrows():
            if ((not ('publish_date' in article['publish_date']) and (isinstance(article['text'], str)))):
                article['publish_date'] = datetime.strptime(article['publish_date'][0:10], "%Y-%m-%d").date()
                self.articles.append(
                    PlainArticle(
                        title = article['title'],
                        text = article['text'],
                        keywords = article['keywords'],
                        summary = article['summary'],
                        publish_date = article['publish_date']
                    )
                )
       
    
    def loadFromWeb(self, linksNumber=50, sourcesToBan = ['www.ccn.com']):
        
        self._parseLinks(linksNumber)
        self._filterLinks(sourcesToBan)
                
        print('Found ' + str(len(self.links)) + ' links')
        
        self._downloadNews()
    
    def prepare(self):
        print('preparing')
        self._prepare()
    
    
    def writeToFile(self, path='', filename='', prepared=True):
        if (not (os.path.exists(path))):
            os.makedirs(path, exist_ok=True)
        
        if (prepared): 
            articles = self.preparedArticles
        else:
            articles = self.articles
        
        df = pd.DataFrame(articles)
        df.to_csv(path + '/' + filename, index=None, mode='w')

        print(str(len(articles)) + ' news stored')
        
    def _parseLinks(self, linksNumber = 50):
        flag = True
        i = 0
        
        while(i < linksNumber):
            try:
                url = "https://bitcointicker.co/news/loadnews.php?start=" + str(i)
                print(url)
                
                response = urlopen(url).read()
                
                if (response == b'\n'):
                    flag = False
                    print('empty')
                else:
                    print('not empty')
                    
                    html = response
                    soup = BeautifulSoup(html, 'html.parser')
                    self.links.extend(soup.findAll('a', attrs={'data-disqus-identifier': False}))
                    i += 50
            except HTTPError:
                print('HttpError')
                i+=1
                
    def _filterLinks(self, sources = []):
        for source in sources:
            self.links = [link['href'] for link in self.links if (not(source in link['href']))]
        
    def _downloadNews(self):
        doneCounter = 0
        linksCount = len(self.links)
        
        for link in self.links:
            try:
                article = Article(link, fetch_images=False, request_timeout=10)
                article.download()
                article.parse()
                
                if (article.publish_date == None):
                    article.publish_date = datetime.today()
                    
                article.nlp()
                self.articles.append(
                    PlainArticle(
                        title = article.title,
                        text = article.text,
                        keywords = article.keywords,
                        summary = article.summary,
                        publish_date = article.publish_date.date()
                    )
                )
                
                
                doneCounter += 1
                
                if (doneCounter % 10 == 0):
                    print(str(linksCount - doneCounter) + ' news left...')
                    
            except ArticleException:
                pass
            
        print('Downloaded ' + str(len(self.articles)) + " news \n")
        
   
   
    
    def _prepare(self):
        print('cleaning')
        snow_stemmer = nltk.stem.SnowballStemmer("english")
        counter = 0
        keys = []
        values = [0 * len(self.articles)]
        for article in self.articles:
            article_text = article.text
            article_text = article_text.lower()                 # Converting to lowercase
            cleaner = re.compile('<.*?>')
            article_text = re.sub(cleaner, ' ', article_text)        #Removing HTML tags
            article_text = re.sub(r'[?|!|\'|"|#]',r'',article_text)
            article_text = re.sub(r'[.|,|)|(|\|/|:|;]',r' ',article_text)        #Removing Punctuations
            words = [snow_stemmer.stem(word) for word in article_text.split() if word not in stopwords.words('english')]   # Stemming and removing stopwords
            date = str(article.publish_date)
            if (date not in keys):
                keys.append(date)
            
            
            if ( not values[keys.index(date)]):
                values.insert(keys.index(date), '')
                
            values[keys.index(date)] += ' '.join(word for word in words)
            
            counter += 1
            if (counter % 50 == 0):
                    print(str(len(self.preparedArticles)-counter) + " articles left...")
                    
        temp_dict = {}
        for i in range(0, len(keys) - 1):
            temp_dict.update({keys[i]: [values[i]]})
            
        self.preparedArticles = pd.DataFrame.from_dict(temp_dict)
        print(self.preparedArticles)
