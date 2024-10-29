import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sqlite3
from datetime import datetime

# Titre avec Emoji
st.markdown("# 🚀 Évaluation Interactive des Compétences en Prompting IA")

# Connexion à la base de données et création des tables si nécessaire
def create_connection():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            nom TEXT,
            email TEXT,
            poste TEXT,
            secteur TEXT,
            niveau_maturité TEXT,
            connaissance_agile TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            question TEXT,
            response TEXT,
            FOREIGN KEY(user_id) REFERENCES profiles(id)
        )
    ''')
    conn.commit()
    return conn

# Fonction pour sauvegarder le profil utilisateur
def save_profile(nom, email, poste, secteur, niveau_maturité, connaissance_agile):
    conn = create_connection()
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO profiles (date, nom, email, poste, secteur, niveau_maturité, connaissance_agile)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (date, nom, email, poste, secteur, niveau_maturité, connaissance_agile))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

# Fonction pour sauvegarder les réponses
def save_responses(user_id, responses):
    conn = create_connection()
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for question, response in responses.items():
        cursor.execute('''
            INSERT INTO responses (user_id, date, question, response)
            VALUES (?, ?, ?, ?)
        ''', (user_id, date, question, response))
    conn.commit()
    conn.close()

# Initialisation de l'état de session
if "step" not in st.session_state:
    st.session_state["step"] = "profil"

# Formulaire de profil utilisateur
if st.session_state["step"] == "profil":
    st.header("🔍 Informations sur votre profil")
    with st.form("profil_form"):
        nom = st.text_input("Nom complet")
        email = st.text_input("Email")
        poste = st.text_input("Votre poste actuel")
        secteur = st.text_input("Secteur d'activité")
        niveau_maturité = st.selectbox(
            "Niveau de maturité en IA",
            ["Sélectionnez une option", "Débutant", "Intermédiaire", "Avancé"]
        )
        connaissance_agile = st.selectbox(
            "Connaissance des méthodes Agiles",
            ["Sélectionnez une option", "Oui", "Non"]
        )
        submitted = st.form_submit_button("Commencer l'évaluation")
    
    if submitted:
        if nom and email and poste and secteur and niveau_maturité != "Sélectionnez une option" and connaissance_agile != "Sélectionnez une option":
            user_id = save_profile(nom, email, poste, secteur, niveau_maturité, connaissance_agile)
            st.session_state["user_id"] = user_id
            st.session_state["step"] = "questions"
        else:
            st.error("Veuillez remplir tous les champs requis.")

# Questions d'évaluation
elif st.session_state["step"] == "questions":
    # Initialisation de la progression des questions
    if "question_number" not in st.session_state:
        st.session_state["question_number"] = 1
        st.session_state["responses"] = {}
    
    def next_question():
        """ Fonction pour passer à la question suivante """
        st.session_state["question_number"] += 1
    
    # Définition des questions avec emojis et options
    questions = [
        ("🌱 **Quel est votre niveau de familiarité avec l’écriture de prompts pour l’IA ?**",
         ["Sélectionnez une réponse", "🔰 Débutant(e)", "📘 Intermédiaire", "🌟 Avancé(e)"]),
        ("🧩 **Utilisez-vous déjà des techniques d’expression de besoin comme les User Stories ou les Epics ?**",
         ["Sélectionnez une réponse", "✅ Oui", "📙 Non, mais curieux(se) d’en apprendre plus", "❓ Pas familier(e) avec ces termes"]),
        ("🔍 **Comment définiriez-vous votre capacité à exprimer des besoins clairs et spécifiques pour une tâche ?**",
         ["Sélectionnez une réponse", "📝 Très clair et structuré", "📄 Clair, mais manque parfois de détails", "⚠️ Besoin d’amélioration"]),
        ("📐 **Savez-vous diviser une tâche en plusieurs étapes pour aider l’IA à répondre plus précisément ?**",
         ["Sélectionnez une réponse", "✔️ Oui, j’utilise cette approche régulièrement", "🔄 J’ai quelques idées, mais je pourrais m’améliorer", "❌ Non, je ne suis pas sûr(e) de comment faire"]),
        ("🎯 **Comment évalueriez-vous votre capacité à adapter le ton du prompt au contexte ?**",
         ["Sélectionnez une réponse", "🗣 Très adaptable", "😊 Souvent adaptable", "🛑 Peu adaptable"]),
        ("🎯 **Comment évalueriez-vous votre capacité à structurer les réponses pour obtenir des informations claires et organisées ?**",
         ["Sélectionnez une réponse", "📊 Très structuré", "📈 Parfois structuré", "🚧 Peu structuré"])
    ]
    
    # Récupération du profil utilisateur
    user_id = st.session_state["user_id"]
    
    # Affichage de la question courante
    if st.session_state["question_number"] <= len(questions):
        question_text, choices = questions[st.session_state["question_number"] - 1]
        st.markdown(f"<div style='padding: 20px; background-color: #e3f2fd; border-radius: 10px; color: #0d47a1;'><b>{question_text}</b></div>", unsafe_allow_html=True)
        response = st.selectbox("Sélectionnez une réponse :", choices, key=f"question_{st.session_state['question_number']}")
        
        # Affichage du bouton pour passer à la question suivante
        if response != "Sélectionnez une réponse":
            if st.button("Suivant"):
                st.session_state["responses"][f"Question {st.session_state['question_number']}"] = response
                next_question()
    else:
        # Sauvegarde des réponses dans la base de données
        save_responses(user_id, st.session_state["responses"])
        
        # Calcul des scores pour le graphique radar
        responses_scores = {
            "🔰 Débutant(e)": 1, "📘 Intermédiaire": 2, "🌟 Avancé(e)": 3,
            "❓ Pas familier(e) avec ces termes": 1, "📙 Non, mais curieux(se) d’en apprendre plus": 2, "✅ Oui": 3,
            "⚠️ Besoin d’amélioration": 1, "📄 Clair, mais manque parfois de détails": 2, "📝 Très clair et structuré": 3,
            "❌ Non, je ne suis pas sûr(e) de comment faire": 1, "🔄 J’ai quelques idées, mais je pourrais m’améliorer": 2, "✔️ Oui, j’utilise cette approche régulièrement": 3,
            "🛑 Peu adaptable": 1, "😊 Souvent adaptable": 2, "🗣 Très adaptable": 3,
            "🚧 Peu structuré": 1, "📈 Parfois structuré": 2, "📊 Très structuré": 3
        }
        
        competence_scores = {
            "Familiarité": responses_scores.get(st.session_state["responses"].get("Question 1", "🔰 Débutant(e)"), 1),
            "Expérience Agile": responses_scores.get(st.session_state["responses"].get("Question 2", "❓ Pas familier(e) avec ces termes"), 1),
            "Clarté": responses_scores.get(st.session_state["responses"].get("Question 3", "⚠️ Besoin d’amélioration"), 1),
            "Diviser une Tâche": responses_scores.get(st.session_state["responses"].get("Question 4", "❌ Non, je ne suis pas sûr(e) de comment faire"), 1),
            "Adaptabilité du Ton": responses_scores.get(st.session_state["responses"].get("Question 5", "🛑 Peu adaptable"), 1),
            "Structure des Réponses": responses_scores.get(st.session_state["responses"].get("Question 6", "🚧 Peu structuré"), 1)
        }
        
        categories = list(competence_scores.keys())
        values = list(competence_scores.values())
        
        # Création du graphique radar avec Plotly
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            marker=dict(color='rgba(56, 128, 255, 0.6)')
        ))
        
        fig.update_layout(
            title="🌟 Votre Radar de Compétences en Prompting IA 🌟",
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 3]
                ),
                angularaxis=dict(showline=True, linecolor="lightgrey")
            ),
            showlegend=False
        )
        
        st.plotly_chart(fig)
        
        # Calcul du pourcentage de connaissances
        total_score = sum(values)
        max_score = len(values) * 3
        pourcentage = (total_score / max_score) * 100
        
        st.metric("🔢 Votre Niveau de Connaissance en IA", f"{pourcentage:.1f}%")
        
        # Proposition de formation
        st.markdown(f"""
            ---
            🎓 **Prolongez votre apprentissage !**
            
            Vous avez obtenu un score de **{pourcentage:.1f}%** dans votre évaluation. Pour perfectionner vos connaissances et pratiques en IA et en prompting, découvrez nos **formations personnalisées** adaptées à votre niveau.
            
            👉 [Découvrez nos formations](https://votre-site.com/formations)
        """)
        
        # Bouton pour recommencer l'évaluation
        if st.button("🔄 Recommencer l'évaluation"):
            st.session_state["step"] = "profil"
            st.session_state["question_number"] = 1
            st.session_state["responses"] = {}
