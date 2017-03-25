To run the postagger HMM using bigrams:

python postagger.py data_public/hw3_train data_public/hw3_heldout

Expected output for input value: 1

ENGLISH LANGUAGE POS TAGGER
---------------------------------


Enter which smoothing to apply
1) Laplace (Add 1)
2) Backoff
3) Linear Interpolation

Enter your choice:
1
Training Completed
Should wait around 4 mins for every 10,000 sentences

Accuracy in training [35000 sentences]: 97.1367913238
Accuracy in training [13928 sentences]: 96.0443516494


Expected output for input value: 3

ENGLISH LANGUAGE POS TAGGER
---------------------------------


Enter which smoothing to apply
1) Laplace (Add 1)
2) Backoff
3) Linear Interpolation

Enter your choice:
1
Training Completed
Should wait around 4 mins for every 10,000 sentences

Accuracy in training [35000 sentences]: 97.0254359684
Accuracy in training [13928 sentences]: 95.9265807472

Expected output for input value: 2

ENGLISH LANGUAGE POS TAGGER
---------------------------------


Enter which smoothing to apply
1) Laplace (Add 1)
2) Backoff
3) Linear Interpolation

Enter your choice:
2
Training Completed
Should wait around 4 mins for every 10,000 sentences

Accuracy in training [35000 sentences]: 96.6756437045
Accuracy in training [13928 sentences]: 95.5758851719


To run the postagger HMM using trigrams:

python postagger_tri.py data_public/hw3_train data_public/hw3_test_tri

expected output:
Training Completed
Accuracy in training [2 sentences]: 16.6666666667
