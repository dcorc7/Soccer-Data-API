import streamlit as st
import requests
from datetime import date


# ----------------------
# ----- PAGE SETUP -----
# ----------------------

st.set_page_config(
    page_title = "Soccer Dashboard",
    layout = "wide"
)

st.markdown(
    """
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h2>Soccer Analytics Dashboard</h2>
        <a href="https://corcoran.georgetown.domains/Homepage/" target="_blank">Portfolio Homepage</a>
        <a href="https://github.com/dcorc7/" target="_blank">GitHub</a>
        <a href="https://www.linkedin.com/in/david-corcoran-70677917a/" target="_blank">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html = True
)

API_KEY = st.secrets.get("API_KEY", "")

LEAGUE_IDS = {
    "England": "PL",
    "Germany": "BL1",
    "Italy": "SA",
    "France": "FL1",
    "Spain": "PD",
    "UEFA Champions League": "CL"
}


def build_urls(league_id):
    base = "https://api.football-data.org/v4/competitions"
    return {
        "standings": f"{base}/{league_id}/standings",
        "scorers": f"{base}/{league_id}/scorers",
        "matches": f"{base}/{league_id}/matches"
    }


@st.cache_data(ttl = 3600)
def fetch_data(url):
    headers = { "X-Auth-Token": API_KEY }
    response = requests.get(url, headers = headers)
    return response.json()


# Sidebar league selection
st.sidebar.title("Leagues")

league = st.sidebar.selectbox(
    "Select a league",
    list(LEAGUE_IDS.keys())
)

league_id = LEAGUE_IDS[league]
urls = build_urls(league_id)


# Tabs layout
tab1, tab2, tab3 = st.tabs([
    "Standings",
    "Top Scorers",
    "Matches"
])


# ---------------------
# ----- STANDINGS -----
# ---------------------

with tab1:
    st.title(f"{league} Standings")

    data = fetch_data(urls["standings"])

    table = data["standings"][0]["table"]

    rows = []
    for team in table:
        rows.append({
            "Rank": team["position"],
            "Team": team["team"]["name"],
            "Wins": team["won"],
            "Draws": team["draw"],
            "Losses": team["lost"],
            "Points": team["points"]
        })

    st.dataframe(rows, use_container_width = True)



# -----------------------
# ----- TOP SCORERS -----
# -----------------------

with tab2:
    st.title(f"{league} Top Scorers")

    data = fetch_data(urls["scorers"])

    scorers = data["scorers"]

    rows = []
    for player in scorers:
        rows.append({
            "Player": player["player"]["name"],
            "Team": player["team"]["name"],
            "Goals": player["goals"],
            "Penalties": player["penalties"] if player["penalties"] else 0
        })

    st.dataframe(rows, use_container_width = True)


# --------------------------
# ----- TODAYS MATCHES -----
# --------------------------

with tab3:
    today = str(date.today())
    st.title(f"{league} Matches Today - {today}")

    data = fetch_data(urls["matches"])

    matches = data["matches"]

    rows = []

    for m in matches:
        if m["utcDate"][:10] == today:
            rows.append({
                "Matchday": m["matchday"],
                "Home": m["homeTeam"]["name"],
                "Away": m["awayTeam"]["name"]
            })

    if len(rows) > 0:
        st.dataframe(rows, use_container_width = True)
    else:
        st.write("No matches today")