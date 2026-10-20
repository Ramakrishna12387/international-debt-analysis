SELECT c.country_name, SUM(d.debt) AS total_debt
FROM countries c
JOIN debt_data d ON c.country_code = d.country_code
GROUP BY c.country_name
ORDER BY total_debt DESC
LIMIT 10;
SELECT c.country_name, SUM(d.debt) AS total_debt,
       DENSE_RANK() OVER (ORDER BY SUM(d.debt) DESC) AS debt_rank
FROM countries c
JOIN debt_data d ON c.country_code = d.country_code
GROUP BY c.country_name;
SELECT c.country_name, SUM(d.debt) AS total_debt,
       CASE 
           WHEN SUM(d.debt) > 50000000000 THEN 'High Debt'
           WHEN SUM(d.debt) BETWEEN 10000000000 AND 50000000000 THEN 'Medium Debt'
           ELSE 'Low Debt'
       END AS debt_category
FROM countries c
JOIN debt_data d ON c.country_code = d.country_code
GROUP BY c.country_name;