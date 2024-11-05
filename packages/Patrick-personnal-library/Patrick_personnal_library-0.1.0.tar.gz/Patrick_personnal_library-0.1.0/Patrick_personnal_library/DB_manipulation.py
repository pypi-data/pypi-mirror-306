import sqlite3
import os

def build_list_for_one_colonne_to_create_DB(name, TYPE="INTEGER", PRIMARY_KEY=False, AUTOINCREMENT=False, NOT_NULL=False, UNIQUE=False):
    """Crée une liste pour définir une colonne dans la base de données.

    Args:
        name (str): Le nom de la colonne.
        TYPE (str): Type de données de la colonne (en majuscules, ex : INTEGER). Par défaut INTEGER.
        PRIMARY_KEY (bool, optional): Définit si c'est une clé primaire. Par défaut False.
        AUTOINCREMENT (bool, optional): Définit si la colonne s'auto-incrémente. Par défaut False.
        NOT_NULL (bool, optional): Définit si la colonne doit obligatoirement avoir une valeur. Par défaut False.
        UNIQUE (bool, optional): Définit si la valeur doit être unique. Par défaut False.

    Returns:
        list: Liste des propriétés de la colonne.
    """
    # Initialise la liste avec le nom de la colonne et son type
    liste_colonne = [name, TYPE]
    
    # Ajoute les contraintes en fonction des paramètres
    if PRIMARY_KEY:
        liste_colonne.append("PRIMARY KEY")
    if AUTOINCREMENT:
        liste_colonne.append("AUTOINCREMENT")
    if NOT_NULL:
        liste_colonne.append("NOT NULL")
    if UNIQUE:
        liste_colonne.append("UNIQUE")
    
    return liste_colonne      



"""def create_DB(db_name:str, list_of_list_name_config:list):
    # Connexion à la base de données (ou création si elle n'existe pas)
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
"""

def initialize_database(db_name):
    # Connexion à la base de données (ou création si elle n'existe pas)
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Définition d'une requête SQL pour créer une table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    connection.close()
    print(f"La base de données '{db_name}' et la table 'users' ont été créées.")


def insert_in_DB_from_excel(db_path, table, colonnes, valeurs, fichier_excel):
    try:
        # Connexion a la base de donnee
        connexion = sqlite3.connect(db_path)
        curseur = connexion.cursor()
        # creer la requete d'insertion
        colonnes_str = ', '.join([f'"{colonne}"' for colonne in colonnes])
        placeholders = ', '.join(['?'] * len(valeurs))
        requete = f"INSERT INTO {table} ({colonnes_str}) VALUES ({placeholders})"
        # print(f"Requete SQL: {requeste})          # Pour Debugger seulement
        # print(f"Valeurs : {valeurs}")             # Pour Debugger seulement
        # Executer la requete d'insertion
        curseur.execute(requete, valeurs)
        # Valider les changements
        connexion.commit()
        nom_fichier_excel = os.path.basename(fichier_excel)
        print(f"Insertion reussi du fichier : {nom_fichier_excel}.")
    except:
        print(f"Erreur lors de l'insertion dans la base de donnee : {e}")
    finally:
        #fermer la connexion
        connexion.close()




