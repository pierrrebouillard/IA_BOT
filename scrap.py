import requests
import sqlite3
import time

API_KEY = "3"  # Remplace par ta clé API

def create_db():
    """Crée la base de données SQLite et les tables."""
    conn = sqlite3.connect('football.db')
    c = conn.cursor()
    
    # Table des équipes
    c.execute('''CREATE TABLE IF NOT EXISTS teams
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 team_id TEXT UNIQUE, 
                 league TEXT, 
                 name TEXT, 
                 stadium TEXT, 
                 capacity INTEGER)''')

    # Table des matchs
    c.execute('''CREATE TABLE IF NOT EXISTS matches
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 team_id TEXT, 
                 opponent TEXT, 
                 date TEXT, 
                 home_score INTEGER, 
                 away_score INTEGER, 
                 FOREIGN KEY(team_id) REFERENCES teams(team_id))''')
    
    conn.commit()
    conn.close()

def insert_team(team_id, league, name, stadium, capacity):
    """Ajoute une équipe à la base de données."""
    conn = sqlite3.connect('football.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO teams (team_id, league, name, stadium, capacity) VALUES (?, ?, ?, ?, ?)",
              (team_id, league, name, stadium, capacity))
    conn.commit()
    conn.close()

def insert_match(team_id, opponent, date, home_score, away_score):
    """Ajoute un match dans la base de données."""
    conn = sqlite3.connect('football.db')
    c = conn.cursor()
    c.execute("INSERT INTO matches (team_id, opponent, date, home_score, away_score) VALUES (?, ?, ?, ?, ?)",
              (team_id, opponent, date, home_score, away_score))
    conn.commit()
    conn.close()

def fetch_teams(league_id, league_name):
    """Récupère les équipes d'un championnat donné."""
    url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/search_all_teams.php?l={league_name}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur API pour {league_name}: {response.status_code}")
        return
    
    data = response.json()
    teams = data.get('teams', [])
    
    if not teams:
        print(f"Aucune équipe trouvée pour {league_name}")
        return
    
    for team in teams:
        team_id = team.get('idTeam')
        name = team.get('strTeam')
        stadium = team.get('strStadium')
        capacity = team.get('intStadiumCapacity') or 0  # Si None, on met 0
        
        # Insérer l'équipe en DB
        insert_team(team_id, league_name, name, stadium, capacity)
        
        # Récupérer les 10 derniers matchs de l'équipe
        fetch_matches(team_id)

def fetch_matches(team_id):
    """Récupère les 10 derniers matchs d'une équipe donnée."""
    url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/eventslast.php?id={team_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur lors de la récupération des matchs pour l'équipe {team_id}")
        return
    
    data = response.json()
    matches = data.get('results', [])

    if not matches:
        print(f"Aucun match trouvé pour l'équipe {team_id}")
        return

    for match in matches[:10]:  # On limite aux 10 derniers matchs
        date = match.get('dateEvent')
        opponent = match.get('strAwayTeam') if match.get('idHomeTeam') == team_id else match.get('strHomeTeam')
        home_score = int(match.get('intHomeScore') or 0)
        away_score = int(match.get('intAwayScore') or 0)
        
        insert_match(team_id, opponent, date, home_score, away_score)
        team_id = '133597'  # Remplace par l'ID de l'équipe réelle
        moyenne_buts = calculer_moyenne_buts(team_id)
        print(f"Nombre moyen de buts récemment pour l'équipe {team_id}: {moyenne_buts}")



def calculer_moyenne_buts(team_id):
    conn = sqlite3.connect('football.db')
    c = conn.cursor()
    c.execute("SELECT home_score, away_score FROM matches WHERE team_id = ?", (team_id,))
    matches = c.fetchall()
    total_buts = sum(home + away for home, away in matches)
    moyenne_buts = total_buts / len(matches) if matches else 0
    conn.close()
    return moyenne_buts


def main():
    create_db()

    # Liste des ligues majeures avec leurs ID
    leagues = {
        '4328': 'English Premier League',
        '4335': 'Spanish La Liga',
        '4332': 'Italian Serie A',
        '4331': 'German Bundesliga',
        '4334': 'French Ligue 1'
    }

    for league_id, league_name in leagues.items():
        fetch_teams(league_id, league_name)
        time.sleep(2)  # Pour éviter d'être bloqué par l'API

if __name__ == "__main__":
    main()
