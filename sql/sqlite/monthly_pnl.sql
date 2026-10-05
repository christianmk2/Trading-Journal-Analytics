--monthly_pnl.sql
SELECT
    strftime('%Y-%m', date) AS month,
    ROUND(SUM(pnl),2) AS pnl
FROM deals
WHERE row_type='trade'
GROUP BY month
ORDER BY month;
--EOF