import LDAModel

class NewsPreprocessor:
    
    data = []
    combinedData = []
    
    def setData(self, data):
        self.data = data
    
    def getKeywords(self):
        return LDAmodel.topic(self.combinedData)
    
    def readFromFile(self, path='', filename=''):
        self.data = pd.read_csv(path + '/' + filename, encoding='ISO-8859-1')
        
    def writeToFile(self):
        return
        
    def combine(self, date_from, date_to, period):
        start_date = datetime.strptime(date_from, "%Y-%m-%d").date()
        end_date = datetime.strptime(date_to, "%Y-%m-%d").date()

        current = start_date
        end = current + timedelta(days=period)
        
        while(end <= end_date):
            current = start_date
            current_data = ''
            while (current < end):
                current_data += self.data[str(current)]
                current = current + timedelta(days=1)
            self.combinedData.append(current_data[0].split())
            start_date = start_date + timedelta(days=1)
            end = start_date + timedelta(days=period)