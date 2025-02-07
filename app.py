from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import openai
import hashlib

openai.api_key = ''

app = Flask(__name__)
CORS(app)


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']  # In production, hash this password before storing

    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Simple hashing for demonstration

    token = hashlib.sha256(username.encode()).hexdigest()  # Generate a token for the user

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

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Simple hashing for demonstration

    conn = sqlite3.connect('football_stats.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password, token FROM Users WHERE username = ?', (username,))
    stored_password = cursor.fetchone()

    if stored_password and stored_password[0] == hashed_password:
        return jsonify({"message": "Login successful", "token": stored_password[1]}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

def generate_textual_response(description, data, probability):
    prompt = f"{description} Here are the details: {data}. How would you summarize this for a sports betting enthusiast? and the probability of this happening is {probability}"

    try:
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
              {"role": "system", "content": "You are a knowledgeable assistant for sports betting. awnsert in french, be original and concise. awnser like a chatbot. Make the prediction like is our prediction"},
              {"role": "user", "content": prompt}
          ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Failed to generate response: {str(e)}"


@app.route('/')
def home():
    return "Welcome to the Football Match Predictor!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    league = data.get('league')
    team1 = data.get('team1')
    team2 = data.get('team2')
    bet = data.get('bet', "draw")  # Default to 0 if bet is not provided
    if not league or not team1 or not team2:
        return jsonify({"error": "Missing data for league, team1, or team2"}), 400

    prediction = get_match_prediction(league, team1, team2)
    probability = calculate_bet_probability_winner(prediction, bet)
    response_text = generate_textual_response(f"The match prediction between {team1} and {team2} in {league} is:", prediction, probability)
    return jsonify({"prediction": prediction, "ai_response": response_text, "bet_probability": probability})

@app.route('/predict_score', methods=['POST'])
def predict_score():
    data = request.get_json()
    league = data.get('league')
    team1 = data.get('team1')
    team2 = data.get('team2')
    bet = data.get('bet', 0)


    prediction = get_score_prediction(league, team1, team2)
    probability = calculate_bet_probability_score(prediction, bet)
    response_text = generate_textual_response(f"The match prediction between {team1} and {team2} in {league} is:", prediction, probability)
    return jsonify({
        "predicted_score": prediction,
        "bet_probability": probability,
        "ai_response": response_text
    })

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

@app.route('/upcoming_matches', methods=['POST'])
def upcoming_matches():
    data = request.get_json()
    print(data)
    league = data.get('league')
    print(league)
    if not league:
        return jsonify({"error": "Missing data for league"}), 400
    return jsonify(get_upcoming_matches(league))

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

        if team1_stats and team2_stats:
            # Adjust predictions based on point differences
            point_diff = abs(team1_stats[8] - team2_stats[8])  # Points column index)
            home_advantage = 5

            # Adjust based on current form, historical results etc.
            team1_adjusted = team1_stats[-1] + home_advantage - point_diff / 10
            team2_adjusted = team2_stats[-1] - point_diff / 10

            if get_score_prediction(league, team1, team2)["predicted_score"]["team1"] == get_score_prediction(league, team1, team2)["predicted_score"]["team2"]:
                return {"winner": "draw"}
            print(get_score_prediction(league, team1, team2))
            if team1_adjusted > team2_adjusted:
                # return in json prediction winner team1
                return {"winner": team1}
            elif team1_adjusted < team2_adjusted:
                return {"winner": team2}
            else:
                return "This match is likely to be a draw."
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