# Recurrent Neural Network


################################### Importing libraries###################################
# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# Feature Scaling
from sklearn.preprocessing import MinMaxScaler
# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout


################################### Importing the training set ###################################
#dataset_train = pd.read_csv('Google_Stock_Price_Train.csv')
dataset_train = pd.read_csv(r"C:\Users\User\desk\machine_learning\deeplearning-master\deeplearning-master\Part 3 - Recurrent_Neural_Networks\Google_Stock_Price_Train.csv")
training_set = dataset_train.iloc[:, 1:2].values


################################### Pre-processing ###################################
# Feature Scaling
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)

#https://www.udemy.com/le-deep-learning-de-a-a-z/learn/lecture/8859616#overview
# Creating a data structure with 60 timesteps and 1 output
# The neural network will look at the stock values in the last 60 days and from the values of these last 60 days 
# it will predict the next day so 60 days prior to 60 timesteps

X_train = []
y_train = []

for i in range(60, 1258):
    X_train.append(training_set_scaled[i-60:i, 0])
    y_train.append(training_set_scaled[i, 0])
	
X_train, y_train = np.array(X_train), np.array(y_train)	
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1)) # Reshaping


################################### Build the  RNN###################################
# Initialising the RNN
regressor = Sequential()

# Adding the first LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

# Adding a second LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

# Adding a third LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

# Adding a fourth LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

# Adding the output layer
regressor.add(Dense(units = 1))

# Compiling the RNN
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

################################### Run the  model: Fitting the RNN to the Training set ###################################
regressor.fit(X_train, y_train, epochs = 100, batch_size = 32)

################################### Making new predictions ###################################

# Getting the real stock price of 2017
#dataset_test = pd.read_csv('Google_Stock_Price_Test.csv')
dataset_test = pd.read_csv(r"C:\Users\User\desk\machine_learning\deeplearning-master\deeplearning-master\Part 3 - Recurrent_Neural_Networks\Google_Stock_Price_Test.csv")
real_stock_price = dataset_test.iloc[:, 1:2].values

# Getting the predicted stock price of 2017
dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis = 0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)

X_test = []
for i in range(60, 80):
    X_test.append(inputs[i-60:i, 0])
	
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

################################### visualising the results ###################################
# Visualising the results
plt.plot(real_stock_price, color = 'red', label = 'Real Google Stock Price')
plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted Google Stock Price')
plt.title('Google Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
plt.show()
