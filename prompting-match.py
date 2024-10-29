import streamlit as st
import pandas as pd
import plotly.express as px
import time

# Title with Emoji
st.markdown("# 🚀 Évaluation Interactive des Compétences en Prompting IA")

# Initialize session state for question progression and responses
if "question_number" not in st.session_state:
    st.session_state["question_number"] = 1

def next_question():
    """ Function to move to the next question """
    st.session_state["question_number"] += 1

# Define questions with emojis, colors, and a default "Select" option
questions = [
    ("🌱 **Quel est votre niveau de familiarité avec l’écriture de prompts pour l’IA ?**",
     ["Sélectionnez une réponse", "🔰 Débutant(e)", "📘 Intermédiaire", "🌟 Avancé(e)"]),
    ("🧩 **Utilisez-vous déjà des techniques d’expression de besoin comme les User Stories ou les Epics ?**",
     ["Sélectionnez une réponse", "✅ Oui", "📙 Non, mais curieux(se) d’en apprendre plus", "❓ Pas familier(e) avec ces termes"]),
    ("🔍 **Comment définiriez-vous votre capacité à exprimer des besoins clairs et spécifiques pour une tâche ?**",
     ["Sélectionnez une réponse", "📝 Très clair et structuré", "📄 Clair, mais manque parfois de détails", "⚠️ Besoin d’amélioration"]),
    ("📐 **Savez-vous diviser une tâche en plusieurs étapes pour aider l’IA à répondre plus précisément ?**",
     ["Sélectionnez une réponse", "✔️ Oui, j’utilise cette approche régulièrement", "🔄 J’ai quelques idées, mais je pourrais m’améliorer", "❌ Non, je ne suis pas sûr(e) de comment faire"])
]

# Mapping responses to a numeric score for radar chart
responses_scores = {
    "🔰 Débutant(e)": 1, "📘 Intermédiaire": 2, "🌟 Avancé(e)": 3,
    "❓ Pas familier(e) avec ces termes": 1, "📙 Non, mais curieux(se) d’en apprendre plus": 2, "✅ Oui": 3,
    "⚠️ Besoin d’amélioration": 1, "📄 Clair, mais manque parfois de détails": 2, "📝 Très clair et structuré": 3,
    "❌ Non, je ne suis pas sûr(e) de comment faire": 1, "🔄 J’ai quelques idées, mais je pourrais m’améliorer": 2, "✔️ Oui, j’utilise cette approche régulièrement": 3
}

# Display current question with enhanced visibility and background color
if st.session_state["question_number"] <= len(questions):
    question_text, choices = questions[st.session_state["question_number"] - 1]
    st.markdown(f"<div style='padding: 20px; background-color: #e3f2fd; border-radius: 10px; color: #0d47a1;'><b>{question_text}</b></div>", unsafe_allow_html=True)
    response = st.selectbox("Sélectionnez une réponse :", choices, key=f"question_{st.session_state['question_number']}")
    
    # Display the button to proceed to the next question only when a valid response is selected
    if response != "Sélectionnez une réponse":
        st.button("Suivant", on_click=next_question)
else:
    # Calculate scores for radar chart
    competence_scores = {
        "Familiarité": responses_scores[st.session_state.get("question_1", "🔰 Débutant(e)")],
        "Expérience Agile": responses_scores[st.session_state.get("question_2", "❓ Pas familier(e) avec ces termes")],
        "Clarté": responses_scores[st.session_state.get("question_3", "⚠️ Besoin d’amélioration")],
        "Diviser une Tâche": responses_scores[st.session_state.get("question_4", "❌ Non, je ne suis pas sûr(e) de comment faire")]
    }
    
    # DataFrame for Radar Chart
    df = pd.DataFrame(dict(
        competence=list(competence_scores.keys()),
        score=list(competence_scores.values())
    ))
    
    # Radar chart with Plotly
    fig = px.line_polar(df, r='score', theta='competence', line_close=True)
    fig.update_traces(fill='toself')
    fig.update_layout(title="🎯 Votre Radar de Compétences en Prompting IA", 
                      font=dict(size=14), 
                      polar=dict(radialaxis=dict(visible=True, range=[0, 3])))
    
    # Display radar chart
    st.plotly_chart(fig)
    
    # Restart button
    st.button("🔄 Recommencer l'évaluation", on_click=lambda: st.session_state.update(question_number=1))
