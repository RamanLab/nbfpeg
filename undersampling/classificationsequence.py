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
from sklearn.metrics import average_precision_score
##SVM 
from sklearn.metrics import precision_recall_curve
##SVM 
from sklearn import grid_search
from sklearn.svm import SVC
import random
def compute_measures(tp, fp, fn, tn):
     """Computes effectiveness measures given a confusion matrix."""
     specificity = tn / (tn + fp) 
     sensitivity = tp / (tp + fn)
     acura=(tp+tn)/(tp+fp+fn+tn)
     preci=tp/(tp+fp)
     f1=(2*preci*sensitivity)/(preci+sensitivity)
     return sensitivity, specificity,acura,preci,f1
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
    ##10-fold test for mod xtr
    modxtr=np.array(modxtr)
    modytr=np.array(modytr)
    pipe_svc = Pipeline([('clf', SVC(probability=True,random_state=1))])
    param_range = [0.0001, 0.001, 0.01, 0.1, 1.0,100,1000]
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
                  n_jobs=100,verbose=10)
    gs = gs.fit(modxtr, modytr)
    print(gs.best_score_)
    print(gs.best_params_)
    return gs.best_estimator_
    
def randomundersampler(sequence,size,state):
    np.random.seed(state)
    sampledone=np.random.choice(sequence,size,replace=False)
    return sampledone
newfile=open(sys.argv[1])
positive_sequences=[]
positive_labels=[]
for ii in newfile:
    positive_sequences.append([float(i) for i in ii[:-3].split(" ")])
    positive_labels.append(1)
#print len(positive_sequences)
anotherfile=open(sys.argv[2])
negative_sequences=[]
negative_labels=[]
for i in anotherfile:
    negative_sequences.append([float(i) for i in i[:-3].split(" ")])
    negative_labels.append(0)
#print len(negative_sequences)
posnegrep=np.array(positive_sequences+negative_sequences)
posneglabels=np.array(positive_labels+negative_labels)
print len(posnegrep),len(posneglabels)
indices = np.arange(posnegrep.shape[0])
np.random.shuffle(indices)
print indices
X = posnegrep[indices]
y=posneglabels[indices]
index=np.array([376, 489, 330, 560, 481, 283, 446,   9, 278, 533,  27, 320, 544, 506, 468,  19, 483, 287, 268,  33, 365, 499, 582,  93, 226,  24, 369,  53,  16,  29, 561, 448, 327, 552, 580, 308, 458, 513,  23, 55, 572,   2, 363, 217, 493, 488, 315, 362,   3,  17,  68,  34, 512,  25, 474, 331, 416, 311,  26, 143, 364, 515, 571,   8, 486, 118,   6,  21, 218, 236, 459, 508, 199, 431, 319,  87, 209, 361, 198, 517,  30, 157, 300,  10, 505, 453, 289, 241, 158, 245, 504, 196,  31, 168,  60,  45,  42,  98, 100,  49])
Xnew= np.squeeze(X[:,index])

#print posnegrep
#svmcrossvalidation(posnegrep,posneglabels)
#modcrossvalidation(posnegrep,posneglabels)

#Outer loop Do 5 times
##split dataset into train and test(2/3rd training and 1/3rd testing)
final_sensitivity=[]
final_specificity=[]
final_auc=[]
final_average=[]
final_acura=[]
final_prec=[]
final_f1=[]
final_area=[]
final_area1=[]
random_state_numbers=[0,1,2,3,4]
for outer in range(5):
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(Xnew, y, test_size=0.333333333333,random_state=random_state_numbers[outer])
    #Inner loop Do 10 times
    for inner in range(10):
        ##get undersampled training data
        ess_sequences=[i for i in range(len(X_train)) if y_train[i] == 1]
        noness_sequences=[i for i in range(len(X_train)) if y_train[i] == 0]
        print len(ess_sequences)
        print len(noness_sequences)
        x=randomundersampler(noness_sequences,len(ess_sequences),inner)
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
        ##take the train test and do 5 fold cross validation
        svmbestclf=svmcrossvalidation(x_train_undersampled,y_train_undersampled)
        ##test on 1/3rd testing set
        testpredictionssvm=svmbestclf.predict(X_test)
        testpredictionssvmproba=svmbestclf.predict_proba(X_test)
        print accuracy_score(y_test,testpredictionssvm)
        truen, falsep, falsen, truep = confusion_matrix(y_test,testpredictionssvm).ravel()
        print truen, falsep, falsen, truep
        sens,speci,ac,pr,f1=compute_measures(truep, falsep, falsen, truen)
        print sens,speci
        average=(sens+speci)/2
        final_sensitivity.append(sens)
        final_specificity.append(speci)
        final_acura.append(ac)
        final_prec.append(pr)
        final_f1.append(f1)
        fpr, tpr, thresholds = roc_curve(y_test, testpredictionssvmproba[:,1])
        roc_auc1 = auc(fpr, tpr)
        print roc_auc1
        precision, recall, thresholds = precision_recall_curve(y_test, testpredictionssvmproba[:,1])
        area = auc(recall, precision)
        area1=average_precision_score(y_test, testpredictionssvmproba[:,1])
        final_auc.append(roc_auc1)
        final_average.append(average)
        final_area.append(area)
        final_area1.append(area1)
print np.mean(np.array(final_sensitivity))
print np.mean(np.array(final_specificity))
print np.mean(np.array(final_auc))
print np.mean(np.array(final_average))
print np.mean(np.array(final_acura))
print np.mean(np.array(final_prec))
print np.mean(np.array(final_f1))
print np.mean(np.array(final_area))
print np.mean(np.array(final_area1))
