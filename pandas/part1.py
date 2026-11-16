from pathlib import Path

import pandas as pd

"""
 ########## CREATING DATA ##########

df = pd.DataFrame({
    'Yes': [50, 21],
    'No': [131, 2]
})

print(df)

print()
print("-" * 40)
print()

df2 = pd.DataFrame({
    'Bob': ['I liked it.', 'It was awful.'], 
    'Sue': ['Pretty good.', 'Bland.']
})

print(df2)

print()
print("-" * 40)
print()

s = pd.Series([1, 2, 3, 4, 5])

print(s)

print()
print("-" * 40)
print()

s2 = pd.Series(
    [30, 35, 40],
    index=[
        '2015 Sales',
        '2016 Sales',
        '2017 Sales'
    ],
    name='Product A'
)

print(s2)
"""



"""
########## READING DATA FILES ##########

Pandas can read data from CSV files using:

- pd.read_csv()

CSV stands for:
Comma-Separated Values

A CSV file stores data in rows and columns,
making it easy to load into a DataFrame.
"""

file_path = Path(__file__).parent / "netflix_titles.csv"

netflix_df = pd.read_csv(file_path)

print(netflix_df)   # print everthing
print(netflix_df.head())  # print first 5 rows
print(netflix_df.tail())  # print last 5 rows
print(netflix_df.shape)   # check number of rows and columns
print(netflix_df.columns) # view column names

"""  Part 1: Inspect
df.head()
df.tail(3)
df.sample(5)

df.info()
df.describe()          # only release_year is numeric

df.isna().sum().sort_values(ascending=False)   # director has the most

df.columns.tolist()
df.dtypes              # date_added is object (text)
"""


"""Part 2: Select
df["title"]                      # Series
df[["title"]]                    # DataFrame (double brackets)
df[["title", "type", "release_year"]]

df.iloc[:10, :3]
df.loc[100:110, ["title", "country"]]   # loc includes 110, so 11 rows

df.loc[0, "title"]
df.iloc[5, 3]                    # director is column index 3
"""


"""Part 3: Filter
movies = df[df["type"] == "Movie"]
len(movies)                      # about 6,131

df[(df["type"] == "Movie") & (df["release_year"] > 2015)]

df[(df["type"] == "TV Show") & (df["country"] == "United States")]

df[df["rating"].isin(["TV-MA", "R"])]

df[df["country"].isin(["India", "Japan"]) & (df["release_year"] >= 2018)]

df[df["director"].isna()]

df[df["title"].str.contains("Love", na=False)]
"""




"""
########## INDEXING, SELECTING & ASSIGNING ##########

Indexing and selecting allow us to access
specific data from a DataFrame.

Common operations:

- Select a column
- Select multiple columns
- Select rows
- Select specific values
- Assign new values
"""

print(netflix_df['title'])  #Select a Single Column

print(
    netflix_df[
        ['title', 'type', 'release_year']
    ]
)                          #Select Multiple Columns

print(netflix_df.iloc[0])  #Select the First Row

print(netflix_df.iloc[:5])  #Select the First 5 Rows

print(
    netflix_df.loc[
        0:4,
        ['title', 'type']
    ]
)                           #Select Specific Rows and Columns,First 5 rows and only title/type


movies = netflix_df[
    netflix_df['type'] == 'Movie'
]
print(movies.head())        #Select Movies Only


tv_shows = netflix_df[
    netflix_df['type'] == 'TV Show'
]
print(tv_shows.head())     #Select TV Shows Only


netflix_df['streaming_service'] = 'Netflix'
print(netflix_df.head())     #Assign a New Column with a Default Value


netflix_df['next_year'] = (
    netflix_df['release_year'] + 1
)
print(
    netflix_df[
        ['release_year', 'next_year']
    ].head()
)                          # Assign Values Using Existing Data

"""
# dataframe['column']      -> select one column
# dataframe[['c1','c2']]   -> select multiple columns
# dataframe.iloc[]         -> select by position
# dataframe.loc[]          -> select by label
# dataframe[condition]     -> filter rows
# dataframe['new_col'] = x -> create/assign column
"""