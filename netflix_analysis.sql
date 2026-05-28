-- ============================================================
-- Netflix Top 10 Streaming Data Analysis (2021–2026)
-- Author: Karma Yangden
-- Tools: Google BigQuery (SQL)
-- Dataset: netflix-497014.runtime.netflix_runtime
-- Description: 8 analytical queries exploring viewership trends,
--              content performance, and audience behaviour across
--              10,200 weekly data points from July 2021 to May 2026
-- ============================================================


-- ============================================================
-- QUERY 1: All-Time Most-Watched Titles
-- Purpose: Identify the top 20 titles by total hours viewed
--          across all categories and all years
-- ============================================================
SELECT 
  show_title, 
  category,
  SUM(weekly_hours_viewed) AS total_hours_viewed,
  SUM(weekly_views) AS total_views,
  MAX(cumulative_weeks_in_top_10) AS peak_weeks_in_top10
FROM `netflix-497014.runtime.netflix_runtime`
GROUP BY show_title, category
ORDER BY total_hours_viewed DESC
LIMIT 20;


-- ============================================================
-- QUERY 2: Longest-Staying Titles in the Top 10
-- Purpose: Find titles with the highest cumulative weeks
--          in the Top 10 — identifies slow-burn hits vs
--          flash-in-the-pan viral moments
-- ============================================================
SELECT 
  show_title, 
  category,
  MAX(cumulative_weeks_in_top_10) AS weeks_in_top10
FROM `netflix-497014.runtime.netflix_runtime`
GROUP BY show_title, category
ORDER BY weeks_in_top10 DESC
LIMIT 20;


-- ============================================================
-- QUERY 3: Does Film Runtime Affect Viewership?
-- Purpose: Bucket films by runtime and compare average
--          weekly views — identifies the optimal film length
--          for audience engagement
-- ============================================================
SELECT
  CASE
    WHEN runtime < 1.5 THEN 'Short (<90 min)'
    WHEN runtime BETWEEN 1.5 AND 2.0 THEN 'Standard (90–120 min)'
    ELSE 'Long (>120 min)'
  END AS runtime_bucket,
  COUNT(*) AS entries,
  ROUND(AVG(weekly_views), 0) AS avg_weekly_views,
  ROUND(AVG(weekly_hours_viewed), 0) AS avg_weekly_hours
FROM `netflix-497014.runtime.netflix_runtime`
WHERE category LIKE 'Films%' 
  AND runtime IS NOT NULL
GROUP BY runtime_bucket
ORDER BY avg_weekly_views DESC;


-- ============================================================
-- QUERY 4: Non-English Content Growth Over Time
-- Purpose: Track the share of Non-English titles in the
--          Top 10 month by month — measures the success of
--          Netflix's global content strategy
-- ============================================================
SELECT
  DATE_TRUNC(week, MONTH) AS month,
  COUNTIF(category LIKE '%Non-English%') AS non_english_entries,
  COUNTIF(category LIKE '%English%') AS english_entries,
  ROUND(COUNTIF(category LIKE '%Non-English%') * 100.0 / COUNT(*), 1) AS non_english_pct
FROM `netflix-497014.runtime.netflix_runtime`
GROUP BY month
ORDER BY month;


-- ============================================================
-- QUERY 5: Titles That Sat at #1 the Most Weeks
-- Purpose: Find the most dominant titles that held the
--          number one ranking position for the longest
-- ============================================================
SELECT 
  show_title, 
  category, 
  COUNT(*) AS weeks_at_rank_1
FROM `netflix-497014.runtime.netflix_runtime`
WHERE weekly_rank = 1
GROUP BY show_title, category
ORDER BY weeks_at_rank_1 DESC
LIMIT 15;


-- ============================================================
-- QUERY 6: Seasonal Viewing Trends by Month
-- Purpose: Identify peak and low viewing months across
--          the year — useful for content release strategy
-- ============================================================
SELECT
  EXTRACT(MONTH FROM week) AS month_num,
  FORMAT_DATE('%B', week) AS month_name,
  ROUND(AVG(weekly_hours_viewed), 0) AS avg_hours_viewed,
  ROUND(AVG(weekly_views), 0) AS avg_views
FROM `netflix-497014.runtime.netflix_runtime`
GROUP BY month_num, month_name
ORDER BY month_num;


-- ============================================================
-- QUERY 7: TV vs Films Viewership by Quarter
-- Purpose: Compare total hours viewed between TV and Films
--          across each quarter — tracks content format trends
-- ============================================================
SELECT
  CASE 
    WHEN category LIKE 'TV%' THEN 'TV' 
    ELSE 'Films' 
  END AS content_type,
  DATE_TRUNC(week, QUARTER) AS quarter,
  SUM(weekly_hours_viewed) AS total_hours,
  SUM(weekly_views) AS total_views
FROM `netflix-497014.runtime.netflix_runtime`
GROUP BY content_type, quarter
ORDER BY quarter, content_type;


-- ============================================================
-- QUERY 8: Flash-in-the-Pan Titles
-- Purpose: Find titles that debuted at #1 but disappeared
--          from the Top 10 within 2 weeks — identifies
--          high-hype but low-retention content
-- ============================================================
SELECT 
  show_title, 
  category,
  MIN(weekly_rank) AS best_rank,
  MAX(cumulative_weeks_in_top_10) AS total_weeks,
  SUM(weekly_hours_viewed) AS total_hours
FROM `netflix-497014.runtime.netflix_runtime`
GROUP BY show_title, category
HAVING MAX(cumulative_weeks_in_top_10) <= 2 
  AND MIN(weekly_rank) = 1
ORDER BY total_hours DESC;
