--monthly_rank.sql
WITH monthly AS (
    SELECT
        strftime('%Y-%m', date) AS month,
        ROUND(SUM(pnl),2) AS pnl
    FROM deals
    WHERE row_type='trade'
    GROUP BY month
)
SELECT
    *,
    RANK() OVER(
        ORDER BY pnl DESC
    ) AS month_rank
FROM monthly;
--EOF