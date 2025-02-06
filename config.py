import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Clés API
openai_api_key = os.getenv("OPENAI_API_KEY")
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")

# Paramètres LangSmith
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = langsmith_api_key