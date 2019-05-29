class BitcoinPreprocessor:
    
    data = []
    deltas = []
    
    def setData(self, data):
        self.data = data
        
    def _filter(self, attribute, date):
        filteredData = pd.DataFrame(self.data.loc[self.data.Date == date])
        return list(filteredData[attribute])
    
    def indicators(self, indicators=[]):
        return
        
    def transform(self):
        return
    
    def calculateDeltas(self, date_from, date_to, news_period, btc_period, attribute="Price"):
        start_date = datetime.strptime(date_from, "%Y-%m-%d").date()
        end_date = datetime.strptime(date_to, "%Y-%m-%d").date() - timedelta(days=news_period)
        period = btc_period + news_period

        current = start_date
        
        while(current <= end_date):
            btc_temp = []

#             print("working with " + str(current))
            current_btc = current + timedelta(days=period)
            delta = self._filter(attribute, str(current_btc))[0]-self._filter(attribute, str(current))[0]
            if (delta >= 0):
                btc_temp.append(1)
            else :
                btc_temp.append(0)

            current = current + timedelta(days=1)

            self.deltas.append(btc_temp)
            
        return self.deltas
            
        
         
    
    def writeToFile(self, path='', filename=''):
        path += '/btcProcessed/'
        df = pd.DataFrame(self.data)
        if (not (os.path.exists(path))):
            os.makedirs(path, exist_ok=True)
        df.to_csv(path + filename, index=None, mode='w')
        
    def readFromFile(self, path='', filename=''):
        self.data = pd.read_csv(path + '/' + filename, encoding = "ISO-8859-1")