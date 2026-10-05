-- session_analysis.sql
SELECT

    CASE
        WHEN date::time BETWEEN '08:00:00' AND '11:59:59'
            THEN 'Asian KZ'

        WHEN date::time BETWEEN '14:00:00' AND '16:59:59'
            THEN 'London Open KZ'

        WHEN date::time BETWEEN '19:00:00' AND '21:59:59'
            THEN 'New York Open KZ'

        WHEN date::time BETWEEN '22:00:00' AND '23:59:59'
            THEN 'London Close KZ'

        ELSE 'Outside KZ'
    END AS session,

    COUNT(*) AS trades,

    ROUND(SUM(pnl),2) AS total_pnl,

    ROUND(AVG(pnl),2) AS average_pnl,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN pnl > 0 THEN 1
                ELSE 0
            END
        )
        / COUNT(*),
        2
    ) AS win_rate

FROM deals

WHERE row_type = 'trade'

GROUP BY session;
