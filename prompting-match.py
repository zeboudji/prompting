import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

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
            print(f"Erreur de connexion à la base de données : {e}")
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
                print(f"Erreur lors de la création de la table : {e}")
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
                print("Le prompt a été sauvegardé avec succès.")
                return True
            except sqlite3.Error as e:
                print(f"Erreur lors de la sauvegarde du prompt : {e}")
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
                print(f"Erreur lors de la récupération des prompts : {e}")
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
                print(f"Erreur lors de la récupération du prompt : {e}")
            finally:
                conn.close()
        return prompt

# Classe pour gérer l'interface graphique
class PromptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Prompts IA")
        self.manager = PromptManager()

        self.create_widgets()

    def create_widgets(self):
        tab_control = ttk.Notebook(self.root)

        # Onglet de création
        self.create_tab = ttk.Frame(tab_control)
        tab_control.add(self.create_tab, text='Créer Prompt')

        # Onglet de liste
        self.list_tab = ttk.Frame(tab_control)
        tab_control.add(self.list_tab, text='Lister Prompts')

        # Onglet de visualisation
        self.view_tab = ttk.Frame(tab_control)
        tab_control.add(self.view_tab, text='Voir Prompt')

        tab_control.pack(expand=1, fill="both")

        self.create_create_tab()
        self.create_list_tab()
        self.create_view_tab()

    def create_create_tab(self):
        labels = ["Epic", "User Story", "Task", "Business Rules", "Acceptance Criteria", "Response"]
        self.entries = {}
        for idx, label in enumerate(labels):
            ttk.Label(self.create_tab, text=label + " :").grid(row=idx, column=0, padx=10, pady=5, sticky='e')
            if label == "Business Rules" or label == "Acceptance Criteria" or label == "Response":
                entry = tk.Text(self.create_tab, width=50, height=4)
                entry.grid(row=idx, column=1, padx=10, pady=5)
            else:
                entry = ttk.Entry(self.create_tab, width=50)
                entry.grid(row=idx, column=1, padx=10, pady=5)
            self.entries[label.lower().replace(" ", "_")] = entry

        ttk.Button(self.create_tab, text="Sauvegarder Prompt", command=self.save_prompt).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def create_list_tab(self):
        self.tree = ttk.Treeview(self.list_tab, columns=("ID", "Date", "Epic"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Epic", text="Epic")
        self.tree.pack(fill='both', expand=True)
        self.refresh_list_tab()

    def create_view_tab(self):
        ttk.Label(self.view_tab, text="ID du Prompt :").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.view_id_entry = ttk.Entry(self.view_tab, width=20)
        self.view_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        ttk.Button(self.view_tab, text="Voir Détails", command=self.view_prompt).grid(row=0, column=2, padx=10, pady=10)

        self.prompt_details = tk.Text(self.view_tab, width=80, height=20, state='disabled')
        self.prompt_details.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    def save_prompt(self):
        prompt_data = {}
        for key, entry in self.entries.items():
            if isinstance(entry, tk.Text):
                value = entry.get("1.0", tk.END).strip()
            else:
                value = entry.get().strip()
            prompt_data[key] = value

        # Vérifier que tous les champs sont remplis
        if all(prompt_data.values()):
            success = self.manager.save_prompt(prompt_data)
            if success:
                messagebox.showinfo("Succès", "Prompt sauvegardé avec succès.")
                for key, entry in self.entries.items():
                    if isinstance(entry, tk.Text):
                        entry.delete("1.0", tk.END)
                    else:
                        entry.delete(0, tk.END)
                self.refresh_list_tab()
            else:
                messagebox.showerror("Erreur", "Une erreur est survenue lors de la sauvegarde du prompt.")
        else:
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs.")

    def refresh_list_tab(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        prompts = self.manager.list_prompts()
        for prompt in prompts:
            self.tree.insert("", tk.END, values=prompt)

    def view_prompt(self):
        try:
            prompt_id = int(self.view_id_entry.get().strip())
            prompt = self.manager.view_prompt(prompt_id)
            if prompt:
                self.prompt_details.config(state='normal')
                self.prompt_details.delete("1.0", tk.END)
                details = (
                    f"ID : {prompt[0]}\n"
                    f"Date : {prompt[1]}\n"
                    f"Epic : {prompt[2]}\n"
                    f"User Story : {prompt[3]}\n"
                    f"Task : {prompt[4]}\n"
                    f"Business Rules :\n{prompt[5]}\n\n"
                    f"Acceptance Criteria :\n{prompt[6]}\n\n"
                    f"Response :\n{prompt[7]}"
                )
                self.prompt_details.insert(tk.END, details)
                self.prompt_details.config(state='disabled')
            else:
                messagebox.showinfo("Non trouvé", "Aucun prompt trouvé avec cet ID.")
        except ValueError:
            messagebox.showwarning("Entrée invalide", "Veuillez entrer un ID valide.")

# Fonction principale pour lancer l'application
def main():
    root = tk.Tk()
    app = PromptApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
