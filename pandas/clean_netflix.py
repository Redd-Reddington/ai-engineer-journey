from pathlib import Path
import pandas as pd

folder = Path(__file__).parent
netflix_df = pd.read_csv(folder / "netflix_titles.csv")

netflix_df = netflix_df.drop_duplicates()

# a few rows have a duration like "74 min" stored in rating
mask = netflix_df["rating"].str.contains("min", na=False)
netflix_df.loc[mask, "duration"] = netflix_df.loc[mask, "rating"]
netflix_df.loc[mask, "rating"] = None

for col in ["director", "cast", "country", "rating"]:
    netflix_df[col] = netflix_df[col].fillna("Unknown")

netflix_df["date_added"] = pd.to_datetime(
    netflix_df["date_added"].str.strip(), format="%B %d, %Y"
)

parts = netflix_df["duration"].str.split(" ", expand=True)
netflix_df["duration_value"] = pd.to_numeric(parts[0]).astype("Int64")
netflix_df["duration_unit"] = parts[1].replace({"Season": "Seasons"})

netflix_df = netflix_df.rename(columns={"cast": "cast_members"})
netflix_df = netflix_df[[
    "show_id", "type", "title", "director", "cast_members", "country",
    "date_added", "release_year", "rating", "duration_value",
    "duration_unit", "listed_in", "description",
]]

netflix_df.to_csv(folder / "netflix_clean.csv", index=False)

print(netflix_df.shape)
print(netflix_df.isna().sum())