from __future__ import division
import sklearn
import sys
from sklearn import svm
import numpy as np
np.random.seed(0)
import glob
from random import randint
from sklearn import cross_validation
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
##SVM 
from sklearn.metrics import precision_recall_curve
from sklearn import grid_search
from sklearn.svm import SVC
import random
def compute_measures(tp, fp, fn, tn):
     """Computes effectiveness measures given a confusion matrix."""
     specificity = tn / (tn + fp)
     sensitivity = tp / (tp + fn)
     return sensitivity, specificity
def randomundersampler(sequence,size,state):
    np.random.seed(state)
    sampledone=np.random.choice(sequence,size,replace=False)
    return sampledone
def accuracy(labelcorrect,labelpred):
    return round(sklearn.metrics.accuracy_score(labelcorrect, labelpred),2)
def mutualinfo(labelcorrect,labelpred):
    return round(sklearn.metrics.mutual_info_score(labelcorrect, labelpred,   contingency=None),2)
def normmutualinfo(labelcorrect,labelpred):
    return round(sklearn.metrics.normalized_mutual_info_score(labelcorrect, labelpred),2)
def fbeta(labelcorrect,labelpred):
    return round(sklearn.metrics.fbeta_score(labelcorrect, labelpred, beta=0.5, labels=None, pos_label=1, average='micro'),2)
def rand(labelcorrect,labelpred):
    return round(sklearn.metrics.adjusted_rand_score(labelcorrect,labelpred),2)
def precision(labelcorrect,labelpred):
    return round(sklearn.metrics.precision_score(labelcorrect,labelpred),2) 
def svmcrossvalidation(modxtr,modytr):
    ess_sequences=[i for i in range(len(X_train)) if y_train[i] == 1]
    noness_sequences=[i for i in range(len(X_train)) if y_train[i] == 0]
    print len(ess_sequences)
    print len(noness_sequences)
    x=randomundersampler(noness_sequences,len(ess_sequences),0)
    print x
    x_train_undersampled=[]
    y_train_undersampled=[]
    for i in ess_sequences:
        x_train_undersampled.append(X_train[i])
        y_train_undersampled.append(y_train[i])
    for i in x:
        x_train_undersampled.append(X_train[i])
        y_train_undersampled.append(y_train[i])
    print len(x_train_undersampled)
    print len(y_train_undersampled)
    ##10-fold test for mod xtr
    modxtr=np.array(x_train_undersampled)
    modytr=np.array(y_train_undersampled)
    indices = np.arange(modxtr.shape[0])
    np.random.shuffle(indices)
    modxtr = modxtr[indices]
    modytr = modytr[indices]
    pipe_svc = Pipeline([('clf', SVC(probability=True,random_state=1))])
    param_range = [0.0001, 0.001, 0.01, 0.1, 1.0]
    ##grid search for linear and rbf kernels with different parameter ranges
    #param_grid = [{'clf__C': param_range, 'clf__kernel': ['linear','rbf']}]
    param_grid = [
 {'clf__C': param_range, 
                  'clf__gamma': param_range, 
                  'clf__kernel': ['rbf']}]

    gs = grid_search.GridSearchCV(estimator=pipe_svc, 
                  param_grid=param_grid, 
                  scoring='accuracy', 
                  cv=5,
                  n_jobs=32,verbose=10)
    gs = gs.fit(modxtr, modytr)
    print(gs.best_score_)
    print(gs.best_params_)
    return gs.best_estimator_


allrolx={}
newfile=open(sys.argv[1])
for ii in newfile:
    h=ii[:-2].split(" ") #change the delimiter accordingly
    allrolx[h[0]]=[float(i) for i in h[1:]]
trainfiles=
testfiles=
trainproteins=[]
for i in trainfiles:
    f=open(i+".nuclnew.prot")
    for j in f:
        trainproteins.append(j[:-1])
testproteins=[]
for i in testfiles:
    f=open(i+".nuclnew.prot")
    for j in f:
        testproteins.append(j[:-1])
print len(trainproteins),len(testproteins)
oca1ess=[]
oca2ess=[]
oca1noness=[]
oca2noness=[] 
g=open("full.map")
ess={}
for i in g:
    hh=i[:-1].split(",")
    ess[hh[0]]=hh[1]
for i in trainproteins:
    if ess[i]=="1":
        oca1ess.append(i)
    elif ess[i]=="0":
        oca1noness.append(i)
for i in testproteins:
    if ess[i]=="1":
        oca2ess.append(i)
    elif ess[i]=="0":
        oca2noness.append(i)
oca1zero=[]
oca1one=[]
for filenames in oca1ess:
    if allrolx.has_key(filenames):
        oca1zero.append(allrolx[filenames])
for filenames in oca1noness:
    if allrolx.has_key(filenames):
        oca1one.append(allrolx[filenames])
oca2zero=[]
oca2one=[]
for filenames in oca2ess:
    if allrolx.has_key(filenames):
        oca2zero.append(allrolx[filenames])
print len(oca2zero)
for filenames in oca2noness:
    if allrolx.has_key(filenames):
        oca2one.append(allrolx[filenames])
print len(oca2one)
combinedarraytrain=[]
combinedlabeltrain=[]
for i in range(len(oca1zero)):
    combinedarraytrain.append(oca1zero[i])
    combinedlabeltrain.append(1)
for i in range(len(oca1one)):
    combinedarraytrain.append(oca1one[i])
    combinedlabeltrain.append(0)
combinedarraytest=[]
combinedlabeltest=[]
for i in range(len(oca2zero)):
    combinedarraytest.append(oca2zero[i])
    combinedlabeltest.append(1)
for i in range(len(oca2one)):
    combinedarraytest.append(oca2one[i])
    combinedlabeltest.append(0)
posnegrep=np.array(combinedarraytrain)
posneglabels=np.array(combinedlabeltrain)
indices = np.arange(posnegrep.shape[0])
np.random.shuffle(indices)
X = posnegrep[indices]
y=posneglabels[indices]
posnegrep1=np.array(combinedarraytest)
posneglabels1=np.array(combinedlabeltest)
indices1 = np.arange(posnegrep1.shape[0])
np.random.shuffle(indices1)
X1 = posnegrep1[indices1]
y1=posneglabels1[indices1]
X_train=X
y_train=y
ess_sequences=[i for i in range(len(X_train)) if y_train[i] == 1]
noness_sequences=[i for i in range(len(X_train)) if y_train[i] == 0]
print len(ess_sequences)
print len(noness_sequences)
x=randomundersampler(noness_sequences,len(ess_sequences),0)
print x
x_train_undersampled=[]
y_train_undersampled=[]
for i in ess_sequences:
    x_train_undersampled.append(X_train[i])
    y_train_undersampled.append(y_train[i])
for i in x:
    x_train_undersampled.append(X_train[i])
    y_train_undersampled.append(y_train[i])
print len(x_train_undersampled)
print len(y_train_undersampled)
##10-fold test for mod xtr
modxtr=np.array(x_train_undersampled)
modytr=np.array(y_train_undersampled)

clf = RFC(n_estimators = 100)
#svmbestclf=svmcrossvalidation(X,y)
svmbestclf=clf.fit(modxtr,modytr)
testpredictionssvm=svmbestclf.predict(X1)
testpredictionssvmproba=svmbestclf.predict_proba(X1)
accu= accuracy_score(y1,testpredictionssvm)
truen, falsep, falsen, truep = confusion_matrix(y1,testpredictionssvm).ravel()
print truen, falsep, falsen, truep
prec=precision_score(y1,testpredictionssvm)
f1=f1_score(y1,testpredictionssvm)
sens,speci=compute_measures(truep, falsep, falsen, truen)
print sens,speci
average=(sens+speci)/2
fpr, tpr, thresholds = roc_curve(y1, testpredictionssvmproba[:,1])
roc_auc1 = auc(fpr, tpr)
precision, recall, thresholds = precision_recall_curve(y1, testpredictionssvmproba[:,1])
area = auc(recall, precision)
#area1=average_precision_score(y1, testpredictionssvmproba[:,1])
print sens,speci,average,roc_auc1,accu,prec,f1,area
