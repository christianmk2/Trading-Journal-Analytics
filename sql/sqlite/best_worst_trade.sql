--best_worst_trade.sql
SELECT  
    MAX(pnl) AS best_trade,  
    MIN(pnl) AS worst_trade  
FROM deals
WHERE row_type = 'trade';  
--EOF