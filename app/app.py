import streamlit as st
import requests
from datetime import date


# ----------------------
# ----- PAGE SETUP -----
# ----------------------

# Page Title
st.set_page_config(
    page_title = "Soccer API Dashboard",
    layout = "wide"
)

# Page Header
st.markdown(
    """
    <style>
    .custom-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        border-bottom: 1px solid #ddd;
        background-color: white;
        margin-bottom: 2rem;
    }

    .header-left,
    .header-right {
        display: flex;
        gap: 1.5rem;
        align-items: center;
        width: 25%;
    }

    .header-right {
        justify-content: flex-end;
    }

    .header-center {
        width: 50%;
        text-align: center;
    }

    .header-center h2 {
        margin: 0;
        font-size: 2rem;
    }

    .custom-header a {
        text-decoration: none;
        color: #1f1f1f;
        font-weight: 500;
    }

    .custom-header a:hover {
        color: #0073e6;
    }
    </style>

    <div class="custom-header">

        <div class="header-left">
            <a href="https://corcoran.georgetown.domains/Homepage/" target="_blank">
                Portfolio Homepage
            </a>
        </div>

        <div class="header-center">
            <h2>Soccer Data API Dashboard</h2>
        </div>

        <div class="header-right">
            <a href="https://github.com/dcorc7/" target="_blank">
                GitHub
            </a>

            <a href="https://www.linkedin.com/in/david-corcoran-70677917a/" target="_blank">
                LinkedIn
            </a>
        </div>

    </div>
    """,
    unsafe_allow_html = True
)

# Retreive API key from Streamlit secrets
API_KEY = st.secrets.get("API_KEY", "")

# Dictionaty to map League IDs recognized by the API to real-english names
LEAGUE_IDS = {
    "English Permier League (UK)": "PL",
    "Bundesliga (GER)": "BL1",
    "Serie A (ITA)": "SA",
    "Lique 1 (FRA)": "FL1",
    "La Liga (ESP)": "PD",
    "UEFA Champions League": "CL"
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

# Select box for user to pick a league
league = st.sidebar.selectbox(
    "Select a league",
    list(LEAGUE_IDS.keys())
)

# Variable to hold what league the user selected
league_id = LEAGUE_IDS[league]

# List of urls based on the selected league
urls = build_urls(league_id)


# Tab Layout
tab1, tab2, tab3, tab4 = st.tabs([
    "Dashboard Homepage"
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
        <div style="
            padding: 3rem;
            border-radius: 15px;
            background: linear-gradient(to right, #0f172a, #1e293b);
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        ">
            <h1 style="font-size: 3rem;">
                Soccer Data API Dashboard
            </h1>

            <p style="font-size: 1.2rem;">
                Explore league standings, top scorers, and live match data
                powered by the Football-Data.org API.
            </p>
        </div>
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
    # Set varaible to hold todays date
    today = str(date.today())

    st.title(f"{league} Upcoming Matches")

    # Get match json data for today
    data = fetch_data(urls["matches"])

    # Find data just for matches
    matches = data["matches"]

    # Creates table rows with matchday, home team name, away tame name
    rows = []
    for m in matches:
        if today + 7 <= m["utcDate"][:10] >= today:
            rows.append({
                "Matchday": m["matchday"],
                "Home Team Name": m["homeTeam"]["name"],
                "Away Team Name": m["awayTeam"]["name"]
            })

    # Display the dataframe 
    st.dataframe(rows, use_container_width = True)

    # Write no matches today if there are no rows
    if len(rows) <= 0:
        st.write("No matches today")

    st.markdown("---")
