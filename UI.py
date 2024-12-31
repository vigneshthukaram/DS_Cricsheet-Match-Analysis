import streamlit as st
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('cricket_matches.db')
cursor = conn.cursor()

# Function to fetch data for visualizations
def fetch_data(query):
    return pd.read_sql(query, conn)

# Streamlit setup
st.title("Cricket Data Insights")
st.sidebar.title("Select Insight")
def extract_margin(match_result):
    if match_result and "by" in match_result:
        margin_str = match_result.split("by")[1].strip()
        # Extract the number from the string (could be either 'runs' or 'wickets')
        margin = ''.join([char for char in margin_str if char.isdigit()])
        return int(margin) if margin else None
    return None

# 1. Top 10 Batsmen by Total Runs in ODI Matches
if st.sidebar.checkbox('Top 10 Batsmen by Total Runs in ODI Matches'):
    query = """
    SELECT player_of_match,
           IFNULL(SUM(runs_batter), 0) AS total_runs
    FROM odi_matches
    WHERE player_of_match != 'Unknown'
    GROUP BY player_of_match
    ORDER BY total_runs DESC LIMIT 10;
    """
    data = fetch_data(query)

    st.subheader('Top 10 Batsmen by Total Runs in ODI Matches')
    st.dataframe(data)

    # Creating a figure and axis before plotting
    fig, ax = plt.subplots(figsize=(10,6))
    ax.barh(data['player_of_match'], data['total_runs'], color='skyblue')
    ax.set_xlabel('Total Runs')
    ax.set_title('Top 10 Batsmen by Total Runs in ODI Matches')
    st.pyplot(fig)

# 2. Leading Wicket-Takers in T20 Matches
if st.sidebar.checkbox('Leading Wicket-Takers in T20 Matches'):
    query = """
    SELECT player_of_match,
           IFNULL(SUM(wickets_bowler), 0) AS total_wickets
    FROM t20_matches
    WHERE player_of_match != 'Unknown'
    GROUP BY player_of_match
    ORDER BY total_wickets DESC LIMIT 10;
    """
    data = fetch_data(query)

    st.subheader('Leading Wicket-Takers in T20 Matches')
    st.dataframe(data)

    # Creating a figure and axis before plotting
    fig, ax = plt.subplots(figsize=(10,6))
    ax.barh(data['player_of_match'], data['total_wickets'], color='salmon')
    ax.set_xlabel('Total Wickets')
    ax.set_title('Leading Wicket-Takers in T20 Matches')
    st.pyplot(fig)

# 3. Total Number of Centuries Across All Match Types
if st.sidebar.checkbox('Total Number of Centuries Across All Match Types'):
    query = """
    SELECT COUNT(*) AS total_centuries
    FROM (
        SELECT runs_batter FROM test_matches WHERE runs_batter >= 100
        UNION ALL
        SELECT runs_batter FROM odi_matches WHERE runs_batter >= 100
        UNION ALL
        SELECT runs_batter FROM t20_matches WHERE runs_batter >= 100
        UNION ALL
        SELECT runs_batter FROM it20_matches WHERE runs_batter >= 100
    );
    """
    data = fetch_data(query)

    st.subheader('Total Number of Centuries Across All Match Types')
    st.write(f'Total Centuries: {data["total_centuries"][0]}')


# 4. Top 10 Batsmen by Total Runs in Test Matches
if st.sidebar.checkbox('Top 10 Batsmen by Total Runs in Test Matches'):
    query = """
    SELECT player_of_match,
           IFNULL(SUM(runs_batter), 0) AS total_runs
    FROM test_matches
    WHERE player_of_match != 'Unknown'
    GROUP BY player_of_match
    ORDER BY total_runs DESC LIMIT 10;
    """
    data = fetch_data(query)

    st.subheader('Top 10 Batsmen by Total Runs in Test Matches')
    st.dataframe(data)

    # Creating a figure and axis before plotting
    fig, ax = plt.subplots(figsize=(10,6))
    ax.barh(data['player_of_match'], data['total_runs'], color='lightcoral')
    ax.set_xlabel('Total Runs')
    ax.set_title('Top 10 Batsmen by Total Runs in Test Matches')
    st.pyplot(fig)

# 5. Best Bowling Performance by Player in T20 Matches
if st.sidebar.checkbox('Best Bowling Performance by Player in T20 Matches'):
    query = """
    SELECT player_of_match,
           MAX(wickets_bowler) AS best_bowling_performance
    FROM t20_matches
    WHERE player_of_match != 'Unknown'
    GROUP BY player_of_match
    ORDER BY best_bowling_performance DESC LIMIT 10;
    """
    data = fetch_data(query)

    st.subheader('Best Bowling Performance by Player in T20 Matches')
    st.dataframe(data)

    # Creating a figure and axis before plotting
    fig, ax = plt.subplots(figsize=(10,6))
    ax.barh(data['player_of_match'], data['best_bowling_performance'], color='darkblue')
    ax.set_xlabel('Best Bowling Performance (Wickets)')
    ax.set_title('Best Bowling Performance by Player in T20 Matches')
    st.pyplot(fig)

# 6. Most Runs in a Single ODI Match (By Player)
if st.sidebar.checkbox('Most Runs in a Single ODI Match (By Player)'):
    query = """
    SELECT player_of_match,
           MAX(runs_batter) AS most_runs
    FROM odi_matches
    WHERE player_of_match != 'Unknown'
    GROUP BY player_of_match
    ORDER BY most_runs DESC LIMIT 10;
    """
    data = fetch_data(query)

    st.subheader('Most Runs in a Single ODI Match (By Player)')
    st.dataframe(data)

# 7. Total Number of Matches Played by Team in ODI Matches
if st.sidebar.checkbox('Total Number of Matches Played by Team in ODI Matches'):
    query = """
    SELECT teams, COUNT(*) AS total_matches
    FROM odi_matches
    WHERE teams != 'Unknown'
    GROUP BY teams
    ORDER BY total_matches DESC LIMIT 10;
    """
    data = fetch_data(query)

    st.subheader('Total Number of Matches Played by Team in ODI Matches')
    st.dataframe(data)

    # Creating a figure and axis before plotting
    fig, ax = plt.subplots(figsize=(10,6))
    ax.barh(data['teams'], data['total_matches'], color='seagreen')
    ax.set_xlabel('Total Matches')
    ax.set_title('Total Number of Matches Played by Team in ODI Matches')
    st.pyplot(fig)

# Close the connection
conn.close()
