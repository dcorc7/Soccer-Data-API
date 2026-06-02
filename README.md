# Soccer API Dashboard

A Streamlit web application for exploring live soccer data — standings, top scorers, and upcoming fixtures — powered by the [Football-Data.org](https://www.football-data.org/) API.

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red) ![API](https://img.shields.io/badge/API-Football--Data.org-green)

---

## Features

- **Standings** — Full league table with wins, draws, losses, and total points
- **Top Scorers** — Leading goal scorers with penalty breakdowns and scoring efficiency
- **Upcoming Matches** — Fixtures for the next 7 days with matchday details
- **6 Leagues** — Switch between competitions instantly via the sidebar

### Supported Leagues

| League | Country | API ID |
|--------|---------|--------|
| Premier League | England 🏴󠁧󠁢󠁥󠁮󠁧󠁿 | `PL` |
| Bundesliga | Germany 🇩🇪 | `BL1` |
| Serie A | Italy 🇮🇹 | `SA` |
| Ligue 1 | France 🇫🇷 | `FL1` |
| La Liga | Spain 🇪🇸 | `PD` |
| Champions League | Europe 🏆 | `CL` |

---

## Prerequisites

- Python 3.8+
- A free API key from [football-data.org](https://www.football-data.org/)
- The following Python packages:

```
streamlit
requests
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/soccer-dashboard.git
cd soccer-dashboard
```

### 2. Install dependencies

```bash
pip install streamlit requests
```

### 3. Configure your API key

Create a `.streamlit/secrets.toml` file in the project root:

```toml
# .streamlit/secrets.toml
API_KEY = "your_football_data_api_key_here"
```

### 4. Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## Project Structure

```
soccer-dashboard/
└── .github                  
    └── daily_refresh.yml   # Continuous Deployment for daily refershing of content
└── .streamlit/
    └── secrets.toml        # API key (not committed to git)
└── app.py                  
    └── app.py              # Main Streamlit application

```

---

## Data & Caching

All data is fetched from the [Football-Data.org](https://www.football-data.org/) free-tier API (`v4`). API responses are cached for **1 hour** via `@st.cache_data(ttl=3600)` to stay within the free plan's rate limit of 10 requests per minute.

---

## Deployment

To deploy on [Streamlit Community Cloud](https://streamlit.io/cloud):

1. Push your code to a public GitHub repository (without `secrets.toml`)
2. Connect the repo in the Streamlit Cloud dashboard
3. Add `API_KEY` under **Settings → Secrets** in the Streamlit Cloud UI

---

## Links

- [GitHub](https://github.com/dcorc7/)
- [LinkedIn](https://www.linkedin.com/in/david-corcoran-70677917a/)
- [Portfolio](https://corcoran.georgetown.domains/Homepage/)