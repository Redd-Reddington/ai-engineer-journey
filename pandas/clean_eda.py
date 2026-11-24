from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
file_path = Path(__file__).parent / "netflix_titles.csv"

netflix_df = pd.read_csv(file_path)


########## Data Cleaning Pass ##########

## Check Shape

print("\nSHAPE")
print(netflix_df.shape)

## Check Missing Values

print("\nMISSING VALUES")
print(netflix_df.isnull().sum())

"""
Questions:

Which columns have missing values?
How many missing values are there?
"""

## Check Duplicates

print("\nDUPLICATES")
print(netflix_df.duplicated().sum())

#Remove duplicates if any:
netflix_df = netflix_df.drop_duplicates()

## Check Data Types

print("\nDATA TYPES")
print(netflix_df.dtypes)

## Summary Statistics

print("\nSUMMARY")
print(netflix_df.describe())

## Check Outliers

#Use release year.
plt.boxplot(netflix_df["release_year"])

plt.title("Release Year Outliers")

plt.show()  



## Fix Missing Values and Types

# a few rows have a duration like "74 min" stored in rating
mask = netflix_df["rating"].str.contains("min", na=False)
print("\nMISPLACED RATINGS:", mask.sum())
netflix_df.loc[mask, "duration"] = netflix_df.loc[mask, "rating"]
netflix_df.loc[mask, "rating"] = None

for col in ["director", "cast", "country", "rating"]:
    netflix_df[col] = netflix_df[col].fillna("Unknown")

netflix_df["date_added"] = pd.to_datetime(
    netflix_df["date_added"].str.strip(), format="%B %d, %Y"
)

## Check Outliers (movie duration)

movies = netflix_df[netflix_df["type"] == "Movie"].copy()
movies["minutes"] = pd.to_numeric(
    movies["duration"].str.replace(" min", "", regex=False), errors="coerce"
)
q1, q3 = movies["minutes"].quantile([0.25, 0.75])
iqr = q3 - q1
outliers = movies[(movies["minutes"] < q1 - 1.5 * iqr) | (movies["minutes"] > q3 + 1.5 * iqr)]
print("\nDURATION OUTLIERS:", len(outliers))



########## Initial EDA (6 Visualizations) ##########

### Visualization 1 ###
#Movies vs TV Shows

netflix_df["type"].value_counts().plot(
kind="bar"
)

plt.title("Movies vs TV Shows")

plt.show()

#Question answered:
#Are there more Movies or TV Shows?



### Visualization 2 ###
#Movies vs TV Shows Pie Chart

netflix_df["type"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.ylabel("")

plt.title("Content Types")

plt.show()




### Visualization 3 ###
#Release Year Trend

(
    netflix_df["release_year"]
    .value_counts()
    .sort_index()
).plot(kind="line")

plt.title("Titles Released Over Time")

plt.show()

#Question answered:
#Which years produced the most content?




### Visualization 4 ###
#Ratings Distribution

netflix_df["rating"].value_counts().plot(
    kind="bar"
)

plt.title("Netflix Ratings")

plt.show()

#Question answered:
#What ratings are most common?




### Visualization 5 ###
#Release Year Histogram

netflix_df["release_year"].plot(
    kind="hist",
    bins=20
)

plt.title("Release Year Distribution")

plt.show()

#Question answered:
#How are titles distributed over time?




### Visualization 6 ###
#Top 10 Countries

country_counts = (
    netflix_df["country"]
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)
)

country_counts.plot(
    kind="bar"
)

plt.title("Top 10 Countries")

plt.show()

#Question answered:
#Which countries contribute the most content?




### Histogram ###

sns.histplot(
data=netflix_df,
x="release_year",
bins=20
)

plt.show()


###Box Plot ###

sns.boxplot(
    data=netflix_df,
    y="release_year"
)

plt.show()


###Count Plot ###

sns.countplot(
    data=netflix_df,
    x="type"
)

plt.show()




########## NUMPY Practice ##########

## Dot Product by Hand

import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

result = (
    a[0] * b[0]
    + a[1] * b[1]
    + a[2] * b[2]
)

print(result)

"""
Formula:
(1*4) + (2*5) + (3*6)
= 4 + 10 + 18
= 32
"""


## Matrix Multiplication by Hand

A = np.array([
    [1, 2],
    [3, 4]
])

B = np.array([
    [5, 6],
    [7, 8]
])

C = np.array([
    [
        (1*5) + (2*7),
        (1*6) + (2*8)
    ],
    [
        (3*5) + (4*7),
        (3*6) + (4*8)
    ]
])

print(C)
"""
[[19 22]
 [43 50]]
 """

print(result == np.dot(a, b))          # True

print(np.array_equal(C, A @ B))        # True