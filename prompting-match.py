import streamlit as st
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="Niveau d'acculturation à l'IA",
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
        "theme": "Familiarité avec les Concepts",
        "question": "🔍 **Les notions de prompt et de GPT vous parlent-elles ?**",
        "choices": ["Sélectionnez une réponse", "🔰 Débutant(e)", "📘 Intermédiaire", "🌟 Avancé(e)"]
    },
    {
        "theme": "Compréhension de RAG",
        "question": "🤖 **Connaissez-vous les concepts de RAG (Retrieval-Augmented Generation) ?**",
        "choices": ["Sélectionnez une réponse", "❓ Pas familier(e)", "🧠 Je connais les bases", "🚀 Je suis expérimenté(e)"]
    },
    {
        "theme": "Utilisation des Outils IA",
        "question": "📈 **Utilisez-vous des outils d'IA dans vos tâches quotidiennes ?**",
        "choices": ["Sélectionnez une réponse", "✅ Oui, régulièrement", "📉 Parfois", "❌ Jamais"]
    },
    {
        "theme": "Machine Learning",
        "question": "🧠 **Quel est votre niveau de compréhension du machine learning ?**",
        "choices": ["Sélectionnez une réponse", "📚 Compréhension de base", "🔍 Compréhension intermédiaire", "🚀 Expertise avancée"]
    },
    {
        "theme": "Intégration de Modèles IA",
        "question": "🛠️ **Avez-vous déjà intégré des modèles d'IA dans vos projets professionnels ?**",
        "choices": ["Sélectionnez une réponse", "✅ Oui, plusieurs fois", "🟡 Une ou deux fois", "🔴 Non, jamais"]
    },
    {
        "theme": "Rédaction de Prompts",
        "question": "📝 **Comment évalueriez-vous votre capacité à rédiger des prompts efficaces pour l'IA ?**",
        "choices": ["Sélectionnez une réponse", "📝 Très efficace", "📄 Moyennement efficace", "⚠️ Peu efficace"]
    },
    {
        "theme": "Gestion de Projets Complexes",
        "question": "🔄 **Dans quelle mesure savez-vous diviser un projet complexe en étapes plus petites pour faciliter l'interaction avec l'IA ?**",
        "choices": ["Sélectionnez une réponse", "✔️ Oui, j’utilise cette approche régulièrement", "🔄 J’ai quelques idées, mais je pourrais m’améliorer", "❌ Non, je ne suis pas sûr(e) de comment faire"]
    },
    {
        "theme": "Adaptabilité des Prompts",
        "question": "🗣️ **Comment évalueriez-vous votre capacité à adapter le ton et le style des prompts en fonction du contexte de votre projet ?**",
        "choices": ["Sélectionnez une réponse", "🗣️ Très adaptable", "😊 Souvent adaptable", "🛑 Peu adaptable"]
    },
    {
        "theme": "Structuration des Réponses IA",
        "question": "📊 **Comment évalueriez-vous votre capacité à structurer les réponses de l'IA pour obtenir des informations claires et organisées dans vos rapports ou présentations ?**",
        "choices": ["Sélectionnez une réponse", "📊 Très structuré", "📈 Parfois structuré", "🚧 Peu structuré"]
    }
]

# Mapping des réponses à un score numérique pour le graphique radar
responses_scores = {
    "🔰 Débutant(e)": 1, "📘 Intermédiaire": 2, "🌟 Avancé(e)": 3,
    "❓ Pas familier(e)": 1, "🧠 Je connais les bases": 2, "🚀 Je suis expérimenté(e)": 3,
    "✅ Oui, régulièrement": 3, "📉 Parfois": 2, "❌ Jamais": 1,
    "📚 Compréhension de base": 1, "🔍 Compréhension intermédiaire": 2, "🚀 Expertise avancée": 3,
    "✅ Oui, plusieurs fois": 3, "🟡 Une ou deux fois": 2, "🔴 Non, jamais": 1,
    "📝 Très efficace": 3, "📄 Moyennement efficace": 2, "⚠️ Peu efficace": 1,
    "✔️ Oui, j’utilise cette approche régulièrement": 3, "🔄 J’ai quelques idées, mais je pourrais m’améliorer": 2, "❌ Non, je ne suis pas sûr(e) de comment faire": 1,
    "🗣️ Très adaptable": 3, "😊 Souvent adaptable": 2, "🛑 Peu adaptable": 1,
    "📊 Très structuré": 3, "📈 Parfois structuré": 2, "🚧 Peu structuré": 1
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
    st.markdown("<div class='result-container'><h2>🌟 Félicitations ! 🌟</h2></div>", unsafe_allow_html=True)
    st.balloons()
    
    # Calcul des scores pour le graphique radar
    competence_scores = {}
    for idx, q in enumerate(questions, 1):
        response = st.session_state["responses"].get(f"Question {idx}", "🔰 Débutant(e)")
        score = responses_scores.get(response, 1)
        theme = q["theme"]
        competence_scores[theme] = score
    
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
    st.markdown(f"### 🔢 Votre Niveau d'Acculturation à l'IA: **{pourcentage:.1f}%**")
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
        display_question(current_q, current_question_num)
    else:
        st.session_state["show_results"] = True

if st.session_state["show_results"]:
    display_results()
