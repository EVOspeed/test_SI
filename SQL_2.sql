/*По умолчанию запрос выдает активные задачи на текущий момент,
чтобы посмотреть активные задачи на определенную дату в прошлом 
необходимо в столбце 'time' в подзапросе вместо 'now' указать дату/время
в формате '%Y-%m-%d %H:%M'.*/

WITH sq AS (SELECT *,
              strftime('%Y-%m-%d %H:%M', 'now') AS "time", /*change time to watch open tasks at another period*/
              strftime('%Y-%m-%d %H:%M', datetime(started_at / 1000, 'unixepoch')) AS "start",
              strftime('%Y-%m-%d %H:%M', datetime(ended_at / 1000, 'unixepoch')) AS "end"
            FROM (
                SELECT 
                  issue_key,
                  status,
                  started_at,
                  CASE 
                    WHEN ended_at IS NULL THEN STRFTIME('%s') * 1000
                    ELSE ended_at
                  END AS "ended_at"
                FROM history
                WHERE status NOT IN ('Closed', 'Resolved')
                ) AS t1
            WHERE time > start AND time <= end 
            )
SELECT 
  issue_key,
  status,
  start
FROM 
  sq
ORDER BY issue_key