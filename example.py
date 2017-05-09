import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load users info

userHeader = ['user_id','gender','age','ocupation','zip']
users = pd.read_table('dataSet/users.txt',engine='python',sep='::',header=None,names=userHeader)

#print 5 first users
#print("# 5 first users: \n%s" % users[:5])

# users.to_csv('Myusers.csv', sep=',')
myusers_csv = pd.read_csv('Myusers.csv', header=0)
print("# read fron csv: \n\n%s" % myusers_csv[:5])


#Load Movies
movieHeader = ['movie_id', 'title', 'genders']
movies = pd.read_table('dataSet/movies.txt', engine='python', sep='::', header=None, names=movieHeader)
#movies.to_csv('Mymovies.csv', sep=',')
mymovies_csv = pd.read_csv('Mymovies.csv',header=0)
print("# read movies from csv: \n\n%s" % mymovies_csv[:5])

# Load ratings
ratingHeader = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('dataSet/ratings.txt', engine='python', sep='::', header=None, names=ratingHeader)
#ratings.to_csv('Myratings.csv', sep=',')
myratings_csv = pd.read_csv('Myratings.csv', header=0)
print("# read ratings from csv: \n\n%s" % myratings_csv[:5])

# Merge tables users + ratings by user_id field
merger_ratings_users = pd.merge(users, ratings)
print('# Merge tables users + ratings by user_id field \n\n%s' % merger_ratings_users[:10])


# Merge all data
mergeRatings = pd.merge(pd.merge(users, ratings), movies)

info1000 = mergeRatings.ix[1000]
print('\nInfo of 1000 position of the table: \n%s' % info1000[:10])



# Clone DataFrame
def cloneDF(df):
    return pd.DataFrame(df.values.copy(), df.index.copy(), df.columns.copy()).convert_objects(convert_numeric=True)


# Show Films with more votes. (groupby + sorted)
numberRatings = cloneDF(mergeRatings)
numberRatings = numberRatings.groupby('title').size().sort_values(ascending=False)
print('Films with more votes: \n%s' % numberRatings[:10])
top20 = numberRatings[100:200]
print('>>>>>>>top20\n',top20)
top20_dict = top20.to_dict()
top20_items = top20_dict.items()

movies20_name = []
movies20_value = []

for name,value in top20_items:
	movies20_name.append(name)

for name,value in top20_items:
	movies20_value.append(value)

values20 = movies20_value
name20 = movies20_name
pos = np.arange(50)+.5

"""
plt.barh(pos, values20)
plt.yticks(pos, (name20))
plt.xlabel('ratings')
plt.title('top 5 movies')
plt.tight_layout()
plt.show()
"""
plt.hist(values20)
plt.title("Histograma de rankings")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()

print(">>>>>>>>>>movies\n",movies20_name)
print(">>>>>>>>>>moviesv\n",movies20_value)

"""
	Vemos como con el método 'groupby()' nos permite agrupar por la columna 
	que le indiquemos, con el método 'size()' nos hace la cuenta del número 
	de veces que se repiten los títulos tras la agrupación y por último 
	con el método 'sort_values()' nos ordena el resultado de mayor a menor
"""

# Show avg ratings movie (groupby + avg)
avgRatings = cloneDF(mergeRatings)
avgRatings = avgRatings.groupby(['movie_id', 'title']).mean()
print('Avg ratings: \n%s' % avgRatings['rating'][:20])
"""
	En este caso hemos indicado que nos muestre el valor medio del campo 'rating'
	, pero al aplicar el método 'mean()' en el DataFrame nos ha calculado todas 
	las médias de todas las columnas que tienen datos numéricos.
"""


# Show data ratings movies (groupby + several funtions)
dataRatings = cloneDF(mergeRatings)
dataRatings = dataRatings.groupby(['movie_id', 'title'])['rating'].agg(['mean', 'sum', 'count', 'std'])
print('Films ratings info: \n%s' % dataRatings[:10])

"""
	Ahora seguimos agrupando por titulo e identificador, pero además vamos a 
	hacer varios cálculos simultáneos que le indicaremos con una lista que 
	le pasamos al método 'agg()':
"""


# Show data ratings movies, applying a function (groupby + lambda function)
myAvg = cloneDF(mergeRatings)
myAvg = myAvg.groupby(['movie_id', 'title'])['rating'].agg(
    {'SUM': np.sum, 'COUNT': np.size, 'AVG': np.mean, 'myAVG': lambda x: x.sum() / float(x.count())})
print('My info ratings: \n%s' % myAvg[:10])



# Sort data ratings by created field (groupby + lambda function + sorted)
sortRatingsField = cloneDF(mergeRatings)
sortRatingsField = sortRatingsField.groupby(['movie_id', 'title'])['rating'].agg(
    {'COUNT': np.size, 'myAVG': lambda x: x.sum() / float(x.count())}).sort('COUNT', ascending=False)
print('My info sorted: \n%s' % sortRatingsField[:15])

"""
	Como último ejemplo vamos a agrupar por tíyulo e identificador y vamos 
	a calcular el número de votos recibidos por película, calculamos la nota 
	media y por último ordenamos las películas por el número de votos para poder 
	ver la nota media de las películas más votadas:
"""
