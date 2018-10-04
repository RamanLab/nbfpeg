# -*- coding: utf-8 -*-

# Contains functions to perform leave-one-out-species validaton.

from __future__ import print_function, division

import glob
import random
import sys
from random import randint

import numpy as np
import sklearn
from sklearn import cross_validation, grid_search, svm
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.metrics import (accuracy_score, auc, confusion_matrix, f1_score,
                             precision_recall_curve, precision_score,
                             roc_curve)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

np.random.seed(0)

def compute_measures(tp, fp, fn, tn):
     """Computes effectiveness measures given a confusion matrix."""
     specificity = tn / (tn + fp)
     sensitivity = tp / (tp + fn)
     return sensitivity, specificity


def random_undersampler(sequence, size, state):
     """Gives random undersampled values."""
     np.random.seed(state)
     sample = np.random.choice(sequence, size, replace=False)
     return sample


allrolx = {}
with open(sys.argv[1]) as newfile:
     for val in newfile:
          h = val[:-2].split(" ") #change the delimiter accordingly
          allrolx[h[0]] = [float(i) for i in h[1:]]

trainfiles=
testfiles=

train_proteins = []
for i in trainfiles:
    with open(i+".nuclnew.prot") as f:
         for j in f:
              train_proteins.append(j[:-1])

test_proteins = []
for i in testfiles:
    with open(i+".nuclnew.prot") as f:
         for j in f:
              test_proteins.append(j[:-1])
print(len(train_proteins),len(test_proteins))
oca1ess = []
oca2ess = []
oca1noness = []
oca2noness = [] 
with open("full.map") as g:
     ess = {}
     for i in g:
          hh = i[:-1].split(",")
          ess[hh[0]] = hh[1]

     for i in train_proteins:
          if ess[i] == "1":
               oca1ess.append(i)
          elif ess[i] == "0":
               oca1noness.append(i)

     for i in test_proteins:
          if ess[i] == "1":
               oca2ess.append(i)
          elif ess[i] == "0":
               oca2noness.append(i)

oca1zero = []
oca1one = []
for filenames in oca1ess:
    if allrolx.has_key(filenames):
        oca1zero.append(allrolx[filenames])
for filenames in oca1noness:
    if allrolx.has_key(filenames):
        oca1one.append(allrolx[filenames])

oca2zero = []
oca2one = []
for filenames in oca2ess:
    if allrolx.has_key(filenames):
        oca2zero.append(allrolx[filenames])
print(len(oca2zero))
for filenames in oca2noness:
    if allrolx.has_key(filenames):
        oca2one.append(allrolx[filenames])
print(len(oca2one))

combined_array_train = []
combined_label_train = []
for i in range(len(oca1zero)):
    combined_array_train.append(oca1zero[i])
    combined_label_train.append(1)
for i in range(len(oca1one)):
    combined_array_train.append(oca1one[i])
    combined_label_train.append(0)

combined_array_test = []
combined_label_test = []
for i in range(len(oca2zero)):
    combined_array_test.append(oca2zero[i])
    combined_label_test.append(1)
for i in range(len(oca2one)):
    combined_array_test.append(oca2one[i])
    combined_label_test.append(0)

pos_neg_rep = np.array(combined_array_train)
pos_neg_labels = np.array(combined_label_train)
indices = np.arange(pos_neg_rep.shape[0])
np.random.shuffle(indices)
X = pos_neg_rep[indices]
y = pos_neg_labels[indices]
pos_neg_rep_1 = np.array(combined_array_test)
pos_neg_labels_1 = np.array(combined_label_test)
indices_1 = np.arange(pos_neg_rep_1.shape[0])
np.random.shuffle(indices_1)
X1 = pos_neg_rep_1[indices_1]
y1 = pos_neg_labels_1[indices_1]
X_train = X
y_train = y
ess_sequences = [i for i in range(len(X_train)) if y_train[i] == 1]
noness_sequences = [i for i in range(len(X_train)) if y_train[i] == 0]
print(len(ess_sequences))
print(len(noness_sequences))

x = random_undersampler(noness_sequences, len(ess_sequences), 0)
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

modxtr = np.array(x_train_undersampled)
modytr = np.array(y_train_undersampled)

clf = RFC(n_estimators=100)
svm_best_clf = clf.fit(modxtr, modytr)
test_predictions_svm = svmbestclf.predict(X1)
test_predictions_svm_proba = svm_best_clf.predict_proba(X1)
accuracy = accuracy_score(y1,test_predictions_svm)
true_n, false_p, false_n, true_p = confusion_matrix(
     y1, test_predictions_svm).ravel()
print(true_n, false_p, false_n, true_p)

prec = precision_score(y1, test_predictions_svm)
f1 = f1_score(y1, test_predictions_svm)
sensitivity, specficity = compute_measures(true_p, false_p, false_n, true_n)
print(sensitivity, specificity)

average = (sensitivity + specificity) / 2
fpr, tpr, thresholds = roc_curve(y1, test_predictions_svm_proba[:, 1])
roc_auc1 = auc(fpr, tpr)
precision, recall, thresholds = precision_recall_curve(
     y1, test_predictions_svm_proba[:, 1])
area = auc(recall, precision)

print(sensitivity, specificity, average,
      roc_auc1, accuracy, precision, f1,
      area)
