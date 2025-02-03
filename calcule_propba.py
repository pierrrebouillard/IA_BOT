import requests
import sqlite3
import time


def calculer_chances_resultats(team_id, opponent_id):
    conn = sqlite3.connect('football.db')
    c = conn.cursor()
    # Sélectionne les résultats précédents entre deux équipes
    query = """
    SELECT home_score, away_score FROM matches
    WHERE (team_id = ? AND opponent = ?) OR (team_id = ? AND opponent = ?)
    """
    c.execute(query, (team_id, opponent_id, opponent_id, team_id))
    results = c.fetchall()
    
    victories = sum(1 for home, away in results if (home > away and team_id == str(opponent_id)) or (home < away and team_id != str(opponent_id)))
    defeats = sum(1 for home, away in results if (home < away and team_id == str(opponent_id)) or (home > away and team_id != str(opponent_id)))
    draws = sum(1 for home, away in results if home == away)
    total_games = len(results)
    
    prob_victories = victories / total_games if total_games else 0
    prob_draws = draws / total_games if total_games else 0
    prob_defeats = defeats / total_games if total_games else 0
    conn.close()
    
    return prob_victories, prob_draws, prob_defeats

# Exemple d'utilisation
team_id = '133604'  # ID de Birmingham
opponent_id = '133613'  # ID de Lincoln
probs = calculer_chances_resultats(team_id, opponent_id)
print(f"Chances de Victoire, Nul, Défaite contre {opponent_id}: {probs}")

from scipy.stats import poisson

def probabilite_nombre_buts(moyenne_buts):
    # Probabilités pour 0, 1, 2, 3, 4 buts
    return [poisson.pmf(i, moyenne_buts) for i in range(5)]

# Exemple d'utilisation
probs_buts = probabilite_nombre_buts(3)
print(f"Probabilités des résultats de 0 à 4 buts: {probs_buts}")

