import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
from io import StringIO
import os

def initialize_db():
    # os.remove('football_stats.db')
    conn = sqlite3.connect('football_stats.db')
    cursor = conn.cursor()
    leagues = ['Premier_League', 'La_Liga', 'Serie_A', 'Bundesliga', 'Ligue_1']
    for league in leagues:
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
    for league in leagues:
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {league}_Upcoming (
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
    conn.commit()
    conn.close()

def get_next_matches(url, league_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    match_results_table = soup.find('table', {'class': 'stats_table'})


def scrape_and_store_data(url, league_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    match_results_table = soup.find('table', {'class': 'stats_table'})

    html_io = StringIO(str(match_results_table))
    df = pd.read_html(html_io)[0]

    conn = sqlite3.connect('football_stats.db')
    cursor = conn.cursor()

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

    conn.commit()
    conn.close()


def scrape_and_store_upcoming_matches(url, league_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    match_table = soup.find('table', {'class': 'stats_table'})
    html_io = StringIO(str(match_table))
    df = pd.read_html(html_io)[0]

    # Filter out rows where the 'Score' column is empty
    upcoming_matches = df[df['Score'].isna()]

    conn = sqlite3.connect('football_stats.db')
    cursor = conn.cursor()

    for _, row in upcoming_matches.iterrows():
        cursor.execute(f'''
        INSERT INTO {league_name}_Upcoming (Week, Day, Date, Time, HomeTeam, AwayTeam, Venue, MatchReport)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row['Sem.'], row['Jour'], row['Date'], row['Heure'], row['Domicile'], row['Extérieur'], row['Tribune'], row['Rapport de match']))
    
    conn.commit()
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
        'Premier_League_matches':'https://fbref.com/fr/comps/9/calendrier/Scores-et-tableaux-Premier-League'
    }

    for league, url in leagues_info.items():
        scrape_and_store_data(url, league)

    for league, url in leagues_matches.items():
        scrape_and_store_upcoming_matches(url, league)

if __name__ == "__main__":
    main()
