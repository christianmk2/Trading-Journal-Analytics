--longest_winning_streak.sql
WITH ordered_trades AS (
    SELECT
        date,
        pnl,
        CASE
            WHEN pnl > 0 THEN 1
            ELSE 0
        END AS is_win,

        ROW_NUMBER() OVER (
            ORDER BY date
        ) AS trade_number
    FROM deals
    WHERE row_type = 'trade'
),

winning_trades AS (
    SELECT
        date,
        trade_number,

        trade_number
        - ROW_NUMBER() OVER (
            ORDER BY trade_number
        ) AS streak_group
    FROM ordered_trades
    WHERE is_win = 1
),

winning_streaks AS (
    SELECT
        streak_group,
        COUNT(*) AS streak_length,
        MIN(date) AS streak_start,
        MAX(date) AS streak_end
    FROM winning_trades
    GROUP BY streak_group
)
SELECT
    streak_length AS longest_winning_streak,
    streak_start, streak_end
FROM winning_streaks
ORDER BY streak_length DESC, streak_start
LIMIT 1;
--EOF