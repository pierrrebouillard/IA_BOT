from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
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
        cursor.execute('INSERT INTO Users (username, password, token) VALUES (?, ?, ?)', (username, hashed_password, token))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400
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

def calculate_bet_probability_score(prediction, bet):
    g_team1 = prediction['predicted_score']['team1']
    g_team2 = prediction['predicted_score']['team2']

    numbers = bet.split('-')

    num1 = int(numbers[0])
    num2 = int(numbers[1])

    if g_team1 == num1 and g_team2 == num2:
        probability = 81
    elif g_team1 - num1 == 1 or g_team2 - num2 == 1 or g_team1 - num1 == -1 or g_team2 - num2 == -1:
        probability = 49  # 50% chance of winning the bet if predicted goals match the bet exactly
    elif g_team1 - num1 == 2 or g_team2 - num2 == 2 or g_team1 - num1 == -2 or g_team2 - num2 == -2:
        probability = 18
    elif g_team1 - num1 == 3 or g_team2 - num2 == 3 or g_team1 - num1 == -3 or g_team2 - num2 == -3:
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
    elif predicted_total_goals - bet == 1 or predicted_total_goals - bet == -1:
        probability = 49  # 50% chance of winning the bet if predicted goals match the bet exactly
    elif predicted_total_goals - bet == 2 or predicted_total_goals - bet == -2:
        probability = 18
    elif predicted_total_goals - bet == 3 or predicted_total_goals - bet == -3:
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
            return "Data not found for one or both teams."
    finally:
        conn.close()

def get_total_goals(league, team1, team2):
    try:
        score = get_score_prediction(league, team1, team2)

        total_goals = score["predicted_score"]["team1"] + score["predicted_score"]["team2"]
        json = {
            "total_goals": total_goals
        }
        return json
    except:
        return {"error": "Error in prediction"}

def get_score_prediction(league, team1, team2):
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
            team1_goals = (team1_stats[5] / team1_stats[1])
            team2_goals = (team2_stats[5] / team2_stats[1])

            team1_concede = (team1_stats[6] / team1_stats[1])
            team2_concede = (team2_stats[6] / team2_stats[1])

            predicted_score_team1 = ((team1_goals + team2_concede) / 2) + 0.3
            predicted_score_team2 = ((team2_goals + team1_concede) / 2) - 0.3

            print(predicted_score_team1)
            print(predicted_score_team2)

            json = {
                "predicted_score": {
                    "team1": round(predicted_score_team1),
                    "team2": round(predicted_score_team2)
                }
            }
            return json
        else:
            return "Insufficient data to predict score."
    finally:
        conn.close()

def get_upcoming_matches(league):
    try:
        conn = sqlite3.connect('football_stats.db')
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {league}_matches_Upcoming')
        print('SELECT * FROM ' + league + '_matches_Upcoming')
        matches = cursor.fetchall()
        match_list = []
        for match in matches:
            match_list.append({
                "home_team": match[4],
                "away_team": match[5],
                "date": match[3]
            })
        return match_list[:10]
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)
