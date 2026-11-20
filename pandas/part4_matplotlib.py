########## MATPLOTLIB BASICS ##########
"""
Matplotlib is used to create charts
and visualizations.
"""

#plt.plot()      -> line chart
#plt.bar()       -> bar chart
#plt.hist()      -> histogram
#plt.pie()       -> pie chart
#plt.scatter()   -> scatter plot
#plt.show()      -> display chart

# sns.lineplot()   -> Seaborn Line Plot
# sns.countplot()  -> Seaborn Bar Plot
# sns.histplot()   -> Seaborn Histogram
# sns.scatterplot()-> Seaborn Scatter Plot
# sns.boxplot()    -> Seaborn Box Plot

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = Path(__file__).parent / "netflix_titles.csv"

netflix_df = pd.read_csv(file_path)


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


"""     Bar chart Using Notebook
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




########## MATPLOTLIB & SEABORN ##########
"""
Data visualization helps us understand
patterns, trends, and distributions.

Common plots:

- Line Plot      -> trends over time
- Bar Plot       -> compare categories
- Histogram      -> distribution of values
- Scatter Plot   -> relationship between variables
- Box Plot       -> spread and outliers
"""




########## LINE PLOT ##########
"""
Shows trends over time.
"""

# Count titles released per year
titles_per_year = (
    netflix_df["release_year"]
    .value_counts()
    .sort_index()
)

# Create line plot
titles_per_year.plot(kind="line")

# Chart title
plt.title("Netflix Titles Over Time")

# Axis labels
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")

# Display chart
plt.show()


"""   Line Chart Using Notebook
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
df = pd.read_csv("netflix_titles.csv")

added = pd.to_datetime(df["date_added"].str.strip(), format="%B %d, %Y")
per_year = added.dt.year.dropna().astype(int).value_counts().sort_index()

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(per_year.index, per_year.to_numpy(), marker="o")
ax.set_title("Titles added to Netflix per year")
ax.set_xlabel("Year added")
ax.set_ylabel("Number of titles")
plt.show()
"""



########## BAR PLOT ##########
"""
Compare Movies and TV Shows.
"""

# Count content types
type_counts = (
    netflix_df["type"]
    .value_counts()
)

# Create bar chart
type_counts.plot(
    kind="bar"
)

# Chart title
plt.title("Movies vs TV Shows")

# Axis labels
plt.xlabel("Content Type")
plt.ylabel("Count")

# Display chart
plt.show()


"""     Bar chart: top 10 ratings Using Notebook(Matplotlib, then Seaborn)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
df = pd.read_csv("netflix_titles.csv")

top_ratings = df["rating"].value_counts().head(10)

# Matplotlib version
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(top_ratings.index, top_ratings.to_numpy())
ax.set_title("Top 10 ratings (Matplotlib)")
ax.set_xlabel("Rating")
ax.set_ylabel("Number of titles")
plt.show()

# Seaborn version: the same chart in fewer lines
plt.figure(figsize=(8, 4))
sns.countplot(data=df, x="rating", order=top_ratings.index)
plt.title("Top 10 ratings (Seaborn)")
plt.xlabel("Rating")
plt.ylabel("Number of titles")
plt.show()
"""



########## HISTOGRAM ##########
"""
Shows the distribution
of release years.
"""

plt.hist(
    netflix_df["release_year"],
    bins=20
)

plt.title("Distribution of Release Years")
plt.xlabel("Release Year")
plt.ylabel("Frequency")

plt.show()


"""   Histogram: movie duration Using Notebook
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
df = pd.read_csv("netflix_titles.csv")

movies = df[df["type"] == "Movie"].copy()
movies["minutes"] = pd.to_numeric(
    movies["duration"].str.replace(" min", "", regex=False), errors="coerce"
)
movies = movies.dropna(subset=["minutes"])

plt.figure(figsize=(8, 4))
sns.histplot(data=movies, x="minutes", bins=30)
plt.axvline(movies["minutes"].mean(), color="red", linestyle="--", label="mean")
plt.title("Movie duration")
plt.xlabel("Minutes")
plt.ylabel("Number of movies")
plt.legend()
plt.show()

print(movies["minutes"].describe())
"""



########## SCATTER PLOT ##########
"""
Shows the relationship
between row position and release year.
"""

sample_df = netflix_df.head(200)

plt.scatter(
    sample_df.index,
    sample_df["release_year"]
)

plt.title("Index vs Release Year")

plt.xlabel("Dataset Index")
plt.ylabel("Release Year")

plt.show()


"""  Scatter plot Using Notebook: release year vs years until added
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
df = pd.read_csv("netflix_titles.csv")

tmp = pd.DataFrame({
    "release_year": df["release_year"],
    "year_added": pd.to_datetime(df["date_added"].str.strip(), format="%B %d, %Y").dt.year,
})
tmp["years_to_netflix"] = tmp["year_added"] - tmp["release_year"]
tmp = tmp.dropna()

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(tmp["release_year"], tmp["years_to_netflix"], alpha=0.3)
ax.set_title("How long until a title reached Netflix")
ax.set_xlabel("Release year")
ax.set_ylabel("Years between release and being added")
plt.show()
"""



########## BOX PLOT ##########
"""
Shows spread, median,
and outliers.
"""

plt.boxplot(
    netflix_df["release_year"]
)

plt.title("Release Year Box Plot")

plt.ylabel("Release Year")

plt.show()


"""   Box plot Using Notebook: movie duration by rating
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
df = pd.read_csv("netflix_titles.csv")

movies = df[df["type"] == "Movie"].copy()
movies["minutes"] = pd.to_numeric(
    movies["duration"].str.replace(" min", "", regex=False), errors="coerce"
)
movies = movies.dropna(subset=["minutes"])

top = movies["rating"].value_counts().head(8).index

plt.figure(figsize=(9, 5))
sns.boxplot(data=movies[movies["rating"].isin(top)], x="rating", y="minutes", order=top)
plt.title("Movie duration by rating")
plt.xlabel("Rating")
plt.ylabel("Minutes")
plt.show()
"""



########## SEABORN LINE PLOT ##########

titles_per_year = (
    netflix_df["release_year"]
    .value_counts()
    .sort_index()
)

sns.lineplot(
    x=titles_per_year.index,
    y=titles_per_year.values
)

plt.title("Netflix Titles Over Time")

plt.show()




########## SEABORN BAR PLOT ##########

sns.countplot(
    data=netflix_df,
    x="type"
)

plt.title("Movies vs TV Shows")

plt.show()




########## SEABORN HISTOGRAM ##########

sns.histplot(
    data=netflix_df,
    x="release_year",
    bins=20
)

plt.title("Distribution of Release Years")

plt.show()




########## SEABORN SCATTER PLOT ##########

sample_df = netflix_df.head(200)

sns.scatterplot(
    data=sample_df,
    x=sample_df.index,
    y="release_year"
)

plt.title("Index vs Release Year")

plt.show()





########## SEABORN BOX PLOT ##########

sns.boxplot(
    data=netflix_df,
    y="release_year"
)

plt.title("Release Year Box Plot")

plt.show()