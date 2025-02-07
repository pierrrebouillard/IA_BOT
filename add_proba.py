import sqlite3
from app import get_score_prediction, get_match_prediction, get_top_scorers


def get_unresolved_matches():
    conn = sqlite3.connect('football_stats.db')
    cursor = conn.cursor()
    
    upcoming_matches = []
    leagues = ["Premier_League", "Serie_A", "La_Liga", "Bundesliga", "Ligue_1"]
    
    for league in leagues:
        cursor.execute(f'''
            SELECT HomeTeam, AwayTeam, Date 
            FROM {league}_matches_Upcoming
        ''')
        matches = cursor.fetchall()
        
        for match in matches:
            home_team, away_team, date = match
            upcoming_matches.append((league, home_team, away_team, date))
    
    conn.close()
    return upcoming_matches


def calculate_match_probabilities(league, team1, team2):
    prediction = get_score_prediction(league, team1, team2)
    
    if "error" in prediction:
        return None

    predicted_score_team1 = prediction["predicted_score"]["team1"]
    predicted_score_team2 = prediction["predicted_score"]["team2"]

    # Déterminer les probabilités de victoire, match nul, ou défaite
    match_winner = get_match_prediction(league, team1, team2)
    
    if "winner" not in match_winner:
        return None

    if match_winner["winner"] == team1:
        prob_win_team1 = 0.55
        prob_draw = 0.25
        prob_win_team2 = 0.20
    elif match_winner["winner"] == team2:
        prob_win_team1 = 0.20
        prob_draw = 0.25
        prob_win_team2 = 0.55
    else:
        prob_win_team1 = 0.33
        prob_draw = 0.34
        prob_win_team2 = 0.33

    # Sélection des buteurs potentiels
    top_scorers = get_top_scorers(league, team1, team2)
    top_scorers_list = [f"{scorer[0]} ({scorer[1]} buts)" for scorer in top_scorers]

    return {
        "league": league,
        "team1": team1,
        "team2": team2,
        "prob_win_team1": prob_win_team1,
        "prob_draw": prob_draw,
        "prob_win_team2": prob_win_team2,
        "predicted_score_team1": predicted_score_team1,
        "predicted_score_team2": predicted_score_team2,
        "top_scorers": ", ".join(top_scorers_list)
    }


def store_match_probabilities(match_data):
    conn = sqlite3.connect('football_stats.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR REPLACE INTO Match_Probabilities 
        (league, team1, team2, date, prob_win_team1, prob_draw, prob_win_team2, 
        predicted_score_team1, predicted_score_team2, top_scorers)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        match_data["league"], match_data["team1"], match_data["team2"], match_data["date"],
        match_data["prob_win_team1"], match_data["prob_draw"], match_data["prob_win_team2"],
        match_data["predicted_score_team1"], match_data["predicted_score_team2"], match_data["top_scorers"]
    ))

    conn.commit()
    conn.close()



def process_all_upcoming_matches():
    upcoming_matches = get_unresolved_matches()
    for match in upcoming_matches:
        league, team1, team2, date = match
        probabilities = calculate_match_probabilities(league, team1, team2)
        
        if probabilities:
            probabilities["date"] = date  # Ajouter la date avant insertion
            store_match_probabilities(probabilities)

    print("Toutes les probabilités des matchs à venir ont été calculées et enregistrées.")


if __name__ == "__main__":
    process_all_upcoming_matches()
