-- What are the different genres --

SELECT DISTINCT prime_genre FROM data;

-- Which is the genre with the most apps rated? --

SELECT prime_genre,
		SUM(rating_count_tot) as sum_rating_count
	 FROM data
    GROUP BY prime_genre
   ORDER BY sum_rating_count
  DESC
 LIMIT 1;

 -- Which is the genre with most apps? --

 SELECT prime_genre,
		COUNT(track_name) as qty_apps
	 FROM data
    GROUP BY prime_genre
   ORDER BY qty_apps
  DESC
 LIMIT 1;

 -- Which is the one with least? --

 SELECT prime_genre,
		COUNT(track_name) as qty_apps
	 FROM data
    GROUP BY prime_genre
   ORDER BY qty_apps
  ASC
 LIMIT 1;

-- Find the top 10 apps most rated --

SELECT track_name,
		SUM(price),
		SUM(rating_count_tot) as sum_rating_count
	 FROM data
    GROUP BY track_name
   ORDER BY sum_rating_count
  DESC
 LIMIT 10;

 -- Find the top 10 apps best rated by users --

CREATE TABLE best_rated AS
SELECT track_name,
		AVG(user_rating) as avg_rating,
		SUM(rating_count_tot)
	 FROM data
    GROUP BY track_name
   ORDER BY avg_rating
  DESC;

 SELECT * FROM best_rated
 WHERE avg_rating = 5
 ORDER BY sum
 DESC
 LIMIT 10;

 -- Take a look at the data you retrieved in question 5. Give some insights. --
 --famous apps--

 -- Take a look at the data you retrieved in question 6. Give some insights. --
 -- users don't download it very often --

 -- Now compare the data from questions 5 and 6. What do you see? --
 -- the apps that have more ratings, therefore are more downloaded, don't have the best ratings.

-- How could you take the top 3 regarding both user ratings and number of votes? --

 SELECT * FROM best_rated
 WHERE avg_rating = 5
 ORDER BY sum
 DESC
 LIMIT 3;

-- Do people care about the price of an app? --

CREATE TABLE teste AS
	SELECT track_name,
			price,
			rating_count_tot
			FROM data
			AS price_rating
			WHERE price = 0
			;
SELECT price,
	SUM(rating_count_tot) AS sum_rating_count
	FROM teste
	GROUP BY price;

CREATE TABLE teste2 AS
	SELECT track_name,
			price,
			rating_count_tot
			FROM data
			AS price_rating
			WHERE price != 0
			;
CREATE TABLE teste3 AS
SELECT price,
	SUM(rating_count_tot) AS sum_rating_count
	FROM teste2
	GROUP BY price;

SELECT SUM(sum_rating_count) from teste3;

-- people care about price. The number of rating_counts it's almost 7 times bigger for apps that are free than the ones that are not.

 -- Bonus: Find the total number of games available in more than 1 language. --

 CREATE TABLE more_1_lang AS
 SELECT (track_name),
 		"lang.num"
 	FROM data
	WHERE "lang.num" > 1 and prime_genre = 'Games'
;

SELECT COUNT(*) FROM more_1_lang;

-- Bonus2: Find the number of free vs paid apps --

SELECT COUNT(track_name) as free_apps_count
FROM teste;

SELECT COUNT(track_name) as paid_apps_count
FROM teste2;

-- Bonus3: Find the number of free vs paid apps for each genre --

-- free apps --
SELECT prime_genre, COUNT(track_name)
	FROM data
	WHERE price = 0
	GROUP BY prime_genre, price
	;

-- paid apps --
SELECT prime_genre, COUNT(track_name)
	FROM data
	WHERE price != 0
	GROUP BY prime_genre
	;