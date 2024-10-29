import streamlit as st
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="L'IA c'est pour moi ?",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto",
)

# Styles personnalisés
st.markdown("""
    <style>
    /* Style général de la page */
    .main {
        background-color: #121212;
        color: #ffffff;
    }
    /* Style pour les conteneurs de questions */
    .question-container {
        padding: 20px;
        background-color: #1e1e1e;
        border-radius: 10px;
        margin-bottom: 20px;
        color: #ffffff;
    }
    /* Style pour le conteneur des résultats */
    .result-container {
        padding: 30px;
        background-color: #1a237e;
        border-radius: 15px;
        text-align: center;
        color: #ffffff;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }
    /* Style pour les boutons */
    .button-container {
        text-align: center;
        margin-top: 30px;
    }
    /* Style pour les textes d'erreur */
    .error-message {
        color: #ff1744;
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
        font-size: 0.8em; /* Réduction de la taille du texte */
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
    /* Style pour les cartes */
    .card {
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        color: #ffffff;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        transition: 0.3s;
        cursor: pointer;
    }
    .card:hover {
        background-color: #2e7d32;
    }
    /* Style pour le titre des cartes */
    .card-title {
        font-size: 1.5em;
        margin-bottom: 10px;
    }
    /* Style pour les descriptions des cartes */
    .card-description {
        font-size: 1em;
        color: #cccccc;
    }
    /* Style pour le graphique radar */
    .radar-title {
        text-align: center;
        color: #ffffff;
        margin-bottom: -30px;
    }
    /* Style pour le niveau */
    .niveau {
        font-size: 1.2em;
        margin-top: 10px;
    }
    /* Style pour les recommandations */
    .recommandation {
        font-size: 1em;
        margin-top: 20px;
    }
    /* Style pour les icônes */
    .icon {
        font-size: 3em;
        margin-bottom: 10px;
    }
    /* Style pour les messages motivants */
    .motivation-message {
        font-size: 1.1em;
        margin-top: 10px;
        color: #81c784;
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
st.markdown("# 🤖 L'IA c'est pour moi ?")

# Initialisation de l'état de session avec setdefault pour éviter KeyError
for key in ["responses", "question_number", "show_results"]:
    if key not in st.session_state:
        if key == "responses":
            st.session_state[key] = {}
        elif key == "question_number":
            st.session_state[key] = 0
        elif key == "show_results":
            st.session_state[key] = False

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

# Mapping des réponses à un score numérique pour le graphique radar
responses_scores = {
    "🔰 Rarement": 1, "📘 Parfois": 2, "🌟 Fréquemment": 3,
    "🔰 Jamais": 1, "📘 Occasionnellement": 2, "🌟 Régulièrement": 3,
    "🔰 Pas du tout": 1, "📘 Un peu": 2, "🌟 Oui, je l'applique régulièrement": 3,
    "🔰 Jamais": 1, "📘 Parfois": 2, "🌟 Fréquemment": 3,
    "🔰 Jamais": 1, "📘 Rarement": 2, "🌟 Souvent": 3,
    "🔰 Peu structuré": 1, "📘 Moyennement structuré": 2, "🌟 Très structuré": 3
}

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

# Fonction pour afficher les résultats
def display_results():
    st.markdown("<div class='result-container'>", unsafe_allow_html=True)
    
    # Icône de félicitations
    st.markdown("<div class='icon'>🌟</div>", unsafe_allow_html=True)
    
    # Titre de félicitations
    st.markdown("**Félicitations !**", unsafe_allow_html=True)
    
    # Calcul des scores pour le graphique radar
    competence_scores = {}
    for idx, q in enumerate(questions, 1):
        response = st.session_state["responses"].get(f"Question {idx}", "🔰 Rarement")
        score = responses_scores.get(response, 1)
        theme = q["theme"]
        competence_scores[theme] = score
    
    categories = list(competence_scores.keys())
    values = list(competence_scores.values())
    
    # Calcul du pourcentage de connaissances
    total_score = sum(values)
    max_score = len(values) * 3
    pourcentage = (total_score / max_score) * 100
    
    # Détermination du niveau basé sur le pourcentage avec messages motivants par tranche de 10%
    if pourcentage <= 10:
        niveau = "🟠 Débutant en IA"
        motivation_message = "Il est encore temps d'explorer les bases de l'intelligence artificielle. Continuez à apprendre !"
    elif pourcentage <= 20:
        niveau = "🟡 Sensibilisation Initiale"
        motivation_message = "Vous avez une première approche de l'IA. Poursuivez vos efforts pour mieux comprendre ses applications."
    elif pourcentage <= 30:
        niveau = "🟢 Sensibilisation Approfondie"
        motivation_message = "Vous avez une bonne compréhension des concepts de base de l'IA. Continuez sur cette lancée !"
    elif pourcentage <= 40:
        niveau = "🔵 Compétent en IA"
        motivation_message = "Vous maîtrisez les fondamentaux de l'IA. Il ne vous manque pas grand-chose pour une acculturation réussie !"
    elif pourcentage <= 50:
        niveau = "🟣 Avancé en IA"
        motivation_message = "Vous possédez une solide compréhension de l'IA. Vous êtes presque prêt pour devenir un AS de l'IA !"
    elif pourcentage <= 60:
        niveau = "🟤 Très Avancé en IA"
        motivation_message = "Vous avez toutes les compétences nécessaires pour une acculturation réussie. Prêt à devenir un AS de l'IA ?"
    elif pourcentage <= 70:
        niveau = "🔴 Expert en IA"
        motivation_message = "Votre expertise en IA est impressionnante. Vous êtes un véritable AS de l'IA !"
    elif pourcentage <= 80:
        niveau = "🔵 Maître en IA"
        motivation_message = "Vous maîtrisez parfaitement l'IA. Continuez à partager vos connaissances !"
    elif pourcentage <= 90:
        niveau = "🟢 Grand Maître en IA"
        motivation_message = "Votre compréhension de l'IA est exceptionnelle. Vous êtes un leader dans ce domaine !"
    else:
        niveau = "🌟 Légende de l'IA"
        motivation_message = "Vous êtes une véritable légende de l'IA. Félicitations pour votre expertise inégalée !"
    
    # Afficher le niveau avec une mise en page agréable
    st.markdown(f"### 🔢 Votre Niveau d'Acculturation à l'IA: **{pourcentage:.1f}%**", unsafe_allow_html=True)
    st.markdown(f"### **{niveau}**", unsafe_allow_html=True)
    
    # Ajout d'un espace
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Création du graphique radar avec Plotly
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
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
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Ajout d'un espace
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Message de motivation
    st.markdown(f"""
        <div class='motivation-message'>
            <b>{motivation_message}</b>
        </div>
    """, unsafe_allow_html=True)
    
    # Proposition de formation avec lien
    st.markdown(f"""
        ---
        🎓 **Continuez votre parcours !**
        
        Vous avez obtenu un score de **{pourcentage:.1f}%** dans votre évaluation. Cela démontre une forte compatibilité avec nos formations avancées qui vous permettront de devenir un véritable **pro de l'IA**.
        
        👉 [Découvrez nos formations](https://insidegroup.fr/actualites/acculturation-ia/)
    """)
    
    # Bouton pour recommencer l'évaluation
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    if st.button("🔄 Recommencer l'évaluation"):
        reset_evaluation()
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Fonction pour réinitialiser l'évaluation
def reset_evaluation():
    st.session_state["responses"] = {}
    st.session_state["question_number"] = 0
    st.session_state["show_results"] = False

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

# Fonction pour afficher les questions
def display_questions():
    current_question_num = st.session_state["question_number"]
    
    if 1 <= current_question_num <= len(questions):
        current_q = questions[current_question_num - 1]
        display_question(current_q, current_question_num)
    else:
        st.session_state["show_results"] = True

# Fonction pour afficher les résultats
def display_results():
    st.markdown("<div class='result-container'>", unsafe_allow_html=True)
    
    # Icône de félicitations
    st.markdown("<div class='icon'>🌟</div>", unsafe_allow_html=True)
    
    # Titre de félicitations
    st.markdown("**Félicitations !**", unsafe_allow_html=True)
    
    # Calcul des scores pour le graphique radar
    competence_scores = {}
    for idx, q in enumerate(questions, 1):
        response = st.session_state["responses"].get(f"Question {idx}", "🔰 Rarement")
        score = responses_scores.get(response, 1)
        theme = q["theme"]
        competence_scores[theme] = score
    
    categories = list(competence_scores.keys())
    values = list(competence_scores.values())
    
    # Calcul du pourcentage de connaissances
    total_score = sum(values)
    max_score = len(values) * 3
    pourcentage = (total_score / max_score) * 100
    
    # Détermination du niveau basé sur le pourcentage avec messages motivants par tranche de 10%
    if pourcentage <= 10:
        niveau = "🟠 Débutant en IA"
        motivation_message = "Il est encore temps d'explorer les bases de l'intelligence artificielle. Continuez à apprendre !"
    elif pourcentage <= 20:
        niveau = "🟡 Sensibilisation Initiale"
        motivation_message = "Vous avez une première approche de l'IA. Poursuivez vos efforts pour mieux comprendre ses applications."
    elif pourcentage <= 30:
        niveau = "🟢 Sensibilisation Approfondie"
        motivation_message = "Vous avez une bonne compréhension des concepts de base de l'IA. Continuez sur cette lancée !"
    elif pourcentage <= 40:
        niveau = "🔵 Compétent en IA"
        motivation_message = "Vous maîtrisez les fondamentaux de l'IA. Il ne vous manque pas grand-chose pour une acculturation réussie !"
    elif pourcentage <= 50:
        niveau = "🟣 Avancé en IA"
        motivation_message = "Vous possédez une solide compréhension de l'IA. Vous êtes presque prêt pour devenir un AS de l'IA !"
    elif pourcentage <= 60:
        niveau = "🟤 Très Avancé en IA"
        motivation_message = "Vous avez toutes les compétences nécessaires pour une acculturation réussie. Prêt à devenir un AS de l'IA ?"
    elif pourcentage <= 70:
        niveau = "🔴 Expert en IA"
        motivation_message = "Votre expertise en IA est impressionnante. Vous êtes un véritable AS de l'IA !"
    elif pourcentage <= 80:
        niveau = "🔵 Maître en IA"
        motivation_message = "Vous maîtrisez parfaitement l'IA. Continuez à partager vos connaissances !"
    elif pourcentage <= 90:
        niveau = "🟢 Grand Maître en IA"
        motivation_message = "Votre compréhension de l'IA est exceptionnelle. Vous êtes un leader dans ce domaine !"
    else:
        niveau = "🌟 Légende de l'IA"
        motivation_message = "Vous êtes une véritable légende de l'IA. Félicitations pour votre expertise inégalée !"
    
    # Afficher le niveau avec une mise en page agréable
    st.markdown(f"### 🔢 Votre Niveau d'Acculturation à l'IA: **{pourcentage:.1f}%**", unsafe_allow_html=True)
    st.markdown(f"### **{niveau}**", unsafe_allow_html=True)
    
    # Ajout d'un espace
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Création du graphique radar avec Plotly
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
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
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Ajout d'un espace
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Message de motivation
    st.markdown(f"""
        <div class='motivation-message'>
            <b>{motivation_message}</b>
        </div>
    """, unsafe_allow_html=True)
    
    # Proposition de formation avec lien
    st.markdown(f"""
        ---
        🎓 **Continuez votre parcours !**
        
        Vous avez obtenu un score de **{pourcentage:.1f}%** dans votre évaluation. Cela démontre une forte compatibilité avec nos formations avancées qui vous permettront de devenir un véritable **pro de l'IA**.
        
        👉 [Découvrez nos formations](https://insidegroup.fr/actualites/acculturation-ia/)
    """)
    
    # Bouton pour recommencer l'évaluation
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    if st.button("🔄 Recommencer l'évaluation"):
        reset_evaluation()
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Fonction pour réinitialiser l'évaluation
def reset_evaluation():
    st.session_state["responses"] = {}
    st.session_state["question_number"] = 0
    st.session_state["show_results"] = False

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
