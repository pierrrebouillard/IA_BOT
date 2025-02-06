try:
    from utils.database import get_db_connection  # Cas normal avec Streamlit et imports classiques
except ModuleNotFoundError:
    import sys
    import os

    sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # Ajoute utils au chemin Python
    from database import get_db_connection  # Cas d'exécution directe (ex: `python vector_store.py`)

import sqlite3
import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document

print("✅ utils.vector_store importé avec succès !")

# 🔑 Récupération sécurisée de la clé API OpenAI
# Remplace cette clé en dur par une variable d'environnement si nécessaire.
api_key = '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'
if not api_key:
    raise ValueError("❌ Aucune clé API détectée. Vérifie que `OPENAI_API_KEY` est bien défini.")

# ✅ Modèle d'embedding LangChain (OpenAI)
embeddings_model = OpenAIEmbeddings(openai_api_key=api_key)

# 📂 Chemin du VectorStore Chroma
CHROMA_DB_PATH = "chroma_db"

def create_vector_store():
    """
    Génère une base vectorielle ChromaDB à partir des tables SQLite.
    """
    print("🚀 Début de la création du vector store...")

    # ✅ Connexion SQLite
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # 🔥 Récupération des noms de tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📌 Tables détectées : {tables}")

        # 📌 Liste pour stocker les documents vectorisés
        documents = []

        # ✅ Initialisation de ChromaDB
        vector_store = Chroma(embedding_function=embeddings_model, persist_directory=CHROMA_DB_PATH)

        # 🔥 Extraction des données de chaque table avec contexte des colonnes
        for table in tables:
            print(f"📡 Traitement de la table : {table}")

            # ✅ Récupération des noms de colonnes
            cursor.execute(f"PRAGMA table_info({table})")
            columns_info = cursor.fetchall()
            column_names = [col[1] for col in columns_info]  # Récupérer seulement les noms des colonnes

            if not column_names:
                print(f"⚠️ Impossible de récupérer les colonnes de `{table}`. Skipping...")
                continue

            print(f"📊 Colonnes détectées pour `{table}`: {column_names}")

            # ✅ Récupération des données de la table
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()

            if not rows:
                print(f"⚠️ La table `{table}` est vide. Aucun embedding généré.")
                continue

            # 🔹 Conversion des données en texte structuré avec noms de colonnes
            for row in rows:
                row_data = {col_name: value for col_name, value in zip(column_names, row)}
                text_data = " | ".join([f"{col}: {val}" for col, val in row_data.items()])

                # ✅ Création du document avec contexte enrichi
                doc = Document(page_content=text_data, metadata={"table": table})
                documents.append(doc)
                print(f"📝 Ajout du document : {doc}")

        # ✅ Ajout des documents à ChromaDB
        if documents:
            print("🔍 Ajout des embeddings enrichis dans ChromaDB...")
            vector_store.add_documents(documents)
            print(f"✅ Embeddings sauvegardés dans `{CHROMA_DB_PATH}`.")

    print("✅ Fin de la création du vector store.")

def load_vector_store():
    """
    Charge le vector store existant depuis le dossier persistant.
    """
    vector_store = Chroma(embedding_function=embeddings_model, persist_directory=CHROMA_DB_PATH)
    return vector_store

if __name__ == "__main__":
    create_vector_store()
