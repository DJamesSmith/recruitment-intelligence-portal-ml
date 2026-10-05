SELECT id, name, email
FROM recruitments_candidate
WHERE skills ILIKE '%Python%';

SELECT applied_role_id, COUNT(*)
FROM recruitments_candidate
GROUP BY applied_role_id
ORDER BY COUNT(*) DESC;

SELECT id, name, expected_salary
FROM recruitments_candidate
WHERE expected_salary BETWEEN 300000 AND 800000
ORDER BY expected_salary DESC;