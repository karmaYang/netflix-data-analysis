# ============================================================
# Netflix Top 10 Streaming Data Analysis — Visualisations
# Author: Karma Yangden
# Tools: Python, Pandas, Matplotlib
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ── Load Data ─────────────────────────────────────────────────────────────────
df = pd.read_csv('netflix_runtime.csv')
df['week'] = pd.to_datetime(df['week'])
df['quarter'] = df['week'].dt.to_period('Q').astype(str)
df['year'] = df['week'].dt.year
df['month_num'] = df['week'].dt.month
df['month_name'] = df['week'].dt.strftime('%b')
df['content_type'] = df['category'].apply(lambda x: 'TV' if x.startswith('TV') else 'Films')
df['language'] = df['category'].apply(lambda x: 'Non-English' if 'Non-English' in x else 'English')

# ── Style ──────────────────────────────────────────────────────────────────────
RED   = '#E50914'
GRAY  = '#564D4D'
plt.rcParams.update({
    'font.family': 'sans-serif',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.color': '#E5E5E5',
})

# ── Chart 1: Top 10 Most-Watched Titles ───────────────────────────────────────
top10 = df.groupby('show_title')['weekly_hours_viewed'].sum().nlargest(10).sort_values()
fig, ax = plt.subplots(figsize=(10, 6))
colors = [RED if i == 9 else GRAY for i in range(10)]
ax.barh(top10.index, top10.values / 1e9, color=colors, height=0.6)
ax.set_xlabel('Total Hours Viewed (Billions)')
ax.set_title('Top 10 Most-Watched Titles (2021–2026)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('chart1_top10_titles.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 1 saved: chart1_top10_titles.png")

# ── Chart 2: TV vs Films by Quarter ───────────────────────────────────────────
tvfilm = df.groupby(['quarter', 'content_type'])['weekly_hours_viewed'].sum().unstack().fillna(0) / 1e9
fig, ax = plt.subplots(figsize=(12, 5))
x = np.arange(len(tvfilm))
ax.bar(x - 0.2, tvfilm.get('TV', 0), width=0.4, color=RED, label='TV', alpha=0.9)
ax.bar(x + 0.2, tvfilm.get('Films', 0), width=0.4, color=GRAY, label='Films', alpha=0.9)
ax.set_xticks(x)
ax.set_xticklabels([l if i % 4 == 0 else '' for i, l in enumerate(tvfilm.index)], rotation=45, ha='right')
ax.set_ylabel('Hours Viewed (Billions)')
ax.set_title('TV vs Films — Quarterly Viewership', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig('chart2_tv_vs_films.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 2 saved: chart2_tv_vs_films.png")

# ── Chart 3: Seasonal Trends ───────────────────────────────────────────────────
seasonal = df.groupby(['month_num', 'month_name'])['weekly_hours_viewed'].mean().reset_index().sort_values('month_num')
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(seasonal['month_name'], seasonal['weekly_hours_viewed'] / 1e6,
        color=RED, linewidth=2.5, marker='o', markersize=7)
ax.fill_between(seasonal['month_name'], seasonal['weekly_hours_viewed'] / 1e6, alpha=0.12, color=RED)
ax.set_ylabel('Avg Weekly Hours Viewed (Millions)')
ax.set_title('Seasonal Viewing Trends by Month', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('chart3_seasonal_trends.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 3 saved: chart3_seasonal_trends.png")

# ── Chart 4: English vs Non-English by Year ────────────────────────────────────
lang_yr = df.groupby(['year', 'language'])['weekly_hours_viewed'].sum().unstack().fillna(0) / 1e9
fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(len(lang_yr))
ax.bar(x - 0.2, lang_yr.get('English', 0), width=0.4, color=RED, label='English', alpha=0.9)
ax.bar(x + 0.2, lang_yr.get('Non-English', 0), width=0.4, color=GRAY, label='Non-English', alpha=0.9)
ax.set_xticks(x)
ax.set_xticklabels(lang_yr.index)
ax.set_ylabel('Hours Viewed (Billions)')
ax.set_title('English vs Non-English Viewership by Year', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig('chart4_language_trends.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 4 saved: chart4_language_trends.png")

# ── Chart 5: Longest-Staying Titles ───────────────────────────────────────────
longestay = df.groupby('show_title')['cumulative_weeks_in_top_10'].max().nlargest(8).sort_values()
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.barh(longestay.index, longestay.values, color=[RED if i >= 6 else GRAY for i in range(8)], height=0.6)
ax.set_xlabel('Weeks in Top 10')
ax.set_title('Titles With Longest Top 10 Presence', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('chart5_longest_staying.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 5 saved: chart5_longest_staying.png")

# ── Chart 6: Runtime vs Views ──────────────────────────────────────────────────
films = df[df['content_type'] == 'Films'].dropna(subset=['runtime']).copy()
films['runtime_bucket'] = pd.cut(films['runtime'], bins=[0, 1.5, 2.0, 10],
                                  labels=['Short\n(<90 min)', 'Standard\n(90–120 min)', 'Long\n(>120 min)'])
rb = films.groupby('runtime_bucket')['weekly_views'].mean() / 1e6
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(rb.index, rb.values, color=[GRAY, RED, GRAY], width=0.5, alpha=0.9)
ax.set_ylabel('Avg Weekly Views (Millions)')
ax.set_title('Film Runtime vs Average Weekly Views', fontsize=14, fontweight='bold')
for i, val in enumerate(rb.values):
    ax.text(i, val + 0.1, f'{val:.1f}M', ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('chart6_runtime_vs_views.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 6 saved: chart6_runtime_vs_views.png")

print("\n✅ All 6 charts saved successfully!")
