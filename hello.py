from preswald import connect, get_df, text, table, plotly
import pandas as pd
import plotly.express as px

# ----------------------------------------
# 1. Connect to data source and load data
# ----------------------------------------
connect()

try:
    df = get_df("international_matches")
    df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Ensures invalid dates are handled safely
    text("## International Football Match Analysis")
    text(f"**Data successfully loaded** — {len(df)} international matches from 1993 to 2022.")
    text(f"Includes **{df['tournament'].nunique()} tournaments** across **{df['country'].nunique()} host countries**.")
except Exception as e:
    text(f"❌ Error loading data: {e}")
    raise

# ----------------------------------------
# 2. Top Scoring National Teams
# ----------------------------------------
text("## Most Prolific Teams (Total Goals Scored)")

home_goals = df.groupby("home_team")["home_team_score"].sum()
away_goals = df.groupby("away_team")["away_team_score"].sum()
total_goals = (home_goals + away_goals).sort_values(ascending=False)

text("Top 5 teams by combined home and away goals:")
for team, goals in total_goals.head(5).items():
    text(f"- **{team}**: {int(goals)} goals")

# ----------------------------------------
# 3. Tournament Frequency Overview
# ----------------------------------------
text("## Most Frequently Held Tournaments")

tournament_counts = df["tournament"].value_counts().head(5)
text("Top 5 tournaments by number of matches played:")
for tournament, count in tournament_counts.items():
    text(f"- **{tournament}**: {count} matches")

# ----------------------------------------
# 4. Visualization: Top 10 Goal-Scoring Teams
# ----------------------------------------
text("## Visual Breakdown: Top 10 Scoring Teams")

top_teams_df = total_goals.head(10).reset_index()
top_teams_df.columns = ["Team", "Goals"]

fig = px.bar(
    top_teams_df,
    x="Team",
    y="Goals",
    title="Top 10 Goal-Scoring Teams (1993–2022)",
    color="Goals",
    text="Goals",
    labels={"Goals": "Total Goals"}
)
fig.update_traces(textposition='outside')
fig.update_layout(yaxis_title=None, xaxis_title=None)

plotly(fig)


# ----------------------------------------
# 5. Technical Summary
# ----------------------------------------
text("## Technical Summary & Dataset Info")

# Handle edge cases with missing or unsorted dates
valid_dates_df = df.dropna(subset=["date"]).sort_values(by="date")

if not valid_dates_df.empty:
    first_match = valid_dates_df.iloc[0]
    last_match = valid_dates_df.iloc[-1]
    
    text(f"**Source File**: `international_matches.csv`")
    text(f"**First Match**: {first_match['date'].date()} — {first_match['home_team']} vs {first_match['away_team']}")
    text(f"**Most Recent Match**: {last_match['date'].date()} — {last_match['home_team']} vs {last_match['away_team']}")
else:
    text("⚠️ No valid match dates available in the dataset.")
