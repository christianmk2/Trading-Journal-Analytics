--drawdown_analysis.sql
WITH equity AS (
    SELECT
        date,
        SUM(pnl) OVER(
            ORDER BY date
        ) AS equity
    FROM deals
    WHERE row_type='trade'
)
SELECT
    date,
    equity,
    equity -
    MAX(equity) OVER(
        ORDER BY date
    ) AS drawdown
FROM equity;
--EOF