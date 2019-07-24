import pandas as pd
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# important paths
data_path = '../bachelor_thesis/SolverAlgorithm/Input_Output.tsv'

# open data file
data_file = pd.read_csv(data_path, sep='\t')

# define Input and Output
X = data_file.drop(['model','value'],axis=1)
Y = data_file['value']

# split data in training and testing set
X_training, X_testing, Y_training, Y_testing = train_test_split(X, Y, test_size=0.2, random_state=1)

# perform logistic regression
model = LogisticRegression()
model.fit(X_training, Y_training)

# predict for testing models
prediction = model.predict(X_testing)

# get accuracy of prediction
accuracy = accuracy_score(Y_testing, prediction) * 100
print(str(accuracy) + ' %')