# Ancien import (déprécié ❌)
# from langchain.chat_models import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI

# Nouveau import (✅ Correct)
from langchain_openai import ChatOpenAI
from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import openai_api_key

# Initialiser le modèle OpenAI
llm = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-4o", temperature=0.7)

# Définir le template de prompt
prompt = PromptTemplate(
    input_variables=["team1", "team2", "prob_victoire", "prob_nul", "prob_defaite", "team1_stats", "team2_stats", "recent_matches"],
    template="""
    Voici les informations pour le match entre {team1} et {team2} :

    - Probabilités :
      Victoire {team1} : {prob_victoire:.2f}
      Match nul : {prob_nul:.2f}
      Victoire {team2} : {prob_defaite:.2f}

    - Statistiques de {team1} : {team1_stats}
    - Statistiques de {team2} : {team2_stats}

    - Résultats récents entre les deux équipes : {recent_matches}

    Analyse ces données et donne un conseil amical et professionnel à un utilisateur sur le risque de ce pari.
    """
)

# Créer une chaîne LangChain
def create_analysis_chain(team1, team2, prob_victoire, prob_nul, prob_defaite, team1_stats, team2_stats, recent_matches):
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(team1=team1, team2=team2, prob_victoire=prob_victoire, prob_nul=prob_nul, prob_defaite=prob_defaite, team1_stats=team1_stats, team2_stats=team2_stats, recent_matches=recent_matches)