import streamlit as st
import requests
from datetime import date, datetime, timedelta


# ----------------------
# ----- PAGE SETUP -----
# ----------------------

# Page Title
st.set_page_config(
    page_title = "Soccer API Dashboard",
    layout = "wide"
)

# Page Header
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown(
        "<h2 style='margin: 0; padding: 0.5rem 0;'>Soccer Data API Dashboard</h2>",
        unsafe_allow_html=True
    )

with col_right:
    st.markdown(
        """
        <div style="display: flex; gap: 8px; justify-content: flex-end; padding: 0.5rem 0;">
            <a href="https://github.com/dcorc7/" target="_blank"
               style="display: inline-flex; align-items: center; gap: 6px;
                      padding: 6px 14px; border-radius: 8px; font-size: 14px;
                      font-weight: 500; text-decoration: none;
                      background: #1f1f1f; color: white;">
                GitHub
            </a>
            <a href="https://www.linkedin.com/in/david-corcoran-70677917a/" target="_blank"
               style="display: inline-flex; align-items: center; gap: 6px;
                      padding: 6px 14px; border-radius: 8px; font-size: 14px;
                      font-weight: 500; text-decoration: none;
                      background: #0077b5; color: white;">
                LinkedIn
            </a>
            <a href="https://corcoran.georgetown.domains/Homepage/" target="_blank"
               style="display: inline-flex; align-items: center; gap: 6px;
                      padding: 6px 14px; border-radius: 8px; font-size: 14px;
                      font-weight: 500; text-decoration: none;
                      background: #0073e6; color: white;">
                Portfolio
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

# Retreive API key from Streamlit secrets
API_KEY = st.secrets.get("API_KEY", "")

# Dictionaty to map League IDs recognized by the API to real-english names
LEAGUE_IDS = {
    "Premier League (UK)": "PL",
    "Bundesliga (GER)": "BL1",
    "Serie A (ITA)": "SA",
    "Lique 1 (FRA)": "FL1",
    "La Liga (ESP)": "PD",
    "Champions League": "CL"
}

# Function to get the Soccer API urls related to the selected league ID. Returns standings, scorers, and matches data urls
def build_urls(league_id):
    base = "https://api.football-data.org/v4/competitions"
    return {
        "standings": f"{base}/{league_id}/standings",
        "scorers": f"{base}/{league_id}/scorers",
        "matches": f"{base}/{league_id}/matches"
    }

# Function to retrive data the user wants to see in json format based on which tab is selected. 
# Pulls from the previously built urls
@st.cache_data(ttl = 3600)
def fetch_data(url):
    # Get authentication token
    headers = { "X-Auth-Token": API_KEY }
    # Get response using API Key
    response = requests.get(url, headers = headers)

    # Return response data in json format
    return response.json()


# Sidebar for league selection
st.sidebar.title("Leagues")

# Sidebar for user to pick a league
st.sidebar.markdown("### Select a League")

# Set default league to the first in the dictionary
if "selected_league" not in st.session_state:
    st.session_state.selected_league = list(LEAGUE_IDS.keys())[0]

# Loop through all league names 
for league_name in LEAGUE_IDS.keys():
    # Set is_selected to be the selected league name (default is first in list)
    is_selected = st.session_state.selected_league == league_name

    # Highlight the button if selected
    if is_selected:
        st.sidebar.markdown(
            f"""
            <div style="background-color: #0073e6; color: white; padding: 8px 12px;
                        border-radius: 8px; text-align: center; font-weight: 500;
                        font-size: 14px; margin-bottom: 4px;">{league_name}</div>
            """,
            unsafe_allow_html=True
        )
    # Non selected leagues are non-highlighted buttons
    else:
        if st.sidebar.button(league_name, use_container_width=True):
            st.session_state.selected_league = league_name
            st.rerun()

# Set league variable as league that was selected
league = st.session_state.selected_league

# Variable to hold what league the user selected
league_id = LEAGUE_IDS[league]

# List of urls based on the selected league
urls = build_urls(league_id)


# Tab Layout
tab1, tab2, tab3, tab4 = st.tabs([
    "Dashboard Homepage",
    "Standings",
    "Top Scorers",
    "Current Matches"
])


# ---------------------
# ----- STANDINGS -----
# ---------------------

# DASHBOARD HOMEPAGE TAB
with tab1:
    # Page title and Interoduction
    st.markdown(
        """
        <br>
        <p>
            Explore league standings, top scorers, and live match data powered by the <a href="https://www.football-data.org/">Football-Data.org</a> API.
        </p>
        """,
        unsafe_allow_html = True
    )

    st.markdown("---")

    st.subheader("Dashboard Summary")


    # Set 3 columns on the page
    col1, col2, col3 = st.columns(3)

    # Column 1 for the Selected league name
    with col1:
        st.metric(
            label = "Selected League",
            value = league
        )

    # Column 2 for the All available leagues
    with col2:
        st.metric(
            label = "Available Competitions",
            value = len(LEAGUE_IDS)
        )

    # Column 3 for the Data source
    with col3:
        st.metric(
            label = "Data Source",
            value = "Football-Data.org"
        )


    st.markdown("---")

    st.subheader("Dashboard Features")

    # Establish 3 features as more columns
    feature1, feature2, feature3 = st.columns(3)

    # Feature 1 to describe standings
    with feature1:
        st.markdown("""
        ### Standings

        View:
        - League table
        - Wins / draws / losses
        - Points totals
        """)

    # Feature 2 to describe Top Scorers
    with feature2:
        st.markdown("""
        ### Top Scorers

        Analyze:
        - Leading scorers
        - Penalty goals
        - Scoring efficiency
        """)

    # Feature 3 to describe Upcoming matches
    with feature3:
        st.markdown("""
        ### Matches

        Track:
        - Daily fixtures
        - Matchdays
        - Upcoming games
        """)
    
    st.markdown("---")


# LEAGUE STANDINGS TAB
with tab2:
    st.title(f"{league} Standings")

    # Retrieve standings data from selected league
    data = fetch_data(urls["standings"])

    # Gets standings json data
    table = data["standings"][0]["table"]

    # Creates table rows with Team position, team name, num wins, num draws, num losses, and total points
    rows = []
    for team in table:
        rows.append({
            "Position": team["position"],
            "Team Name": team["team"]["name"],
            "# Wins": team["won"],
            "# Draws": team["draw"],
            "# Losses": team["lost"],
            "Total Points": team["points"]
        })

    # Display the dataframe
    st.dataframe(rows, use_container_width = True)

    st.markdown("---")



# -----------------------
# ----- TOP SCORERS -----
# -----------------------

# TOP SCORERS TAB
with tab3:
    st.title(f"{league} Top Scorers")

    # Retrieve standings data from selected league
    data = fetch_data(urls["scorers"])

    # Gets Scorers json data
    scorers = data["scorers"]

    # Creates table rows with player name, team name, num goals, num penalties
    rows = []
    for player in scorers:
        rows.append({
            "Player Name": player["player"]["name"],
            "Team Name": player["team"]["name"],
            "# Goals": player["goals"],
            "# Penalties": player["penalties"] if player["penalties"] else 0,
            "% Penalties": (player["penalties"] / player["goals"] * 100) if player["penalties"] else 0
        })

    # Display the dataframe
    st.dataframe(rows, use_container_width = True)

    st.markdown("---")


# --------------------------
# ----- TODAYS MATCHES -----
# --------------------------

# TODAYS MATCHES TAB
with tab4:
    # Proper date objects
    today = date.today()
    future_date = today + timedelta(days = 7)

    st.title(f"{league} Upcoming Matches")

    data = fetch_data(urls["matches"])
    matches = data["matches"]

    # Reset rows inside tab
    rows = []

    for m in matches:
        match_date = datetime.strptime(m["utcDate"][:10], "%Y-%m-%d").date()

        if today <= match_date <= future_date:
            rows.append({
                "Matchday": m["matchday"],
                "Match Date": match_date,
                "Home Team Name": m["homeTeam"]["name"],
                "Away Team Name": m["awayTeam"]["name"]
            })

    # Display the dataframe 
    st.dataframe(rows, use_container_width = True)

    # Write no matches today if there are no rows
    if len(rows) <= 0:
        st.write("No matches in tje next 7 days")

    st.markdown("---")
