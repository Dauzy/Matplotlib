# -*- coding: utf-8 -*-

# Data Graduates: Analysis and Other Examples
# Author: Jorge Raze

# First import urllib for downloading and uncompress the file

import urllib.request
import zipfile
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean


DEBUG = False

# # This is the URL for the public data
url = "http://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
# This is the working directory
working_dir = "./data/movies/"
# Destination filename
file_name = working_dir + "movies.zip"
# We already know the expected files so:
expected_files = [
    'links.csv',
    'movies.csv',
    'ratings.csv',
    'README.txt',
    'tags.csv']
# movie.ID mv.ID MV.ID MV_ID
movie_names = ['movie_id', 'title', 'genres']
rating_names = ['user_id', 'movie_id', 'rating', 'timestamp']
# Helper arrays for generating the final files
filenames_array = [
    working_dir + 'top20.csv',
    working_dir + 'top5.csv',
    working_dir + 'final.csv']


# Download the file from `url` and save it locally under `file_name`:
if os.path.isfile(file_name):
    if DEBUG:
        print('Data is already downloaded')
else:
    if DEBUG:
        print("Downloading file")
    urllib.request.urlretrieve(url, file_name)

# There's an extra dir level in thwe extracted files
inner_dir = "ml-latest-small/"
# I want to know the names of the extracted files
file_names = os.listdir(working_dir + inner_dir)

if file_names == expected_files:
    if DEBUG:
        print("You already have the data files, check it!")
else:
    # This is the code for uncompress hte zipfile
    path_to_zip_file = working_dir + "movies.zip"
    # Reference to zipfile
    zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
    print("Extracting files")
    zip_ref.extractall(working_dir)
    # Is important to use .close()
    zip_ref.close()


# Reading the files needed for this analysis
movies = pd.read_csv(
    working_dir +
    inner_dir +
    expected_files[1],
    sep=',',
    names=movie_names)
ratings = pd.read_csv(
    working_dir +
    inner_dir +
    expected_files[2],
    sep=',',
    names=rating_names)


# Let's print the first lines of each dataframe
if DEBUG:
    print(movies.head())
    print(ratings.head())

    print("The names of our new data frames are:")
    print(list(movies.columns.values))
    print(list(ratings.columns.values))

    print("The dimension of the dataframes are:")
    print(movies.count())
    print(ratings.count())

rated_movies = pd.merge(movies, ratings, on='movie_id')
rated_movies = rated_movies.sort_values('rating', ascending=False)



#dicount = rated_movies['movie_id'].groupby(rated_movies['title']).count()
dicount = rated_movies['title'].groupby(rated_movies['title']).count()
dicrating = rated_movies['title'].groupby(rated_movies['title']).count()
#print(dicount)
#print(">>>>>>>> vlas")
#print(dicrating['title'])
"""
for idmov,countt in dicount:
    moviesid.append(idmov)

for idmov, countt in dicount:
    moviescount.append(countt)
""" 
#print(dicount)
#print(rated_movies['title'].groupby(rated_movies['title'].count())
#print(rated_movies[rated_movies['title'] == 'Shawshank Redemption, The (1994)'])
rated_movies.to_csv(working_dir + 'rated_movies.csv')


# Number of movies: 9126
# Number of evaluations: 100005

# Rated movies names:
# ['movie_id', 'title', 'genres', 'user_id', 'rating', 'timestamp']

# Shortcut for names
rated_movies.dtypes

# Get summary of your data
rated_movies.describe()
#print(rated_movies['movie_id'])


# Getting the Transpose
transposed_movies = rated_movies.T

# Sorting by an index
rated_movies.sort_index(axis=1, ascending=False)

# You can get the first two rows with
rated_movies[0:3]

# You can select data based in value of a column
rated_movies['rating'] = pd.to_numeric(rated_movies['rating'][1:100005])
rated_movies[rated_movies['rating'] > 4]
rated_movies[rated_movies['title'] == 'Shawshank Redemption, The (1994)']

#print(rated_movies)

# rated_movies = rated_movies.pop(0)

#rat = rated_movies.groupby('id')
#print(rat)


# You can aggregate data like this  
grouped = rated_movies.groupby('title')
groupcout = rated_movies.groupby('title').count()
groupedd = rated_movies.groupby('title').mean()
kgrouped = groupedd.to_dict()['rating']
group_by_sum = grouped.aggregate(sum)
group_by_mean = grouped.aggregate(mean)
#group_by_count = grouped.aggregate(count)
# Or the short way
grouped = rated_movies.groupby('title').sum()
print(groupcout)

dict1={}

for s in kgrouped.values():
    s = round(s)
    if(s.is_integer()):
        dict1[int(s)] = dict1.get(s, 0) + 1

val=list(dict1.values())
mx=max(val)
val_mx = []
for i in val:
    val_mx.append(i/mx)
key=list(dict1.keys())




# Subsetting for our results
top20 = grouped.sort_values('rating', ascending=False)[0:20]
top5 = top20[0:5]
# Wee need to transform it to a dict
# so we can get the movies' titles
top5_dict = top5.to_dict()
# We need to get the items (Movies titles)
top5_items = top5_dict['rating'].items()
#print(top5_dict['rating'])
# A helper array for stacking the results per movie
frames = []
#print(top5_items)
# A for loop for getting all the results matching a movie
for name, value in top5_items:
    frames.append(rated_movies[rated_movies['title'] == name])

# Concatenate into a single data frame
result = pd.concat(frames)

# Helper array for generating target files
final_variables_array = [top20, top5, result]
#print(top20.values)
#print(top5)
#print(">>>>>>>reuslt ",final_variables_array[0])

# We can get the observations as well
ratings_by_title = rated_movies.groupby('title').size()
# Do we need to subset?
hottest_titles = ratings_by_title.index[ratings_by_title >= 250]

# Getting the mean of rated movies
mean_ratings = rated_movies.pivot_table(
    'rating',
    index='title',
    aggfunc='mean')

# The mean of the hottest movies
mean_ratings = mean_ratings.ix[hottest_titles]
#print(">>>>>>>> ",mean_ratings)

movies5_name = []
movies5_ratings = []
text_size = 10

for name, value in top5_items:
    movies5_name.append(name)

for name, value in top5_items:
    movies5_ratings.append(value)

#print(movies5_name)
#print(movies5_ratings)

values5 = movies5_ratings
name5 = movies5_name
pos = np.arange(5)+.5


plt.plot(pos,values5)
plt.xticks(pos,(name5), fontsize= 5)
plt.ylabel("Values")
#plt.xlabel(movies5_name, fontsize = 8)
plt.title("Top 5 movies")
plt.tight_layout()
plt.show()


plt.bar(pos,values5)
plt.xticks(pos, (name5), fontsize= 5)
plt.xlabel('ratings')
plt.title('top 5 movies')
plt.tight_layout()
plt.show()

plt.bar(key,val)
plt.title('ratings mas repetidos')
plt.xlabel('ratings');
plt.ylabel('Peliculas');
plt.show()

bins = np.asarray([0.5,1.5,2.5,3.5,4.5,5.5])
values = np.asarray(rat.values()) 
plt.hist(list(rat.values()),bins=bins)
plt.show()


# For loop for generating the files
for i in range(3):
    if os.path.isfile(filenames_array[i]):
        if DEBUG:
            print("File %s already exists!" % i)
    else:
        # Export to CSV
        print("Exporting file to CSV")
final_variables_array[i].to_csv(filenames_array[i])