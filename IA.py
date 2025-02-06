import os
# Désactivation de la télémétrie de Chroma
os.environ["CHROMA_DISABLE_TELEMETRY"] = "true"
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"

import streamlit as st
import openai
from openai import OpenAIError
from utils.vector_store import create_vector_store, load_vector_store
import logging
import time

# Configuration du logger pour afficher les messages dans la console
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    force=True  # Forcer la configuration même s'il y a d'autres configurations
)
logger = logging.getLogger(__name__)

# 🔑 Récupération de la clé API OpenAI
api_key = ''
if not api_key:
    st.error("❌ Aucune clé API OpenAI détectée ! Vérifiez vos variables d'environnement.")
    st.stop()

# Configuration de l'API OpenAI
openai.api_key = api_key

# Configuration de la page Streamlit
st.set_page_config(page_title="Paris Sportifs Chatbot", page_icon="⚽")
st.title("🎰 Chatbot de Paris Sportifs")
st.write("Pose une question et je te dirai si c'est risqué !")
st.write("Chemin courant :", os.getcwd())

# ====================================================================
# Pour diagnostiquer le problème, nous supprimons temporairement le cache.
# Ainsi, get_vector_store() sera exécuté à chaque fois, sans st.cache_resource.
# ====================================================================

def get_vector_store():
    st.write("DEBUG: Début de get_vector_store()")
    logger.debug("DEBUG: Début de get_vector_store()")
    
    if not os.path.exists("chroma_db"):
        st.write("DEBUG: Le dossier 'chroma_db' n'existe pas. Appel à create_vector_store()...")
        logger.debug("DEBUG: Le dossier 'chroma_db' n'existe pas. Appel à create_vector_store()...")
        create_vector_store()
        st.write("DEBUG: create_vector_store() terminé.")
        logger.debug("DEBUG: create_vector_store() terminé.")
    else:
        st.write("DEBUG: Le dossier 'chroma_db' existe.")
        logger.debug("DEBUG: Le dossier 'chroma_db' existe.")
    
    st.write("DEBUG: Appel de load_vector_store()...")
    logger.debug("DEBUG: Appel de load_vector_store()...")
    start_time = time.time()
    vs = load_vector_store()
    elapsed = time.time() - start_time
    st.write("DEBUG: load_vector_store() a retourné :", vs, "après", elapsed, "secondes")
    logger.debug("DEBUG: load_vector_store() a retourné : %s après %s secondes", vs, elapsed)
    return vs

with st.spinner("📡 Chargement de ChromaDB..."):
    try:
        vector_store = get_vector_store()
        st.success("✅ ChromaDB chargée et prête à l'emploi !")
    except Exception as e:
        st.error(f"⚠️ Erreur lors du chargement de ChromaDB : {str(e)}")
        logger.exception("Erreur lors du chargement de ChromaDB :")
        st.stop()

st.write("DEBUG: Vector store chargé. Affichage du champ de saisie.")

# Champ de saisie utilisateur
user_input = st.text_input("📝 Tape ton pari ici :")
st.write("DEBUG: Champ de saisie affiché. Valeur actuelle :", user_input)

# Bouton pour lancer l'analyse
if st.button("🚀 Analyser le Risque"):
    if user_input:
        try:
            # Recherche dans ChromaDB pour enrichir le contexte
            search_results = vector_store.similarity_search(user_input, k=3)
            context = "\n".join([doc.page_content for doc in search_results])
            st.write("DEBUG: Contexte récupéré :", context)
            
            # Préparation du prompt pour OpenAI
            messages = [
                {"role": "system", "content": "Tu es un expert en paris sportifs. Analyse les risques du pari."},
                {"role": "user", "content": f"Voici les données pertinentes trouvées :\n{context}\n\nPari : {user_input}"}
            ]
            
            # Appel à l'API OpenAI via ChatCompletion
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            
            # Récupération et affichage de la réponse
            chatbot_reply = response.choices[0].message.content
            st.write("🤖 **Chatbot :**", chatbot_reply)
        except OpenAIError as e:
            st.error(f"⚠️ Erreur OpenAI : {str(e)}")
            logger.exception("Erreur lors de l'appel à OpenAI :")
    else:
        st.warning("❌ Merci d'entrer un message avant d'envoyer.")
