SELECT
  gr,
  status,
  ROUND(AVG(minutes_in_status) / 60, 2) AS "average_hours"
FROM (
    SELECT SUBSTR(issue_key, 1,1) AS "gr",
      --issue_key,
      status,
      minutes_in_status
    FROM history
    WHERE status LIKE 'open'
      AND minutes_in_status NOT NULL
    ) AS t1
GROUP BY
  gr, status
ORDER BY gr