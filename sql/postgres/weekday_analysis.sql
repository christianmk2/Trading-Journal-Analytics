-- weekday_analysis.sql
SELECT
    CASE EXTRACT(DOW FROM date)
        WHEN '0' THEN 'Sunday'
        WHEN '1' THEN 'Monday'
        WHEN '2' THEN 'Tuesday'
        WHEN '3' THEN 'Wednesday'
        WHEN '4' THEN 'Thursday'
        WHEN '5' THEN 'Friday'
        WHEN '6' THEN 'Saturday'
    END AS weekday,
    COUNT(*) AS trades,
    ROUND(SUM(pnl),2) AS total_pnl,
    ROUND(AVG(pnl),2) AS average_pnl
FROM deals
WHERE row_type = 'trade'
GROUP BY EXTRACT(DOW FROM date)
ORDER BY EXTRACT(DOW FROM date);
--EOF