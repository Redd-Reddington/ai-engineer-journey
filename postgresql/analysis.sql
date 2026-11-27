-- Create a lookup table that maps ratings to audience groups.
-- This gives us a second table so we can practice JOINs.

CREATE TABLE rating_audience (
    rating   TEXT PRIMARY KEY,
    audience TEXT NOT NULL
);

-- Insert audience categories for each rating.

INSERT INTO rating_audience (rating, audience) VALUES
    ('TV-Y', 'Kids'),
    ('TV-Y7', 'Kids'),
    ('TV-Y7-FV', 'Kids'),
    ('G', 'Kids'),
    ('TV-G', 'Kids'),
    ('PG', 'Family'),
    ('TV-PG', 'Family'),
    ('PG-13', 'Teens'),
    ('TV-14', 'Teens'),
    ('R', 'Adults'),
    ('TV-MA', 'Adults'),
    ('NC-17', 'Adults');




-- JOINS


-- INNER JOIN returns only rows that have matching ratings
-- in both tables.
--
-- netflix_titles contains the title information.
-- rating_audience contains the audience category.
--
-- This query counts how many titles belong
-- to each audience group.

SELECT
    a.audience,
    COUNT(*) AS total_titles
FROM netflix_titles AS t
INNER JOIN rating_audience AS a
    ON a.rating = t.rating
GROUP BY a.audience
ORDER BY total_titles DESC;

-- LEFT JOIN keeps every row from netflix_titles.
--
-- If a rating does not exist in rating_audience,
-- the audience column becomes NULL.
--
-- This query helps us find ratings
-- that are missing from the lookup table.

SELECT
    t.rating,
    COUNT(*) AS total_titles
FROM netflix_titles AS t
LEFT JOIN rating_audience AS a
    ON a.rating = t.rating
WHERE a.audience IS NULL
GROUP BY t.rating;




-- WINDOW FUNCTIONS(A window function calculates across related rows without collapsing them the way GROUP BY does.)


-- RANK() assigns a ranking to each release year.
--
-- Years with the most titles get the highest rank.
-- Unlike GROUP BY alone, the rank stays attached
-- to each result row.

SELECT
    release_year,
    COUNT(*) AS total_titles,
    RANK() OVER (
        ORDER BY COUNT(*) DESC
    ) AS year_rank
FROM netflix_titles
GROUP BY release_year
ORDER BY year_rank
LIMIT 10;

-- LAG() looks at the previous row.
--
-- This query compares each year's total titles
-- to the year before it.
--
-- Positive numbers mean growth.
-- Negative numbers mean a decline.

SELECT
    release_year,
    COUNT(*) AS total_titles,
    COUNT(*) -
    LAG(COUNT(*))
        OVER (ORDER BY release_year)
    AS change_from_prev_year
FROM netflix_titles
GROUP BY release_year
ORDER BY release_year;





-- A CTE (Common Table Expression) creates a temporary
-- result set that can be used by another query.
--
-- ROW_NUMBER() numbers movies inside each rating group.
-- rn = 1 identifies the longest movie for that rating.

WITH ranked AS (
    SELECT
        rating,
        title,
        duration_value,
        ROW_NUMBER() OVER (
            PARTITION BY rating
            ORDER BY duration_value DESC
        ) AS rn
    FROM netflix_titles
    WHERE type = 'Movie'
      AND duration_value IS NOT NULL
)

SELECT
    rating,
    title,
    duration_value
FROM ranked
WHERE rn = 1
ORDER BY duration_value DESC;




-- CROSS JOIN LATERAL


-- Some rows contain multiple countries
-- such as:
--
-- 'United States, India'
--
-- string_to_table() splits the text into
-- separate country values.
--
-- CROSS JOIN LATERAL runs the split
-- for each row in the table.
--
-- This query finds the top countries
-- by number of titles.

SELECT
    c.country_name,
    COUNT(*) AS total_titles
FROM netflix_titles AS t
CROSS JOIN LATERAL
    string_to_table(
        t.country,
        ', '
    ) AS c(country_name)
GROUP BY c.country_name
ORDER BY total_titles DESC
LIMIT 5;






-- Netflix PostgreSQL dataset 10 solid business questions 
-- that can be answered using SQL only.

         --Question 1: How many titles does Netflix have?
-- Count all titles in the dataset.

SELECT COUNT(*) AS total_titles
FROM netflix_titles;


         --Question 2: Are Movies or TV Shows more common?
-- Count titles by content type.

SELECT
    type,
    COUNT(*) AS total_titles
FROM netflix_titles
GROUP BY type;

--Business Value: Understand Netflix's content mix.


         --Question 3: Which ratings are the most common?
-- Count titles by rating.
-- Sort from most common to least common.

SELECT
    rating,
    COUNT(*) AS total_titles
FROM netflix_titles
GROUP BY rating
ORDER BY total_titles DESC;

--Business Value: Understand the target audience.


         --Question 4: Which release years produced the most content?
-- Count titles released each year.

SELECT
    release_year,
    COUNT(*) AS total_titles
FROM netflix_titles
GROUP BY release_year
ORDER BY total_titles DESC;

--Business Value: Identify peak content-production years.


         --Question 5: Which countries contribute the most content?
-- Split multi-country rows and count titles per country.

SELECT
    c.country_name,
    COUNT(*) AS total_titles
FROM netflix_titles AS t
CROSS JOIN LATERAL
    string_to_table(t.country, ', ')
    AS c(country_name)
GROUP BY c.country_name
ORDER BY total_titles DESC
LIMIT 10;

--Business Value: Identify Netflix's strongest content markets.


         --Question 6: How many titles were added to Netflix each year?
-- Count additions by year.

SELECT
    EXTRACT(YEAR FROM date_added) AS year_added,
    COUNT(*) AS total_titles
FROM netflix_titles
WHERE date_added IS NOT NULL
GROUP BY year_added
ORDER BY year_added;

--Business Value: Measure catalog-growth trends.


         --Question 7: What is the average movie duration?
-- Calculate the average movie length.

SELECT
    ROUND(AVG(duration_value), 1) AS avg_minutes
FROM netflix_titles
WHERE type = 'Movie';

--Business Value: Understand typical movie length.


         --Question 8: What are the 10 longest movies?
-- Find the longest movies.

SELECT
    title,
    duration_value
FROM netflix_titles
WHERE type = 'Movie'
ORDER BY duration_value DESC
LIMIT 10;

--Business Value: Identify exceptional content.



         --Question 9: Which audience category has the most titles?
-- Join titles with audience groups.

SELECT
    a.audience,
    COUNT(*) AS total_titles
FROM netflix_titles AS t
INNER JOIN rating_audience AS a
    ON t.rating = a.rating
GROUP BY a.audience
ORDER BY total_titles DESC;

--Business Value: Determine whether Netflix focuses more on Kids, Family, Teens, or Adults.


          --Question 10: What percentage of Netflix content is Movies vs TV Shows?
-- Calculate content percentages.

SELECT
    type,
    COUNT(*) AS total_titles,
    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM netflix_titles
GROUP BY type;

--Business Value: Understand catalog composition at a glance.


