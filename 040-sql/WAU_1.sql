
-- Define a CTE with filtered event data
WITH BaseData AS (
    SELECT
        event_date,                      -- Date of the event
        event_user_guid AS user_guid     -- Unique user identifier
        -- Optionally extract request_id from JSON if needed
    FROM dpaas_uccatalog_prd.ace_analytics.ets_genai_web_service_silver
    WHERE
        source_client_id = 'clio-playground-web'      -- Filter for specific client
        AND event_subtype = 'page'                   -- Page-level events
        AND event_type = 'render'                    -- Render events
        AND event_subcategory = 'GenerationHistory'  -- Specific page type
        AND event_date >= '2025-04-10'               -- Only recent events
),

-- Find the earliest event date from BaseData
FirstEventDate AS (
    SELECT MIN(event_date) AS first_date
    FROM BaseData
),

-- Generate a series of reporting dates (every 6 days) from first_date to yesterday
DateSeries AS (
    SELECT explode(sequence(
        CAST(first_date AS DATE),                    -- Start date
        CAST(date_add(current_date(), -1) AS DATE),  -- End date (yesterday)
        INTERVAL 6 DAY                               -- Step size (6 days)
    )) AS reporting_date
    FROM FirstEventDate
)

-- Main query: count distinct users per 7-day window ending on reporting_date
SELECT
    ds.reporting_date,                               -- Weekly bucket end date
    COUNT(DISTINCT b.user_guid) AS weekly_active_users -- Unique users in that week
FROM DateSeries ds
INNER JOIN BaseData b
    ON b.event_date BETWEEN                         -- Range join: include events
       ds.reporting_date - INTERVAL 6 DAY          -- Start of 7-day window
       AND ds.reporting_date                       -- End of window
GROUP BY ds.reporting_date
ORDER BY ds.reporting_date;                        -- Sort by reporting date
