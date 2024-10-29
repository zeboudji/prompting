import streamlit as st
import pandas as pd
import numpy as np
from math import pi
import plotly.express as px

# Application Title
st.title("Évaluation des Compétences pour le Prompting IA")

# Introduction Section
st.write("Bienvenue dans cet outil d'évaluation de vos compétences en prompting IA et en techniques agiles d'expression des besoins !")
st.write("À travers quelques questions simples, nous allons explorer vos capacités et visualiser votre profil de compétences.")

# Questions Guided Section
st.header("Questions Guidées")

# Initial Familiarity Question
st.subheader("1. Familiarité avec le Prompting et l'Agilité")
familiarity = st.radio(
    "Quel est votre niveau de familiarité avec l’écriture de prompts pour l’IA ?",
    ("Débutant(e)", "Intermédiaire", "Avancé(e)")
)

if familiarity == "Débutant(e)":
    st.write("Pas de souci ! Nous allons vous guider à chaque étape.")
elif familiarity == "Intermédiaire":
    st.write("Super, vous avez déjà quelques bases !")
else:
    st.write("Excellent ! Vous êtes prêt(e) à approfondir vos compétences.")

# Experience with Agile Concepts
st.subheader("2. Expérience avec les Techniques d'Expression de Besoin Agile")
experience_agile = st.radio(
    "Utilisez-vous déjà des techniques d’expression de besoin comme les User Stories ou les Epics ?",
    ("Oui", "Non, mais curieux(se) d’en apprendre plus", "Pas familier(e) avec ces termes")
)

if experience_agile == "Oui":
    st.write("Génial ! Vous verrez rapidement les similitudes avec le prompting IA.")
elif experience_agile == "Non, mais curieux(se) d’en apprendre plus":
    st.write("Pas de problème, vous découvrirez comment ces techniques peuvent améliorer vos prompts.")
else:
    st.write("Pas de souci, nous allons rendre cela accessible et simple.")

# Specific Skill Assessment
st.subheader("3. Capacité à Exprimer des Besoins Clairs")
clarity = st.selectbox(
    "Comment définiriez-vous votre capacité à exprimer des besoins clairs et spécifiques pour une tâche ?",
    [
        "Très clair et structuré",
        "Clair, mais manque parfois de détails",
        "Besoin d’amélioration"
    ]
)

if clarity == "Très clair et structuré":
    st.write("Exemple : 'Je sais donner des consignes précises, même pour des tâches complexes.'")
elif clarity == "Clair, mais manque parfois de détails":
    st.write("Exemple : 'Je donne souvent les grandes lignes, mais oublie des informations.'")
else:
    st.write("Exemple : 'Je trouve parfois difficile de décrire ce que j’attends.'")

# Question about Task Breakdown
st.subheader("4. Capacité à Diviser une Tâche")
task_division = st.radio(
    "Savez-vous diviser une tâche en plusieurs étapes pour aider l’IA à répondre plus précisément ?",
    ["Oui, j’utilise cette approche régulièrement", "J’ai quelques idées, mais je pourrais m’améliorer", "Non, je ne suis pas sûr(e) de comment faire"]
)

if task_division == "Oui, j’utilise cette approche régulièrement":
    st.write("Bravo ! Cette approche est essentielle pour un prompting optimal.")
elif task_division == "J’ai quelques idées, mais je pourrais m’améliorer":
    st.write("Pas de souci, nous allons voir comment renforcer cette compétence.")
else:
    st.write("Nous allons découvrir comment cette technique peut rendre vos prompts plus efficaces.")

# Radar Chart Data Preparation
st.header("Visualisation des Compétences en Prompting IA")

# Mapping answers to a score for radar chart
competence_scores = {
    "Familiarité": 1 if familiarity == "Débutant(e)" else (2 if familiarity == "Intermédiaire" else 3),
    "Expérience Agile": 1 if experience_agile == "Pas familier(e) avec ces termes" else (2 if experience_agile == "Non, mais curieux(se) d’en apprendre plus" else 3),
    "Clarté": 1 if clarity == "Besoin d’amélioration" else (2 if clarity == "Clair, mais manque parfois de détails" else 3),
    "Diviser une Tâche": 1 if task_division == "Non, je ne suis pas sûr(e) de comment faire" else (2 if task_division == "J’ai quelques idées, mais je pourrais m’améliorer" else 3)
}

# DataFrame for Radar Chart
df = pd.DataFrame(dict(
    competence=list(competence_scores.keys()),
    score=list(competence_scores.values())
))
categories = list(df['competence'])
fig = px.line_polar(df, r='score', theta='competence', line_close=True)
fig.update_traces(fill='toself')
fig.update_layout(title="Votre Radar de Compétences en Prompting IA")

# Display Radar Chart
st.plotly_chart(fig)

# Final Feedback
st.write("Merci d'avoir répondu à ces questions ! Voici votre profil de compétences en prompting IA. Utilisez ce radar pour identifier les points à améliorer et devenir un(e) prompteur(se) IA encore plus efficace.")

