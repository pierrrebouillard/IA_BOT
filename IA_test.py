import os
import openai
from openai import OpenAIError
from utils.vector_store import create_vector_store, load_vector_store

# Désactivation de la télémétrie de Chroma (facultatif)
os.environ["CHROMA_DISABLE_TELEMETRY"] = "true"
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"

# Récupération de la clé API OpenAI (remplacez-la par votre clé ou utilisez une variable d'environnement)
api_key = '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'
if not api_key:
    raise ValueError("Aucune clé API détectée !")
openai.api_key = api_key

def main():
    # Vérifier l'existence du dossier de la base vectorielle
    if not os.path.exists("chroma_db"):
        print("Le dossier 'chroma_db' n'existe pas. Création de la base vectorielle...")
        create_vector_store()
        print("Base vectorielle créée.")
    else:
        print("Le dossier 'chroma_db' existe déjà.")
    
    # Charger le vector store
    print("Chargement du vector store...")
    vector_store = load_vector_store()
    print("Vector store chargé :", vector_store)
    
    print("\n=== Test du chatbot ===")
    print("Entrez 'exit' pour quitter.\n")
    
    while True:
        # Saisie de l'utilisateur dans le terminal
        user_input = input("📝 Tape ton pari ici : ")
        if user_input.lower() in ['exit', 'quit']:
            print("Arrêt du chatbot.")
            break
        
        try:
            # Recherche de similarités dans le vector store pour enrichir le contexte
            search_results = vector_store.similarity_search(user_input, k=3)
            context = "\n".join([doc.page_content for doc in search_results])
            print("\nContexte récupéré :")
            print(context)
            
            # Préparation du prompt pour OpenAI
            messages = [
                {"role": "system", "content": "Tu es un expert en paris sportifs. Analyse les risques du pari."},
                {"role": "user", "content": f"Voici les données pertinentes trouvées :\n{context}\n\nPari : {user_input}"}
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
