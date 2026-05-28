# 🎬 Netflix Top 10 Streaming Data Analysis (2021–2026)

**Tools:** SQL · Google BigQuery · Python · Pandas · Matplotlib  
**Dataset:** Netflix Top 10 Weekly Data — 10,200 rows · 9 columns · July 2021 to May 2026  
**Author:** Karma Yangden · Perth, WA · [LinkedIn](https://www.linkedin.com/in/karma-yangden-480658289/)

---

## 📌 Project Overview

This project analyses Netflix's global Top 10 weekly viewership data spanning 5 years across 4 content categories (English/Non-English × TV/Films). The goal was to uncover patterns in viewership behaviour, content longevity, language trends, and audience engagement using SQL and Python.

---

## 🗂️ Dataset

| Column | Description |
|---|---|
| `week` | Week start date |
| `category` | Content category (TV English, TV Non-English, Films English, Films Non-English) |
| `weekly_rank` | Rank within category for that week (1–10) |
| `show_title` | Title of the show or film |
| `weekly_hours_viewed` | Total hours viewed that week globally |
| `weekly_views` | Total number of views that week |
| `runtime` | Runtime in hours (films only) |
| `cumulative_weeks_in_top_10` | Total weeks the title has appeared in Top 10 |

---

## 🔍 Queries & Analysis

| # | Query | Key Question |
|---|---|---|
| 1 | All-time most-watched titles | Which titles dominated Netflix overall? |
| 2 | Longest-staying titles | Which titles had the most staying power? |
| 3 | Runtime vs viewership | Does film length affect how many people watch? |
| 4 | Non-English content growth | Is Netflix's global content strategy working? |
| 5 | Most weeks at #1 | Which titles held the top spot the longest? |
| 6 | Seasonal viewing trends | When do people watch Netflix the most? |
| 7 | TV vs Films by quarter | Which format drives more hours viewed? |
| 8 | Flash-in-the-pan titles | Which titles debuted big but disappeared fast? |

---

## 💡 Key Findings

- **TV dominates** — TV content consistently accounts for ~73% of total hours viewed every quarter
- **January & December** are peak viewing months, April and August are the quietest
- **Standard-length films (90–120 min)** attract the highest average weekly views — the sweet spot for engagement
- **Non-English content** maintains a stable and significant share of the Top 10 every year, proving Netflix's global strategy is working
- **Stranger Things** is the all-time most-watched title with over 5.8 billion hours viewed

---

## 📊 Full Report

A complete data analysis report with 6 visualisations and written insights was produced from this project.  
👉 [View Full Report on LinkedIn](https://www.linkedin.com/in/karma-yangden-480658289/)

---

## 🛠️ How to Run

1. Upload the dataset to Google BigQuery
2. Create a dataset and table (project: your-project-id)
3. Run queries from `netflix_analysis.sql` in the BigQuery console
4. For Python visualisations, run `netflix_visualisation.py` (requires pandas, matplotlib)

---

## 📁 Files in This Repository

```
netflix-data-analysis/
│
├── netflix_analysis.sql        ← All 8 BigQuery SQL queries
├── netflix_visualisation.py    ← Python charts and visualisations
└── README.md                   ← Project overview (this file)
```

---

*This project was completed as part of my data analytics portfolio. Data sourced from Netflix public Top 10 dataset.*
