import sqlite3
from utils.database import get_db_connection
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# 🔑 Récupération sécurisée de la clé API OpenAI
api_key = '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'
if not api_key:
    raise ValueError("❌ Aucune clé API détectée. Vérifie que tu as bien défini `OPENAI_API_KEY`.")

# ✅ Création du modèle d'embedding avec LangChain
embeddings_model = OpenAIEmbeddings(openai_api_key=api_key)

def generate_table_embeddings():
    """
    Génère des embeddings à partir des tables SQLite et stocke les vecteurs avec FAISS.
    """
    print("🚀 Début de la génération des embeddings...")

    # ✅ Ouvre une connexion temporaire
    conn = get_db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]

        print(f"📌 Tables détectées : {tables}")

        # Liste pour stocker les données vectorisées
        documents = []

        # 🔥 Génération des embeddings pour chaque table
        for table in tables:
            print(f"📡 Génération des embeddings pour la table : {table}")

            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()

            if not rows:
                print(f"⚠️ La table `{table}` est vide. Aucun embedding généré.")
                continue

            # 🔹 Conversion des données en texte lisible pour LangChain
            table_data_as_string = "\n".join([", ".join(map(str, row)) for row in rows])

            # Ajout de la donnée sous forme de document LangChain
            documents.append(table_data_as_string)

        if documents:
            # ✅ Création des embeddings avec LangChain
            print("🔍 Création des embeddings vectoriels avec LangChain...")
            vectorstore = FAISS.from_texts(documents, embeddings_model)
            
            # ✅ Sauvegarde du store FAISS
            vectorstore.save_local("faiss_index")
            print("✅ Embeddings sauvegardés avec succès dans FAISS.")

    except sqlite3.OperationalError as e:
        print(f"❌ Erreur SQLite : {e}")

    finally:
        cursor.close()  # ✅ Ferme le curseur
        conn.close()  # ✅ Ferme la connexion immédiatement
        print("✅ Connexion SQLite fermée après génération des embeddings.")
