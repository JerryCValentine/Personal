import numpy as np 
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import collections
import pandas as pd
from datetime import datetime

# Super class for machine learning models 

class BaseModel(ABC):
    """ Super class for ITCS Machine Learning Class"""
    
    @abstractmethod
    def train(self, X, T):
        pass

    @abstractmethod
    def use(self, X):
        pass

    
class LinearModel(BaseModel):
    """
        Abstract class for a linear model 
        
        Attributes
        ==========
        w       ndarray
                weight vector/matrix
    """

    def __init__(self):
        """
            weight vector w is initialized as None
        """
        self.w = None

    # check if the matrix is 2-dimensional. if not, raise an exception    
    def _check_matrix(self, mat, name):
        if len(mat.shape) != 2:
            raise ValueError(''.join(["Wrong matrix ", name]))
        
    # add a basis
    def add_ones(self, X):
        """
            add a column basis to X input matrix
        """
        self._check_matrix(X, 'X')
        return np.hstack((np.ones((X.shape[0], 1)), X))

    ####################################################
    #### abstract funcitons ############################
    @abstractmethod
    def train(self, X, T):
        """
            train linear model
            
            parameters
            -----------
            X     2d array
                  input data
            T     2d array
                  target labels
        """        
        pass
    
    @abstractmethod
    def use(self, X):
        """
            apply the learned model to input X
            
            parameters
            ----------
            X     2d array
                  input data
            
        """        
        pass 

# Linear Regression Class for least squares
class LinearRegress(LinearModel): 
    """ 
        LinearRegress class 
        
        attributes
        ===========
        w    nd.array  (column vector/matrix)
             weights
    """
    def __init__(self):
        LinearModel.__init__(self)
        
    # train lease-squares model
    def train(self, X, T):
        X = self.add_ones(X)
        if(self.w is None):
            self.w = np.zeros(X.shape[1])
        self.w = np.reshape(self.w, (self.w.shape[0],1))
        self.w = np.linalg.inv(X.T @ X) @ X.T @ T
    
    # apply the learned model to data X
    def use(self, X):
        X = self.add_ones(X)
        return X @ self.w

# LMS class 
class LMS(LinearModel):
    """
        Lease Mean Squares. online learning algorithm
    
        attributes
        ==========
        w        nd.array
                 weight matrix
        alpha    float
                 learning rate
    """
    def __init__(self, alpha):
        LinearModel.__init__(self)
        self.alpha = alpha
    
    # train LMS model one step 
    # here the x is 1d vector
    def train_step(self, x, t):
        x = np.hstack((1, x))
        if(self.w is None):
            self.w = np.zeros(x.shape)
        self.w = np.reshape(self.w, (self.w.shape[0],1))
        x = np.reshape(x, (-1, 1))
        # t = np.reshape(t, (1, 1))
        self.w = self.w - self.alpha * ((self.w.T @ x) - t) * x

    # batch training by using train_step function
    def train(self, X, T):
        if(type(X) is pd.core.frame.DataFrame):
            X = X.values
        for K in range(X.shape[0]):
            self.train_step(X[K], T[K])
    
    # apply the current model to data X
    def use(self, X):
        X = self.add_ones(X)
        return X @ self.w

""" partitioning data

    parameters
    -----------
    X        pd.DataFrame
             input data to partition
    T        pd.DataFrame
             target labels to partition
    raito    list
             list of ratios for partitions (should be summed to 1) 
             the number of return pairs are different
"""
def partition(X, T, ratio=[0.8, 0.2]): 
    
    # Checks to make sure ratio sums to 1
    assert(np.sum(ratio) == 1)
    
    # Shuffle the data indices 
    idxs = np.random.permutation(X.index)
    
    # Store the number of data samples 
    N = X.shape[0]
    
    Xs = []
    Ts = []
    i = 0  # first index to zero
    for k, r in enumerate(ratio):
         # Number of rows that corresponds to kth element in ratios
        nrows = int(round(N * r)) 
        
        # If we are on the last ratio simply use the remaining data samples
        if k == len(ratio)-1:
            Xs.append(X.iloc[i:, :])
            Ts.append(T.iloc[i:, :])
        else:
            Xs.append(X.iloc[i:i+nrows, :])
            Ts.append(T.iloc[i:i+nrows, :])
        
        i += nrows
    
    return Xs, Ts

## LINEAR REGRESSION ON DATA ##

# Load Data
df = pd.read_csv("D:\\School Work\\Machine Learning\\Metro_Interstate_Traffic_Volume.csv")

# Convert Strings to ints
# holidaydic = {'None': 0, 'Columbus Day': 1, 'Veterans Day': 2, 'Thanksgiving Day': 3, 'Christmas Day': 4, 'New Years Day': 5, 'Washingtons Birthday': 6, 'Memorial Day': 7, 'Independence Day': 8, 'State Fair': 9, 'Labor Day': 10, 'Martin Luther King Jr Day': 11}
# weatherdic = {'Clear': 0, 'Clouds': 1, 'Drizzle': 2, 'Mist': 3, 'Rain': 4, 'Thunderstorm': 5, 'Haze': 6, 'Fog': 7, 'Snow': 8, 'Squall': 9, 'Smoke': 10}

# df.holiday = df.holiday.apply(lambda s: holidaydic[s])
# df.weather_main = df.weather_main.apply(lambda s: weatherdic[s])
df.date_time = df.date_time.apply(lambda s: datetime.timestamp(datetime.strptime(s, "%Y-%m-%d %H:%M:%S")))

# Adding Indicators

indicatorHoliday = pd.get_dummies(df.loc[:, 'holiday'])
indicatorWeather = pd.get_dummies(df.loc[:, 'weather_main'])

df = pd.concat([
        indicatorHoliday,
        df.iloc[:, 1:4], 
        indicatorWeather,
        df.iloc[:, -3:]],
        axis=1)

print(df)

# Get rid of bad data
df = df[df.temp != 0] # Null values 
df = df[df.date_time > 1434063600] # Get rid of gap in time

X = df.iloc[:, :-1].copy()
X = X.drop('weather_description', axis=1) # not great feature

normX = (X-np.mean(X, axis=0))/np.std(X, axis=0)

T = df.iloc[:, -1].copy()
Tlog = np.log(T + 1)

Tlog = Tlog.to_numpy()

lsModel = LinearRegress()
lsModel.train(normX, Tlog)
Y = lsModel.use(normX)

Tlog = Tlog.reshape((Tlog.shape[0], 1))
Y = Y.reshape((Y.shape[0], 1))

E = np.subtract(Tlog, Y)
squaredE = (np.subtract(Tlog, Y))**2
R2 = 1 - np.divide(np.square(np.subtract(Tlog, Y)), np.square(np.subtract(Tlog, Tlog.mean())))
MSE = np.square(np.subtract(Tlog, Y)).mean()
MAE = np.square(np.abs(np.subtract(Tlog, Y))).mean()
RMSE = np.sqrt(np.square(np.subtract(Tlog, Y)).mean())

print(E)
print(squaredE)
print(R2)
print(MAE)
print(MSE)
print(RMSE)

plt.plot(Tlog, 'ob')
plt.plot(Y, 'xr')
plt.show()

lsModel = LMS(.000055)
lsModel.train(normX, Tlog)
Y = lsModel.use(normX)

Tlog = Tlog.reshape((Tlog.shape[0], 1))

E = np.subtract(Tlog, Y)
squaredE = (np.subtract(Tlog, Y))**2
R2 = 1 - np.divide(np.square(np.subtract(Tlog, Y)), np.square(np.subtract(Tlog, Tlog.mean())))
MSE = np.square(np.subtract(Tlog, Y)).mean()
MAE = np.square(np.abs(np.subtract(Tlog, Y))).mean()
RMSE = np.sqrt(np.square(np.subtract(Tlog, Y)).mean())

print(E)
print(squaredE)
print(R2)
print(MAE)
print(MSE)
print(RMSE)

plt.plot(Tlog, 'ob')
plt.plot(Y, 'xr')
plt.show()

# Testing data LS

Tlog = pd.DataFrame(data=Tlog[:])
Xlst, Tlst = partition(normX, Tlog)

XTrain = Xlst[0] 
XTest = Xlst[1]
TTrain = Tlst[0]
TTest = Tlst[1]

XTrain = XTrain.values
TTrain = TTrain.values

lsModel = LinearRegress()
lsModel.train(XTrain, TTrain)
Y = lsModel.use(XTest)

TTest = TTest.reset_index(drop=True)

plt.plot(TTest, 'ob')
plt.plot(Y, 'xr')
plt.show()

## TESTING LMS

Tlog = pd.DataFrame(data=Tlog[:])
Xlst, Tlst = partition(normX, Tlog)

XTrain = Xlst[0] 
XTest = Xlst[1]
TTrain = Tlst[0]
TTest = Tlst[1]

XTrain = XTrain.values
TTrain = TTrain.values

lsModel = LMS(.000055)
lsModel.train(XTrain, TTrain)
Y = lsModel.use(XTest)

TTest = TTest.reset_index(drop=True)

plt.plot(TTest, 'ob')
plt.plot(Y, 'xr')
plt.show()
