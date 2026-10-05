--monthly_pnl.sql
SELECT
    TO_CHAR(date, 'YYYY-MM') AS month,
    ROUND(SUM(pnl),2) AS pnl
FROM deals
WHERE row_type='trade'
GROUP BY month
ORDER BY month;
--EOF