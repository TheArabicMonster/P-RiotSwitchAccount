import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
import pyautogui
import time
import subprocess
import pickle
import os

# Chemin du fichier où les comptes seront sauvegardés
accounts_file = "accounts.pkl"
config_file = "config.pkl"

# Charger les comptes et la configuration depuis les fichiers
def load_data():
    accounts = {}
    config = {}
    if os.path.exists(accounts_file):
        with open(accounts_file, 'rb') as f:
            accounts = pickle.load(f)
    if os.path.exists(config_file):
        with open(config_file, 'rb') as f:
            config = pickle.load(f)
    return accounts, config

# Sauvegarder les comptes et la configuration dans les fichiers
def save_data(accounts, config):
    with open(accounts_file, 'wb') as f:
        pickle.dump(accounts, f)
    with open(config_file, 'wb') as f:
        pickle.dump(config, f)

# Ajouter un nouveau compte
def add_account():
    username = simpledialog.askstring("Ajouter un compte", "Entrez le pseudo du compte :")
    if username:
        password = simpledialog.askstring("Ajouter un compte", "Entrez le mot de passe :", show='*')
        if password:
            accounts[username] = password
            save_data(accounts, config)
            update_account_list()
        else:
            messagebox.showwarning("Avertissement", "Le mot de passe ne peut pas être vide.")
    else:
        messagebox.showwarning("Avertissement", "Le pseudo ne peut pas être vide.")

# Supprimer un compte
def delete_account():
    username = simpledialog.askstring("Supprimer un compte", "Entrez le pseudo du compte à supprimer :")
    if username in accounts:
        del accounts[username]
        save_data(accounts, config)
        update_account_list()
    else:
        messagebox.showwarning("Avertissement", "Compte non trouvé.")

# Mettre à jour la liste des comptes affichés
def update_account_list():
    listbox.delete(0, tk.END)
    for username in accounts:
        listbox.insert(tk.END, username)

# Ouvrir le client Riot
def open_riot_client():
    if "riot_client_path" in config:
        subprocess.Popen(config["riot_client_path"])
        time.sleep(5)  # Attendre que le client s'ouvre
    else:
        messagebox.showerror("Erreur", "Chemin du client Riot non défini. Veuillez définir le chemin d'exécutable.")

# Se connecter avec les identifiants fournis
def login(username):
    password = accounts[username]
    
    # Fermer la session actuelle si besoin
    pyautogui.hotkey('ctrl', 'shift', 'q')  # Exemple de raccourci pour déconnexion (à ajuster)
    time.sleep(2)
    
    # Saisir le nom d'utilisateur
    pyautogui.click(100, 200)  # Coordonées de la zone de saisie du nom d'utilisateur
    pyautogui.typewrite(username, interval=0.1)
    
    # Saisir le mot de passe
    pyautogui.click(100, 250)  # Coordonées de la zone de saisie du mot de passe
    pyautogui.typewrite(password, interval=0.1)
    
    # Cliquer sur le bouton de connexion
    pyautogui.click(100, 300)  # Coordonées du bouton de connexion
    time.sleep(5)  # Attendre que la connexion s'établisse

# Gérer la sélection d'un compte
def select_account(event):
    selected_account = listbox.get(listbox.curselection())
    open_riot_client()
    login(selected_account)

# Définir le chemin de l'exécutable du client Riot
def set_riot_client_path():
    path = filedialog.askopenfilename(title="Sélectionner l'exécutable Riot Client",
                                      filetypes=[("Executable", "*.exe")])
    if path:
        config["riot_client_path"] = path
        save_data(accounts, config)
        messagebox.showinfo("Information", "Chemin du client Riot défini.")

# Interface utilisateur avec tkinter et ttk
root = tk.Tk()
root.title("Sélecteur de compte Riot Games")
root.geometry("400x300")
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccc")

# Charger les comptes et la configuration
accounts, config = load_data()

# Frame pour les boutons d'ajout et de suppression de compte
frame_buttons = ttk.Frame(root)
frame_buttons.pack(pady=10)

button_add = ttk.Button(frame_buttons, text="Ajouter un compte", command=add_account)
button_add.grid(row=0, column=0, padx=5)

button_delete = ttk.Button(frame_buttons, text="Supprimer un compte", command=delete_account)
button_delete.grid(row=0, column=1, padx=5)

button_set_path = ttk.Button(frame_buttons, text="Définir chemin Riot Client", command=set_riot_client_path)
button_set_path.grid(row=0, column=2, padx=5)

# Liste des comptes
frame_listbox = ttk.Frame(root)
frame_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

listbox = tk.Listbox(frame_listbox, activestyle="dotbox", bg="white", fg="black", highlightcolor="blue", selectbackground="lightblue", selectforeground="black")
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
listbox.bind('<Double-1>', select_account)

scrollbar = ttk.Scrollbar(frame_listbox, orient="vertical", command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

update_account_list()

root.mainloop()