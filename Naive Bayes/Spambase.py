import numpy as np

#after splitting data into a training set of both spam and not spam, as well as
#a test set read in from the corresponding file and put into a matrix
spam_train_set = np.genfromtxt('spamtrainset.txt', delimiter=',')
ns_train_set = np.genfromtxt('nstrainset.txt', delimiter=',')
test_set = np.genfromtxt('testset.txt', delimiter=',')

#creates constants referenced in the program
SPAM_TRAIN_SET_EXAMPLES = spam_train_set.shape[0]
NS_TRAIN_SET_EXAMPLES = ns_train_set.shape[0]
TEST_SET_EXAMPLES = test_set.shape[0]
FEATURES = spam_train_set.shape[1]

#calculate the prior probabilities that the example is spam or not spam in
#roughly a 40% spam to 60% not spam ratio
spam_prior = float(SPAM_TRAIN_SET_EXAMPLES)/(SPAM_TRAIN_SET_EXAMPLES + NS_TRAIN_SET_EXAMPLES)
ns_prior = float(NS_TRAIN_SET_EXAMPLES)/(SPAM_TRAIN_SET_EXAMPLES + NS_TRAIN_SET_EXAMPLES)

#calculate the mean and standard deviation of the spam and not spam training set
spam_train_mean = spam_train_set.mean(0)[:-1]
spam_train_std = spam_train_set.std(0)[:-1]
ns_train_mean = ns_train_set.mean(0)[:-1]
ns_train_std = ns_train_set.std(0)[:-1]

#if we have a 0 standard deviation, replace with .0001 to avoid dividing by 0
#in the naive bayes calculation
for i in range(len(spam_train_std)):
    if(spam_train_std[i] == 0):
        spam_train_std[i] += .0001

for i in range(len(ns_train_std)):
    if(ns_train_std[i] == 0):
        ns_train_std[i] += .0001

#calculate the probability that a feature is in the given class using
#naive bayes algorithm
def prob_density(x, mean, std):
    return (1 / (np.sqrt(2 * np.pi) * std)) * (
        np.exp(-np.power((x - mean), 2) / (2 * np.power(std, 2))))

#replaces all values of 0 in the matrix passed in with the smallest value in the
#test set to avoid taking a log of 0
def replace_zeros(arr, value):
    for i in range(TEST_SET_EXAMPLES):
        for j in range(FEATURES - 1):
            if(arr[i][j] == 0):
                arr[i][j] = value
    return arr

#finds the smallest value in the test set and calls the above function to replace
#all values of 0 in the spam and not spam probability matrices with this value
def find_min_and_replace(arr1, arr2):
    min_val = min(arr1[arr1 > 0].min(), arr2[arr2 > 0].min())
    arr1 = replace_zeros(arr1, min_val)
    arr2 = replace_zeros(arr2, min_val)

    return (arr1, arr2)

#create matrices to hold values for spam and not spam probabilities as well as
#a confusion matrix
ns_density = np.zeros((TEST_SET_EXAMPLES, FEATURES - 1))
spam_density = np.zeros((TEST_SET_EXAMPLES, FEATURES - 1))
confusion_matrix = np.zeros((2,2))

#run the naive bayes algorithm on all elements in the test set and set the values
#to the corresponding spam and not spam matrices
for i in range(TEST_SET_EXAMPLES):
    for j in range(FEATURES - 1):
        ns_density[i][j] = prob_density(test_set[i][j], ns_train_mean[j], ns_train_std[j])
        spam_density[i][j] = prob_density(test_set[i][j], spam_train_mean[j], spam_train_std[j])

#call the function to find the min value in the test set and replace all zeros
#in the spam and not spam matrices
ns_density, spam_density = find_min_and_replace(ns_density, spam_density)
#calculate the probability that an example is spam or not spam by taking the log
#of the prior plus the sum of the log of all features in the example
prob_ns = np.log(ns_prior) + np.sum(np.log(ns_density), axis = 1)
prob_spam = np.log(spam_prior) + np.sum(np.log(spam_density), axis = 1)

#loop through all examples and predict if it is spam or not spam
for i in range(TEST_SET_EXAMPLES):
    if(prob_ns[i] > prob_spam[i]):
        predicted_class = 0
    else:
        predicted_class = 1
    #put the prediction into the confusion matrix
    confusion_matrix[int(test_set[i][FEATURES - 1]), predicted_class] += 1

#print consufion matrix, accuracy, precision, and recall
print 'Confusion Matrix:'
print confusion_matrix
print ' '
print 'Accuracy: ', ((confusion_matrix[0][0] + confusion_matrix[1][1]) /
                      np.sum(confusion_matrix))
print 'Precision: ', (confusion_matrix[0][0] / np.sum(confusion_matrix,
                                                       axis=0)[0])
print 'Recall: ', (confusion_matrix[0][0] / np.sum(confusion_matrix,
                                                    axis=1)[0])
