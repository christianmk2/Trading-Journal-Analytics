--daily_pnl.sql
SELECT  
    DATE(date) AS trade_day,  
  
    COUNT(*) AS total_trades,  
  
    ROUND(SUM(pnl), 2) AS daily_pnl  
  
FROM deals  

WHERE row_type = 'trade'

GROUP BY DATE(date)  
  
ORDER BY trade_day;  
--EOF