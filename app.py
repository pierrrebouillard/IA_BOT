# from flask import Flask, request, jsonify
# import sqlite3

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return "Welcome to the Football Match Predictor!"

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json()
#     team1 = data['team1']
#     team2 = data['team2']
#     prediction = get_match_prediction(team1, team2)
#     return jsonify(prediction)


# @app.route('/predict_sc', methods=['POST'])
# def predict_match_score():
#     data = request.get_json()
#     team1 = data['team1']
#     team2 = data['team2']
#     return jsonify(get_score_prediction(team1, team2))


# def get_score_prediction(team1, team2):
#     data = request.get_json()
#     team1 = data['team1']
#     team2 = data['team2']

#     conn = sqlite3.connect('football_stats.db')
#     cursor = conn.cursor()
    
#     # Get data for both teams
#     cursor.execute('SELECT * FROM Premier_League WHERE Team = ?', (team1,))
#     team1_stats = cursor.fetchone()
    
#     cursor.execute('SELECT * FROM Premier_League WHERE Team = ?', (team2,))
#     team2_stats = cursor.fetchone()
    
#     conn.close()

#     # Example prediction logic using average goals scored and conceded
#     if team1_stats and team2_stats:
#         # Calculate average goals expected to score
#         team1_goals = (team1_stats[5] / team1_stats[1])  # Goals_For / Played
#         team2_goals = (team2_stats[5] / team2_stats[1])  # Goals_For / Played

#         # Calculate average goals expected to concede
#         team1_concede = (team1_stats[6] / team1_stats[1])  # Goals_Against / Played
#         team2_concede = (team2_stats[6] / team2_stats[1])  # Goals_Against / Played

#         # Simple prediction by averaging expected goals scored and goals conceded by the opponent
#         predicted_score_team1 = (team1_goals + team2_concede) / 2
#         predicted_score_team2 = (team2_goals + team1_concede) / 2

#         return f"Predicted score: {team1} {round(predicted_score_team1)} - {round(predicted_score_team2)} {team2}"
#     else:
#         return "Insufficient data to predict score."

# def get_match_prediction(team1, team2):
#     # Connect to SQLite Database
#     conn = sqlite3.connect('football_stats.db')
#     cursor = conn.cursor()
    
#     # Get data for both teams
#     cursor.execute('SELECT * FROM Premier_League WHERE Team = ?', (team1,))
#     team1_stats = cursor.fetchone()
    
#     cursor.execute('SELECT * FROM Premier_League WHERE Team = ?', (team2,))
#     team2_stats = cursor.fetchone()
    
#     conn.close()

#     if team1_stats and team2_stats:
#         # Adjust predictions based on point differences
#         point_diff = abs(team1_stats[8] - team2_stats[8])  # Points column index


#         # Consider home advantage or any other factors
#         # Assume +5 advantage points for home team (this is a simplistic assumption)
#         home_advantage = 5  # Dummy value, replace with actual logic to determine home team

#         # Adjust based on current form, historical results etc.
#         team1_adjusted = team1_stats[-1] + home_advantage - point_diff / 10
#         team2_adjusted = team2_stats[-1] - point_diff / 10

#         if team1_adjusted > team2_adjusted:
#             return f"{team1} is more likely to win based on adjusted current form."
#         elif team1_adjusted < team2_adjusted:
#             return f"{team2} is more likely to win based on adjusted current form."
#         else:
#             return "This match is likely to be a draw."
#     else:
#         return "Data not found for one or both teams."

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
import sqlite3
import json
import openai
import torch
from transformers import GPTNeoForCausalLM, GPT2Tokenizer

model_name = "EleutherAI/gpt-neo-2.7B"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPTNeoForCausalLM.from_pretrained(model_name)

app = Flask(__name__)

# def generate_response(prompt):
#     inputs = tokenizer(prompt, return_tensors="pt")
#     with torch.no_grad():
#         outputs = model.generate(**inputs, max_length=100, num_return_sequences=1)
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return response

# @app.route('/generate-text', methods=['POST'])
# def generate_text():
#     data = request.get_json()
#     prompt = data.get('prompt', '')
#     response = generate_response(prompt)
#     return jsonify({'response': response})

def generate_response(prompt):
    print(f"Received prompt: {prompt}")  # Debug: Print the input prompt
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=150, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Generated response: {response}")  # Debug: Print the generated response
    return response


@app.route('/')
def home():
    return "Welcome to the Football Match Predictor!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    league = data.get('league')
    team1 = data.get('team1')
    team2 = data.get('team2')
    if not league or not team1 or not team2:
        return jsonify({"error": "Missing data for league, team1, or team2"}), 400

    # prediction = get_match_prediction(league, team1, team2)
    # # Generate a response that includes the prediction
    # response_text = generate_textual_response(f"The match prediction between {team1} and {team2} in {league} is:", prediction)
    
    score_prediction = get_score_prediction(league, team1, team2)
    print(prompt)
    ai_response = generate_response(prompt)
    return jsonify({"score_prediction": score_prediction, "ai_response": ai_response})

    
    return jsonify({"prediction": prediction, "ai_response": response_text})

@app.route('/predict_score', methods=['POST'])
def predict_score():
    data = request.get_json()
    league = data.get('league')
    team1 = data.get('team1')
    team2 = data.get('team2')
    if not league or not team1 or not team2:
        return jsonify({"error": "Missing data for league, team1, or team2"}), 400
    return jsonify(get_score_prediction(league, team1, team2))

@app.route('/predict_goal', methods=['POST'])
def predict_goal():
    data = request.get_json()
    league = data.get('league')
    team1 = data.get('team1')
    team2 = data.get('team2')
    if not league or not team1 or not team2:
        return jsonify({"error": "Missing data for league, team1, or team2"}), 400
    return jsonify(get_total_goals(league, team1, team2))

@app.route('/upcoming_matches', methods=['GET'])
def upcoming_matches():
    data = request.get_json() 
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
                #make draw prediction
                return f"This match is likely to be a draw."
            print(get_score_prediction(league, team1, team2))
            if team1_adjusted > team2_adjusted:
                # return in json prediction winner team1
                return f"{team1} is likely to win against {team2}."
            elif team1_adjusted < team2_adjusted:
                return f"{team2} is likely to win against {team1}."
            else:
                return "This match is likely to be a draw."
        else:
            return "Data not found for one or both teams."
    finally:
        conn.close()

# Set up your OpenAI API key
openai.api_key = 'your-api-key-here'

def generate_textual_response(input_text):
    try:
        response = openai.Completion.create(
          engine="davinci",  # You can choose other models based on performance needs
          prompt=input_text,
          max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Failed to generate response: {str(e)}"


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
            # Calculate average goals expected to score
            team1_goals = (team1_stats[5] / team1_stats[1])
            team2_goals = (team2_stats[5] / team2_stats[1])

            # Calculate average goals expected to concede
            team1_concede = (team1_stats[6] / team1_stats[1])
            team2_concede = (team2_stats[6] / team2_stats[1])

            # Simple prediction by averaging expected goals scored and goals conceded by the opponent
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
        #return the 10 next matches
        return match_list[:10]
    finally:
        conn.close()

openai.api_key = 'your-api-key-here'

def generate_textual_response(description, data):
    # Create a prompt that includes the result or data and asks for a conversational response
    prompt = f"{description} Here are the details: {data}. How would you summarize this for a sports betting enthusiast?"
    
    try:
        response = openai.Completion.create(
          engine="davinci",
          prompt=prompt,
          max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Failed to generate response: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
