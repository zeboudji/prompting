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
    </style>
    """, unsafe_allow_html=True)

# Titre principal
st.markdown("# 🚀 Évaluation Interactive des Compétences en Prompting IA")

# Initialisation de l'état de session
if "responses" not in st.session_state:
    st.session_state["responses"] = {}
    st.session_state["question_number"] = 0
    st.session_state["show_results"] = False

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

# Mapping des réponses à un score numérique pour le graphique radar
responses_scores = {
    "🔰 Débutant(e)": 1, "📘 Intermédiaire": 2, "🌟 Avancé(e)": 3,
    "❓ Pas familier(e) avec ces termes": 1, "📙 Non, mais curieux(se) d’en apprendre plus": 2, "✅ Oui": 3,
    "⚠️ Besoin d’amélioration": 1, "📄 Clair, mais manque parfois de détails": 2, "📝 Très clair et structuré": 3,
    "❌ Non, je ne suis pas sûr(e) de comment faire": 1, "🔄 J’ai quelques idées, mais je pourrais m’améliorer": 2, "✔️ Oui, j’utilise cette approche régulièrement": 3,
    "🛑 Peu adaptable": 1, "😊 Souvent adaptable": 2, "🗣 Très adaptable": 3,
    "🚧 Peu structuré": 1, "📈 Parfois structuré": 2, "📊 Très structuré": 3
}

def save_response(response, question_num):
    """Sauvegarder la réponse et passer à la question suivante"""
    st.session_state["responses"][f"Question {question_num}"] = response
    st.session_state["question_number"] += 1
    if st.session_state["question_number"] >= len(questions):
        st.session_state["show_results"] = True

# Fonction pour afficher une question
def display_question(question_text, choices, question_num):
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
        "Familiarité": responses_scores.get(st.session_state["responses"].get("Question 1", "🔰 Débutant(e)"), 1),
        "Expérience Agile": responses_scores.get(st.session_state["responses"].get("Question 2", "❓ Pas familier(e) avec ces termes"), 1),
        "Clarté": responses_scores.get(st.session_state["responses"].get("Question 3", "⚠️ Besoin d’amélioration"), 1),
        "Diviser une Tâche": responses_scores.get(st.session_state["responses"].get("Question 4", "❌ Non, je ne suis pas sûr(e) de comment faire"), 1),
        "Adaptabilité du Ton": responses_scores.get(st.session_state["responses"].get("Question 5", "🛑 Peu adaptable"), 1),
        "Structure des Réponses": responses_scores.get(st.session_state["responses"].get("Question 6", "🚧 Peu structuré"), 1)
    }
    
    categories = list(competence_scores.keys())
    values = list(competence_scores.values())
    
    # Calcul du pourcentage de connaissances
    total_score = sum(values)
    max_score = len(values) * 3
    pourcentage = (total_score / max_score) * 100
    
    # Afficher le pourcentage au-dessus du radar
    st.markdown(f"### 🔢 Votre Niveau de Connaissance en IA: **{pourcentage:.1f}%**")
    
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
    
    # Proposition de formation
    st.markdown(f"""
        ---
        🎓 **Félicitations !** 🎓
        
        Vous avez obtenu un score de **{pourcentage:.1f}%** dans votre évaluation. Cela démontre une forte compatibilité avec nos formations avancées qui vous permettront de devenir un véritable **pro de l'IA**.
        
        👉 [Découvrez nos formations](https://votre-site.com/formations)
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
    st.experimental_rerun()

# Affichage des questions ou des résultats selon l'état
if not st.session_state["show_results"]:
    if st.session_state["question_number"] < len(questions):
        current_question_num = st.session_state["question_number"] + 1
        current_q = questions[st.session_state["question_number"]]
        question_text, choices = current_q
        display_question(question_text, choices, current_question_num)
    else:
        st.session_state["show_results"] = True
        st.experimental_rerun()

if st.session_state["show_results"]:
    display_results()
