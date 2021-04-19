'''This program implements the basic K-means algorithm and returns the following:
1 - Print out of the initial data as read from the csv file (3 csv files are used namely "data1953.txt", "data2008.csv"'
    and "dataBoth.csv". Note that any one of these files can be used but for the purposed of this task "databoth"
    were used. Each of the files have however been tested.
2 - A randomly selected set of centroids printouts based on the "k" input received from the user.
3 - A print out of the newly rewritten centroids after each iteration based on
    the mean calculation of the cluster data points.
4 - The sum of the counts of countries per cluster upon each iteration.
5 - A list of countries per cluster after each iteration.
6 - Birth Rate and Life Expectancy Averages per cluster upon each iterations.
7 - A plot of each iteration's cluster configuration.'''

# Note this is compulsary task 1 and 2 for task 22 level 3
# When the code is run the first figure must be closed (closing the window) to see the final and second figure
# that is plotted. The second figure must also be closed (the window) to allow for the next figure (the update) to
# show if the user requested more than one iteration. The isteration will then also be printed out until the last iteration is printed.
 
import random                         # This is forvthe random centroids.
import numpy as np                    # For various data wrangling tasks
from math import sqrt                 # For returning the square root of a number or calculation
import matplotlib.pyplot as plt       # For plots on the graph/figures
import seaborn as sns                 # For plots, their styling and colouring.
import pandas as pd                   # For reading of the data and drawing inferences from it
pd.options.display.max_rows = 4000    # To display all the rows of the data frame


def read_csv_pd(filename):  
    '''Reading a csv file with pandas that prints the dataframe and returns
    the two columns in numpy array for processing and also the country names in
    numpy array needed for cluster matched results'''
    data1 = pd.read_csv(filename, delimiter=',')
    print(data1)
    country_names = data1[data1.columns[0]].values
    list_array = data1[[
        data1.columns[1], data1.columns[2]]].values
    return list_array, country_names

def distance_between(cent, data_points):
    '''Calculates the euclidean distance between each data point and each centroid.
    It appends all the values to a list and returns this list.'''
    distances_arr = []     # create a list to which all distance calculations could be appended.
    for centroid in cent:
        for datapoint in data_points:
            distances_arr.append(
                sqrt((datapoint[0]-centroid[0])**2 + (datapoint[1]-centroid[1])**2))
    return distances_arr


# Assign the function for reading the csv to a variable as this will deliver for us a
# Numpy array with all the values in the two columns as well as the country names in a
# separate array. We can access them via slicing.
x = read_csv_pd("dataBoth.csv")
# convert the ndarray to a list for sampling
x_list = np.ndarray.tolist(x[0][0:, :])

# User imput for the number of clusters
# in addition to the number of iterations that the algorithm must run
k = int(input("Please enter the number of clusters: "))
iterations = int(
    input("Please enter the number of iterations that the algorithm must run: "))

# Set the random number of centroids based on the user input value of "k".
centroids = random.sample(x_list, k)
print('The Randomly selected Centroids are: ' + str(centroids))


def assign_to_cluster_mean_centroid (x_in=x, centroids_in=centroids, n_user=k):
    '''Calling the distance_between() function. Each data point is pinpointed
    to the cluster/centroid it is the closest to. It also rewrites the centroids
    with the newly calculated means. Lastly a list is returned with the allocation of clusters
    with regards to the ordering of the countries as well as returning the cluster dictionary.
    Finally it returns the list with cluster allocations that are 
    in line with the order of the countries. It also returns the clusters dictionary.'''
    distances_arr_re = np.reshape(distance_between(
        centroids_in, x_in[0]), (len(centroids_in), len(x_in[0])))
    datapoint_cen = []
    distances_min = []                        # Done if needed
    for value in zip(*distances_arr_re):
        distances_min.append(min(value))
        datapoint_cen.append(np.argmin(value)+1)
    # Create clusters dictionary and add number of clusters according to
    # user input
    clusters = {}
    for no_user in range(0, n_user):
        clusters[no_user+1] = []
    # Allocate each data point to it's closest cluster
    for d_point, cent in zip(x_in[0], datapoint_cen):
        clusters[cent].append(d_point)

    # Run a for loop and rewrite the centroids
    # with the newly calculated means
    for i, cluster in enumerate(clusters):
        reshaped = np.reshape(clusters[cluster], (len(clusters[cluster]), 2))
        centroids[i][0] = sum(reshaped[0:, 0])/len(reshaped[0:, 0])
        centroids[i][1] = sum(reshaped[0:, 1])/len(reshaped[0:, 1])
    print('Iteration centroids are :' + str(centroids))
    return datapoint_cen, clusters

# Scatterplot of the data before clustering
plt.scatter(x[0][0:, 0], x[0][0:, 1])
plt.xlabel('Birthrate')
plt.ylabel('Life Expectancy')
plt.title('Data points with randomly selected centroids\nNo data points allocated')
cv = np.reshape(centroids, (k, 2))
plt.plot(cv[0:, 0], cv[0:, 1],
         c='#000000', marker="*", markersize=15, linestyle=None, linewidth=0)
plt.show()

# set the font size of the labels on matplotlib
plt.rc('font', size=14)

# set style of plots
sns.set_style('dark')

# define a custom pallette
customPalette = ['#630C3A', '#39C8C6', '#D3500C', '#FFB139',
                 '#53ff39', '#3943ff', '#e539ff', '#39f5ff',
                 '#8B008B', '#C71585', '#00008B', '#66CDAA']
sns.set_palette(customPalette)
# The below line is to print a palette if needed.
# sns.palplot(customPalette)

# =========
# MAIN LOOP
# =========

for iteration in range(0, iterations):
    # Print the iteration number
    print("ITERATION: " + str(iteration+1))
    # assign the function to a variable as it has more than one return value
    assigning = assign_to_cluster_mean_centroid()
    # Create the dataframe for vizualisation
    cluster_data = pd.DataFrame({'Birth Rate': x[0][0:, 0],
                                 'Life Expectancy': x[0][0:, 1],
                                 'label': assigning[0],
                                 'Country': x[1]})

    # Create the dataframe and grouping, then print out inferences
    group_by_cluster = cluster_data[['Country', 'Birth Rate', 'Life Expectancy', 'label']].groupby('label')
    count_clusters = group_by_cluster.count()
    # Inference 1
    print("COUNTRIES PER CLUSTER: \n" + str(count_clusters))
    # Inference 2
    print("LIST OF COUNTRIES PER CLUSTER: \n",
          list(group_by_cluster))
    # Inference 3
    print("AVERAGES: \n", str(cluster_data.groupby(['label']).mean()))

    # Set the variable mean that holds the clusters dict
    mean = assigning[1]
    # create a dict that will hold the distances of between each data point in
    # a particular cluster and its mean. The loop here will create the amount of clusters based
    # on user input.
    means = {}
    for clst in range(0, k):
        means[clst+1] = []

    # Create a for loop to calculate the squared distances between each
    # data point and its cluster mean
    for index, data in enumerate(mean):
        array = np.array(mean[data])
        array = np.reshape(array, (len(array), 2))
        # Set two variables, one for each variable in the data set that
        # holds the calculation of the cluster mean of each variable
        birth_rate = sum(array[0:, 0])/len(array[0:, 0])
        life_exp = sum(array[0:, 1])/len(array[0:, 1])
        # within this for loop, create another for loop that appends to the means dict
        # the squared distance of between each data point in it's cluster and the cluster mean.
        for data_point in array:
            distance = sqrt(
                (birth_rate-data_point[0])**2+(life_exp-data_point[1])**2)
            means[index+1].append(distance)
    # create a list that will hold all the sums of the means in each of the clusters.
    total_distance = []
    for ind, summed in enumerate(means):
        total_distance.append(sum(means[ind+1]))

    # print the summed distance
    print("Total distance of all the clusters: " + str(sum(total_distance)))

    # plot data with seaborn. This plot will show the clusters in colour with the centroids
    facet = sns.lmplot(data=cluster_data, x='Birth Rate', y='Life Expectancy', hue='label',
                       fit_reg=False, legend=False, legend_out=False)
    plt.legend(loc='upper right')
    centr = np.reshape(centroids, (k, 2))
    # centroids plot
    plt.plot(centr[0:, 0], centr[0:, 1],
             c='#000000', marker="*", markersize=15, linestyle=None, linewidth=0)
    plt.title('Iteration: ' + str(iteration+1) +
              "\nTotal distance of all clusters: " + str(round(sum(total_distance), 0)))
    # print the sns plot
    plt.show()
