import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random


def make_data():
    '''
    Open the file and create a list of pairs
    '''
    with open('kmeans_dataset.txt') as f:
        data = []
        for line in f:
            x, y = line.split()
            data.append((float(x), float(y)))

    return data



def k_means(data):
    '''
    Run k-means on the data passed in
    '''
    #Run on 15 clusters
    k = 15
    sse = []
    final_clusters = []
    final_centroids = []

    #Run the algorithm 10 times and take the best result
    for i in range(10):
        #Randomly assign centroids and create the cluster matrix
        centroids = random.sample(data, k)
        clusters = [[centroids[j]] for j in range(k)]
        new_centroids = np.zeros((k, 2))

        #Continue iterating through the algorithm until convergence
        while not np.all(np.isclose(centroids, new_centroids)):
            #If not the first iteration, assign centroids to the previous result
            if np.all(new_centroids != np.zeros((k, 2))):
                clusters = [[] for m in range(k)]
                centroids = new_centroids
                new_centroids = np.zeros((k, 2))
            #Find the distance for each point to each centroid and assign
            #the point to the centroid with the shortest distance
            for point in data:
                distances = []
                for centroid in centroids:
                    distances.append(np.linalg.norm(np.array(point) - np.array(centroid)))
                clusters[distances.index(min(distances))].append(point)

            #Find the mean of all points in the cluster to create the new centroid
            for cluster in clusters:
                new_centroids[clusters.index(cluster)] = tuple(map(np.mean, zip(*cluster)))

        #Calculate the squared error for each cluster
        squared_error = 0
        for cluster in clusters:
            for point in cluster:
                squared_error += (np.linalg.norm(np.array(point) -
                                                 np.array(new_centroids[clusters.index(cluster)])))**2

        #Find the iteration with the smallest squared error
        sse.append(squared_error / k)
        final_clusters.append(clusters)
        final_centroids.append(new_centroids)
        min_sse_index = sse.index(min(sse))

    #Plot the best result
    for cluster in final_clusters[min_sse_index]:
        x = [x[0] for x in cluster]
        y = [y[1] for y in cluster]
        g = sns.scatterplot(x, y)
        g.set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])
    plt.show()



def main():
    data = make_data()
    k_means(data)



if __name__ == '__main__':
    main()
