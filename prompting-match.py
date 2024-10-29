import streamlit as st
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="L'IA, est ce pour moi ? ",
     page_title="Calculez votre score de compatibilité avec l'IA et découvrez si vous êtes déjà prêt, sans même le savoir !",
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
