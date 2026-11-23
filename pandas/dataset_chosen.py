########## Load the data and take a first look: shape, dtypes, missing values, describe()

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
file_path = Path(__file__).parent / "netflix_titles.csv"

netflix_df = pd.read_csv(file_path)
"""
# Shape
print("\nSHAPE")
print(netflix_df.shape)

# Columns
print("\nCOLUMNS")
print(netflix_df.columns)

# Data Types
print("\nDTYPES")
print(netflix_df.dtypes)

# Missing Values
print("\nMISSING VALUES")
print(netflix_df.isnull().sum())

# Summary Statistics
print("\nDESCRIBE")
print(netflix_df.describe())

# First 5 Rows
print("\nHEAD")
print(netflix_df.head())
"""


#### Write down 5 questions you want the data to answer

             ########## Question 1 ##########
    #Are there more Movies or TV Shows on Netflix?
#Pandas:
type_counts = (
    netflix_df["type"]
    .value_counts()
)

print("\nMovies or TV Shows:")
print(type_counts)


#Visualization:
type_counts.plot(
    kind="bar",
    color=["steelblue", "orange"]
)

plt.title("Movies vs TV Shows")
plt.xlabel("Content Type")
plt.ylabel("Number of Titles")

plt.show()



"""  Question 1 Using Notebook
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
df = pd.read_csv("netflix_titles.csv")

counts = df["type"].value_counts()
print(counts)
print((df["type"].value_counts(normalize=True) * 100).round(1))

plt.figure(figsize=(6, 4))
sns.countplot(data=df, x="type", order=counts.index)
plt.title("Movies vs TV Shows")
plt.xlabel("Type")
plt.ylabel("Number of titles")
plt.show()
"""



             ########## QUESTION 2 ##########
   #What are the Top 10 Countries by Number of Titles?
#Pandas:
country_counts = (
    netflix_df["country"]
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)
)

print("\nTop 10 Countries by Number of Titles:")
print(country_counts)


#Visualization:
country_counts.plot(
    kind="bar"
)

plt.title("Top 10 Countries")
plt.xlabel("Country")
plt.ylabel("Number of Titles")

plt.show()



"""   Question 2 Using Notebook
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
df = pd.read_csv("netflix_titles.csv")

# many titles list several countries ("United States, India"), so split them first
countries = df["country"].dropna().str.split(",").explode().str.strip()
top_countries = countries.value_counts().head(10)
print(top_countries)

plt.figure(figsize=(8, 5))
sns.barplot(x=top_countries.to_numpy(), y=top_countries.index, orient="h")
plt.title("Top 10 countries by number of titles")
plt.xlabel("Number of titles")
plt.ylabel("Country")
plt.show()
"""




             ########## QUESTION 3 ##########
    #Which Release Years Have the Most Titles?
#Pandas:
titles_per_year = (
    netflix_df["release_year"]
    .value_counts()
    .sort_index()
)

print("\nRelease Years with the Most Titles:")
print(titles_per_year.tail())


#Visualization:
titles_per_year.plot(
    kind="line"
)

plt.title("Titles Released Per Year")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")

plt.show()



"""   Question 3 Using Notebook
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
df = pd.read_csv("netflix_titles.csv")

top_years = df["release_year"].value_counts().head(10)
print(top_years)

plt.figure(figsize=(8, 4))
sns.barplot(x=top_years.index.astype(str), y=top_years.to_numpy())
plt.title("Top 10 release years by number of titles")
plt.xlabel("Release year")
plt.ylabel("Number of titles")
plt.show()
"""




             ########## QUESTION 4 ##########
    #What Are the Most Common Ratings?
#Pandas:
rating_counts = (
    netflix_df["rating"]
    .value_counts()
)

print("\nMost Common Ratings:")
print(rating_counts)


#Visualization:
rating_counts.plot(
    kind="bar"
)

plt.title("Content Ratings")
plt.xlabel("Rating")
plt.ylabel("Count")

plt.show()



"""   Question 4 Using Notebook
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
df = pd.read_csv("netflix_titles.csv")

# a few rows have a duration like "74 min" stored in rating, so leave those out
ratings = df["rating"].dropna()
ratings = ratings[~ratings.str.contains("min")]

top_ratings = ratings.value_counts().head(10)
print(top_ratings)

plt.figure(figsize=(8, 4))
sns.barplot(x=top_ratings.index, y=top_ratings.to_numpy())
plt.title("Top 10 content ratings")
plt.xlabel("Rating")
plt.ylabel("Number of titles")
plt.show()
"""




             ########## QUESTION 5 ##########
    #What Does the Distribution of Release Years Look Like?
print("\nDistribution of Release Years:")
print(
    netflix_df["release_year"]
    .describe()
)


#Histogram:
netflix_df["release_year"].plot(
    kind="hist",
    bins=20
)

plt.title("Distribution of Release Years")
plt.xlabel("Release Year")
plt.ylabel("Frequency")

plt.show()



"""   Question 5 Using Notebook
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
df = pd.read_csv("netflix_titles.csv")

print(df["release_year"].describe())
print("median:", df["release_year"].median())
print("skew:", round(df["release_year"].skew(), 2))   # negative = long tail of older titles

plt.figure(figsize=(8, 4))
sns.histplot(data=df, x="release_year", bins=30, kde=True)
plt.axvline(df["release_year"].median(), color="red", linestyle="--", label="median")
plt.title("Distribution of release years")
plt.xlabel("Release year")
plt.ylabel("Number of titles")
plt.legend()
plt.show()
"""




             ########## BONUS QUESTION 6 ##########
   #Are There Outliers in Release Years?
#Box Plot:
netflix_df.boxplot(
    column="release_year"
)

plt.title("Release Year Box Plot")

plt.show()