-- Count all rows in the table.
-- This tells us how many Netflix titles were imported.SELECT COUNT(*)
FROM netflix_titles;


-- Count Movies and TV Shows.
-- GROUP BY creates one group for each content type.
-- COUNT(*) counts the number of titles in each group.SELECT
    type,
    COUNT(*) AS total_titles
FROM netflix_titles
GROUP BY type;


-- Count how many titles were added to Netflix each year.
-- EXTRACT pulls the year from the date_added column.
-- WHERE removes rows with missing dates.
-- GROUP BY creates one group for each year.
-- ORDER BY sorts the years from oldest to newest.
SELECT
    EXTRACT(YEAR FROM date_added) AS year_added,
    COUNT(*) AS total_titles
FROM netflix_titles
WHERE date_added IS NOT NULL
GROUP BY year_added
ORDER BY year_added;


-- Find the average movie length in minutes.
-- AVG calculates the average duration_value.
-- ROUND limits the result to 1 decimal place.
-- Only Movie rows are included.
SELECT
    ROUND(AVG(duration_value), 1) AS avg_minutes
FROM netflix_titles
WHERE type = 'Movie';


-- Display the structure of the table.
-- information_schema.columns stores metadata about tables.
-- This query shows every column and its data type.
SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'netflix_titles'
ORDER BY ordinal_position;


-- Count titles by rating.
-- ORDER BY sorts from most common rating to least common.
SELECT
    rating,
    COUNT(*) AS total_titles
FROM netflix_titles
GROUP BY rating
ORDER BY total_titles DESC;


-- Find the top 10 countries by number of titles.
-- LIMIT returns only the first 10 results.

SELECT
    country,
    COUNT(*) AS total_titles
FROM netflix_titles
WHERE country IS NOT NULL
GROUP BY country
ORDER BY total_titles DESC
LIMIT 10;