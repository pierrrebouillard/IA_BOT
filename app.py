from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Football Match Predictor!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    team1 = data['team1']
    team2 = data['team2']
    prediction = get_match_prediction(team1, team2)
    return jsonify(prediction)


@app.route('/predict_sc', methods=['POST'])
def predict_match_score():
    data = request.get_json()
    team1 = data['team1']
    team2 = data['team2']
    return jsonify(get_score_prediction(team1, team2))


def get_score_prediction(team1, team2):
    data = request.get_json()
    team1 = data['team1']
    team2 = data['team2']

    conn = sqlite3.connect('football_stats.db')
    cursor = conn.cursor()
    
    # Get data for both teams
    cursor.execute('SELECT * FROM Premier_League WHERE Team = ?', (team1,))
    team1_stats = cursor.fetchone()
    
    cursor.execute('SELECT * FROM Premier_League WHERE Team = ?', (team2,))
    team2_stats = cursor.fetchone()
    
    conn.close()

    # Example prediction logic using average goals scored and conceded
    if team1_stats and team2_stats:
        # Calculate average goals expected to score
        team1_goals = (team1_stats[5] / team1_stats[1])  # Goals_For / Played
        team2_goals = (team2_stats[5] / team2_stats[1])  # Goals_For / Played

        # Calculate average goals expected to concede
        team1_concede = (team1_stats[6] / team1_stats[1])  # Goals_Against / Played
        team2_concede = (team2_stats[6] / team2_stats[1])  # Goals_Against / Played

        # Simple prediction by averaging expected goals scored and goals conceded by the opponent
        predicted_score_team1 = (team1_goals + team2_concede) / 2
        predicted_score_team2 = (team2_goals + team1_concede) / 2

        return f"Predicted score: {team1} {round(predicted_score_team1)} - {round(predicted_score_team2)} {team2}"
    else:
        return "Insufficient data to predict score."

def get_match_prediction(team1, team2):
    # Connect to SQLite Database
    conn = sqlite3.connect('football_stats.db')
    cursor = conn.cursor()
    
    # Get data for both teams
    cursor.execute('SELECT * FROM Premier_League WHERE Team = ?', (team1,))
    team1_stats = cursor.fetchone()
    
    cursor.execute('SELECT * FROM Premier_League WHERE Team = ?', (team2,))
    team2_stats = cursor.fetchone()
    
    conn.close()

    if team1_stats and team2_stats:
        # Adjust predictions based on point differences
        point_diff = abs(team1_stats[8] - team2_stats[8])  # Points column index

        # Consider home advantage or any other factors
        # Assume +5 advantage points for home team (this is a simplistic assumption)
        home_advantage = 5  # Dummy value, replace with actual logic to determine home team

        # Adjust based on current form, historical results etc.
        team1_adjusted = team1_stats[-1] + home_advantage - point_diff / 10
        team2_adjusted = team2_stats[-1] - point_diff / 10

        if team1_adjusted > team2_adjusted:
            return f"{team1} is more likely to win based on adjusted current form."
        elif team1_adjusted < team2_adjusted:
            return f"{team2} is more likely to win based on adjusted current form."
        else:
            return "This match is likely to be a draw."
    else:
        return "Data not found for one or both teams."

if __name__ == '__main__':
    app.run(debug=True)
