# predict the outcome for simulation worked, best 10% and best setting via cross validation

import pandas as pd
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing
from sklearn import utils
from Y_testing import *
from sklearn.model_selection import cross_validate
from sklearn import svm


# important paths
data_path = '../bachelor_thesis/SolverAlgorithm/Input_Output_Data_0_1_updated.tsv'

# open data file
data_file = pd.read_csv(data_path, sep='\t')
all_columns = data_file.columns

# rename 'levchenko' for uniqueness
names = data_file['model']
for iModel in range(0, len(names)):
    if names[iModel] == '{levchenko2000_fig2-user}' and data_file['num_x'][iModel] == 31:
        names[iModel] = '{levchenko2000_fig2-user}_1'
    elif names[iModel] == '{levchenko2000_fig2-user}' and data_file['num_x'][iModel] == 22:
        names[iModel] = '{levchenko2000_fig2-user}_2'
data_file['model'] = names

# define Input and Output
X = data_file.drop('value',axis=1)
X = X.drop('model', axis=1)
Y = data_file.drop(all_columns[1:len(all_columns)-1], axis=1)
Y = Y.drop('model', axis=1)

#### output must be categorical values for logistic regression, e.g. integers !!! #####
if utils.multiclass.type_of_target(Y) != 'multiclass':
    lab_enc = preprocessing.LabelEncoder()
    Y_encoded = lab_enc.fit_transform(Y)
    print(utils.multiclass.type_of_target(Y.astype('int')))
    print(utils.multiclass.type_of_target(Y_encoded))


#### Prediction #########
# split X and Y into five blocks for "manual" cross validation
X1 = X[:1320]               # 40*33
X2 = X[1320:2640]           # 40*33
X3 = X[2640:3960]           # 40*33
X4 = X[3960:5280]           # 40*33
X5 = X[5280:]               # 40*34
Y1 = Y_encoded[:1320]       # 40*33
Y2 = Y_encoded[1320:2640]   # 40*33
Y3 = Y_encoded[2640:3960]   # 40*33
Y4 = Y_encoded[3960:5280]   # 40*33
Y5 = Y_encoded[5280:]       # 40*34

# joining data frames
V1 = X1.append(X2).append(X3).append(X4)
V2 = X1.append(X3).append(X4).append(X5)
V3 = X1.append(X2).append(X4).append(X5)
V4 = X1.append(X2).append(X3).append(X5)
V5 = X2.append(X3).append(X4).append(X5)
W1 = np.concatenate((Y1, Y2, Y3, Y4))
W2 = np.concatenate((Y1, Y3, Y4, Y5))
W3 = np.concatenate((Y1, Y2, Y4, Y5))
W4 = np.concatenate((Y1, Y2, Y3, Y5))
W5 = np.concatenate((Y2, Y3, Y4, Y5))

# list of all permutations
first_batch = [V1, X5, W1, Y5]
second_batch = [V2, X2, W2, Y2]
third_batch = [V3, X3, W3, Y3]
fourth_batch = [V4, X4, W4, Y4]
fifth_batch = [V5, X1, W5, Y1]

All_permutations = [first_batch, second_batch, third_batch, fourth_batch, fifth_batch]

# amount of cross validations
cv = 5

# logistic regression
clf = []
for iCrossValidation in range(0, cv):
    X_training = All_permutations[iCrossValidation][0]
    X_testing = All_permutations[iCrossValidation][1]
    Y_training = All_permutations[iCrossValidation][2]
    Y_testing = All_permutations[iCrossValidation][3]
    clf.append(LogisticRegression())
    Fit = clf[iCrossValidation].fit(X_training, Y_training)
    ExpSigmoid = Fit.decision_function(X_training)

    df = valuesSigmoid(ExpSigmoid)
    #test_score = clf[iCrossValidation].predict(X_testing)            #(train_score > test_score)
