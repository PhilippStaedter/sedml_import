import pandas as pd
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing
from sklearn import utils


# important paths
data_path = '../bachelor_thesis/SolverAlgorithm/Input_Output_Data.tsv'

# open data file
data_file = pd.read_csv(data_path, sep='\t')
all_columns = data_file.columns
Input = all_columns[: len(all_columns) - 1] # 14
Output = all_columns.drop(all_columns[1 : len(all_columns) - 1])

# define Input and Output
X = data_file.drop(Output,axis=1)        # np.transpose(np.array([[1,2,3,4,5,6]]))
Y = data_file.drop(Input, axis=1)        # np.transpose(np.array([1,1,0,1,0,0]))

###### output must be categorical values for logistic regression, e.g. integers !!! #####
if utils.multiclass.type_of_target(Y) == 'continuous':
    lab_enc = preprocessing.LabelEncoder()
    Y_encoded = lab_enc.fit_transform(Y)
    print(utils.multiclass.type_of_target(Y.astype('int')))
    print(utils.multiclass.type_of_target(Y_encoded))

    # split data in training and testing set
    X_training, X_testing, Y_training, Y_testing = train_test_split(X, Y_encoded, test_size=0.2)#, random_state=1)
else:
    # split data in training and testing set
    X_training, X_testing, Y_training, Y_testing = train_test_split(X, Y, test_size=0.2)#, random_state=1)

# perform logistic regression
clf = LogisticRegression()
clf.fit(X_training, Y_training) # (X,Y)

# predict for testing models
prediction = clf.predict(X_testing) #(X)

# get confusion metrics
cm = confusion_matrix(Y_testing, prediction) # (Y, prediction)
print(cm)

# get accuracy of prediction
accuracy = accuracy_score(Y_testing, prediction) * 100   # (Y, prediction)
print('Accuracy: ' + str(accuracy) + ' %')