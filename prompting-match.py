import streamlit as st
import plotly.graph_objects as go

# Titre avec Emoji
st.markdown("# 🚀 Évaluation Interactive des Compétences en Prompting IA")

# Initialisation de l'état de session
if "responses" not in st.session_state:
    st.session_state["responses"] = {}
    st.session_state["question_number"] = 0
    st.session_state["show_results"] = False

def next_question():
    """Fonction pour passer à la question suivante"""
    st.session_state["question_number"] += 1

def reset_evaluation():
    """Fonction pour recommencer l'évaluation"""
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

# Affichage des questions
if st.session_state["show_results"] == False:
    if st.session_state["question_number"] < len(questions):
        current_q = questions[st.session_state["question_number"]]
        question_text, choices = current_q
        st.markdown(f"<div style='padding: 20px; background-color: #e3f2fd; border-radius: 10px; color: #0d47a1;'><b>{question_text}</b></div>", unsafe_allow_html=True)
        
        selected = st.selectbox("Sélectionnez une réponse :", choices)
        
        if st.button("Suivant"):
            if selected != "Sélectionnez une réponse":
                st.session_state["responses"][f"Question {st.session_state['question_number'] +1}"] = selected
                next_question()
            else:
                st.error("Veuillez sélectionner une réponse valide.")
    else:
        # Toutes les questions ont été répondues, afficher le bouton pour voir les résultats
        if st.button("Voir les Résultats"):
            st.session_state["show_results"] = True

# Affichage des résultats
if st.session_state["show_results"]:
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
                range=[0, 3]
            ),
            angularaxis=dict(showline=True, linecolor="lightgrey")
        ),
        showlegend=False
    )
    
    st.plotly_chart(fig)
    
    # Calcul du pourcentage de connaissances
    total_score = sum(values)
    max_score = len(values) * 3
    pourcentage = (total_score / max_score) * 100
    
    st.metric("🔢 Votre Niveau de Connaissance en IA", f"{pourcentage:.1f}%")
    
    # Proposition de formation
    st.markdown(f"""
        ---
        🎓 **Prolongez votre apprentissage !**
        
        Vous avez obtenu un score de **{pourcentage:.1f}%** dans votre évaluation. Pour perfectionner vos connaissances et pratiques en IA et en prompting, découvrez nos **formations personnalisées** adaptées à votre niveau.
        
        👉 [Découvrez nos formations](https://votre-site.com/formations)
    """)
    
    # Bouton pour recommencer l'évaluation
    if st.button("🔄 Recommencer l'évaluation"):
        reset_evaluation()
