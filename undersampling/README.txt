Undersampling strategy Description[1]:
Step 1: The entire dataset was split into 2/3 rd training set and 1/3 rd testing set. This was
repeated 5 times with different random splitting of train and test datasets.
Step 2: Then, under-sampled training data was obtained from 2/3 rd training set and this was
repeated 10 times (Under sampling of the dataset of non-essential genes was repeated 10
times whereas essential genes is fixed for all 10 times)
Step 3: Now, new train set (under sampled non-essential and essential) was constructed and 5
fold cross validation was done to find the best parameters using SVM.
Step 4: The best classifier was found and tested on 1/3rd testing set.
Step 5: Then,different metrics are reported - Sensitivity, Specificity, AUC, Average of sensitivity
and specificity, Precision and Accuracy.
Step 6: Thus, 5 times random splitting of the entire dataset combined with 10 times under
sampling of training data gives 50 values. The average of this is taken and reported.



#1liu.txt has all essential and oliu.txt has all non-essential genes
python classificationsequence.py 1liu.txt 0liu.txt
