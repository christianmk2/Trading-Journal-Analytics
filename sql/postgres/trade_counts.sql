--trade_counts.sql
SELECT  
    COUNT(*) AS total_trades,  
  
    SUM(  
        CASE  
            WHEN pnl > 0 THEN 1  
            ELSE 0  
        END  
    ) AS winning_trades,  
  
    SUM(  
        CASE  
            WHEN pnl < 0 THEN 1  
            ELSE 0  
        END  
    ) AS losing_trades,  
  
    SUM(  
        CASE  
            WHEN pnl = 0 THEN 1  
            ELSE 0  
        END  
    ) AS breakeven_trades  
  
FROM deals
WHERE row_type = 'trade';  
--EOF