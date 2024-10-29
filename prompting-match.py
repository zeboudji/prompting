import streamlit as st
import pandas as pd
import numpy as np
from math import pi
import plotly.express as px
import time

# App Title
st.title("Évaluation Interactive des Compétences en Prompting IA")

# State management
if "question_number" not in st.session_state:
    st.session_state["question_number"] = 1

# Define questions and responses
questions = [
    ("Quel est votre niveau de familiarité avec l’écriture de prompts pour l’IA ?",
     ["Débutant(e)", "Intermédiaire", "Avancé(e)"]),
    ("Utilisez-vous déjà des techniques d’expression de besoin comme les User Stories ou les Epics ?",
     ["Oui", "Non, mais curieux(se) d’en apprendre plus", "Pas familier(e) avec ces termes"]),
    ("Comment définiriez-vous votre capacité à exprimer des besoins clairs et spécifiques pour une tâche ?",
     ["Très clair et structuré", "Clair, mais manque parfois de détails", "Besoin d’amélioration"]),
    ("Savez-vous diviser une tâche en plusieurs étapes pour aider l’IA à répondre plus précisément ?",
     ["Oui, j’utilise cette approche régulièrement", "J’ai quelques idées, mais je pourrais m’améliorer", "Non, je ne suis pas sûr(e) de comment faire"])
]

# Mapping responses to a numeric score
responses_scores = {
    "Débutant(e)": 1, "Intermédiaire": 2, "Avancé(e)": 3,
    "Pas familier(e) avec ces termes": 1, "Non, mais curieux(se) d’en apprendre plus": 2, "Oui": 3,
    "Besoin d’amélioration": 1, "Clair, mais manque parfois de détails": 2, "Très clair et structuré": 3,
    "Non, je ne suis pas sûr(e) de comment faire": 1, "J’ai quelques idées, mais je pourrais m’améliorer": 2, "Oui, j’utilise cette approche régulièrement": 3
}

# Display the current question
question_text, choices = questions[st.session_state["question_number"] - 1]
response = st.radio(question_text, choices, key=f"question_{st.session_state['question_number']}")

# Move to next question automatically when answered
if response:
    st.session_state[f"response_{st.session_state['question_number']}"] = response
    time.sleep(1)  # Adding a delay to simulate a smooth transition
    st.session_state["question_number"] += 1

# When all questions are answered, show results
if st.session_state["question_number"] > len(questions):
    # Calculate scores for the radar chart
    competence_scores = {
        "Familiarité": responses_scores[st.session_state.get("response_1", "Débutant(e)")],
        "Expérience Agile": responses_scores[st.session_state.get("response_2", "Pas familier(e) avec ces termes")],
        "Clarté": responses_scores[st.session_state.get("response_3", "Besoin d’amélioration")],
        "Diviser une Tâche": responses_scores[st.session_state.get("response_4", "Non, je ne suis pas sûr(e) de comment faire")]
    }
    
    # DataFrame for Radar Chart
    df = pd.DataFrame(dict(
        competence=list(competence_scores.keys()),
        score=list(competence_scores.values())
    ))
    
    # Plot radar chart
    fig = px.line_polar(df, r='score', theta='competence', line_close=True)
    fig.update_traces(fill='toself')
    fig.update_layout(title="Votre Radar de Compétences en Prompting IA")
    
    # Display radar chart
    st.plotly_chart(fig)
    
    # Reset question state after completion for replay
    st.button("Recommencer l'évaluation", on_click=lambda: st.session_state.update(question_number=1))
