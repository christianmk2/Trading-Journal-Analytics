--profit_factor.sql
SELECT  
    ROUND(  
        SUM(  
            CASE  
                WHEN pnl > 0 THEN pnl  
                ELSE 0  
            END  
        ),  
        2  
    ) AS gross_profit,  
  
    ROUND(  
        ABS(  
            SUM(  
                CASE  
                    WHEN pnl < 0 THEN pnl  
                    ELSE 0  
                END  
            )  
        ),  
        2  
    ) AS gross_loss,  
  
    ROUND(  
        SUM(  
            CASE  
                WHEN pnl > 0 THEN pnl  
                ELSE 0  
            END  
        )  
        /  
        ABS(  
            SUM(  
                CASE  
                    WHEN pnl < 0 THEN pnl  
                    ELSE 0  
                END  
            )  
        ),  
        2  
    ) AS profit_factor  
  
FROM deals
WHERE row_type = 'trade';  
--EOF