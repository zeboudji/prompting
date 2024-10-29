import streamlit as st
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="Évaluation des Compétences en IA",
    page_icon="🚀",
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
        padding: 20px;
        background-color: #2e7d32;
        border-radius: 10px;
        text-align: center;
        color: #ffffff;
    }
    /* Style pour les boutons */
    .button-container {
        text-align: center;
        margin-top: 20px;
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
st.markdown("# 🚀 Évaluation Interactive des Compétences en IA et IA Assistée")

# Initialisation de l'état de session avec setdefault pour éviter KeyError
for key in ["responses", "question_number", "show_results", "mode", "profile"]:
    if key not in st.session_state:
        if key == "responses":
            st.session_state[key] = {}
        elif key == "question_number":
            st.session_state[key] = 0
        elif key == "show_results":
            st.session_state[key] = False
        else:
            st.session_state[key] = None

# Définition des questions pour différentes sections
questions = {
    "Formation Technique": [
        {"theme": "Compétences Techniques", "question": "🔍 **À quel point êtes-vous à l'aise avec les langages de programmation (Python, R, etc.) ?**",
         "choices": ["Sélectionnez une réponse", "🟢 Très à l'aise", "🟡 Assez à l'aise", "🔴 Peu à l'aise"]},
        {"theme": "Outils IA", "question": "🤖 **Quelle est votre expérience avec les frameworks d'IA tels que TensorFlow ou PyTorch ?**",
         "choices": ["Sélectionnez une réponse", "🟢 Expérimenté(e)", "🟡 Connaissances de base", "🔴 Aucune expérience"]},
        {"theme": "Gestion de Projet", "question": "📊 **Avez-vous déjà géré des projets impliquant l'intégration de l'IA ?**",
         "choices": ["Sélectionnez une réponse", "🟢 Oui, plusieurs", "🟡 Quelques-uns", "🔴 Aucun"]},
    ],
    "Formation Non Technique": [
        {"theme": "Connaissances de Base", "question": "🔍 **Comprenez-vous les concepts fondamentaux de l'intelligence artificielle et du machine learning ?**",
         "choices": ["Sélectionnez une réponse", "🟢 Oui, bien", "🟡 Moyennement", "🔴 Non"]},
        {"theme": "Utilisation d'Outils", "question": "🛠️ **Avez-vous déjà utilisé des outils d'IA pour des tâches non techniques (ex. marketing, gestion) ?**",
         "choices": ["Sélectionnez une réponse", "🟢 Oui, régulièrement", "🟡 Parfois", "🔴 Jamais"]},
        {"theme": "Adaptabilité", "question": "📚 **Êtes-vous prêt(e) à apprendre et à adopter de nouvelles technologies liées à l'IA ?**",
         "choices": ["Sélectionnez une réponse", "🟢 Très prêt(e)", "🟡 Assez prêt(e)", "🔴 Pas vraiment"]},
    ],
    "Projet IA": [
        {"theme": "Connaissances Numériques", "question": "💻 **À quel point êtes-vous à l'aise avec l'utilisation des technologies numériques dans votre travail actuel ?**",
         "choices": ["Sélectionnez une réponse", "🟢 Très à l'aise", "🟡 Assez à l'aise", "🔴 Peu à l'aise"]},
        {"theme": "Utilisation d'Outils Automatisés", "question": "🔧 **Votre emploi actuel implique-t-il l'utilisation fréquente de logiciels ou d'outils automatisés ?**",
         "choices": ["Sélectionnez une réponse", "🟢 Fréquemment", "🟡 Parfois", "🔴 Rarement"]},
        {"theme": "Expérience avec l'IA", "question": "🤖 **Quelle est votre expérience avec les technologies d'intelligence artificielle (IA) ou d'apprentissage automatique (Machine Learning) ?**",
         "choices": ["Sélectionnez une réponse", "🟢 Expérimenté(e)", "🟡 Connaissances de base", "🔴 Aucune expérience"]},
        {"theme": "Capacité d'Apprentissage", "question": "📚 **Comment évaluez-vous votre capacité à apprendre et à adopter de nouvelles technologies dans votre domaine ?**",
         "choices": ["Sélectionnez une réponse", "🟢 Très bonne", "🟡 Moyenne", "🔴 Faible"]},
        {"theme": "Impact de l'IA sur le Travail", "question": "🚀 **Dans quelle mesure pensez-vous que l'IA pourrait améliorer l'efficacité de votre travail ?**",
         "choices": ["Sélectionnez une réponse", "🟢 Beaucoup", "🟡 Modérément", "🔴 Peu"]},
        {"theme": "Bénéfices Potentiels de l'IA", "question": "🎯 **Quels aspects de votre travail actuel pensez-vous pourraient bénéficier d'une automatisation ou d'une assistance par l'IA ?**",
         "choices": ["Sélectionnez une réponse", "🟢 Tâches répétitives", "🟡 Analyse de données", "🔴 Créativité et prise de décision"]},
    ]
}

# Mapping des réponses à un score numérique pour le graphique radar
responses_scores = {
    "🟢 Très à l'aise": 3, "🟡 Assez à l'aise": 2, "🔴 Peu à l'aise": 1,
    "🟢 Expérimenté(e)": 3, "🟡 Connaissances de base": 2, "🔴 Aucune expérience": 1,
    "🟢 Oui, bien": 3, "🟡 Moyennement": 2, "🔴 Non": 1,
    "🟢 Oui, régulièrement": 3, "🟡 Parfois": 2, "🔴 Jamais": 1,
    "🟢 Très prêt(e)": 3, "🟡 Assez prêt(e)": 2, "🔴 Pas vraiment": 1,
    "🟢 Fréquemment": 3, "🟡 Parfois": 2, "🔴 Rarement": 1,
    "🟢 Très bonne": 3, "🟡 Moyenne": 2, "🔴 Faible": 1,
    "🟢 Beaucoup": 3, "🟡 Modérément": 2, "🔴 Peu": 1,
    "🟢 Tâches répétitives": 3, "🟡 Analyse de données": 2, "🔴 Créativité et prise de décision": 1
}

def reset_evaluation():
    """Réinitialiser l'évaluation"""
    for key in ["responses", "question_number", "show_results", "mode", "profile"]:
        if key == "responses":
            st.session_state[key] = {}
        elif key == "question_number":
            st.session_state[key] = 0
        elif key == "show_results":
            st.session_state[key] = False
        else:
            st.session_state[key] = None

def select_mode():
    """Sélectionner le mode : Projet IA ou Formation IA"""
    st.markdown("## 📋 Choisissez votre objectif")
    mode = st.radio("Voulez-vous utiliser ce questionnaire pour :", 
                    ("Sélectionnez une option", "Projet IA", "Formation IA"), 
                    key="mode_selection")
    if mode != "Sélectionnez une option":
        st.session_state["mode"] = mode
        st.session_state["question_number"] += 1

def select_profile():
    """Sélectionner le profil : Technique ou Non Technique"""
    st.markdown("## 🎓 Sélectionnez votre profil")
    profile = st.radio("Pour une Formation IA, veuillez indiquer votre profil :", 
                       ("Sélectionnez une option", "Technique", "Non Technique"), 
                       key="profile_selection")
    if profile != "Sélectionnez une option":
        st.session_state["profile"] = profile
        st.session_state["question_number"] += 1

def display_question(question, choices, question_num, total_questions):
    """Afficher une question avec ses choix et le fil d'Ariane"""
    # Récupérer le thème de la question courante
    theme = questions[current_section][question_num - 1]["theme"]

    # Création du fil d'Ariane avec thèmes
    breadcrumb = '<ul class="breadcrumb">'
    for i in range(1, total_questions+1):
        if i < question_num:
            breadcrumb += f'<li><span class="active">{questions[current_section][i-1]["theme"]}</span></li>'
        elif i == question_num:
            breadcrumb += f'<li><span class="active">{questions[current_section][i-1]["theme"]}</span></li>'
        else:
            breadcrumb += f'<li>{questions[current_section][i-1]["theme"]}</li>'
    breadcrumb += '</ul>'
    st.markdown(breadcrumb, unsafe_allow_html=True)
    
    # Affichage de la question
    st.markdown(f"<div class='question-container'><b>{question}</b></div>", unsafe_allow_html=True)
    
    # Gestion des réponses avec callback
    selected = st.radio("Sélectionnez une réponse :", choices, key=f"response_{question_num}")
    
    if selected != "Sélectionnez une réponse":
        st.session_state["responses"][f"Question {question_num}"] = selected
        st.session_state["question_number"] += 1
    else:
        st.markdown("<span class='error-message'>Veuillez sélectionner une réponse valide.</span>", unsafe_allow_html=True)

def display_questions():
    """Afficher les questions en fonction du mode et du profil"""
    if st.session_state["mode"] == "Formation IA":
        if st.session_state["profile"] == "Technique":
            current_section = "Formation Technique"
        else:
            current_section = "Formation Non Technique"
    elif st.session_state["mode"] == "Projet IA":
        current_section = "Projet IA"
    else:
        current_section = None  # Pour éviter les erreurs

    if current_section:
        current_question_num = st.session_state["question_number"]
        total_questions = len(questions[current_section])
        
        if current_question_num <= total_questions:
            current_q = questions[current_section][current_question_num - 1]
            display_question(current_q["question"], current_q["choices"], current_question_num, total_questions)
        else:
            st.session_state["show_results"] = True
    else:
        st.error("Mode inconnu. Veuillez réinitialiser l'évaluation.")

def display_results():
    """Afficher les résultats après l'évaluation"""
    st.markdown("<div class='result-container'><h2>🌟 Félicitations ! 🌟</h2></div>", unsafe_allow_html=True)
    st.balloons()
    
    # Déterminer le mode actuel
    mode = st.session_state["mode"]
    
    # Déterminer le profil si mode est Formation IA
    if mode == "Formation IA":
        profile = st.session_state["profile"]
        if profile == "Technique":
            current_section = "Formation Technique"
        else:
            current_section = "Formation Non Technique"
    elif mode == "Projet IA":
        current_section = "Projet IA"
    else:
        current_section = None  # Pour éviter les erreurs

    # Calcul des scores pour le graphique radar
    competence_scores = {}
    for idx, q in enumerate(questions[current_section], 1):
        response = st.session_state["responses"].get(f"Question {idx}", "🔴 Aucun")
        score = responses_scores.get(response, 1)
        competence_scores[q["theme"]] = score

    categories = list(competence_scores.keys())
    values = list(competence_scores.values())

    # Calcul du pourcentage de connaissances
    total_score = sum(values)
    max_score = len(values) * 3
    pourcentage = (total_score / max_score) * 100

    # Détermination du niveau basé sur le pourcentage
    if mode == "Formation IA":
        if pourcentage < 60:
            niveau = "🎓 Sensibilisation à l'IA"
            niveau_message = "Vous êtes éligible à la **Sensibilisation** pour mieux comprendre les fondamentaux de l'IA. Toutes les conditions sont réunies !"
        else:
            niveau = "🚀 Acculturation pour devenir un AS de l'IA"
            niveau_message = "Félicitations ! Vous êtes éligible à l'**Acculturation** pour devenir un **AS de l'IA**. Toutes les conditions sont réunies !"
    elif mode == "Projet IA":
        if pourcentage < 60:
            niveau = "🛠️ Prérequis insuffisants"
            niveau_message = "Il semble que vous n'ayez pas encore les prérequis nécessaires pour lancer un projet IA. Découvrez nos formations pour vous préparer."
        else:
            niveau = "✅ Prérequis satisfaits"
            niveau_message = "Vous possédez les prérequis nécessaires pour démarrer un projet IA. Contactez-nous pour bénéficier de notre expertise et de nos services d'accompagnement."
    else:
        niveau = "Inconnu"
        niveau_message = "Mode inconnu."

    # Afficher le pourcentage et le niveau
    st.markdown(f"### 🔢 Votre Niveau de Compétence en IA: **{pourcentage:.1f}%**")
    st.markdown(f"### **{niveau}**")

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

    # Message de niveau
    st.markdown(f"""
        <div style='text-align: center; padding: 10px;'>
            <b>{niveau_message}</b>
        </div>
    """, unsafe_allow_html=True)

    # Proposition de formation avec lien
    if mode == "Formation IA":
        st.markdown(f"""
            ---
            🎓 **Continuez votre parcours !**
            
            Vous avez obtenu un score de **{pourcentage:.1f}%** dans votre évaluation. Cela démontre une forte compatibilité avec nos formations avancées qui vous permettront de devenir un véritable **pro de l'IA**.
            
            👉 [Découvrez nos formations](https://insidegroup.fr/actualites/acculturation-ia/)
        """)
    elif mode == "Projet IA":
        if pourcentage < 60:
            st.markdown(f"""
                ---
                🛠️ **Préparez-vous pour votre Projet IA !**
                
                Il semble que vous ayez besoin de renforcer certaines compétences avant de vous lancer dans un projet IA. Nos formations sont conçues pour vous accompagner dans ce processus.
                
                👉 [Découvrez nos formations](https://insidegroup.fr/actualites/acculturation-ia/)
            """)
        else:
            st.markdown(f"""
                ---
                ✅ **Lancez votre Projet IA !**
                
                Vous possédez les prérequis nécessaires pour démarrer un projet IA. Contactez-nous pour bénéficier de notre expertise et de nos services d'accompagnement.
                
                👉 [Contactez-nous](https://insidegroup.fr/actualites/acculturation-ia/)
            """)

    # Bouton pour recommencer l'évaluation
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    if st.button("🔄 Recommencer l'évaluation"):
        reset_evaluation()
    st.markdown("</div>", unsafe_allow_html=True)

# Afficher le mode de l'utilisateur
if not st.session_state["mode"]:
    select_mode()
elif st.session_state["mode"] == "Formation IA" and not st.session_state["profile"]:
    select_profile()
elif not st.session_state["show_results"]:
    display_questions()
else:
    display_results()
