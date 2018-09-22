## Undersampling strategy description:

1. The entire dataset is split into 2/3rd training set and 1/3rd testing set.
   This is repeated 5 times with different random splitting of train and test
   datasets.

2. The undersampled training data is obtained from 2/3rd training set and this
   is repeated 10 times (undersampling of the dataset of non-essential genes is
   repeated 10 times whereas essential genes is fixed for all 10 times).

3. The new train set (undersampled non-essential and essential) is constructed
   and 5-fold cross-validation is performed to get the best parameters using
   SVM.

4. The best classifier is found and tested on 1/3rd testing set.

5. The following metrics are reported: Sensitivity, Specificity, AUC,
   Average of sensitivity and specificity, Precision and Accuracy.

6. Thus, 5x random splitting of the entire dataset combined with 10x
   undersampling of training data gives 50 values. The average is taken and
   reported.

## Directions to run `classification_sequence.py`:

`python classification_sequence.py 1liu.txt 0liu.txt`

 Note: `1liu.txt` has all essential and `0liu.txt` has all non-essential genes.
