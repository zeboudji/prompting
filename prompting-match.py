import streamlit as st
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="L'IA, est-ce pour moi ?",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed",
)
# Ajout du logo en haut à gauche
st.markdown("""
    <div style="display: flex; align-items: center;">
        <img src="data:image/png;base64,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" alt="Logo" style="height: 60px; margin-right: 10px;">
        <h1>L'IA, est-ce pour moi ?</h1>
    </div>
""", unsafe_allow_html=True)
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

# Affichage du sous-titre
st.title("L'IA, est-ce pour moi ?")
st.subheader("Calculez votre score de compatibilité avec l'IA et découvrez si vous êtes déjà prêt, sans même le savoir ! 🚀")

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
        "question": "🗣️ Dans votre métier, vous arrive-t-il d'exprimer des besoins spécifiques à votre équipe ou à votre supérieur ?",
        "choices": ["Sélectionner une réponse","🔰 Rarement", "📚 Parfois", "🌟 Fréquemment"]
    },
    {
        "theme": "Identification des Besoins",
        "question": "📋 Est-ce que vous avez l'habitude de récolter les besoins de vos clients ou de vos collègues pour définir des projets ?",
        "choices": ["Sélectionner une réponse","🔰 Jamais", "📚 Occasionnellement", "🌟 Régulièrement"]
    },
    {
        "theme": "Connaissance de l'Agilité",
        "question": "⚡ Le concept d'agilité en gestion de projet vous est-il familier ?",
        "choices": ["Sélectionner une réponse","🔰 Pas du tout", "📚 Un peu", "🌟 Oui, je l'applique régulièrement"]
    },
    {
        "theme": "Utilisation des Outils IA",
        "question": "🤖 Utilisez-vous des outils d'intelligence artificielle (IA) pour améliorer votre efficacité au travail ?",
        "choices": ["Sélectionner une réponse","🔰 Jamais", "📚 Parfois", "🌟 Fréquemment"]
    },
    {
        "theme": "Rédaction de Prompts",
        "question": "📝 Avez-vous déjà rédigé des prompts pour interagir avec des outils d'IA comme ChatGPT ?",
        "choices": ["Sélectionner une réponse","🔰 Jamais", "📚 Rarement", "🌟 Souvent"]
    },
    {
        "theme": "Structuration des Informations",
        "question": "📊 **Comment évaluez-vous votre capacité à organiser les informations fournies par un outil d'IA dans vos rapports ou présentations ?",
        "choices": ["Sélectionner une réponse","🔰 Peu structuré", "📚 Moyennement structuré", "🌟 Très structuré"]
    }
]

def save_response():
    """Sauvegarder la réponse et passer à la question suivante"""
    current_question = st.session_state["question_number"]
    response_key = f"response_{current_question}"
    response = st.session_state.get(response_key, None)
    if response:  # Vérifier si une réponse est sélectionnée
        st.session_state["responses"][f"Question {current_question + 1}"] = response
        st.session_state["question_number"] += 1
        # Vérification directe pour afficher les résultats si dernière question
        if st.session_state["question_number"] >= len(questions):
            st.session_state["show_results"] = True

# Fonction pour afficher une question sous forme d'accordéon
def display_question_accordion():
    for idx, question_data in enumerate(questions):
        if idx == st.session_state["question_number"]:
            with st.expander(f"{question_data['theme']}", expanded=True):  # Créer un accordéon pour la question courante
                question_text = question_data["question"]
                choices = question_data["choices"]
                st.radio(question_text, choices, key=f"response_{idx}", on_change=save_response)
        else:
            with st.expander(f"{question_data['theme']}", expanded=False):
                st.markdown(f"**{question_data['question']}**")

# Fonction pour réinitialiser l'évaluation
def reset_evaluation():
    st.session_state["responses"] = {}
    st.session_state["question_number"] = 0
    st.session_state["show_results"] = False
    st.experimental_rerun()

# Fonction pour afficher les résultats

def display_results():
    # Calcul des scores pour le graphique radar
    competence_scores = {}
    for idx, q in enumerate(questions, 1):
        response = st.session_state["responses"].get(f"Question {idx}", "")
        try:
            score = q["choices"].index(response) + 1
        except ValueError:
            score = 0
        competence_scores[q["theme"]] = score

    categories = list(competence_scores.keys())
    values = list(competence_scores.values())

    # Ajout d'une valeur égale à la première pour fermer le radar
    values += values[:1]
    categories += categories[:1]

    # Calcul du pourcentage de compatibilité
    total_score = sum(values[:-1])
    max_score = (len(values) - 1) * 3
    pourcentage = (total_score / max_score) * 100 if max_score > 0 else 0

    # Détermination du niveau basé sur le pourcentage
    if pourcentage < 60:
        niveau = "🎓 Sensibilisation à l'IA"
        niveau_message = "Vous êtes éligible à la **Sensibilisation** pour mieux comprendre les fondamentaux de l'IA. Toutes les conditions sont réunies !"
        recommandation = "Nous vous recommandons de suivre notre formation de sensibilisation pour approfondir vos connaissances sur l'intelligence artificielle."
    else:
        niveau = "Vous avez besoin d'une acculturation pour exploiter pleinement le potentiel de l'IA 🚀"
        niveau_message = "Vous disposez déjà d'un certain nombre deprérequis pour devenir un **AS de l'IA** !"
        recommandation = "Nous vous invitons à consulter notre programme d'acculturation avancée pour maîtriser pleinement les outils et concepts de l'intelligence artificielle."

    # Création du graphique radar avec Plotly
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Compétences',
        marker=dict(color='rgba(56, 128, 255, 0.6)')
    ))

    fig.update_layout(
        title="🌟 Votre Radar de Compétences en IA 🌟",
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 3],
                tickvals=[0, 1, 2, 3],
                ticktext=["0", "1", "2", "3"]
            ),
            angularaxis=dict(showline=True, linecolor="lightgrey")
        ),
        showlegend=False,
        template="plotly_dark",
        margin=dict(l=50, r=50, t=50, b=50)
    )

    # Niveau d'acculturation
    st.markdown(f"### Votre score de compatibilité avec l'IA est de : **{pourcentage:.1f}%**", unsafe_allow_html=True)
    st.markdown(f"### **{niveau}**", unsafe_allow_html=True)

    # Afficher le graphique radar
    st.plotly_chart(fig, use_container_width=True)

    # Message de niveau
    st.markdown(f"<div class='motivation-message'><b>{niveau_message}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='motivation-message'>{recommandation}</div>", unsafe_allow_html=True)

    # Proposition de formation avec lien
    st.markdown("""
        ---
        🎓 **Continuez votre parcours !**
        👉 [Découvrez nos formations](https://insidegroup.fr/actualites/acculturation-ia/)
    """, unsafe_allow_html=True)

    # Bouton pour recommencer l'évaluation
    if st.button("🔄 Recommencer l'évaluation"):
        reset_evaluation()

# Affichage des questions ou des résultats selon l'état
if not st.session_state["show_results"]:
    display_question_accordion()
else:
    display_results()
