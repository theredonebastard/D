class LSTMClassifier:
    
    data = []
    scaled = []
    
    
    def setData(self, data):
        self.data = data
        
    def showInfo(self):
        print(self.data.head(20))
        print(pd.isnull(self.data).sum())
        print(self.data.shape)
        
#         PLOTS
        fig = plt.figure(figsize=[15, 7])
        plt.suptitle('Bitcoin exchanges, mean USD', fontsize=22)

        plt.subplot(221)
        plt.plot(self.data.Price, '-', label='Price')
        plt.legend()
        
        plt.subplot(222)
        plt.plot(self.data['Vol.'], '-', label='Volume')
        plt.legend()
        
        plt.subplot(223)
        plt.plot(self.data['Change %'], '-', label='Change')
        plt.legend()

        plt.show()
        
        print(self.data.Price.values)
        
    def _create_dataset(self, dataset, look_back=1):
        dataX, dataY = [], []
        for i in range(len(dataset) - look_back):
            a = dataset[i:(i + look_back), 0]
            dataX.append(a)
            dataY.append(dataset[i + look_back, 0])
        print(len(dataY))
        return np.array(dataX), np.array(dataY)

    def scale(self, attribute='Price', feature_range=(0,1)):
        values = self.data[attribute].values.reshape(-1,1)
        values = values.astype('float32')
        scaler = MinMaxScaler(feature_range)
        self.scaled = scaler.fit_transform(values)
        
    def split(self, train_percent=0.7, look_back=1):
        scaled_len = len(self.scaled)
        train_size = int(scaled_len * train_percent)
        test_size = scaled_len - train_size
        train, test = self.scaled[0:train_size,:], self.scaled[train_size:scaled_len,:]
        print('train test lengths:')
        print(len(train), len(test))

        self.trainX, self.trainY = self._create_dataset(train, look_back)
        self.testX, self.testY = self._create_dataset(test, look_back)

        self.trainX = np.reshape(self.trainX, (self.trainX.shape[0], 1, self.trainX.shape[1]))
        self.testX = np.reshape(self.testX, (self.testX.shape[0], 1, self.testX.shape[1]))
        
    def classify(self, hidden_size=100):
        model = Sequential()
        model.add(LSTM(hidden_size, input_shape=(self.trainX.shape[1], self.trainX.shape[2])))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        self.history = model.fit(self.trainX, self.trainY, epochs=500, batch_size=100, validation_data=(self.testX, self.testY), verbose=2, shuffle=False)
        self.predict = model.predict(self.testX)