import numpy as np
import idx2numpy
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

EPOCHS = 50
INPUTS = 784
HIDDEN_NODES = 100
OUTPUT_NODES = 10
MOMENTUM = .9
LEARNING_RATE = .1

#convert files to a usable format
train_images = idx2numpy.convert_from_file('train-images.idx3-ubyte')
train_labels = idx2numpy.convert_from_file("train-labels.idx1-ubyte")
test_images = idx2numpy.convert_from_file("t10k-images.idx3-ubyte")
test_labels = idx2numpy.convert_from_file("t10k-labels.idx1-ubyte")

#normalize all images in both sets so that input values are between 0 and 1
normalize = np.vectorize(lambda i: float(i) / 255)
train_images = normalize(train_images)
test_images = normalize(test_images)

#create matrices with random initial weights and zeros to hold previous weights
#when calculating momentum
hweights = np.random.uniform(-.05, .05, (INPUTS + 1, HIDDEN_NODES))
oweights = np.random.uniform(-.05, .05, (HIDDEN_NODES + 1, OUTPUT_NODES))
prev_hweights = np.zeros((INPUTS + 1, HIDDEN_NODES))
prev_oweights = np.zeros((HIDDEN_NODES + 1, OUTPUT_NODES))

#initialize arrays for training and test accuracy
train_accuracy = np.zeros(EPOCHS)
test_accuracy = np.zeros(EPOCHS)



#return sigmoid of output
def sigmoid(z):
    return 1 / (1 + np.exp(-z))



#forward propagate through both layers of the NN
def forward_prop(image, hweights, oweights):
    #create lists to hold activation values
    hnode_activation = np.zeros(HIDDEN_NODES)
    onode_activation = np.zeros(OUTPUT_NODES)

    #calculate hidden node activation values when passing in the image input by
    #taking the sigmoid of the sum of the dot product of the inputs and weights
    hnode_activation = sigmoid(np.dot(image, hweights))
    #add a bias input to the end of the hidden node activation array
    hnode_activation = np.append(hnode_activation, 1)
    #calculate output node activation values when passing in hidden nodes as
    #input in a similar fashion to calculating the hidden node values above
    onode_activation = sigmoid(np.dot(hnode_activation, oweights))

    return (np.argmax(onode_activation), hnode_activation, onode_activation)



#back propagate if the result from forward prop doesn't match the target
def back_prop(target, image, prev_hweights, prev_oweights, hweights, \
              oweights, hnode_activation, onode_activation):
    #create lists for hidden node and output node error
    oerror = np.zeros(OUTPUT_NODES)
    herror = np.zeros(HIDDEN_NODES)
    #calculates half of the error equation: output * (1 - output)
    errorcalc = np.vectorize(lambda i: i * (1 - i))

    #if target node, use target value of .9, otherwise use .1 to calculate
    #error
    oerror = errorcalc(onode_activation)
    for i in range(len(onode_activation)):
        if (i == target):
            oerror[i] *= (.9 - onode_activation[i])
        else:
            oerror[i] *= (.1 - onode_activation[i])

    #calculate output * (1 - output) for each node in the hidden layer, then do
    #an element wise multiplication with the dot product of the output weights
    #and the output error
    herror = errorcalc(hnode_activation)
    oweights_cross_oerror = np.dot(oerror, np.transpose(oweights))
    herror = np.multiply(herror, oweights_cross_oerror)

    #calculate the learning rate * output node error * input, as well as
    #momentum * (t-1) weights and store them in temp variables, then add them
    #to output node weights to update
    learn_temp = LEARNING_RATE * np.dot(oerror[:,None], hnode_activation[None,:])
    momentum_temp = MOMENTUM * prev_oweights
    prev_oweights = learn_temp.T + momentum_temp
    oweights += prev_oweights

    #calculate the learning rate * hidden node error * input, as well as
    #momentum * (t-1) weights and store them in temp variables, then add them
    #to hidden node weights to update
    learn_temp = LEARNING_RATE * np.dot(herror[:-1,None], image[None,:])
    momentum_temp = MOMENTUM * prev_hweights
    prev_hweights = learn_temp.T + momentum_temp
    hweights += prev_hweights

    return (prev_hweights, prev_oweights, hweights, oweights)






#train and test the data sets for each epoch
for x in range(EPOCHS):
    #randomize the inputs and targets to eliminate training in the same order
    #over multiple epochs
    np.random.seed(x)
    np.random.shuffle(train_images)
    np.random.seed(x)
    np.random.shuffle(train_labels)

    #training set:
    correct = 0 #variable to hold number of correct results
    for i in range(len(train_images)):
        #turn the image into from a matrix into a single list and add a 1 at
        #the end for a bias
        image = train_images[i].flatten()
        image = np.append(image, 1)

        #call the forward prop function and store return variables
        result, hnode_activation, onode_activation = \
                forward_prop(image, hweights, oweights)
        #if the result is correct, increment correct counter and do nothing
        if (result == train_labels[i]):
            correct += 1
        #otherwise, run the back prop function to update the weights
        else:
            prev_hweights, prev_oweights, hweights, oweights = \
                    back_prop(train_labels[i], image, prev_hweights, \
                              prev_oweights, hweights, oweights, \
                              hnode_activation, onode_activation)

    #store ratio of correct results to images processed to plot later
    train_accuracy[x] = (float(correct)/len(train_images))

    #test set:
    correct = 0
    #create a confusion matrix at last epoch
    if(x == EPOCHS - 1):
        cm = np.zeros((OUTPUT_NODES, OUTPUT_NODES), dtype = int)

    for i in range(len(test_images)):
        image = test_images[i].flatten()
        image = np.append(image, 1)

        result, hnode_activation, onode_activation = \
                forward_prop(image, hweights, oweights)
        if (result == test_labels[i]):
            correct += 1
        #update confusion matrix at last epoch
        if(x == EPOCHS - 1):
            cm[result][test_labels[i]] += 1

    #print confusion matrix at last epoch
    if(x == EPOCHS - 1):
        print(cm)

    test_accuracy[x] = (float(correct)/len(test_images))

#plot the ratio of correct results to total images processed for both training
#data and test data at each epoch
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Network Accuracy')
plt.gca().yaxis.set_major_formatter(PercentFormatter())
train_data, = plt.plot(train_accuracy * 100, 'b-')
test_data, = plt.plot(test_accuracy * 100, 'g-')
plt.legend([train_data, test_data], ['Training Data', 'Test Data'])
plt.show()
