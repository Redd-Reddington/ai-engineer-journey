"""
########## SUMMARY FUNCTIONS ##########

Summary functions help us quickly understand
our dataset by providing useful statistics
and information.
"""

# info()            -> dataset information
# describe()        -> summary statistics
# count()           -> count non-null values
# value_counts()    -> count occurrences

# map()             -> transform values

# groupby()         -> group data
# agg()             -> multiple calculations

# sort_values()     -> sort rows

from pathlib import Path
import pandas as pd

file_path = Path(__file__).parent / "netflix_titles.csv"

netflix_df = pd.read_csv(file_path)

#print(netflix_df.info())   # Summary Statistics
print(netflix_df.count())  # Count Unique Values
print(netflix_df['type'].value_counts()) # Most Frequent Value

"""          Summary functions using pandas notebook
df["release_year"].describe()      # numeric summary
df["type"].describe()              # text summary: count, unique, top, freq
df["release_year"].mean()
df["release_year"].median()
df["rating"].unique()
df["type"].value_counts()
df["type"].value_counts(normalize=True)   # proportions
"""



"""
########## MAPS ##########

Maps allow us to transform data by applying
a function to every value in a column.
"""

print(
    netflix_df['title'].head().map(str.upper)  # Convert Titles to Uppercase
)


print(
    netflix_df['title']
    .head()
    .map(lambda title: f"Netflix: {title}")   # Add Text/Prefix to Every Title
)


netflix_df['title_upper'] = (
    netflix_df['title'].map(str.upper)
)
print(
    netflix_df[
        ['title', 'title_upper']            # Create New Column
    ].head()
)


"""        Maps using pandas notebook
# map with a function
df["title_length"] = df["title"].map(len)

# map with a lambda
df["is_recent"] = df["release_year"].map(lambda y: y >= 2018)

# map with a dictionary
df["type_code"] = df["type"].map({"Movie": "M", "TV Show": "T"})

# apply across rows
def label(row):
    return f"{row['title']} ({row['release_year']})"

df["label"] = df.apply(label, axis=1)
"""




"""
########## GROUPING ##########

Grouping allows us to combine rows and
perform calculations on groups of data.
"""

print(
    netflix_df.groupby('type').size()    # Count Movies and TV Shows
)


print(
    netflix_df.groupby('rating').size()  # Count by Rating
)


print(
    netflix_df.groupby('type')['release_year']   # Calculate the Average Release Year by Type
    .mean()
)


print(
    netflix_df.groupby('type')['release_year']
    .agg(['min', 'max', 'mean'])              # Calculate the Minimum, Maximum, and Average Release Year by Type
)


"""        Grouping using pandas notebook
df.groupby("type").size()
df.groupby("type")["release_year"].mean()
df.groupby("type")["release_year"].agg(["min", "max", "mean"])
df.groupby("rating")["title"].count()
df.groupby(["type", "rating"]).size()
df.groupby("release_year")["title"].apply(list).head()   # list titles per year
"""




"""
########## SORTING ##########

Sorting allows us to organize data
in ascending or descending order.
"""

print(
    netflix_df.sort_values(
        by='release_year'      # Sort by Release Year
    ).head()
)


print(
    netflix_df.sort_values(
        by='release_year',
        ascending=False       # Sort by Release Year in Descending Order
    ).head()
)


print(
    netflix_df.sort_values(
        by='title'           # Sort by Title Alphabetically
    ).head()
)


print(
    netflix_df.sort_values(
        by=['type', 'release_year']     # Sort by Type and then by Release Year
    ).head()
)



"""        Sorting using pandas notebook
df.sort_values("release_year")
df.sort_values("release_year", ascending=False)
df.sort_values(["release_year", "title"], ascending=[False, True])
df.groupby("rating").size().sort_values(ascending=False)
df.groupby("release_year").size().sort_index(ascending=False)
"""