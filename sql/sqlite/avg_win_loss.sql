--avg_win_loss.sql
SELECT  
  
    ROUND(  
        AVG(  
            CASE  
                WHEN pnl > 0 THEN pnl  
            END  
        ),  
        2  
    ) AS average_win,  
  
    ROUND(  
        AVG(  
            CASE  
                WHEN pnl < 0 THEN pnl  
            END  
        ),  
        2  
    ) AS average_loss  
  
FROM deals
WHERE row_type = 'trade';  
--EOF