--time_day_analysis.sql
SELECT
    TO_CHAR(date, 'HH24') AS hour,
    COUNT(*) AS trades,
    ROUND(SUM(pnl),2) AS pnl
FROM deals
WHERE row_type='trade'
GROUP BY hour
ORDER BY hour;
--EOF
