We also evaluated our features using leave-one-species-out validation in which one
species is left out as test set whereas all the other 26 species are kept as training set.
We repeated this 27 times with different set of organisms as training and test set. This
experiment was performed to check whether the features are effective to predict
essential genes in a new unseen organism and are transferable across organisms. We
used Random Forest Classifier [27] with 100 trees after undersampling equal number of
non-essential genes since it was easily scalable for predicting essential genes in new
organisms.



1.change feature name to the any of the desires features in loo.sh 1st line
allfeatsorted.txt ..597 network and sequence features
allrefexsorted.txt..267 ReFeX features
allnetsorted.txt..283 network features
allcentsorted.txt..12 centralities
all.propsorted ..network naive baseline (4 properties)
all.seqsorted..sequence Liu
allcentsorted.txt..14 network
all12centsorted.txt...12 centralities
2.change delimiter of leaveoneoutnetworkacrossSVMAC_1.py or selected features in index of leaveoneoutselected/leaveoneoutnetworkacrossSVMAC_1.py and then run the following 
3.bash dothis.sh
4.for x in `cat listrolx.txt`;do (bash loo.sh "$x")>loo_"$x".sh;done;
5.bash all.sh
