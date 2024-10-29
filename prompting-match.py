import streamlit as st
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="L'IA, c'est pour moi ?",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
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
st.markdown("# 🤖 L'IA, c'est pour moi ?")

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
        "theme": "Identification des Besoins",
        "question": "📋 **Est-ce que vous avez l'habitude de récolter les besoins de vos clients ou de vos collègues pour définir des projets ?**",
        "choices": ["Sélectionnez une réponse", "🔰 Jamais", "📘 Occasionnellement", "🌟 Régulièrement"]
    },
    {
        "theme": "Expression des Besoins",
        "question": "🗣️ **Dans votre métier, vous arrive-t-il d'exprimer des besoins spécifiques à votre équipe ou à votre supérieur ?**",
        "choices": ["Sélectionnez une réponse", "🔰 Rarement", "📘 Parfois", "🌟 Fréquemment"]
    },
    {
        "theme": "Gestion de Projet",
        "question": "⚡ **Le concept d'agilité en gestion de projet vous est-il familier ?**",
        "choices": ["Sélectionnez une réponse", "🔰 Pas du tout", "📘 Un peu", "🌟 Oui, je l'applique régulièrement"]
    },
    {
        "theme": "Utilisation Actuelle des Outils",
        "question": "🛠️ **Utilisez-vous actuellement des outils numériques pour gérer vos tâches quotidiennes ?**",
        "choices": ["Sélectionnez une réponse", "🔰 Jamais", "📘 Parfois", "🌟 Fréquemment"]
    },
    {
        "theme": "Ouverture à l'Adoption de Nouveaux Outils",
        "question": "🤖 **Seriez-vous ouvert(e) à intégrer des outils d'intelligence artificielle pour améliorer votre efficacité au travail ?**",
        "choices": ["Sélectionnez une réponse", "🔰 Pas du tout", "📘 Peut-être", "🌟 Absolument"]
    },
    {
        "theme": "Adaptabilité et Flexibilité",
        "question": "📝 **Comment évaluez-vous votre capacité à apprendre et à vous adapter à de nouveaux outils technologiques ?**",
        "choices": ["Sélectionnez une réponse", "🔰 Peu adaptable", "📘 Moyennement adaptable", "🌟 Très adaptable"]
    },
    {
        "theme": "Structuration et Organisation",
        "question": "📈 **Comment évaluez-vous votre capacité à organiser les informations fournies par un outil numérique dans vos rapports ou présentations ?**",
        "choices": ["Sélectionnez une réponse", "🔰 Peu structuré", "📘 Moyennement structuré", "🌟 Très structuré"]
    },
    {
        "theme": "Collaboration et Communication",
        "question": "💬 **Utilisez-vous des plateformes de collaboration (comme Slack, Teams, etc.) pour communiquer avec votre équipe ?**",
        "choices": ["Sélectionnez une réponse", "🔰 Jamais", "📘 Parfois", "🌟 Fréquemment"]
    }
]

def save_response(response, question_num):
    """Sauvegarder la réponse et passer à la question suivante"""
    st.session_state["responses"][f"Question {question_num}"] = response
    st.session_state["question_number"] += 1

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
    def on_change():
        selected = st.session_state[f"response_{question_num}"]
        if selected != "Sélectionnez une réponse":
            save_response(selected, question_num)
    
    selected = st.radio("Sélectionnez une réponse :", choices, key=f"response_{question_num}", on_change=on_change)
    
    if selected == "Sélectionnez une réponse":
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
        response = st.session_state["responses"].get(f"Question {idx}", "Sélectionnez une réponse")
        if response == "Sélectionnez une réponse":
            score = 0  # Vous pouvez ajuster cette valeur selon votre logique
        else:
            # Calculer le score basé sur l'index de la réponse
            score = q["choices"].index(response)  # 1, 2, 3
        theme = q["theme"]
        competence_scores[theme] = score

    categories = list(competence_scores.keys())
    values = list(competence_scores.values())

    # Calcul du pourcentage de compatibilité
    total_score = sum(values)
    max_score = len(values) * 3
    pourcentage = (total_score / max_score) * 100 if max_score > 0 else 0

    # Détermination du niveau basé sur le pourcentage avec messages motivants par tranche de 10%
    if pourcentage <= 10:
        niveau = "🟠 Très Faible Compatibilité"
        motivation_message = "Il est encore temps d'explorer comment l'intelligence artificielle peut être intégrée dans votre métier. Continuez à apprendre !"
    elif pourcentage <= 20:
        niveau = "🟡 Faible Compatibilité"
        motivation_message = "Vous commencez à comprendre les bénéfices de l'IA. Poursuivez vos efforts pour mieux intégrer l'IA dans vos activités."
    elif pourcentage <= 30:
        niveau = "🟢 Compatibilité Modérée"
        motivation_message = "Vous avez une première approche de l'IA. Continuez sur cette lancée pour optimiser votre utilisation des outils d'IA."
    elif pourcentage <= 40:
        niveau = "🔵 Bonne Compatibilité"
        motivation_message = "Vous maîtrisez les fondamentaux pour intégrer l'IA. Il ne vous manque pas grand-chose pour une acculturation réussie !"
    elif pourcentage <= 50:
        niveau = "🟣 Très Bonne Compatibilité"
        motivation_message = "Vous possédez une solide compréhension de l'IA. Vous êtes presque prêt pour une intégration avancée de l'IA dans votre travail !"
    elif pourcentage <= 60:
        niveau = "🟤 Excellente Compatibilité"
        motivation_message = "Vous avez toutes les compétences nécessaires pour une intégration réussie de l'IA. Prêt à devenir un AS de l'IA ?"
    elif pourcentage <= 70:
        niveau = "🔴 Maîtrise de l'IA"
        motivation_message = "Votre expertise en IA est impressionnante. Vous êtes un véritable AS de l'IA !"
    elif pourcentage <= 80:
        niveau = "🔵 Maître en IA"
        motivation_message = "Vous maîtrisez parfaitement l'IA. Continuez à partager vos connaissances et à optimiser vos processus !"
    elif pourcentage <= 90:
        niveau = "🟢 Grand Maître en IA"
        motivation_message = "Votre compréhension de l'IA est exceptionnelle. Vous êtes un leader dans l'intégration de l'IA dans votre domaine !"
    else:
        niveau = "🌟 Légende de l'IA"
        motivation_message = "Vous êtes une véritable légende de l'IA. Félicitations pour votre expertise inégalée et votre capacité à intégrer l'IA dans votre métier !"

    # Création du graphique radar avec Plotly
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        marker=dict(color='rgba(56, 128, 255, 0.6)')
    ))

    fig.update_layout(
        title="🌟 Votre Radar de Compatibilité avec l'IA 🌟",
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
        <h3>🔢 Votre Niveau de Compatibilité avec l'IA: **{pourcentage:.1f}%**</h3>
        <h3>**{niveau}**</h3>
        <br>
        <div>
            <!-- Le graphique radar sera inséré ici -->
        </div>
        <br>
        <p class='motivation-message'><b>{motivation_message}</b></p>
        <hr>
        <h3>🎓 Continuez votre parcours !</h3>
        <p>Avec un score de **{pourcentage:.1f}%**, vous disposez déjà de nombreux prérequis pour intégrer l'IA dans votre quotidien. Nos formations avancées vous aideront à exploiter pleinement le potentiel de l'intelligence artificielle dans votre métier.</p>
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

# Fonction pour afficher les questions
def display_questions():
    current_question_num = st.session_state["question_number"]
    
    if 1 <= current_question_num <= len(questions):
        current_q = questions[current_question_num - 1]
        display_question(current_q, current_question_num)
    else:
        st.session_state["show_results"] = True

# Affichage des questions ou des résultats selon l'état
if not st.session_state["show_results"]:
    display_questions()

if st.session_state["show_results"]:
    display_results()

