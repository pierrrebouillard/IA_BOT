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
# Pour la production, remplacez cette clé en dur par une variable d'environnement.
api_key = ''
if not api_key:
    raise ValueError("❌ Aucune clé API détectée. Vérifie que `OPENAI_API_KEY` est bien défini.")

# ✅ Initialisation du modèle d'embedding (OpenAI via LangChain)
embeddings_model = OpenAIEmbeddings(openai_api_key=api_key)

# 📂 Chemin de persistance du vector store Chroma
CHROMA_DB_PATH = "chroma_db"

def create_vector_store():
    """
    Génère une base vectorielle ChromaDB à partir des tables SQLite,
    en créant pour chaque ligne une représentation textuelle structurée et en y associant des métadonnées.
    """
    print("🚀 Début de la création du vector store...")

    # Connexion à la base SQLite
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Récupération des noms de toutes les tables de la base
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📌 Tables détectées : {tables}")

        # Liste pour stocker les documents à vectoriser
        documents = []

        # Initialisation du vector store Chroma
        vector_store = Chroma(embedding_function=embeddings_model, persist_directory=CHROMA_DB_PATH)

        # Pour chaque table, extraire les données et créer des documents
        for table in tables:
            print(f"📡 Traitement de la table : {table}")

            # Récupération des informations des colonnes avec PRAGMA
            cursor.execute(f"PRAGMA table_info({table})")
            columns_info = cursor.fetchall()
            column_names = [col[1] for col in columns_info]  # On récupère uniquement les noms des colonnes

            if not column_names:
                print(f"⚠️ Impossible de récupérer les colonnes de `{table}`. Skipping...")
                continue

            print(f"📊 Colonnes détectées pour `{table}`: {column_names}")

            # Récupération de toutes les lignes de la table
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()

            if not rows:
                print(f"⚠️ La table `{table}` est vide. Aucun embedding généré.")
                continue

            # Pour chaque ligne, construire une représentation textuelle structurée
            for row in rows:
                # Association des colonnes aux valeurs sous forme de dictionnaire
                row_data = {col_name: value for col_name, value in zip(column_names, row)}
                # Création d'une représentation multi-lignes
                text_lines = [f"Table: {table}", "-" * (len(table) + 7)]
                for col in column_names:
                    text_lines.append(f"{col}: {row_data[col]}")
                text_data = "\n".join(text_lines)
                
                # Enrichissement avec des métadonnées pour conserver la structure
                metadata = {
                    "table": table,
                    "columns": column_names,
                    "raw_row": row_data
                }
                
                # Création du document avec le texte et les métadonnées
                doc = Document(page_content=text_data, metadata=metadata)
                documents.append(doc)
                print(f"📝 Ajout du document : {doc}")

        # Ajout des documents (embeddings) dans le vector store Chroma
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
