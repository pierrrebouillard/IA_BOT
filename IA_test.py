import os
import openai
from openai import OpenAIError
from utils.vector_store import load_vector_store  # Assurez-vous que ce module est accessible
import logging

# Configuration du logger pour afficher les messages dans la console
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# 🔑 Récupération de la clé API OpenAI
# Remplacez par votre clé ou assurez-vous qu'elle est définie dans vos variables d'environnement
api_key = ''
if not api_key:
    raise ValueError("❌ Aucune clé API détectée !")
openai.api_key = api_key

# Chemin du vector store (doit être identique à celui utilisé lors de la création)
CHROMA_DB_PATH = "chroma_db"

def determine_filter(query: str):
    """
    Détermine, à partir de la requête utilisateur, un filtre à appliquer sur la recherche des documents.
    Par exemple, si la requête contient "date" et "prochain" (ou "suiv"), on suppose que les informations
    sur les prochains matchs se trouvent dans la table "match_schedule". Si la requête contient "score",
    on suppose que les scores se trouvent dans la table "match_scores".
    """
    query_lower = query.lower()
    if "date" in query_lower and ("prochain" in query_lower or "suiv" in query_lower):
        print("DEBUG: Filtrage sur la table 'match_schedule'")
        return {"table": "match_schedule"}
    elif "score" in query_lower:
        print("DEBUG: Filtrage sur la table 'match_scores'")
        return {"table": "match_scores"}
    else:
        return None

def main():
    # Chargement du vector store existant
    print("Chargement du vector store...")
    try:
        vector_store = load_vector_store()
        print("✅ Vector store chargé.")
    except Exception as e:
        print("Erreur lors du chargement du vector store:", e)
        logger.exception("Erreur lors du chargement du vector store")
        return

    print("\n=== Chatbot interactif ===")
    print("Tapez 'exit' ou 'quit' pour quitter.\n")

    while True:
        # Saisie de l'utilisateur
        user_input = input("📝 Tapez votre question: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Arrêt du chatbot.")
            break

        # Détermine un éventuel filtre basé sur la requête
        metadata_filter = determine_filter(user_input)

        try:
            # Recherche par similarité dans le vector store avec éventuellement un filtre sur les métadonnées
            if metadata_filter:
                print("DEBUG: Utilisation du filtre:", metadata_filter)
                search_results = vector_store.similarity_search(user_input, k=3, filter=metadata_filter)
            else:
                search_results = vector_store.similarity_search(user_input, k=3)
            
            # Concatène le contenu textuel des documents trouvés
            context = "\n".join([doc.page_content for doc in search_results])
            print("DEBUG: Contexte récupéré :")
            print(context)
            
            # Préparation du prompt pour OpenAI
            messages = [
                {
                    "role": "system",
                    "content": (
                        "Tu es un expert en paris sportifs. "
                        "Réponds uniquement en te basant sur les données fournies ci-dessous, sans utiliser d'informations externes. "
                        "Si les données sont insuffisantes, indique-le clairement."
                    )
                },
                {
                    "role": "user",
                    "content": f"Voici les données pertinentes trouvées :\n{context}\n\nRequête : {user_input}"
                }
            ]
            
            # Appel à l'API OpenAI via ChatCompletion 
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            chatbot_reply = response.choices[0].message.content
            print("\n🤖 Chatbot :")
            print(chatbot_reply)
        except OpenAIError as e:
            print("Erreur OpenAI :", str(e))
        except Exception as ex:
            print("Erreur :", str(ex))
        print("\n" + "-" * 50 + "\n")

if __name__ == "__main__":
    main()

