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


# important paths
data_path = '../bachelor_thesis/SolverAlgorithm/Input_Output_Data.tsv'
benchmark_collection_path = '../bachelor_thesis/SolverAlgorithm/Benchmark_Input_Data.tsv'
y_testing_path = '../bachelor_thesis/SolverAlgorithm/Benchmark_Output_Data.tsv'

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

# open benchmark files
benchmark_input_file = pd.read_csv(benchmark_collection_path, sep='\t')
benchmark_output_file = pd.read_csv(y_testing_path, sep='\t')

# define Input and Output
X = data_file.drop('value',axis=1)                                              # np.transpose(np.array([[1,2,3,4,5,6]]))
Y = data_file.drop(all_columns[1:len(all_columns)-1], axis=1)                   # np.transpose(np.array([1,1,0,1,0,0]))
X_testing = benchmark_input_file
Y_testing = benchmark_output_file
#Y_testing = bestFit(X, Y, X_testing)

# drop the 'model' column
X = X.drop('model', axis=1)
Y = Y.drop('model', axis=1)
X_testing_1 = X_testing.drop('model', axis=1)
Y_testing_1 = Y_testing.drop('model', axis=1)

'''
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
'''

# perform logistic regression
clf = LogisticRegression()
clf.fit(X,Y)                        #(X_training, Y_training)

# predict for testing models
prediction = clf.predict(X_testing_1) #(X)

# get confusion metrics
cm = confusion_matrix(pd.Series.tolist(Y_testing_1['value']), prediction) # (Y, prediction)
print(cm)

# get accuracy of prediction
accuracy = accuracy_score(pd.Series.tolist(Y_testing_1['value']), prediction) * 100   # (Y, prediction)
print('Accuracy: ' + str(accuracy) + ' %')

####### save 'model', 'real_value', 'predictat_value' in data frame
results = pd.DataFrame(columns=['r_model', 'r_value', 'combinations', 'p_value', 'p_model'], data=[])
results['r_model'] = X_testing['model']
results['r_value'] = Y_testing['value']
results['combinations'] = X_testing['combinations']
results['p_value'] = pd.Series(prediction)
results['p_model'] = Y_testing['model']

results.to_csv('../bachelor_thesis/SolverAlgorithm/Results_0_1.tsv', sep='\t', index=False)