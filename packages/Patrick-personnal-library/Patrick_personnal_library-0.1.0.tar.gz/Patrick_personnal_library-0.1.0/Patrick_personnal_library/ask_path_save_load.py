from tkinter import Tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import os
from genericpath import exists
from datetime import datetime

def select_path_to_save():
    # Sélectionner le dossier de sauvegarde avec tkinter
        root = Tk()
        root.withdraw()  # Masquer la fenêtre principale de Tkinter
        root.attributes("-topmost", True)  # Mettre la fenêtre au premier plan
        save_path = filedialog.askdirectory(title="Sélectionnez le dossier de destination")
        root.attributes("-topmost", False)  # Retirer l'option après avoir sélectionné
        return save_path

def select_file(for_what, filetypes):
        Tk().withdraw() # Cacher la fenetre principale de Tkinter
        fichier = askopenfilename(
                title=f'Selectionner le fichier {for_what}:',
                filetypes= filetypes
        )
        return fichier

def creer_dossier(path, nom_dossier, main=False):
        if main:
                timestamp = datetime.now().strftime('%Y-%m-%d')
                nom_dossier = f'{nom_dossier}_{timestamp}'

        path_to_create = os.path.join(path, nom_dossier)

        if not os.path.exists(path_to_create):
                os.mkdir(path_to_create)  
                
        return path_to_create 

def ask_yes_no_question(question):
        answer_raw = input (f'{question} (1-oui, 2-non) ?')
        try:
                answer = int(answer_raw)
        except:
                
                print('Entrer 1 ou 2 svp')
                return ask_yes_no_question(question)
        
        if answer == 1:
                return True
        elif answer == 2:
                return False
        else:
                print('Entrer 1 ou 2 svp')
                return ask_yes_no_question(question) 
        
                
                
