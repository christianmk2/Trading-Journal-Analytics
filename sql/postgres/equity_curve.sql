--equity_curve.sql
SELECT
    date,
    pnl,
    SUM(pnl) OVER(
        ORDER BY date
    ) AS cumulative_pnl
FROM deals
WHERE row_type='trade';
--EOF