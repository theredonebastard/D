class BitcoinData:
    data = []
    
    def load(self, path='', filename = "bitstamp"):
        self.data = pd.read_csv(path + '/' + filename)
        self.attributes = list (self.data.columns.values)
        self.data.Date = pd.to_datetime(self.data.Date, format='%b %d, %Y')
        self.data.Price = self.data.Price.str.replace(',', '').astype(float)
        self.data.Open = self.data.Open.str.replace(',', '').astype(float)
        self.data.High = self.data.High.str.replace(',', '').astype(float)
        self.data.Low = self.data.Low.str.replace(',', '').astype(float)
        
        
    
    def resample(self, period = 'd'):
        self.data.index = self.data.Date
        
        # Resampling to daily frequency
        if (period == "d"):
            self.data = self.data.resample('D').mean()
        # Resampling to monthly frequency
        if (period == "m"):
            self.data = self.data.resample('M').mean()
        # Resampling to annual frequency
        if (period == "a"):
            self.data = self.data.resample('A-DEC').mean()
        # Resampling to quarterly frequency
        if (period == "q"):
            self.data = self.data.resample('Q-DEC').mean()
            
    def _dropNa(self):
        self.data = self.data.dropna(axis=0) 
            
    def prepare(self, methods=['na']):
        if ('na' in methods):
            self._dropNa()
        
    def writeToFile(self, path='', filename=''):
        path += '/btcData/'
        df = pd.DataFrame(self.data)
        if (not (os.path.exists(path))):
            os.makedirs(path, exist_ok=True)
        df.to_csv(path + filename, index=None, mode='w')
        