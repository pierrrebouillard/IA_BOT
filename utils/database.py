import sqlite3

DB_PATH = "football_stats.db"  # 📌 Vérifie bien que le chemin est correct

def get_db_connection():
    """
    Crée une connexion SQLite avec `check_same_thread=False`, un `timeout=30` pour éviter les blocages,
    et active le mode WAL pour permettre les accès concurrents.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=30, isolation_level=None)
    
    # ✅ Active le mode WAL pour éviter les blocages
    conn.execute("PRAGMA journal_mode=WAL;")
    
    # ✅ Ajoute un timeout pour forcer SQLite à attendre plutôt que de bloquer immédiatement
    conn.execute("PRAGMA busy_timeout = 30000;")  # 30 secondes
    
    return conn

def unlock_database():
    """
    🔓 Force SQLite à libérer la base de données en terminant les transactions bloquées.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("PRAGMA wal_checkpoint(FULL);")  # ✅ Force SQLite à libérer la base
        cursor.execute("PRAGMA journal_mode=WAL;")  # ✅ Réactive WAL pour éviter de futurs blocages
        conn.commit()
        print("✅ Base SQLite libérée avec succès !")

    finally:
        conn.close()  # ✅ Ferme proprement la connexion

def fetch_table_data_as_string(table_name):
    """
    Récupère les données d'une table SQLite et les convertit en une seule chaîne de caractères.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
        if not cursor.fetchone():
            return f"⚠️ Table {table_name} non trouvée."

        # Récupérer toutes les données de la table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Construire une représentation textuelle des données
        table_as_string = "\n".join([", ".join(map(str, row)) for row in rows])

        return table_as_string

    finally:
        conn.close()  # ✅ Assure de fermer la connexion après usage

def list_all_tables():
    """
    Liste toutes les tables disponibles dans la base de données.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]
        return tables

    finally:
        conn.close()  # ✅ Ferme la connexion après usage

def fetch_all_data():
    """
    Récupère toutes les tables et leurs données sous forme de dictionnaire {table_name: data}.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]
        data_dict = {}

        for table in tables:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            data_dict[table] = rows

        return data_dict

    finally:
        conn.close()  # ✅ Ferme la connexion après usage

def insert_test_data():
    """
    Insère des données de test dans une table pour vérifier que la base fonctionne.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER
            )
        """)
        cursor.execute("INSERT INTO test_table (name, age) VALUES (?, ?)", ("Alice", 30))
        cursor.execute("INSERT INTO test_table (name, age) VALUES (?, ?)", ("Bob", 25))
        conn.commit()
        print("✅ Données de test insérées avec succès !")

    finally:
        conn.close()  # ✅ Ferme la connexion après usage

