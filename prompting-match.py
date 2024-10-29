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

# Initialisation de l'état de session
if "responses" not in st.session_state:
    st.session_state["responses"] = {}
    st.session_state["question_number"] = 0
    st.session_state["show_results"] = False

# Définition des questions avec emojis et options adaptées au métier
questions = [
    ("🔍 **À quel point êtes-vous à l'aise avec l'utilisation des technologies numériques dans votre travail actuel ?**",
     ["Sélectionnez une réponse", "🟢 Très à l'aise", "🟡 Assez à l'aise", "🔴 Peu à l'aise"]),
    ("💼 **Dans quelle mesure votre emploi actuel implique-t-il l'utilisation de logiciels ou d'outils automatisés ?**",
     ["Sélectionnez une réponse", "🟢 Fréquemment", "🟡 Parfois", "🔴 Rarement"]),
    ("📚 **Quelle est votre expérience avec les technologies d'intelligence artificielle (IA) ou d'apprentissage automatique (Machine Learning) ?**",
     ["Sélectionnez une réponse", "🟢 Expérimenté(e)", "🟡 Connaissances de base", "🔴 Aucune expérience"]),
    ("📝 **Comment évaluez-vous votre capacité à apprendre et à adopter de nouvelles technologies dans votre domaine ?**",
     ["Sélectionnez une réponse", "🟢 Très bonne", "🟡 Moyenne", "🔴 Faible"]),
    ("🤖 **Dans quelle mesure pensez-vous que l'IA pourrait améliorer l'efficacité de votre travail ?**",
     ["Sélectionnez une réponse", "🟢 Beaucoup", "🟡 Modérément", "🔴 Peu"]),
    ("🎯 **Quels aspects de votre travail actuel pensez-vous pourraient bénéficier d'une automatisation ou d'une assistance par l'IA ?**",
     ["Sélectionnez une réponse", "🟢 Tâches répétitives", "🟡 Analyse de données", "🔴 Créativité et prise de décision"])
]

# Mapping des réponses à un score numérique pour le graphique radar
responses_scores = {
    "🟢 Très à l'aise": 3, "🟡 Assez à l'aise": 2, "🔴 Peu à l'aise": 1,
    "🟢 Fréquemment": 3, "🟡 Parfois": 2, "🔴 Rarement": 1,
    "🟢 Expérimenté(e)": 3, "🟡 Connaissances de base": 2, "🔴 Aucune expérience": 1,
    "🟢 Très bonne": 3, "🟡 Moyenne": 2, "🔴 Faible": 1,
    "🟢 Beaucoup": 3, "🟡 Modérément": 2, "🔴 Peu": 1,
    "🟢 Tâches répétitives": 3, "🟡 Analyse de données": 2, "🔴 Créativité et prise de décision": 1
}

def save_response(response, question_num):
    """Sauvegarder la réponse et passer à la question suivante"""
    st.session_state["responses"][f"Question {question_num}"] = response
    st.session_state["question_number"] += 1

# Fonction pour afficher une question avec fil d'Ariane
def display_question(question_text, choices, question_num):
    # Création du fil d'Ariane
    breadcrumb = '<ul class="breadcrumb">'
    for i in range(1, len(questions)+1):
        if i < question_num:
            breadcrumb += f'<li><span class="active">Étape {i}</span></li>'
        elif i == question_num:
            breadcrumb += f'<li><span class="active">Étape {i}</span></li>'
        else:
            breadcrumb += f'<li>Étape {i}</li>'
    breadcrumb += '</ul>'
    st.markdown(breadcrumb, unsafe_allow_html=True)
    
    st.markdown(f"<div class='question-container'><b>{question_text}</b></div>", unsafe_allow_html=True)
    
    def on_change():
        selected = st.session_state[f"response_{question_num}"]
        if selected != "Sélectionnez une réponse":
            save_response(selected, question_num)
    
    selected = st.radio("Sélectionnez une réponse :", choices, key=f"response_{question_num}", on_change=on_change)
    
    if selected == "Sélectionnez une réponse":
        st.markdown("<span class='error-message'>Veuillez sélectionner une réponse valide.</span>", unsafe_allow_html=True)

# Fonction pour afficher les résultats
def display_results():
    st.markdown("<div class='result-container'><h2>🌟 Félicitations ! 🌟</h2></div>", unsafe_allow_html=True)
    st.balloons()
    
    # Calcul des scores pour le graphique radar
    competence_scores = {
        "Confort Numérique": responses_scores.get(st.session_state["responses"].get("Question 1", "🔴 Peu à l'aise"), 1),
        "Utilisation d'Outils Automatisés": responses_scores.get(st.session_state["responses"].get("Question 2", "🔴 Rarement"), 1),
        "Expérience avec l'IA": responses_scores.get(st.session_state["responses"].get("Question 3", "🔴 Aucune expérience"), 1),
        "Capacité d'Apprentissage": responses_scores.get(st.session_state["responses"].get("Question 4", "🔴 Faible"), 1),
        "Impact de l'IA sur le Travail": responses_scores.get(st.session_state["responses"].get("Question 5", "🔴 Peu"), 1),
        "Bénéfices Potentiels de l'IA": responses_scores.get(st.session_state["responses"].get("Question 6", "🔴 Créativité et prise de décision"), 1)
    }
    
    categories = list(competence_scores.keys())
    values = list(competence_scores.values())
    
    # Calcul du pourcentage de connaissances
    total_score = sum(values)
    max_score = len(values) * 3
    pourcentage = (total_score / max_score) * 100
    
    # Détermination du niveau basé sur le pourcentage
    if pourcentage < 60:
        niveau = "🎓 Sensibilisation à l'IA"
        niveau_message = "Vous êtes éligible à la **Sensibilisation** pour mieux comprendre les fondamentaux de l'IA. Toutes les conditions sont réunies !"
    else:
        niveau = "🚀 Acculturation pour devenir un AS de l'IA"
        niveau_message = "Félicitations ! Vous êtes éligible à l'**Acculturation** pour devenir un **AS de l'IA**. Toutes les conditions sont réunies !"
    
    # Afficher le pourcentage et le niveau
    st.markdown(f"### 🔢 Votre Niveau de Connaissance en IA: **{pourcentage:.1f}%**")
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
        question_text, choices = current_q
        display_question(question_text, choices, current_question_num)
    else:
        st.session_state["show_results"] = True

if st.session_state["show_results"]:
    display_results()
