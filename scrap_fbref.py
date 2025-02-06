import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
from io import StringIO
import os


def initialize_db():
    conn = sqlite3.connect('football_stats.db')
    cursor = conn.cursor()
    leagues = ['Premier_League', 'La_Liga', 'Serie_A', 'Bundesliga', 'Ligue_1']
    for league in leagues:
        # Create general stats table
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {league} (
            Team TEXT PRIMARY KEY,
            Played INTEGER,
            Wins INTEGER,
            Draws INTEGER,
            Losses INTEGER,
            Goals_For INTEGER,
            Goals_Against INTEGER,
            Goal_Difference INTEGER,
            Points INTEGER,
            Current_Form_Win_Percentage REAL
        )
        ''')
        # Create upcoming matches table
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {league}_matches_Upcoming (
            Week INTEGER,
            Day TEXT,
            Date TEXT,
            Time TEXT,
            HomeTeam TEXT,
            AwayTeam TEXT,
            Venue TEXT,
            MatchReport TEXT
        )
        ''')
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {league}_PlayerStats (
            Rank INTEGER,
            Player TEXT,
            Nation TEXT,
            Position TEXT,
            Team TEXT,
            Age INTEGER,
            BirthYear INTEGER,
            Matches INTEGER,
            Starts INTEGER,
            Minutes INTEGER,
            Completed90s REAL,
            Goals INTEGER,
            Assists INTEGER,
            GoalsPlusAssists INTEGER,
            GoalsNonPenalty INTEGER,
            PenaltiesMade INTEGER,
            PenaltiesAttempted INTEGER,
            YellowCards INTEGER,
            RedCards INTEGER,
            ExpectedGoals REAL,
            NonPenaltyExpectedGoals REAL,
            ExpectedAssist REAL,
            NonPenaltyxGPlusxA REAL,
            ProgressiveCarries INTEGER,
            ProgressivePasses INTEGER,
            ProgressiveRuns INTEGER,
            SeasonGoals INTEGER,
            SeasonAssists INTEGER,
            SeasonGoalsPlusAssists INTEGER,
            SeasonGoalsNonPenalty INTEGER,
            SeasonGoalsPlusAssistsNonPenalty INTEGER,
            SeasonxG REAL,
            SeasonxA REAL,
            SeasonxGPlusxA REAL,
            SeasonnpxG REAL,
            SeasonnpxGPlusxA REAL
        )
        ''')
    conn.commit()
    conn.close()


def get_next_matches(url, league_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    match_results_table = soup.find('table', {'class': 'stats_table'})


def scrape_and_store_playerstat(url, league):
    try:
        response = requests.get(url)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return


    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        #print seulement les tableau
        print(soup.find_all('table'))
        match_table = soup.find('table', {'class': 'eq2'})

        tables = soup.find_all('table')
        match_table = tables[2]
        if match_table is None:
            print("No matching table found on the page.")
            return
    except Exception as e:
        print(f"Failed to parse data: {e}")
        return

    try:
        print("Match table found: Processing data...")
        html_io = StringIO(str(match_table))
        df = pd.read_html(html_io)[0]
    except Exception as e:
        print(f"Failed to parse data: {e}")
        return

    try:
        conn = sqlite3.connect('football_stats.db')
        cursor = conn.cursor()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return

    try:
        for _, row in df.iterrows():
            cursor.execute(f'''
            INSERT INTO {league}_PlayerStats (
                Rank, Player, Nation, Position, Team, Age, BirthYear, Matches, Starts,
                Minutes, Completed90s, Goals, Assists, GoalsPlusAssists, GoalsNonPenalty,
                PenaltiesMade, PenaltiesAttempted, YellowCards, RedCards, ExpectedGoals,
                NonPenaltyExpectedGoals, ExpectedAssist, NonPenaltyxGPlusxA, ProgressiveCarries,
                ProgressivePasses, ProgressiveRuns, SeasonGoals, SeasonAssists, SeasonGoalsPlusAssists,
                SeasonGoalsNonPenalty, SeasonGoalsPlusAssistsNonPenalty, SeasonxG, SeasonxA,
                SeasonxGPlusxA, SeasonnpxG, SeasonnpxGPlusxA
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['Clt'], row['Joueur'], row['Nation'], row['Pos'], row['Équipe'], row['Âge'],
                row['Naissance'], row['MJ'], row['Titulaire'], row['Min'], row['90'], row['Buts'],
                row['PD'], row['B+PD'], row['B-PénM'], row['PénM'], row['PénT'], row['CJ'], row['CR'],
                row['xG'], row['npxG'], row['xAG'], row['npxG+xAG'], row['PrgC'], row['PrgP'],
                row['PrgR'], row['Buts'], row['PD'], row['B+PD'], row['B-PénM'], row['B+PD-PénM'],
                row['xG'], row['xAG'], row['xG+xAG'], row['npxG'], row['npxG+xAG']
            ))
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return

    conn.commit()
    conn.close()



def scrape_and_store_data(url, league_name):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        match_results_table = soup.find('table', {'class': 'stats_table'})
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return
    except Exception as e:
        print(f"Failed to parse data: {e}")
        return

    try:
        html_io = StringIO(str(match_results_table))
        df = pd.read_html(html_io)[0]
    except Exception as e:
        print(f"Failed to parse data: {e}")
        return

    try:
        conn = sqlite3.connect('football_stats.db')
        cursor = conn.cursor()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return

    try:
        for _, row in df.iterrows():
            # Process last five matches to calculate the current form win percentage
            last_five = row['5 derniers']
            victory_percentage = ((last_five.count('V') + (last_five.count('N') * 0.5)) / len(last_five.replace(" ", ""))) * 100 if last_five else 0

            # Upsert data into the table
            cursor.execute(f'''
            INSERT INTO {league_name} (Team, Played, Wins, Draws, Losses, Goals_For, Goals_Against, Goal_Difference, Points, Current_Form_Win_Percentage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(Team) DO UPDATE SET
            Played = excluded.Played,
            Wins = excluded.Wins,
            Draws = excluded.Draws,
            Losses = excluded.Losses,
            Goals_For = excluded.Goals_For,
            Goals_Against = excluded.Goals_Against,
            Goal_Difference = excluded.Goal_Difference,
            Points = excluded.Points,
            Current_Form_Win_Percentage = excluded.Current_Form_Win_Percentage
            ''', (row['Équipe'], row['MJ'], row['V'], row['N'], row['D'], row['BM'], row['BE'], row['DB'], row['Pts'], victory_percentage))
    except sqlite3.Error as e:
        print(f"Database error: {e}")

    conn.commit()
    conn.close()


def scrape_and_store_upcoming_matches(url, league_name):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError for bad requests (4XX or 5XX)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        match_table = soup.find('table', {'class': 'stats_table'})
        html_io = StringIO(str(match_table))
        df = pd.read_html(html_io)[0]
        upcoming_matches = df[df['Score'].isna()]
    except Exception as e:
        print(f"Failed to parse data: {e}")
        return

    try:
        conn = sqlite3.connect('football_stats.db')
        cursor = conn.cursor()
        for _, row in upcoming_matches.iterrows():
            # if week = null continue
            if pd.isnull(row['Sem.']):
                continue
            cursor.execute(f'''
            INSERT INTO {league_name}_Upcoming (Week, Day, Date, Time, HomeTeam, AwayTeam, Venue, MatchReport)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (row['Sem.'], row['Jour'], row['Date'], row['Heure'], row['Domicile'], row['Extérieur'], row['Tribune'], row['Rapport de match']))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def main():
    initialize_db()  # Initialize database and tables
    leagues_info = {
        'Premier_League': 'https://fbref.com/fr/comps/9/Statistiques-Premier-League',
        'La_Liga': 'https://fbref.com/fr/comps/12/Statistiques-LaLiga',
        'Serie_A': 'https://fbref.com/fr/comps/11/Statistiques-Serie-A',
        'Bundesliga': 'https://fbref.com/fr/comps/20/Statistiques-Bundesliga',
        'Ligue_1': 'https://fbref.com/fr/comps/13/Statistiques-Ligue-1',
    }

    leagues_matches = {
        'Premier_League_matches':'https://fbref.com/fr/comps/9/calendrier/Scores-et-tableaux-Premier-League',
        'La_Liga_matches':'https://fbref.com/fr/comps/12/calendrier/Scores-et-tableaux-La-Liga',
        'Seria_A_matches':'https://fbref.com/fr/comps/11/calendrier/Scores-et-tableaux-Serie-A',
        'Bundesliga_matches':'https://fbref.com/fr/comps/20/calendrier/Scores-et-tableaux-Bundesliga',
        'Ligue_1_matches':'https://fbref.com/fr/comps/13/calendrier/Scores-et-tableaux-Ligue-1',
    }

    league_player_stats = {
        'Premier_League_players':'https://fbref.com/fr/comps/9/stats/Statistiques-Premier-League',
        'La_Liga_players':'https://fbref.com/fr/comps/stats/Statistiques-La-Liga',
        'Serie_A_players':'https://fbref.com/fr/comps/stats/Statistiques-Serie-A',
        'Bundesliga_players':'https://fbref.com/fr/comps/20/stats/Statistiques-Bundesliga',
        'Ligue_1_players':'https://fbref.com/fr/comps/13/stats/Statistiques-Ligue-1',
    }

    for league, url in leagues_info.items():
        scrape_and_store_data(url, league)

    for league, url in leagues_matches.items():
        scrape_and_store_upcoming_matches(url, league)

    #for league, url in league_player_stats.items():
    #    scrape_and_store_playerstat(url, league)

if __name__ == "__main__":
    main()
