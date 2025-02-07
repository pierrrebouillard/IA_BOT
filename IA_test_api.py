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
    - Si la requête contient "score", on suppose que les scores se trouvent dans la table "match_scores".
    - Si la requête contient "probabil" et ("victoire" ou "match"), on suppose qu'il s'agit d'une demande de probabilités de victoire et on renvoie la table "match_probabilities".
    """
    query_lower = query.lower()
    if "date" in query_lower and ("prochain" in query_lower or "suiv" in query_lower):
        print("DEBUG: Filtrage sur la table 'match_schedule'")
        return {"table": "match_schedule"}
    elif "score" in query_lower:
        print("DEBUG: Filtrage sur la table 'match_scores'")
        return {"table": "match_scores"}
    elif "probabil" in query_lower and ("victoire" in query_lower or "match" in query_lower):
        print("DEBUG: Filtrage sur la table 'match_probabilities'")
        return {"table": "match_probabilities"}
    else:
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

    try:
        if metadata_filter:
            print("DEBUG: Utilisation du filtre:", metadata_filter)
            search_results = vector_store.similarity_search(query, k=3, filter=metadata_filter)
        else:
            search_results = vector_store.similarity_search(query, k=3)
    except Exception as e:
        logger.exception("Erreur lors de la recherche dans le vector store")
        return {"error": "Erreur lors de la recherche dans le vector store"}

    # Concatène le contenu textuel des documents trouvés
    context = "\n".join([doc.page_content for doc in search_results])
    print("DEBUG: Contexte récupéré:")
    print(context)
    
    # Préparation du prompt pour OpenAI.
    # La consigne précise maintenant d'inclure des dates précises et, pour les demandes de probabilités, d'indiquer les probabilités.
    messages = [
        {
          "role": "system",
          "content": (
              "Tu es un expert en paris sportifs. Lorsque tu réponds, indique toujours précisément la date et l'heure du prochain match concerné, "
              "ou les probabilités de victoire si la requête concerne les match probabilities. "
              "Réponds uniquement en te basant sur les données fournies ci-dessous, sans utiliser d'informations externes. "
              "Si les données sont insuffisantes, indique clairement quelles informations manquent."
          )
        },
        {
          "role": "user",
          "content": f"Voici les données pertinentes trouvées :\n{context}\n\nRequête : {query}"
        }
    ]
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
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
