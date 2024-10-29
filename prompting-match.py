# app.py
import sqlite3
from datetime import datetime
import streamlit as st

# Classe pour gérer les opérations sur la base de données
class PromptManager:
    def __init__(self, db_name="prompts.db"):
        self.db_name = db_name
        self.create_table()

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_name)
            return conn
        except sqlite3.Error as e:
            st.error(f"Erreur de connexion à la base de données : {e}")
            return None

    def create_table(self):
        conn = self.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS prompts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        epic TEXT,
                        user_story TEXT,
                        task TEXT,
                        business_rules TEXT,
                        acceptance_criteria TEXT,
                        response TEXT
                    )
                ''')
                conn.commit()
            except sqlite3.Error as e:
                st.error(f"Erreur lors de la création de la table : {e}")
            finally:
                conn.close()

    def save_prompt(self, prompt_data):
        conn = self.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute('''
                    INSERT INTO prompts (date, epic, user_story, task, business_rules, acceptance_criteria, response)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    date,
                    prompt_data.get('epic'),
                    prompt_data.get('user_story'),
                    prompt_data.get('task'),
                    prompt_data.get('business_rules'),
                    prompt_data.get('acceptance_criteria'),
                    prompt_data.get('response')
                ))
                conn.commit()
                st.success("Le prompt a été sauvegardé avec succès.")
                return True
            except sqlite3.Error as e:
                st.error(f"Erreur lors de la sauvegarde du prompt : {e}")
                return False
            finally:
                conn.close()

    def list_prompts(self):
        conn = self.create_connection()
        prompts = []
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT id, date, epic FROM prompts')
                prompts = cursor.fetchall()
            except sqlite3.Error as e:
                st.error(f"Erreur lors de la récupération des prompts : {e}")
            finally:
                conn.close()
        return prompts

    def view_prompt(self, prompt_id):
        conn = self.create_connection()
        prompt = None
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM prompts WHERE id = ?', (prompt_id,))
                prompt = cursor.fetchone()
            except sqlite3.Error as e:
                st.error(f"Erreur lors de la récupération du prompt : {e}")
            finally:
                conn.close()
        return prompt

# Classe pour gérer l'interface Streamlit
class PromptApp:
    def __init__(self):
        self.manager = PromptManager()

    def run(self):
        st.set_page_config(page_title="Gestionnaire de Prompts IA", layout="wide")
        st.title("Gestionnaire de Prompts IA")

        menu = ["Créer Prompt", "Lister Prompts", "Voir Prompt"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Créer Prompt":
            self.create_prompt()
        elif choice == "Lister Prompts":
            self.list_prompts()
        elif choice == "Voir Prompt":
            self.view_prompt()

    def create_prompt(self):
        st.header("Créer un Nouveau Prompt")
        with st.form("prompt_form"):
            epic = st.text_input("Epic (Objectif général)")
            user_story = st.text_input("User Story (Point de vue/Rôle)")
            task = st.text_input("Task (Détails spécifiques)")
            business_rules = st.text_area("Business Rules (Règles de gestion)")
            acceptance_criteria = st.text_area("Acceptance Criteria (Critères de réussite)")
            response = st.text_area("Response (Réponse de l'IA)")
            submitted = st.form_submit_button("Sauvegarder Prompt")

            if submitted:
                prompt_data = {
                    'epic': epic,
                    'user_story': user_story,
                    'task': task,
                    'business_rules': business_rules,
                    'acceptance_criteria': acceptance_criteria,
                    'response': response
                }

                # Vérifier que tous les champs sont remplis
                if all(prompt_data.values()):
                    success = self.manager.save_prompt(prompt_data)
                    if success:
                        st.experimental_rerun()
                else:
                    st.warning("Veuillez remplir tous les champs.")

    def list_prompts(self):
        st.header("Liste des Prompts")
        prompts = self.manager.list_prompts()
        if prompts:
            df = self.convert_to_dataframe(prompts)
            st.dataframe(df)
        else:
            st.info("Aucun prompt trouvé.")

    def view_prompt(self):
        st.header("Voir les Détails d'un Prompt")
        prompt_id = st.text_input("Entrez l'ID du Prompt")
        if st.button("Voir Détails"):
            if prompt_id.isdigit():
                prompt = self.manager.view_prompt(int(prompt_id))
                if prompt:
                    st.subheader(f"Prompt ID {prompt[0]}")
                    st.write(f"**Date :** {prompt[1]}")
                    st.write(f"**Epic :** {prompt[2]}")
                    st.write(f"**User Story :** {prompt[3]}")
                    st.write(f"**Task :** {prompt[4]}")
                    st.write("**Business Rules :**")
                    st.write(prompt[5])
                    st.write("**Acceptance Criteria :**")
                    st.write(prompt[6])
                    st.write("**Response :**")
                    st.write(prompt[7])
                else:
                    st.error("Prompt non trouvé.")
            else:
                st.warning("Veuillez entrer un ID valide.")

    def convert_to_dataframe(self, prompts):
        import pandas as pd
        df = pd.DataFrame(prompts, columns=["ID", "Date", "Epic"])
        return df

# Fonction principale pour lancer l'application
def main():
    app = PromptApp()
    app.run()

if __name__ == "__main__":
    main()
