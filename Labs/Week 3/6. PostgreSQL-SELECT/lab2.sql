SELECT
	a.au_id AS "AUTHOR ID",
	a.au_lname AS "LAST NAME",
	a.au_fname AS "FIRST NAME",
	a.au_lname AS "LAST NAME",
	t.title AS "TITLE",
	p.pub_name AS "PUBLISHER"
	FROM titles t

	JOIN titleauthor ta
	ON t.title_id = ta.title_id
	JOIN authors a
	ON a.au_id = ta.au_id
	JOIN publishers p
	ON p.pub_id = t.pub_id;




SELECT tap."AUTHOR_ID", tap."LAST_NAME", tap."FIRST_NAME", tap."PUBLISHER", COUNT(tap."TITLE") "TITLE COUNT" FROM
(SELECT
	a.au_id AS "AUTHOR_ID",
	a.au_lname AS "LAST_NAME",
	a.au_fname AS "FIRST_NAME",
	t.title AS "TITLE",
	p.pub_name AS "PUBLISHER"
	FROM titles t

	JOIN titleauthor ta
	ON t.title_id = ta.title_id
	JOIN authors a
	ON a.au_id = ta.au_id
	JOIN publishers p
	ON p.pub_id = t.pub_id) AS tap
	GROUP BY tap."AUTHOR_ID", tap."LAST_NAME", tap."FIRST_NAME", tap."PUBLISHER"
	ORDER BY "TITLE COUNT"
	DESC
	;



SELECT a.au_id "AUTHOR ID",
	a.au_lname "LAST NAME",
	a.au_fname "FIRST NAME",
	SUM(s.qty) "TOTAL"
	FROM titles t
	JOIN sales s
	ON t.title_id = s.title_id
	JOIN titleauthor ta
	ON ta.title_id = t.title_id
	JOIN authors a
	ON ta.au_id = a.au_id
	GROUP BY a.au_id, a.au_lname, a.au_fname
	ORDER BY SUM(s.qty) DESC
	LIMIT 3;


SELECT a.au_id "AUTHOR ID",
	a.au_lname "LAST NAME",
	a.au_fname "FIRST NAME",
	COALESCE(SUM(s.qty),0) "TOTAL"
	FROM titles t
	LEFT JOIN sales s
	ON t.title_id = s.title_id
	LEFT JOIN titleauthor ta
	ON ta.title_id = t.title_id
	RIGHT JOIN authors a
	ON ta.au_id = a.au_id
	GROUP BY a.au_id, a.au_lname, a.au_fname
	ORDER BY SUM(s.qty) DESC
;