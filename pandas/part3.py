"""
########## DATA TYPES ##########

Data types determine what type of values
are stored in a column.

Common data types:
- object (text)
- int64 (integer)
- float64 (decimal)
- bool (True/False)
"""

# dtypes          -> view data types
# dtype           -> single column type
# astype()        -> convert type

from pathlib import Path
import pandas as pd


file_path = Path(__file__).parent / "netflix_titles.csv"

netflix_df = pd.read_csv(file_path)


print(netflix_df.dtypes)          # Check Data Types of Each Column
print(netflix_df['release_year'].dtype)    # Check Data Type of a Specific Column

netflix_df['release_year'] = (
    netflix_df['release_year']
    .astype(str)                           # Convert Data Type
)
print(netflix_df['release_year'].dtype)


"""        Data Types using pandas notebook
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("netflix_titles.csv")
---------------------------------------------------
df.dtypes
df["release_year"].dtype
df["type"].astype("category").dtype

# text to real dates (strip first: the raw strings have stray spaces)
df["date_added"] = pd.to_datetime(df["date_added"].str.strip(), format="%B %d, %Y")
df["date_added"].dtype
df["date_added"].dt.year.head()
"""



"""
########## MISSING VALUES ##########

Missing values occur when data is not
available for a particular row or column.
"""

# isnull()        -> find missing values
# fillna()        -> replace missing values
# dropna()        -> remove missing values

print(netflix_df.isnull().sum())    # Count Missing Values in Each Column

missing_directors = netflix_df[
    netflix_df['director'].isnull()   # Filter Rows with Missing Values in a Column
]
print(missing_directors.head())


netflix_df['director'] = (
    netflix_df['director']
    .fillna('Unknown')             # Replace Missing Values
)


clean_df = netflix_df.dropna()    # Remove Missing Values
print(clean_df.shape)


"""     Missing Values Using Pandas Notebook
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("netflix_titles.csv")
---------------------------------------------------

df.isna().sum()
(df.isna().mean() * 100).round(1)       # percent missing
df[df["director"].isna()].head()

df["director"] = df["director"].fillna("Unknown")
df = df.dropna(subset=["date_added"])
"""



"""
########## RENAMING ##########

rename() allows us to change column names.
"""

# rename()        -> rename columns
# rename_axis()   -> rename index

renamed_df = netflix_df.rename(
    columns={
        'release_year': 'year'       # Rename One Column
    }
)
print(renamed_df.columns)


renamed_df = netflix_df.rename(
    columns={
        'title': 'movie_title',
        'release_year': 'year'          # Rename Multiple Columns
    }
)
print(renamed_df.columns)


renamed_df = netflix_df.rename_axis(
    'Record Number'                         # Rename Index
)
print(renamed_df.head())


"""       Renaming Using Pandas Notebook
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("netflix_titles.csv")
---------------------------------------------------

df = df.rename(columns={"listed_in": "genres"})
df.columns = df.columns.str.lower().str.replace(" ", "_")
df = df.rename_axis("row_id")        # name the index
"""




"""
########## COMBINING DATA ##########

Pandas can combine DataFrames using:

- concat()
- merge()
"""

# concat()        -> combine rows
# merge()         -> combine tables

movies = netflix_df[
    netflix_df['type'] == 'Movie'
].head(5)                                # Create Small Sample DataFrames
tv_shows = netflix_df[
    netflix_df['type'] == 'TV Show'
].head(5)


combined_df = pd.concat(
    [movies, tv_shows]
)                                        # Combine Rows
print(combined_df)


ratings_df = netflix_df[
    ['show_id', 'rating']
].head(10)
titles_df = netflix_df[
    ['show_id', 'title']
].head(10)
merged_df = pd.merge(                  # Merge Data
    titles_df,
    ratings_df,
    on='show_id'
)
print(merged_df)


"""           Combining Using Pandas Notebook
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("netflix_titles.csv")
---------------------------------------------------

movies = df[df["type"] == "Movie"]
shows = df[df["type"] == "TV Show"]
both = pd.concat([movies, shows])           # stack rows
both.shape == df.shape

# merge: attach a lookup table
audience = pd.DataFrame({
    "rating": ["TV-Y", "TV-Y7", "G", "TV-G", "PG", "TV-PG", "PG-13", "TV-14", "R", "TV-MA", "NC-17"],
    "audience": ["Kids", "Kids", "Kids", "Kids", "Family", "Family", "Teens", "Teens", "Adults", "Adults", "Adults"],
})
df = df.merge(audience, on="rating", how="left")

# join on the index
movies_per_year = movies.groupby("released").size().rename("movies")
shows_per_year = shows.groupby("released").size().rename("shows")
movies_per_year.to_frame().join(shows_per_year, how="outer").fillna(0)
"""




"""
########## MATPLOTLIB BASICS ##########

Matplotlib is used to create charts
and visualizations.
"""

#plt.plot()      -> line chart
#plt.bar()       -> bar chart
#plt.hist()      -> histogram
#plt.pie()       -> pie chart
#plt.scatter()   -> scatter plot
#plt.show()      -> display chart

import matplotlib.pyplot as plt

#        Line Chart
years = [2018, 2019, 2020, 2021, 2022]
titles = [500, 800, 1200, 1500, 1700]

plt.plot(years, titles)

plt.title("Netflix Titles Over Time")
plt.xlabel("Year")
plt.ylabel("Titles")

plt.show()


##      Bar Chart

# Count Movies and TV Shows using actual Netflix data:
type_counts = netflix_df["type"].value_counts()

type_counts.plot(
    kind='bar'
)

plt.title("Movies vs TV Shows")
plt.xlabel("Content Type")
plt.ylabel("Count")

plt.show()


"""       Matplotlip basics using notebook
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("netflix_titles.csv")

counts = df["type"].value_counts()

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(counts.index, counts.to_numpy())
ax.set_title("Titles by type")
ax.set_xlabel("Type")
ax.set_ylabel("Number of titles")
fig.savefig("titles_by_type.png", dpi=150)

plt.show()
"""


#    Histogram
#Release Year Distribution

plt.hist(
    netflix_df['release_year'],
    bins=20
)

plt.title("Release Year Distribution")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")

plt.show()



#      Pie Chart
type_counts.plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.title("Netflix Content Types")
plt.ylabel("")
plt.show()
