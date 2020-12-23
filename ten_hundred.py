# ------------------------------------------------------------------------------
# Filename: ten_hundred.py
# Project: P7 COVID-19 Growth Trend Clustering
# Author: Nicholas Moeller
# Course: CS540, Spring 2020, LEC 001
# ------------------------------ 80 COLUMNS WIDE -------------------------------
import csv
import scipy
import scipy.cluster
import scipy.spatial
import numpy as np
import math


# takes in a string with a path to a CSV file formatted as in the link above,
# and returns the data (without the lat/long columns but retaining all other columns) in a single structure.
def load_data(filepath):
    dict = []
    with open('covid19.csv') as file:
        reader = list(csv.reader(file))
        header_list = []
        # Create a list that contains the headers without including Lat and Long
        for header in reader[0]:
            header_list.append(header)

        # Add the values to each dictionary header
        for row in reader[1:]:
            temp_dict = {}
            index = 0
            for x in header_list:
                if index != 2 and index != 3:
                    temp_dict[x] = row[index]
                index += 1
            dict.append(temp_dict)

    # Returns a list of the dictionaries
    return dict


#takes in one row from the data loaded from the previous function,
# calculates the corresponding x, y values for that region as specified in the video,
# and returns them in a single structure.
def calculate_x_y(time_series):
    last = '' # Last date in series
    for day in time_series:
        last = day

    n_10 = '' # Inititalize
    n_100 = '' # Inititalize
    n = time_series[last]  # Latest data point
    if n == 0:
        x = float("Nan")
        y = float("Nan")
        return (x, y)

    else:
        # Find the day in which there are n/10 cases or just less
        for day in time_series:
            if time_series[day].isdigit():
                if int(time_series[day]) <= int(n)/10:
                    n_10 = day
                else:
                    continue

        # Find the day in which there are n/100 cases or just less
        for day in time_series:
            if time_series[day].isdigit():
                if int(time_series[day]) <= int(n)/100:
                    n_100 = day
                else:
                    continue

        x = 0 # Initialize
        y = 0 # Initialize
        # Calculate the x and y values
        for day in time_series:
            if time_series[day].isdigit():
                if n_10 == '':
                    x = float("Nan")
                elif int(time_series[day]) > int(time_series[n_10]):
                   x += 1
                else:
                    None
                if n_100 == '':
                    y = float("NaN")
                elif int(time_series[day]) > int(time_series[n_100]):
                    y += 1
                else:
                    None
                if y > 0 and int(time_series[day]) == 0:
                    y = 0
        if x == 0:
            x = float("Nan")
            y = float("Nan")

        if math.isnan(y) or math.isnan(x):
            return(x,y)
        else:
            y = y - x
            return (x, y)

# performs single linkage hierarchical agglomerative clustering
# on the regions with the (x,y) feature representation,  and returns a data structure representing the clustering.
def hac(dataset):
    index = 0 # Compute the index of a given cluster
    new_data = []
    # Filter out data with nan within set
    for data in dataset:
        if math.isnan(data[0]):
            continue
        if math.isnan(data[1]):
            continue
        else:
            new_data.append(data)

    # Create each point into a cluster
    clusters = list()
    for i in range(len(new_data)):
        data = list()
        data.append(i)
        data.append(new_data[i])
        clusters.append(data)

    hac_array = [] # Array for storing the cluster data
    length = len(clusters) # Length of array

    # Hierarchial clustering algorithm
    while len(clusters) > 1:
        closest_distance_value_total = 100
        closest_distance_pair_total = clusters[0]
        closest_distance_cluster_total = clusters[0]

        for row in clusters:
            # If distance is 0 end loop
            if closest_distance_value_total == 0:
                break
            closest_distance_value = 100 # Track the pairs with the closest distance

            for compared_row in clusters:
                # Skip if they are the same row
                if row == compared_row:
                    continue

                d = 100 # Initialize the distance variable

                # If the row has more than one cluster
                if compared_row[0] > 244 or row[0] > 244:
                    for x in range(len(compared_row))[1:]:
                        d_temp = scipy.spatial.distance.euclidean(row[1], compared_row[x])
                        if d == 0 or d == 0.0:
                            break
                        if d_temp < d:
                            d = d_temp
                    if d == 0:
                        closest_distance_value_total = 0
                        closest_distance_cluster_total = row
                        closest_distance_pair_total = compared_row
                        break

                    # Locate the closest pair for a given row
                    if d < closest_distance_value:
                        closest_distance_value = d
                        if closest_distance_value < closest_distance_value_total:
                            closest_distance_value_total = closest_distance_value
                            closest_distance_cluster_total = row
                            closest_distance_pair_total = compared_row

                # If row has less than one cluster
                else:
                    d = scipy.spatial.distance.euclidean(row[1],compared_row[1])
                    if d == 0:
                        closest_distance_value_total = 0
                        closest_distance_cluster_total = row
                        closest_distance_pair_total = compared_row
                        break

                    # Locate the closest pair for a given row
                    if d < closest_distance_value:
                        closest_distance_value = d
                        if closest_distance_value < closest_distance_value_total:
                            closest_distance_value_total = closest_distance_value
                            closest_distance_cluster_total = row
                            closest_distance_pair_total = compared_row

        # Update the clusters list
        cluster_data = []
        cluster_data.append(index + length)
        for i in range(len(closest_distance_cluster_total))[1:]:
            cluster_data.append(closest_distance_cluster_total[i])
        for j in range(len(closest_distance_pair_total))[1:]:
            cluster_data.append(closest_distance_pair_total[j])
        clusters.append(cluster_data)
        index += 1

        # Add the data to a new array
        hac_array_data = []
        hac_array_data.insert(0, closest_distance_cluster_total[0])
        hac_array_data.insert(1, closest_distance_pair_total[0])
        hac_array_data.insert(2, closest_distance_value_total)
        hac_array_data.insert(3, len(clusters[len(clusters)-1]) - 1)
        hac_array.append(hac_array_data)

        # Remove the clusters that were just added
        clusters.remove(closest_distance_cluster_total)
        clusters.remove(closest_distance_pair_total)

    # Convert to np array before returning
    hac_array = np.array(hac_array)
    return hac_array

data = load_data('covid19.csv')
time_series = []
for x in data:
    temp = []
    x,y = calculate_x_y(x)
    temp.append(x)
    temp.append(y)
    time_series.append(temp)
print(hac(time_series))
