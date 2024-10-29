import streamlit as st
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="🚀 Niveau d'acculturation à l'IA",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="auto",
)

# Styles personnalisés
st.markdown("""
    <style>
    /* Style général de la page */
    body {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    /* Style pour les conteneurs de questions */
    .question-container {
        padding: 20px;
        background-color: #2c2c2c;
        border-radius: 10px;
        margin-bottom: 20px;
        color: #ffffff;
    }
    /* Style pour le conteneur des résultats */
    .result-container {
        padding: 40px;
        background-color: #2c2c2c;
        border-radius: 15px;
        text-align: center;
        color: #ffffff;
        box-shadow: 0 8px 16px rgba(0,0,0,0.5);
        max-width: 800px;
        margin: auto;
    }
    /* Style pour les boutons */
    .button-container {
        text-align: center;
        margin-top: 30px;
    }
    /* Style pour les textes d'erreur */
    .error-message {
        color: #ff1744;
        font-size: 0.9em;
    }
    /* Style pour le bouton "Découvrez nos formations" en haut à droite */
    .top-right-button {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
    }
    /* Style pour la barre de progression avec fil d'Ariane */
    .breadcrumb {
        list-style: none;
        display: flex;
        justify-content: space-between;
        padding: 0;
        margin-bottom: 20px;
        font-size: 0.9em;
    }
    .breadcrumb li {
        flex: 1;
        text-align: center;
        position: relative;
    }
    .breadcrumb li::after {
        content: '';
        position: absolute;
        top: 50%;
        right: -50%;
        width: 100%;
        height: 2px;
        background-color: #4CAF50;
        z-index: -1;
    }
    .breadcrumb li:last-child::after {
        content: none;
    }
    .breadcrumb .active {
        font-weight: bold;
        color: #4CAF50;
    }
    /* Style pour les icônes */
    .icon {
        font-size: 4em;
        margin-bottom: 10px;
    }
    /* Style pour les messages motivants */
    .motivation-message {
        font-size: 1.2em;
        margin-top: 20px;
        color: #81c784;
    }
    /* Style pour les titres */
    .result-title {
        font-size: 2em;
        margin-top: 10px;
    }
    /* Responsive adjustments */
    @media (max-width: 600px) {
        .breadcrumb {
            flex-direction: column;
            align-items: center;
        }
        .breadcrumb li::after {
            width: 2px;
            height: 100%;
            top: -50%;
            left: 50%;
            right: auto;
            transform: rotate(90deg);
        }
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
st.markdown("# 🚀 Niveau d'acculturation à l'IA")

# Initialisation de l'état de session avec setdefault pour éviter KeyError
if 'responses' not in st.session_state:
    st.session_state['responses'] = {}
if 'question_number' not in st.session_state:
    st.session_state['question_number'] = 0
if 'show_results' not in st.session_state:
    st.session_state['show_results'] = False

# Définition des questions avec thèmes, emojis et options adaptées
questions = [
    {
        "theme": "Compréhension des Concepts",
        "question": "🗣️ **Dans votre métier, vous arrive-t-il d'exprimer des besoins spécifiques à votre équipe ou à votre supérieur ?**",
        "choices": ["Sélectionnez une réponse", "🔰 Rarement", "📘 Parfois", "🌟 Fréquemment"]
    },
    {
        "theme": "Identification des Besoins",
        "question": "📋 **Est-ce que vous avez l'habitude de récolter les besoins de vos clients ou de vos collègues pour définir des projets ?**",
        "choices": ["Sélectionnez une réponse", "🔰 Jamais", "📘 Occasionnellement", "🌟 Régulièrement"]
    },
    {
        "theme": "Connaissance de l'Agilité",
        "question": "⚡ **Le concept d'agilité en gestion de projet vous est-il familier ?**",
        "choices": ["Sélectionnez une réponse", "🔰 Pas du tout", "📘 Un peu", "🌟 Oui, je l'applique régulièrement"]
    },
    {
        "theme": "Utilisation des Outils IA",
        "question": "🤖 **Utilisez-vous des outils d'intelligence artificielle (IA) pour améliorer votre efficacité au travail ?**",
        "choices": ["Sélectionnez une réponse", "🔰 Jamais", "📘 Parfois", "🌟 Fréquemment"]
    },
    {
        "theme": "Rédaction de Prompts",
        "question": "📝 **Avez-vous déjà rédigé des prompts pour interagir avec des outils d'IA comme ChatGPT ?**",
        "choices": ["Sélectionnez une réponse", "🔰 Jamais", "📘 Rarement", "🌟 Souvent"]
    },
    {
        "theme": "Structuration des Informations",
        "question": "📈 **Comment évaluez-vous votre capacité à organiser les informations fournies par un outil d'IA dans vos rapports ou présentations ?**",
        "choices": ["Sélectionnez une réponse", "🔰 Peu structuré", "📘 Moyennement structuré", "🌟 Très structuré"]
    }
]

def save_response(response, question_num):
    """Sauvegarder la réponse et passer à la question suivante"""
    st.session_state["responses"][f"Question {question_num}"] = response
    st.session_state["question_number"] += 1
    # Si c'est la dernière question, afficher les résultats
    if st.session_state["question_number"] >= len(questions):
        st.session_state["show_results"] = True

# Fonction pour afficher une question avec fil d'Ariane
def display_question(question_data, question_num):
    theme = question_data["theme"]
    question_text = question_data["question"]
    choices = question_data["choices"]

    # Création du fil d'Ariane avec thèmes
    breadcrumb = '<ul class="breadcrumb">'
    for i in range(1, len(questions)+1):
        current_theme = questions[i-1]["theme"]
        if i < question_num:
            breadcrumb += f'<li><span class="active">{current_theme}</span></li>'
        elif i == question_num:
            breadcrumb += f'<li><span class="active">{current_theme}</span></li>'
        else:
            breadcrumb += f'<li>{current_theme}</li>'
    breadcrumb += '</ul>'
    st.markdown(breadcrumb, unsafe_allow_html=True)

    # Affichage de la question
    st.markdown(f"<div class='question-container'><b>{question_text}</b></div>", unsafe_allow_html=True)

    # Gestion des réponses avec callback
    selected = st.radio("Sélectionnez une réponse :", choices, key=f"response_{question_num}")

    if selected != "Sélectionnez une réponse":
        save_response(selected, question_num)
    else:
        st.markdown("<span class='error-message'>Veuillez sélectionner une réponse valide.</span>", unsafe_allow_html=True)

# Fonction pour réinitialiser l'évaluation
def reset_evaluation():
    st.session_state["responses"] = {}
    st.session_state["question_number"] = 0
    st.session_state["show_results"] = False

# Fonction pour afficher les résultats
def display_results():
    # Calcul des scores pour le graphique radar
    competence_scores = {}
    for idx, q in enumerate(questions, 1):
        response = st.session_state["responses"].get(f"Question {idx}", "🔰 Rarement")
        # Calculer le score basé sur l'index de la réponse
        # Les choix sont ["Sélectionnez une réponse", "Option 1", "Option 2", "Option 3"]
        # Donc l'index 1 correspond à score 1, index 2 à score 2, etc.
        try:
            score = q["choices"].index(response)
        except ValueError:
            score = 0  # Si la réponse n'est pas trouvée
        competence_scores[q["theme"]] = score

    categories = list(competence_scores.keys())
    values = list(competence_scores.values())

    # Calcul du pourcentage de compatibilité
    total_score = sum(values)
    max_score = len(values) * 3
    pourcentage = (total_score / max_score) * 100 if max_score > 0 else 0

    # Détermination du niveau basé sur le pourcentage
    if pourcentage < 60:
        niveau = "🎓 Sensibilisation à l'IA"
        niveau_message = "Vous êtes éligible à la **Sensibilisation** pour mieux comprendre les fondamentaux de l'IA. Toutes les conditions sont réunies !"
        recommandation = "Nous vous recommandons de suivre notre formation de sensibilisation pour approfondir vos connaissances sur l'intelligence artificielle."
    else:
        niveau = "🚀 Acculturation pour devenir un AS de l'IA"
        niveau_message = "Félicitations ! Vous êtes éligible à l'**Acculturation** pour devenir un **AS de l'IA**. Toutes les conditions sont réunies !"
        recommandation = "Nous vous invitons à rejoindre notre programme d'acculturation avancée pour maîtriser pleinement les outils et concepts de l'intelligence artificielle."

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
        template="plotly_dark"
    )

    # Création du contenu HTML complet pour la page des résultats
    html_content = f"""
    <div class='result-container'>
        <div class='icon'>🌟</div>
        <div class='result-title'>**Félicitations !**</div>
        <h3>🔢 Votre Niveau d'Acculturation à l'IA: **{pourcentage:.1f}%**</h3>
        <h3>**{niveau}**</h3>
        <br>
        <div>
            <!-- Le graphique radar sera inséré ici -->
        </div>
        <br>
        <p class='motivation-message'><b>{niveau_message}</b></p>
        <hr>
        <h3>🎓 Continuez votre parcours !</h3>
        <p>{recommandation}</p>
        <p>👉 <a href="https://insidegroup.fr/actualites/acculturation-ia/" style="color: #81c784;">Découvrez nos formations</a></p>
        <hr>
        <div class='button-container'>
            <button style="
                background-color: #f44336; 
                color: white; 
                padding: 10px 20px; 
                text-align: center; 
                text-decoration: none; 
                display: inline-block; 
                font-size: 16px; 
                border: none; 
                border-radius: 5px;
                cursor: pointer;" onclick="window.location.reload();">
                🔄 Recommencer l'évaluation
            </button>
        </div>
    </div>
    """

    # Afficher le contenu HTML de la page des résultats
    st.markdown(html_content, unsafe_allow_html=True)

    # Afficher le graphique radar
    st.plotly_chart(fig, use_container_width=True)

# Affichage des questions ou des résultats selon l'état
if not st.session_state["show_results"]:
    if st.session_state["question_number"] < len(questions):
        current_question_num = st.session_state["question_number"] + 1
        current_q = questions[st.session_state["question_number"]]
        display_question(current_q, current_question_num)
    else:
        st.session_state["show_results"] = True

if st.session_state["show_results"]:
    display_results()
