from flask import Flask, request, jsonify
import openai
from openai import OpenAIError
from utils.vector_store import load_vector_store  # Assurez-vous que ce module est accessible
import logging
from flask_cors import CORS

# Configuration du logger
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Autorise les requêtes cross-origin

# 🔑 Récupération de la clé API OpenAI
api_key = ''
if not api_key:
    raise ValueError("❌ Aucune clé API détectée !")
openai.api_key = api_key

CHROMA_DB_PATH = "chroma_db"

def determine_filter(query: str):
    """
    Détermine, à partir de la requête utilisateur, un filtre à appliquer sur la recherche des documents.
    - Si la requête contient "date" et ("prochain" ou "suiv"), on suppose que les informations sur les prochains matchs se trouvent dans la table "match_schedule".
    - Pour les demandes de probabilités de victoire (mots-clés "probabil", "victoire", "match", "score" ou "buteur"), on utilise la table "match_probabilities".
    - Sinon, aucun filtre n'est appliqué.
    """
    query_lower = query.lower()
    if "date" in query_lower and ("prochain" in query_lower or "suiv" in query_lower):
        print("DEBUG: Filtrage sur la table 'match_schedule'")
        return {"table": "match_schedule"}
    elif ("probabil" in query_lower or "score" in query_lower or "buteur" in query_lower) and ("victoire" in query_lower or "match" in query_lower):
        print("DEBUG: Filtrage sur la table 'match_probabilities'")
        return {"table": "match_probabilities"}
    else:
        return None

def extract_team_from_query(query: str):
    """
    Extraction basique du nom d'une équipe depuis la requête.
    Vous pouvez étendre cette fonction avec une liste de noms d'équipes connus ou un traitement NLP plus avancé.
    """
    teams = ["Lille", "Paris", "Marseille", "Lyon", "Monaco", "Bordeaux", "Rennes"]  # Exemple de liste d'équipes
    query_lower = query.lower()
    for team in teams:
        if team.lower() in query_lower:
            return team
    return None

def process_query(query: str):
    # Chargement du vector store existant
    print("Chargement du vector store...")
    try:
        vector_store = load_vector_store()
        print("✅ Vector store chargé.")
    except Exception as e:
        logger.exception("Erreur lors du chargement du vector store")
        return {"error": "Erreur lors du chargement du vector store"}
    
    # Détermine un éventuel filtre basé sur la requête
    metadata_filter = determine_filter(query)

    # Recherche dans le vector store
    try:
        if metadata_filter:
            print("DEBUG: Utilisation du filtre:", metadata_filter)
            search_results = vector_store.similarity_search(query, k=3, filter=metadata_filter)
        else:
            search_results = vector_store.similarity_search(query, k=3)
    except Exception as e:
        logger.exception("Erreur lors de la recherche dans le vector store")
        return {"error": "Erreur lors de la recherche dans le vector store"}

    query_lower = query.lower()
    # Si la requête concerne les matchs à venir (filtre "match_schedule") et mentionne "prochain",
    # tenter d'extraire le nom de l'équipe pour rechercher le prochain match.
    if metadata_filter and metadata_filter.get("table") == "match_schedule" and "prochain" in query_lower:
        team = extract_team_from_query(query)
        if team:
            print(f"DEBUG: Équipe extraite de la requête : {team}")
            match_doc = None
            for doc in search_results:
                if team.lower() in doc.page_content.lower():
                    match_doc = doc
                    break
            if match_doc:
                context = match_doc.page_content
            else:
                error_msg = f"Aucun match à venir trouvé pour l'équipe {team}."
                print("DEBUG:", error_msg)
                return {"error": error_msg}
        else:
            error_msg = "Aucune équipe détectée dans la requête pour rechercher le prochain match."
            print("DEBUG:", error_msg)
            return {"error": error_msg}
    else:
        # Concatène le contenu textuel des documents trouvés
        context = "\n".join([doc.page_content for doc in search_results])
    
    print("DEBUG: Contexte récupéré:")
    print(context)
    
    # Choix du message système en fonction de la requête
    if ("prochain" in query_lower or "suiv" in query_lower) and "date" in query_lower:
        system_message = (
            "Tu es un expert en paris sportifs. Lorsque tu réponds à une question sur les matchs à venir, "
            "fournis la date exacte (jour, mois, année) et l'heure précise du prochain match, ainsi que le nom de l'adversaire si disponible. "
            "Si les données sont insuffisantes, indique clairement quelles informations manquent et donne une estimation par défaut."
        )
    elif metadata_filter and metadata_filter.get("table") == "match_probabilities":
        system_message = (
            "Tu es un expert en paris sportifs. Pour répondre aux questions sur les probabilités de victoire entre deux équipes, "
            "utilise uniquement les informations issues des données suivantes :\n"
            "- Probabilité de victoire de l'équipe 1 (prob_win_team1)\n"
            "- Probabilité de victoire de l'équipe 2 (prob_win_team2)\n"
            "- Score prédit de l'équipe 1 (predicted_score_team1)\n"
            "- Score prédit de l'équipe 2 (predicted_score_team2)\n"
            "- Meilleurs buteurs (top_scorers)\n\n"
            "Présente ces informations de manière claire et structurée. "
            "Si certaines données sont manquantes, indique lesquelles et donne une estimation par défaut (par exemple, 50% pour chaque équipe et 0-0 pour les scores)."
        )
    else:
        system_message = (
            "Tu es un expert en paris sportifs. Réponds uniquement en te basant sur les données fournies ci-dessous, sans utiliser d'informations externes. "
            "Si les données sont insuffisantes, indique clairement quelles informations manquent."
        )
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Voici les données pertinentes trouvées :\n{context}\n\nRequête : {query}"}
    ]
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        chatbot_reply = response.choices[0].message.content
    except OpenAIError as e:
        logger.exception("Erreur OpenAI")
        chatbot_reply = f"Erreur OpenAI: {str(e)}"
    except Exception as ex:
        logger.exception("Erreur inattendue")
        chatbot_reply = f"Erreur: {str(ex)}"
    
    return {"ai_response": chatbot_reply, "context": context}

@app.route("/", methods=["GET"])
def index():
    return "IA Test API is running", 200

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query")
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400
    result = process_query(query)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

