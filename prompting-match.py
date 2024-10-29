import streamlit as st
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="L'IA, est ce pour moi ? ",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Styles personnalisés
st.markdown("""
    <style>
    /* Style général de la page */
    body {
        background-color: #121212;
        color: #ffffff;
    }
    /* Style pour les conteneurs de questions et résultats */
    .container {
        padding: 20px;
        background-color: #1e1e1e;
        border-radius: 10px;
        margin-bottom: 20px;
        color: #ffffff;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    /* Style pour le bouton "Découvrez nos formations" en haut à droite */
    .top-right-button {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

# Bouton "Découvrez nos formations" en haut à droite
st.markdown("""
    <div class="top-right-button">
        <a href="https://insidegroup.fr/actualites/acculturation-ia/" target="_blank">
            <button style="
                background-color: #4CAF50; 
                color: white; 
                padding: 10px 20px; 
                text-align: center; 
                text-decoration: none; 
                display: inline-block; 
                font-size: 16px; 
                border: none; 
                border-radius: 5px;
                cursor: pointer;">
                📚 Découvrez nos formations
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Titre principal
st.markdown("# 🚀 L'IA, est-ce pour moi ?")

# Initialisation de l'état de session avec setdefault pour éviter KeyError
if "responses" not in st.session_state:
    st.session_state["responses"] = {}
if "question_number" not in st.session_state:
    st.session_state["question_number"] = 0
if "show_results" not in st.session_state:
    st.session_state["show_results"] = False

# Définition des questions avec thèmes, emojis et options adaptées
questions = [
    {
        "theme": "Compréhension des Concepts",
        "question": "🗣️ **Dans votre métier, vous arrive-t-il d'exprimer des besoins spécifiques à votre équipe ou à votre supérieur ?**",
        "choices": ["Sélectionnez une réponse", "🔰 Rarement", "📚 Parfois", "🌟 Fréquemment"]
    },
    {
        "theme": "Identification des Besoins",
        "question": "📋 **Est-ce que vous avez l'habitude de récolter les besoins de vos clients ou de vos collègues pour définir des projets ?**",
        "choices": ["Sélectionnez une réponse", "🔰 Jamais", "📚 Occasionnellement", "🌟 Régulièrement"]
