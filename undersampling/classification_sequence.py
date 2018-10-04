# -*- coding: utf-8 -*-

# Contains functions to perform undersampling.

from __future__ import print_function, division

import glob
import random
import sys
from random import randint

import numpy as np
import sklearn 
from sklearn import cross_validation, grid_search, svm
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.metrics import (accuracy_score, auc, average_precision_score,
                              confusion_matrix, precision_recall_curve,
                              roc_curve)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

np.random.seed(0)


def compute_measures(tp, fp, fn, tn):
      """Computes effectiveness measures given a confusion matrix."""
      specificity = tn / (tn + fp) 
      sensitivity = tp / (tp + fn)
      accuracy = (tp+tn) / (tp + fp + fn + tn)
      precision = tp / (tp + fp)
      f1 = (2 * precision * sensitivity) / (precision + sensitivity)
      return sensitivity, specificity, accuracy, precision, f1


def svm_crossvalidation(mod_x_tr, mod_y_tr):
      """Gives the result of 10x cross-validation."""
      modxtr = np.array(mod_x_tr)
      modytr = np.array(mod_y_tr)
      pipe_svc = Pipeline([('clf', SVC(probability=True, random_state=1))])
      param_range = [0.0001, 0.001, 0.01, 0.1, 1.0, 100, 1000]    
      param_grid = [{'clf__C': param_range,
                    'clf__gamma': param_range,
                    'clf__kernel': ['rbf']}]

      gs = grid_search.GridSearchCV(estimator=pipe_svc, param_grid=param_grid,
                                   scoring='accuracy', cv=5, n_jobs=100,
                                   verbose=10)
      gs = gs.fit(modxtr, modytr)
     
      print(gs.best_score_)
      print(gs.best_params_)
     
      return gs.best_estimator_

     
def random_undersampler(sequence, size, state):
      """Gives the random undersampled value."""
      np.random.seed(state)
      sample = np.random.choice(sequence, size, replace=False)
      return sample


with open(sys.argv[1]) as new_file:
      positive_sequences = []
      positive_labels = []

      for val in new_file:
           positive_sequences.append([float(i) for i in val[:-3].split(" ")])
           positive_labels.append(1)

with open(sys.argv[2]) as another_file:
      negative_sequences=[]
      negative_labels=[]

      for val in another_file:
           negative_sequences.append([float(i) for i in val[:-3].split(" ")])
           negative_labels.append(0)
           

pos_neg_rep = np.array(positive_sequences + negative_sequences)
pos_neg_labels = np.array(positive_labels + negative_labels)
indices = np.arange(pos_neg_rep.shape[0])
np.random.shuffle(indices)
print(indices)

X = pos_neg_rep[indices]
y = pos_neg_labels[indices]
'''index = np.array([376, 489, 330, 560, 481, 283, 446, 9, 278, 533, 27, 320, 544,
                   506, 468, 19, 483, 287, 268,  33, 365, 499, 582, 93, 226, 24,
                   369, 53, 16, 29, 561, 448, 327, 552, 580, 308, 458, 513, 23,
                   55, 572, 2, 363, 217, 493, 488, 315, 362, 3, 17, 68, 34, 512,
                   25, 474, 331, 416, 311, 26, 143, 364, 515, 571, 8, 486, 118,
                   6, 21, 218, 236, 459, 508, 199, 431, 319, 87, 209, 361, 198,
                   517, 30, 157, 300, 10, 505, 453, 289, 241, 158, 245, 504,
                   196, 31, 168, 60, 45, 42, 98, 100, 49])'''
#X_new = np.squeeze(X[:, index])

final_sensitivity = []
final_specificity = []
final_auc = []
final_average = []
final_accuracy = []
final_prec = []
final_f1 = []
final_area = []
final_area_1 = []
random_state_numbers = [0,1,2,3,4]

for outer in range(5):
     X_train, X_test, y_train, y_test = cross_validation.train_test_split(
          X, y, test_size=0.333333333333,
          random_state=random_state_numbers[outer])
     for inner in range(10):
         # Gets undersampled training data
         ess_sequences = [i for i in range(len(X_train)) if y_train[i] == 1]
         noness_sequences = [i for i in range(len(X_train)) if y_train[i] == 0]
         print(len(ess_sequences))
         print(len(noness_sequences))
         
         x = random_undersampler(noness_sequences, len(ess_sequences), inner)
         print(x)

         x_train_undersampled = []
         y_train_undersampled = []

         for i in ess_sequences:
             x_train_undersampled.append(X_train[i])
             y_train_undersampled.append(y_train[i])
             
         for i in x:
             x_train_undersampled.append(X_train[i])
             y_train_undersampled.append(y_train[i])

         print(len(x_train_undersampled))
         print(len(y_train_undersampled))  

         # Takes the train test and does 5 fold cross-validation
         svm_best_clf = svm_crossvalidation(x_train_undersampled,
                                            y_train_undersampled)
         # Tests on 1/3rd testing set
         test_predictions_svm = svm_best_clf.predict(X_test)
         test_predictions_svm_proba = svm_best_clf.predict_proba(X_test)
         print(accuracy_score(y_test, testpredictions_svm))
         
         true_n, false_p, false_n, true_p = confusion_matrix(
              y_test, test_predictions_svm).ravel()
         print(true_n, false_p, false_n, true_p)

         sensitivity, specificity, accuracy, precision, f1 = compute_measures(
              true_p, false_p, false_n, true_n)
         print(sensitivity, specificity)

         average = (sensitivity + specificity) / 2
         final_sensitivity.append(sens)
         final_specificity.append(speci)
         final_accuracy.append(ac)
         final_precision.append(pr)
         final_f1.append(f1)

         fpr, tpr, thresholds = roc_curve(y_test,
                                          test_predictions_svm_proba[:,1])
         roc_auc1 = auc(fpr, tpr)
         print(roc_auc1)

         precision, recall, thresholds = precision_recall_curve(
              y_test, test_predictions_svm_proba[:, 1])
         area = auc(recall, precision)
         area_1 = average_precision_score(y_test,
                                         test_predictions_svm_proba[:, 1])
         final_auc.append(roc_auc1)
         final_average.append(average)
         final_area.append(area)
         final_area_1.append(area_1)

print(np.mean(np.array(final_sensitivity)))
print(np.mean(np.array(final_specificity)))
print(np.mean(np.array(final_auc)))
print(np.mean(np.array(final_average)))
print(np.mean(np.array(final_accuracy)))
print(np.mean(np.array(final_precision)))
print(np.mean(np.array(final_f1)))
print(np.mean(np.array(final_area)))
print(np.mean(np.array(final_area_1)))
