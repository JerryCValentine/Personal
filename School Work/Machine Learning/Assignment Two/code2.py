import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from abc import ABC, abstractmethod
from copy import deepcopy as copy
import IPython.display as ipd


# Super class for machine learning models 

class BaseModel(ABC):
    """ Super class for ITCS Machine Learning Class"""
    
    @abstractmethod
    def train(self, X, T):
        pass

    @abstractmethod
    def use(self, X):
        pass

    

class Classifier(BaseModel):
    """
        Abstract class for classification 
        
        Attributes
        ==========
        meanX       ndarray
                    mean of inputs (from standardization)
        stdX        ndarray
                    standard deviation of inputs (standardization)
    """

    def __init__(self, ):
        self.meanX = None
        self.stdX = None

    def normalize(self, X):
        """ standardize the input X """
        
        if not isinstance(X, np.ndarray):
            X = np.asanyarray(X)

        # store the mean and std from the training set
        # when you learned mean & std, we do not update for test
        if self.meanX is None:
            self.meanX = np.mean(X, 0)
            self.stdX = np.std(X, 0)

        Xs = copy(X)
        Xs[:, 0] = (Xs[:, 0] - self.meanX[0]) / self.stdX[0] 
        Xs[:, 8] = (Xs[:, 8] - self.meanX[8]) / self.stdX[8] 
        Xs[:, 59:61] = (Xs[:, 59:61] - self.meanX[59:61]) / self.stdX[59:61] 
        return Xs

    def _check_matrix(self, mat, name):
        """ Utility to assure the input matrix mat is 2D. 
            If not, it throws an exception. 
            
            mat     ndarray
                    input matrix to check the shape
            name    string
                    matrix name to print out error
        """
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
        pass
    
    @abstractmethod
    def use(self, X):
        pass 

class Pocket(Classifier):
    
    def __init__(self, alpha):
        Classifier.__init__(self)
        self.alpha = alpha
        self.w = np.random.rand(103)

    # return 1 if w is better -1 if wp is better
    def compare(self, X, T, wp):
        y = np.sign(X @ self.w)
        yp = np.sign(X @ wp)

        return 1 if np.sum(y == T) >= np.sum(yp == T) else -1

    def train(self, X, T):
        maxiter = 10000

        X1 = self.add_ones(X)
        N = X1.shape[0]

        w_pocket = copy(self.w)

        plt.plot(T)
        for i in range(maxiter):
            print(i)
            hasConverged = True
            for k in np.random.permutation(N): #range(N):
                y = self.w @ X1[k]
                if np.sign(y) != np.sign(T[k]):
                    self.w += self.alpha * T[k] * X1[k]
                    hasConverged = False
                    if self.compare(X1, T, w_pocket) > 0: 
                        w_pocket[:] = self.w[:]
            
            if hasConverged:
                print("converged at ", i)
                break

        print("End of training: ", i)
    
    def use(self, X):
        X1 = self.add_ones(X)
        return X1 @ self.w

class LogisticRegression(Classifier):
    
    def __init__(self, alpha):
        Classifier.__init__(self)
        self.alpha = alpha
        self.w = np.random.rand(103, 2)

    def softmax(self, z):
        if not isinstance(z, np.ndarray):
            z = np.asarray(z)
        f = np.exp(z) 
        return f / (np.sum(f, axis=1, keepdims=True) if len(z.shape) == 2 else np.sum(f))

    # for linear fx
    def g(self, X):
        return self.softmax(X @ self.w) 

    def train(self, X, T):
        # iterate to update weights
        niter = 10000
        
        X1 = self.add_ones(X)
        for step in range(niter):
            ys = self.g(X1)
            # if(step == 0):
            #     ys = np.reshape(ys, (ys.shape[0], 1))
            self.w = self.w + self.alpha * X1.T @ (T - ys)
    
    def use(self, X):
        X1 = self.add_ones(X)
        return X1 @ self.w

""" partitioning data

    parameters
    -----------
    X        numpy array
             input data to partition
    T        numpy array
             target labels to partition
    raito    list
             list of ratios for partitions (should be summed to 1) 
             the number of return pairs are different
    return
    -------
    
    Xs       list of numpy arrays
    
    Ts       list of numpy arrays
"""
def partition(X, T, ratio=[0.8, 0.2]): 
    
    # Checks to make sure ratio sums to 1
    assert(np.sum(ratio) == 1)
    
    # Store the number of data samples 
    N = X.shape[0]

    # change the 1d array to 2d if need
    if len(T.shape) == 1:
        T = T.reshape((N,1))
    
    # Shuffle the data indices 
    idxs = np.random.permutation(N)
        
    Xs = []
    Ts = []
    i = 0  # first index to zero
    for k, r in enumerate(ratio):
        # Number of rows that corresponds to kth element in ratios
        nrows = int(round(N * r)) 
        # If we are on the last ratio simply use the remaining data samples
        if k == len(ratio)-1:
            Xs.append(X[idxs[i:], :])
            Ts.append(T[idxs[i:], :])
        else:
            Xs.append(X[idxs[i:i+nrows], :])
            Ts.append(T[idxs[i:i+nrows], :])
        
        i += nrows
    
    return Xs, Ts

df = pd.read_csv("D:\\School Work\\Machine Learning\\Assignment Two\\adult.csv", delimiter=", ", names=['age', 'workclass', 'fnlwgt', 'education', 'educationnum', 'maritalstatus', 'occupation', 'relationship', 'race', 'sex', 'capitalgain', 'capitalloss', 'hoursperweek', 'nativecountry', 'incomeclass'])
print(df)

## BREAK ## Any null values?

print(np.any(df.isnull()))

df = df[df.workclass != '?']
df = df[df.occupation != '?']
df = df[df.nativecountry != '?']
df = df.drop('educationnum', axis=1)

indicatorClass = pd.get_dummies(df.loc[:, 'workclass'])
indicatorEducation = pd.get_dummies(df.loc[:, 'education'])
indicatorMaritalstatus = pd.get_dummies(df.loc[:, 'maritalstatus'])
indicatorOccupation = pd.get_dummies(df.loc[:, 'occupation'])
indicatorRelationship = pd.get_dummies(df.loc[:, 'relationship'])
indicatorRace = pd.get_dummies(df.loc[:, 'race'])
indicatorSex = pd.get_dummies(df.loc[:, 'sex'])
indicatorNativecountry = pd.get_dummies(df.loc[:, 'nativecountry'])

incomeclassdic = {'>50K': 1, '<=50K': 0}
df.incomeclass = df.incomeclass.apply(lambda s: incomeclassdic[s])

df = pd.concat([
        df.iloc[:, 0],
        indicatorClass, 
        df.iloc[:, 2],
        indicatorEducation,
        indicatorMaritalstatus,
        indicatorOccupation,
        indicatorRelationship,
        indicatorRace,
        indicatorSex,
        df.iloc[:, 9:11],
        indicatorNativecountry,
        df.iloc[:, -1:]],
        axis=1)

print(pd.DataFrame(df).describe())
algoPocket = Pocket(.001)

X = df.iloc[:, :-1] 
T = df.iloc[:, -1]

Xnorm = algoPocket.normalize(X)
T = T.values

print(pd.DataFrame(Xnorm).describe())

Xs, Ts = partition(Xnorm, T)
Xtrain, Xtest = Xs[0][:100, :], Xs[1][:10, :]
Ttrain, Ttest = Ts[0][0:100], Ts[1][0:10]

Titrain = (Ttrain == np.unique(Ttrain)).astype(int)
Titest = (Ttest == np.unique(Ttest)).astype(int)

print(np.sum(Ttrain))

assert (np.argmax(Titrain, axis=1) == Ttrain.flatten()).all()
assert (np.argmax(Titest, axis=1) == Ttest.flatten()).all()
algoPocket.train(Xtrain, Ttrain)

Ytrain = algoPocket.use(Xtrain)

Tl = np.argmax(Titrain, 1)
Yl = np.argmax(Ytrain, 1)

plt.plot(Tl, 'r')
plt.plot(Yl, 'b')
plt.show()

print("Accuracy: ", 100 - np.mean(np.abs(Tl - Yl)) * 100, "%")

Ytest = algoPocket.use(Xtest)

Tl = np.argmax(Titest, 1)
Yl = np.argmax(Ytest, 1)

plt.plot(Tl, 'rx')
plt.plot(Yl, 'bo')
plt.show()

print("Accuracy: ", 100 - np.mean(np.abs(Tl - Yl)) * 100, "%")


# Ytrain = algoPocket.use(Xtrain)

# # plt.plot(Ttrain)
# # plt.plot(Ytrain)
# # plt.show()

# print("Accuracy: ", 100 - np.mean(np.abs(Ttrain - Ytrain)) * 100, "%")

# Ytest = algoPocket.use(Xtest)
# # plt.plot(Ttest)
# # plt.plot(Ytest)
# # plt.show()

# print("Accuracy: ", 100 - np.mean(np.abs(Ttest - Ytest)) * 100, "%")

# ## LOG REG

# algoLogReg = LogisticRegression(.0000001)

# assert (np.argmax(Titrain, axis=1) == Ttrain.flatten()).all()
# assert (np.argmax(Titest, axis=1) == Ttest.flatten()).all()
# algoLogReg.train(Xtrain, Titrain)

# Ytrain = algoLogReg.use(Xtrain)

# Tl = np.argmax(Titrain, 1)
# Yl = np.argmax(Ytrain, 1)

# plt.plot(Tl, 'r')
# plt.plot(Yl, 'b')
# plt.show()

# print("Accuracy: ", 100 - np.mean(np.abs(Tl - Yl)) * 100, "%")

# Ytest = algoLogReg.use(Xtest)

# Tl = np.argmax(Titest, 1)
# Yl = np.argmax(Ytest, 1)

# plt.plot(Tl, 'rx')
# plt.plot(Yl, 'bo')
# plt.show()

# print("Accuracy: ", 100 - np.mean(np.abs(Tl - Yl)) * 100, "%")