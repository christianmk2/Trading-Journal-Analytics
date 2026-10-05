--total_pnl.sql
SELECT  
    ROUND(SUM(pnl), 2) AS total_pnl  
FROM deals
WHERE row_type = 'trade';
--EOF