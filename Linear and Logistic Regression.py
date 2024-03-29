# regression.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to Clemson University and the authors.
# 
# Authors: Pei Xu (peix@g.clemson.edu) and Ioannis Karamouzas (ioannis@g.clemson.edu)

"""
In this assignment, you will implement linear and logistic regression
using the gradient descent method. To complete the assignment, please 
modify the linear_regression(), and logistic_regression() functions. 

The package `matplotlib` is needed for the program to run.
You should also try to use the 'numpy' library to vectorize 
your code, enabling a much more efficient implementation of 
linear and logistic regression. You are also free to use the 
native 'math' library of Python. 

All provided datasets are extracted from the scikit-learn machine learning library. 
These are called `toy datasets`, because they are quite simple and small. 
For more details about the datasets, please see https://scikit-learn.org/stable/datasets/index.html

Each dataset is randomly split into a training set and a testing set using a ratio of 8 : 2. 
You will use the training set to learn a regression model. Once the training is done, the code
will automatically validate the fitted model on the testing set.  
"""

# use math and/or numpy if needed
import math
import random
import numpy as np

max_iter = 1000
alpha = 0.001
ep = 0.0001

def linear_regression(x, y, logger=None):
    """
    Linear regression using full batch gradient descent.
    A 1D array w should be returned by this function such that given a
    sample x, a prediction can be obtained by x^T w, where x is a column vector. 
    The intercept term can be ignored due to that x has been augmented by adding '1' as an extra feature. 
    If you scale the cost function by 1/#samples, you should use as learning rate alpha=0.001, otherwise alpha=0.0001  

    Parameters
    ----------
    x: a 2D array of size [N, f+1]
       where N is the number of samples, f is the number of features
    y: a 1D array of size [N]
       It contains the target value for each sample in x
    logger: a logger instance for plotting the loss
       Usage: logger.log(i, loss) where i is the number of iterations
       Log updates can be performed every several iterations to improve performance.
    
    Returns
    -------
    w: a 1D array
       linear regression parameters
    """
    x=np.array(x)
    converged = False
    iter = 0
    m = x.shape[0] # number of samples
    w = np.random.random(x.shape[1])
    # Iterate Loop
    w1 = w
    while not converged:
        
        prediction = np.dot(x,w)
        h = (prediction - y)
        w = w -(1/m)*alpha*(x.T.dot(h))
        e = 1.0/(2*m) * np.sum(h**2)
       
        J = e   # update error 
          # update iter

        if iter % 100 == 0:
            logger.log(iter,J)
            print(J)
        iter += 1
        
        if(np.max(np.subtract(w,w1))) <= ep:
            converged = True
        w1 = w
        
        if iter == max_iter:
            print("Max interactions exceeded!")
            converged = True

    return w


def logistic_regression(x, y, logger=None):
    """
    Logistic regression using batch gradient descent.
    A 1D array w should be returned by this function such that given a
    sample x, a prediction can be obtained by p = sigmoid(x^T w)
    with the decision boundary:
        p >= 0.5 => x in class 1
        p < 0.5  => x in class 0
    where x is a column vector. 
    The intercept/bias term can be ignored due to that x has been augmented by adding '1' as an extra feature. 
    In gradient descent, you should use as learning rate alpha=0.001    

    Parameters
    ----------
    x: a 2D array of size [N, f+1]
       where N is the number of samples, f is the number of features
    y: a 1D array of size [N]
       It contains the ground truth label for each sample in x
    logger: a logger instance for plotting the loss
       Usage: logger.log(i, loss) where i is the number of iterations
       Log updates can be performed every several iterations to improve performance.
        
    Returns
    -------
    w: a 1D array
       logistic regression parameters
    """
    x=np.array(x)
    y=np.array(y)
    w = None
    converged = False
    iter = 0
    m = x.shape[0]
    w = np.zeros(x.shape[1])
    w1 = w
    
    def sigmoid(Z):
        return 1/(1+np.e**(-Z))

    def logistic_loss(h, y):
        return (-y * np.log(h) - (1 - y) * np.log(1 - h)).mean()

   

    while not converged:
        Z = np.matmul(x,w)
        A = sigmoid(Z)
        loss = logistic_loss(A, y)
        dz = A - y
        dw = (1.0/(m)) * np.matmul(x.T,dz)
        w = w - alpha*dw

          # update iter
        if iter % 100 == 0:
            logger.log(iter,loss)
            print(loss)
        iter += 1
        
        if(np.max(np.subtract(w,w1))) <= ep:
            converged = True
        w1 = w

        if iter == max_iter:
            print("Max interactions exceeded!")
            converged = True
    return w

def linear_regression_sgd(x, y, logger=None):
    """
    Linear regression using stochastic gradient descent.
    A 1D array w should be returned by this function such that given a
    sample x, a prediction can be obtained by x^T w, where x is a column vector. 
    The intercept term can be ignored due to that x has been augmented by adding '1' as an extra feature. 
    If you scale the cost function by 1/#samples, you should use as learning rate alpha=0.001, otherwise alpha=0.0001  

    Parameters
    ----------
    x: a 2D array of size [N, f+1]
       where N is the number of samples, f is the number of features
    y: a 1D array of size [N]
       It contains the target value for each sample in x
    logger: a logger instance for plotting the loss
       Usage: logger.log(i, loss) where i is the number of iterations
       Log updates can be performed every several iterations to improve performance.
        
    Returns
    -------
    w: a 1D array
       linear regression parameters
    """
    x = np.array(x)
    y = np.array(y)
    alpha = 0.01
    epochs = 1000
    m = x.shape[0]
    batchsize = 32
    n_batches = int(m/batchsize)
    w = np.random.normal(0,0.01,x.shape[1])
    iter = 0
    for i in range(epochs):
        indices = np.random.permutation(m)
        x = x[indices]
        y = y[indices]

    
        j = 0
        while j < m:
            x_i = x[j:j+batchsize]
            y_i = y[j:j+batchsize]
            j += batchsize
            prediction = np.dot(x_i,w)
            h = (prediction - y_i)
            e = 1.0/(2*batchsize) * np.sum(h**2)
       
            w = w -(1/batchsize)*alpha*(x_i.T.dot(h))
           
            
        if(i % 100 == 0):
            print(e)
            logger.log(i,e)
    return w


def logistic_regression_sgd(x, y, logger=None):
    """
    Logistic regression using stochastic gradient descent.
    A 1D array w should be returned by this function such that given a
    sample x, a prediction can be obtained by p = sigmoid(x^T w)
    with the decision boundary:
        p >= 0.5 => x in class 1
        p < 0.5  => x in class 0
    where x is a column vector. 
    The intercept/bias term can be ignored due to that x has been augmented by adding '1' as an extra feature. 
    In gradient descent, you should use as learning rate alpha=0.001    

    Parameters
    ----------
    x: a 2D array of size [N, f+1]
       where N is the number of samples, f is the number of features
    y: a 1D array of size [N]
       It contains the ground truth label for each sample in x
    logger: a logger instance for plotting the loss
       Usage: logger.log(i, loss) where i is the number of iterations
       Log updates can be performed every several iterations to improve performance.
    
    Returns
    -------
    w: a 1D array
       logistic regression parameters
    """
    def sigmoid(z):
        return 1/ (1 + np.exp(-z))

    def logistic_loss(h, y):
        return (-y * np.log(h) - (1 - y) * np.log(1 - h)).mean()
    
    x = np.array(x)
    y = np.array(y)
    alpha = 0.001
    epochs = 1000
    m = len(y)
    w = np.zeros(x.shape[1])
    idx = np.arange(m)
    iter = 0
    for i in range(epochs):
        np.random.shuffle(idx)
        s = 0
        bs=32
        while s < m: 
            x_i = x[idx[s:s+bs],:]
            y_i = y[idx[s:s+bs]]
            s += bs
            z = np.dot(x_i,w)
            h = sigmoid(z)
            gradient = np.dot(x_i.T, (h - y_i))/ y_i.shape[0]
            w = w - alpha*gradient
            
        if(i % 100 == 0):
            print(f'loss: {logistic_loss(h, y_i)} \t')
            logger.log(i, logistic_loss(h, y_i))
        
            
    return w


if __name__ == "__main__":
    import os
    import tkinter as tk
    from app.regression import App

    import data.load
    dbs = {
        "Boston Housing": (
            lambda : data.load("boston_house_prices.csv"),
            App.TaskType.REGRESSION
        ),
        "Diabetes": (
            lambda : data.load("diabetes.csv", header=0),
            App.TaskType.REGRESSION
        ),
        "Handwritten Digits": (
            lambda : (data.load("digits.csv", header=0)[0][np.where(np.equal(data.load("digits.csv", header=0)[1], 0) | np.equal(data.load("digits.csv", header=0)[1], 1))],
                      data.load("digits.csv", header=0)[1][np.where(np.equal(data.load("digits.csv", header=0)[1], 0) | np.equal(data.load("digits.csv", header=0)[1], 1))]),
            App.TaskType.BINARY_CLASSIFICATION
        ),
        "Breast Cancer": (
            lambda : data.load("breast_cancer.csv"),
            App.TaskType.BINARY_CLASSIFICATION
        )
     }

    algs = {
       "Linear Regression (Batch Gradient Descent)": (
            linear_regression,
            App.TaskType.REGRESSION
        ),
        "Logistic Regression (Batch Gradient Descent)": (
            logistic_regression,
            App.TaskType.BINARY_CLASSIFICATION
        ),
        "Linear Regression (Stochastic Gradient Descent)": (
            linear_regression_sgd,
            App.TaskType.REGRESSION
        ),
        "Logistic Regression (Stochastic Gradient Descent)": (
            logistic_regression_sgd,
            App.TaskType.BINARY_CLASSIFICATION
        )
    }

    root = tk.Tk()
    App(dbs, algs, root)
    tk.mainloop()
