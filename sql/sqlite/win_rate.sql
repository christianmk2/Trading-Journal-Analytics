--win_rate.sql
SELECT  
    COUNT(*) AS total_trades,  
    SUM(  
        CASE  
            WHEN pnl > 0 THEN 1  
            ELSE 0  
        END  
    ) AS winning_trades,  
  
    ROUND(  
        100.0 *  
        SUM(  
            CASE  
                WHEN pnl > 0 THEN 1  
                ELSE 0  
            END  
        ) / COUNT(*),
        2  
    ) AS win_rate  
  
FROM deals
WHERE row_type = 'trade';  
--EOF