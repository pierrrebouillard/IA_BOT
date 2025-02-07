<<<<<<< Updated upstream
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
=======
>>>>>>> Stashed changes
import sqlite3
import openai
import hashlib
<<<<<<< Updated upstream
import re
import random
=======
import os
import logging
import re
from datetime import datetime
>>>>>>> Stashed changes

# Configurez votre clé API OpenAI ici (ou via une variable d'environnement)
openai.api_key = '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'
if not openai.api_key:
    raise ValueError("❌ Aucune clé API détectée !")

# Configuration du logger
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

<<<<<<< Updated upstream
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']  # In production, hash this password before storing

    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Simple hashing for demonstration

    token = hashlib.sha256(username.encode()).hexdigest()  # Generate a token for the user
=======
# Chemin du vector store (s'il est utilisé ailleurs)
CHROMA_DB_PATH = "chroma_db"

# --------------------- Fonctions de Prédiction ---------------------
>>>>>>> Stashed changes

def get_match_prediction(league, team1, team2):
    try:
        conn = sqlite3.connect('football_stats.db')
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {league} WHERE Team = ?', (team1,))
        team1_stats = cursor.fetchone()
        cursor.execute(f'SELECT * FROM {league} WHERE Team = ?', (team2,))
        team2_stats = cursor.fetchone()
        if not team1_stats or not team2_stats:
            return {"error": "Team data not found"}
        # Calcul simple basé sur la différence de points (exemple : colonne index 8) et avantage domicile
        point_diff = abs(team1_stats[8] - team2_stats[8])
        home_advantage = 5
        team1_adjusted = team1_stats[-1] + home_advantage - point_diff / 10
        team2_adjusted = team2_stats[-1] - point_diff / 10
        score_pred = get_score_prediction(league, team1, team2)
        if score_pred["predicted_score"]["team1"] == score_pred["predicted_score"]["team2"]:
            return {"winner": "draw"}
        if team1_adjusted > team2_adjusted:
            return {"winner": team1}
        elif team1_adjusted < team2_adjusted:
            return {"winner": team2}
        else:
            return {"winner": "draw"}
    finally:
        conn.close()

<<<<<<< Updated upstream
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    print(username)
    print(password)

    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Simple hashing for demonstration

    conn = sqlite3.connect('football_stats.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password, token FROM Users WHERE username = ?', (username,))
    stored_password = cursor.fetchone()

    if stored_password and stored_password[0] == hashed_password:
        #return token and redirect to /chatbot
        return jsonify({"message": "Login successful", "token": stored_password[1]}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

def generate_textual_response(description, data, probability):
    prompt = f"{description} Here are the details: {data}. How would you summarize this for a sports betting enthusiast? and the probability of this happening is {probability}"

=======
def get_score_prediction(league, team1, team2):
>>>>>>> Stashed changes
    try:
        conn = sqlite3.connect('football_stats.db')
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {league} WHERE Team = ?', (team1,))
        team1_stats = cursor.fetchone()
        cursor.execute(f'SELECT * FROM {league} WHERE Team = ?', (team2,))
        team2_stats = cursor.fetchone()
        if not team1_stats or not team2_stats:
            return {"error": "Team data not found"}
        team1_goals = (team1_stats[5] / team1_stats[1])
        team2_goals = (team2_stats[5] / team2_stats[1])
        team1_concede = (team1_stats[6] / team1_stats[1])
        team2_concede = (team2_stats[6] / team2_stats[1])
        predicted_score_team1 = ((team1_goals + team2_concede) / 2) + 0.3
        predicted_score_team2 = ((team2_goals + team1_concede) / 2) - 0.3
        json_result = {
            "predicted_score": {
                "team1": round(predicted_score_team1),
                "team2": round(predicted_score_team2)
            }
        }
        return json_result
    finally:
        conn.close()

def get_upcoming_matches(league):
    """
    Récupère les matchs à venir pour une ligue donnée à partir de la table <league>_matches_Upcoming.
    On suppose que la table contient au moins :
      - La date du match (index 3)
      - L'équipe à domicile (index 4)
      - L'équipe à l'extérieur (index 5)
      - Le lieu du match (index 6)
    """
    try:
        conn = sqlite3.connect('football_stats.db')
        cursor = conn.cursor()
        query = f'SELECT * FROM {league}_matches_Upcoming'
        print(query)
        cursor.execute(query)
        matches = cursor.fetchall()
        match_list = []
        for match in matches:
            raw_date = match[3]
            try:
                if "T" in raw_date:
                    date_obj = datetime.fromisoformat(raw_date)
                else:
                    date_obj = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
                date_formatted = date_obj.strftime("%d/%m/%Y %H:%M")
            except Exception:
                date_formatted = raw_date
            match_list.append({
                "home_team": match[4],
                "away_team": match[5],
                "date": date_formatted,
                "location": match[6]
            })
        return match_list[:10]
    finally:
        conn.close()

# --------------------- Fonctions de Probabilité ---------------------

def get_teams_and_leagues():
    conn = sqlite3.connect('football_stats.db')
    cursor = conn.cursor()
    all_league = {"Premier_League", "Serie_A", "La_Liga", "Bundesliga", "Ligue_1"}
    for leg in all_league:
        league = leg
        cursor.execute(f'SELECT Team, League FROM {league}')
    teams_data = cursor.fetchall()
    conn.close()
    return {team[0].lower(): team[1] for team in teams_data}  # retourne un dictionnaire avec le nom de l'équipe comme clé et la ligue comme valeur


def parse_bet_query(query):
    teams_and_leagues = get_teams_and_leagues()  # Récupère les équipes et leurs ligues
    found_teams = {}

    for team, league in teams_and_leagues.items():
        if team in query.lower():  # Recherche insensible à la casse
            found_teams[team] = league

    if not found_teams:
        return {"type": "unknown", "error": "No teams found in the query"}

    # Détecter le type de pari et les valeurs spécifiques
    if "score exact" in query:
        scores = re.findall(r"(\d+)[\-:](\d+)", query)  # Trouve les motifs de scores comme "2-1" ou "3:0"
        if scores:
            return {"type": "exact_score", "teams": teams, "score": scores[0]}
    elif "nombre de buts" in query:
        total_goals = re.findall(r"plus de (\d+) buts", query)
        if total_goals:
            return {"type": "total_goals", "teams": teams, "total_goals": total_goals[0]}
    elif "buteur" in query:
        return {"type": "goal_scorer", "teams": teams, "scorer": "Specific player name needed"}  # Ceci est simplifié

    return {"type": "unknown"}


@app.route('/make_bet', methods=['POST'])
def make_bet():
    data = request.get_json()
    bet_query = data['bet_query']
    parsed_query = parse_bet_query(bet_query)

    if parsed_query['type'] == "unknown":
        return jsonify({"error": "Query type unknown or missing information"}), 400

    # Traiter le pari ici ou appeler une autre fonction pour gérer le pari
    return jsonify({"result": parsed_query}), 200


def calculate_bet_probability_score(prediction, bet):
    g_team1 = prediction['predicted_score']['team1']
    g_team2 = prediction['predicted_score']['team2']
    numbers = bet.split('-')
    num1 = int(numbers[0])
    num2 = int(numbers[1])
    if g_team1 == num1 and g_team2 == num2:
        probability = 81
    elif abs(g_team1 - num1) == 1 or abs(g_team2 - num2) == 1:
        probability = 49
    elif abs(g_team1 - num1) == 2 or abs(g_team2 - num2) == 2:
        probability = 18
    elif abs(g_team1 - num1) == 3 or abs(g_team2 - num2) == 3:
        probability = 0.1
    else:
        probability = 0.001
    return probability

def calculate_bet_probability_winner(predicted_winner, bet_team):
    predicted_winner = predicted_winner['winner']
    if predicted_winner != "draw":
        if bet_team == 'draw':
            probability_draw = 0.3
            probability_team_win = 0.1
        else:
            probability_draw = 0
            probability_team_win = 0.8
    else:
        probability_draw = 0.45
        probability_team_win = 0.8
    if predicted_winner == bet_team:
        return probability_team_win
    elif predicted_winner == 'draw':
        return probability_draw
    else:
        return 1 - (probability_team_win + probability_draw)

def calculate_bet_probability_goals(prediction, bet):
    predicted_total_goals = prediction['predicted_score']['team1'] + prediction['predicted_score']['team2']
    predicted_total_goals = round(predicted_total_goals)
    if predicted_total_goals - bet == 0:
        probability = 81
    elif abs(predicted_total_goals - bet) == 1:
        probability = 49
    elif abs(predicted_total_goals - bet) == 2:
        probability = 18
    elif abs(predicted_total_goals - bet) == 3:
        probability = 0.1
    else:
        probability = 0.001
    return probability

# --------------------- Génération de la Réponse Textuelle ---------------------

def get_top_scorers(league, team1, team2):
    conn = sqlite3.connect('football_stats.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f'''
        SELECT Player, Goals, Team FROM {league}_players_PlayerStats
        WHERE Goals != 'Buts' AND Goals GLOB '*[0-9]*'
        AND Team IN (?, ?)
        ORDER BY Goals DESC
        LIMIT 6
        ''', (team1, team2))
        top_scorers = cursor.fetchall()
        print(top_scorers)
    finally:
        conn.close()
    return top_scorers

@app.route('/recommend_scorers', methods=['POST', 'GET'])
def recommend_scorers():
    league = request.args.get('league')
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    
    if not league or not team1 or not team2:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    try:
        top_scorers = get_top_scorers(league, team1, team2)
        recommended_scorers = random.sample(top_scorers, 3)
        scorers_info = [{'player': scorer[0], 'goals': scorer[1]} for scorer in recommended_scorers]
        
        message = f"For the match {team1} vs {team2} in the {league}, the players to watch for scoring are: "
        players = ', '.join([f"{scorer['player']} ({scorer['goals']} goals)" for scorer in scorers_info])
        full_message = message + players + ". Good luck with your bets!"

        full_message = generate_textual_response(full_message, '', "50%")
        
        return jsonify({'message': full_message, 'scorers': scorers_info})
    except ValueError:  # Si moins de 3 joueurs sont disponibles pour la sélection
        return jsonify({'error': 'Not enough players to select from'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)



@app.route('/predict_goal', methods=['POST'])
def predict_goal():
    data = request.get_json()
    league = data.get('league')
    team1 = data.get('team1')
    team2 = data.get('team2')
    bet = data.get('bet', "null")
    if not league or not team1 or not team2:
        return jsonify({"error": "Missing data for league, team1, or team2"}), 400
    
    prediction = get_score_prediction(league, team1, team2)
    probability = calculate_bet_probability_goals(prediction, bet)
    response_text = generate_textual_response(f"The match prediction between {team1} and {team2} in {league} is:", prediction, probability)

    return jsonify({
        "predicted_score": prediction,
        "bet_probability": probability,
        "ai_response": response_text
    })

@app.route('/upcoming_matches', methods=['OPTIONS, POST, GET'])
def upcoming_matches():
    print(request.method)
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, PATCH, DELETE',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Credentials': 'true'
        }
        return Response(status=200, headers=headers)
    data = request.get_json()
    league = data.get('league')
    if not league:
        return jsonify({"error": "Missing data for league"}), 400
    return jsonify(get_upcoming_matches(league))

def get_match_prediction(league, team1, team2):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable assistant for sports betting. awnsert in french, be original and concise. awnser like a chatbot. Make the prediction like is our prediction"},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Failed to generate response: {str(e)}"

# --------------------- Détermination du Type de Requête ---------------------

def determine_request_type(query: str):
    """
    Analyse la question libre saisie par l'utilisateur pour déterminer le type de prédiction à effectuer.
    - Si la question contient "date" et ("prochain" ou "suiv"), on considère qu'il s'agit des matchs à venir.
    - Si la question contient "score", on considère qu'il s'agit d'une prédiction de score.
    - Si la question contient "prédiction", "vainqueur" ou "gagnant", on considère qu'il s'agit d'une prédiction du vainqueur.
    - Sinon, par défaut, on considère qu'il s'agit d'une prédiction du vainqueur.
    """
    query_lower = query.lower()
    if "date" in query_lower and ("prochain" in query_lower or "suiv" in query_lower):
        return "upcoming"
    elif "score" in query_lower:
        return "score"
    elif any(keyword in query_lower for keyword in ["prédiction", "vainqueur", "gagnant"]):
        return "match"
    else:
        return "match"

# --------------------- Boucle Interactive du Chatbot en Mode Terminal ---------------------

def main():
    print("=== Chatbot Football Predictor ===")
    print("Posez votre question en langage naturel. Par exemple :")
    print(" - 'Quelle est la probabilité que Rennes gagne son prochain match en Ligue1 ?'")
    print(" - 'Quel score est prévu pour le match Rennes contre Lille ?'")
    print(" - 'Quelles sont les dates des prochains matchs en Ligue1 ?'")
    print("Tapez 'exit' ou 'quit' pour arrêter.\n")

    # Valeurs par défaut
    default_league = "Ligue_1"  # Nom exact de la table dans la DB
    default_team1 = "Rennes"
    default_team2 = "Lille"
    default_bet = "draw"

    while True:
        user_query = input("📝 Entrez votre question: ")
        if user_query.lower() in ['exit', 'quit']:
            print("Arrêt du chatbot.")
            break

        # Extraction de la ligue : recherche d'un motif du type "Ligue 1" ou "Ligue1"
        league_match = re.search(r'(Ligue)\s*(\d+)', user_query, re.IGNORECASE)
        if league_match:
            league = league_match.group(1) + "_" + league_match.group(2)
        else:
            league = default_league

        # Extraction des équipes : recherche d'un motif "Team1 vs Team2" ou "Team1 contre Team2"
        team_match = re.search(r'\b([A-Z][a-zA-Z\s]+?)\s+(?:vs\.?|contre)\s+([A-Z][a-zA-Z\s]+?)\b', user_query)
        if team_match:
            team1 = team_match.group(1).strip()
            team2 = team_match.group(2).strip()
        else:
            team1 = default_team1
            team2 = default_team2

        # Extraction d'un éventuel pari (score) sous la forme "x-y"
        bet_match = re.search(r'\b(\d+\s*-\s*\d+)\b', user_query)
        if bet_match:
            bet = bet_match.group(1).replace(" ", "")
        else:
            if determine_request_type(user_query) == "score":
                bet = "0-0"
            else:
                bet = default_bet

        req_type = determine_request_type(user_query)
        print(f"DEBUG: Type de demande détecté: {req_type}")
        print(f"DEBUG: League: {league}, Team1: {team1}, Team2: {team2}, Bet: {bet}")

        if req_type == "upcoming":
            prediction_data = get_upcoming_matches(league)
            description = f"Les prochains matchs dans {league}"
            probability = None  # Pas de probabilité pour les matchs à venir
        elif req_type == "score":
            prediction_data = get_score_prediction(league, team1, team2)
            description = f"Le score prédit pour le match entre {team1} et {team2} dans {league}"
            probability = calculate_bet_probability_score(prediction_data, bet)
        else:  # req_type == "match"
            prediction_data = get_match_prediction(league, team1, team2)
            description = f"La prédiction du match entre {team1} et {team2} dans {league}"
            probability = calculate_bet_probability_winner(prediction_data, bet)

        # ---------------- Partie d'appel à l'API OpenAI (à ne pas modifier) ----------------
        try:
            messages = [
                {"role": "system", "content": "You are a knowledgeable assistant for sports betting. awnsert in french, be original and concise. awnser like a chatbot. Make the prediction like is our prediction"},
                {"role": "user", "content": f"Voici les données pertinentes trouvées :\n{prediction_data}\n\nRequête : {user_query}"}
            ]
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            chatbot_reply = response.choices[0].message.content
            print("\n🤖 Chatbot :")
            print(chatbot_reply)
        except openai.error.OpenAIError as e:
            print("Erreur OpenAI :", str(e))
        except Exception as ex:
            print("Erreur :", str(ex))
        print("\n" + "-" * 50 + "\n")
        # ---------------- Fin de la partie à ne pas modifier ----------------

if __name__ == '__main__':
    main()