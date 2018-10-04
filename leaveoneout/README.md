## Strategy for leaveoneout:

The features were evaluated using **leave-one-species-out** validation in which
one species is left out as test set whereas all the other 26 species are kept as
training set. This was repeated 27 times with different set of organisms as
training and test set.

This experiment was performed to check whether the features are effective to
predict essential genes in a new unseen organism and are transferable across
organisms. We used **Random Forest Classifier** with 100 trees after
undersampling equal number of non-essential genes since it is easily scalable
for predicting essential genes in new organisms.


## Directions to run:

1. Change feature name to the any of the desired features in 1st line of
   `loo.sh`:
   `allfeatsorted.txt`   => 597 network and sequence features
   `allrefexsorted.txt`  => 267 ReFeX features
   `allnetsorted.txt`    => 283 network features
   `allcentsorted.txt`   => 12 centralities
   `all.propsorted`      => network naive baseline (4 properties)
   `all.seqsorted`       => sequence Liu
   `allcentsorted.txt`   => 14 network
   `all12centsorted.txt` => 12 centralities

2. Change delimiter of `leaveoneoutnetworkacrossSVMAC_1.py` and then run
   the following.

3. `bash dothis.sh`

4. `for x in `/cat listrolx.txt`/; do (bash loo.sh "$x") > loo_"$x".sh; done`

5. `bash all.sh`
