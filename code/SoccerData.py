import requests
import json
from datetime import date

websiteURL = "https://www.football-data.org/"

apiKey = "da6fc67156e34b5580ff508b05945c9f"

selectedID = ""
selectedStandingsURI = ""
selectedScorersURI = ""
selectedMatchesURI = ""
ENGuri = "http://api.football-data.org/v4/competitions/PL/standings"
GERuri = "http://api.football-data.org/v4/competitions/BL1/standings"
ITAuri = "http://api.football-data.org/v4/competitions/SA/standings"
FRAuri = "http://api.football-data.org/v4/competitions/FL1/standings"

leagues = ["England", "Germany", "Italy", "France", "Spain"]
leagueIDs = {"England": "PL", "Germany": "BL1", "Italy": "SA", "France": "FL1", "Spain": "PD", "UEFA Champions League": "CL"}


# Function for user to input which league they want to see the standings for
# The function validates whether the input is a valid league
def inputLeague():
    print("")
    print("LEAGUES AVAILABLE:")
    leagueValidation = True
    
    for league in leagues:
        print(league)

    while leagueValidation == True:
        print("")
        competition = input("Which League would you like to see the standings for?    ")

        if competition in leagues:
            selectedID = leagueIDs[competition]
            globals()["selectedStandingsURI"] = f"http://api.football-data.org/v4/competitions/{selectedID}/standings"
            globals()["selectedScorersURI"] = f"http://api.football-data.org/v4/competitions/{selectedID}/scorers"
            globals()["selectedMatchesURI"] = f"http://api.football-data.org/v4/competitions/{selectedID}/matches"
            leagueValidation = False
        else:
            print("Not a valid league, try again")
            print("")

# Function to print selected table
def printLeagueTable():
    # Make API request and return a json file of the selected league
    headers = { 'X-Auth-Token': apiKey }
    response = requests.get(selectedStandingsURI, headers=headers)

    # Retreiving the league name and season year
    leagueYear = response.json()["season"]["startDate"][:4]
    leagueName = response.json()["competition"]["name"]

    # Retrieving raw League Table with every stat available
    rawLeagueTable = response.json()["standings"][0]["table"]

    # Creating new league table dictionary with only the stats I want
    filteredLeagueTable = {}
    for team in rawLeagueTable:
        rank = team["position"]
        name = team["team"]["name"]
        wins = team["won"]
        draws = team["draw"]
        losses = team["lost"]
        points = team["points"]

        filteredLeagueTable[name] = {"rank": rank, 
                                    "wins": wins,  
                                    "draws": draws, 
                                    "losses": losses, 
                                    "points": points}
        
    # Finding largest team name length
    longestTeam = ""
    for team in filteredLeagueTable:
        if len(team) > len(longestTeam):
            longestTeam = team

    length = int(len(longestTeam))

    # Printing new league table
    print(f"{'':-<60}")
    print(leagueName + " " + str(leagueYear) + " Season Standings")
    print(f"{'':-<60}")
    print(f"{'Rank': <5}{'Team Name': <28}{'W': <5}{'D': <5}{'L': <5}{'Points'}")
    print("")

    for team in filteredLeagueTable:
        print(f"{filteredLeagueTable[team]['rank']: <5}{team: <28}{filteredLeagueTable[team]['wins']: <5}{filteredLeagueTable[team]['draws']: <5}{filteredLeagueTable[team]['losses']: <5}{filteredLeagueTable[team]['points']: <5}")
    
    print("")

def printTopScorers():
    # Make API request and return a json file of the selected league
    headers = { 'X-Auth-Token': apiKey }
    response = requests.get(selectedScorersURI, headers=headers)

    # Retrieving raw goalscorer table with every stat available
    rawScorerTable = response.json()["scorers"]

    # Creating new scorer dictionary with only the stats I want
    filteredScorerTable = {}

    for player in rawScorerTable:
        name = player["player"]["name"]
        goals = player["goals"]
        team = player["team"]["name"]

        if player["penalties"] == None:
            penalties = 0
        else:
            penalties = player["penalties"]

        filteredScorerTable[name] = {"goals": goals,  
                                    "team": team,
                                    "penalties": penalties}

    # Printing new scorer table
    print(f"{'':-<60}")
    print("Top Goalscorers")
    print(f"{'':-<60}")
    print(f"{'Goals': <8}{'Penalties': <12}{'Player Name': <20}{'Team'}")
    print("")

    for player in filteredScorerTable:
        print(f"{filteredScorerTable[player]['goals']: <8}{filteredScorerTable[player]['penalties']: <12}{player: <20}{filteredScorerTable[player]['team']}")

    print("")


def matches():
    # Make API request and return a json file of the selected league
    headers = { 'X-Auth-Token': apiKey }
    response = requests.get(selectedMatchesURI, headers=headers)

    # Retrieving raw match table with every stat available
    rawMatchesTable = response.json()["matches"]

    # Get current date
    todaysDate = date.today()

    # Creating new matches dictionary with only the stats I want
    filteredMatchTable = {}
    
    # Pull matchday, score, and team names for matches occuring today
    gameNum = 1
    for matches in rawMatchesTable:
        gameDate = matches["utcDate"][:10]

        if gameDate == todaysDate:
            matchday = matches["matchday"]
            homeTeam = matches["homeTeam"]["name"]
            awayTeam = matches["awayTeam"]["name"]

            filteredMatchTable[gameNum] = {"awayTeam": awayTeam,  
                                        "homeTeam": homeTeam}
            gameNum += 1

    # Printing all matches that occur today and states if there are none
    if len(filteredMatchTable) != 0:
        print("Matchday " + str(matchday))
        for match in filteredMatchTable:
            print(f"{match: <5}{filteredMatchTable[match]['homeTeam']: <28}{filteredMatchTable[match]['awayTeam']}")
    else:
        print("No matches today")
    print("")


# Function that will prompt the user to search again or exit program
def programLoop():
    activeCheck = input("Would you like to look up another league? Yes/No    ")

    if activeCheck =="yes" or activeCheck == "Yes":
        print("")
        globals()["active"] = True
    else:
        print("Thank You")
        globals()["active"] = False

# Main function for organization
active = True
def main():
    while active == True:
        inputLeague()
        printLeagueTable()
        printTopScorers()
        matches()
        programLoop()
main()