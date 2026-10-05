--pnl_by_symbol.sql
SELECT  
    symbol,  
  
    COUNT(*) AS trade_count,  
  
    ROUND(SUM(pnl), 2) AS total_pnl,  
  
    ROUND(AVG(pnl), 2) AS average_pnl  
  
FROM deals  

WHERE row_type = 'trade'

GROUP BY symbol  
  
ORDER BY total_pnl DESC;  
--EOF