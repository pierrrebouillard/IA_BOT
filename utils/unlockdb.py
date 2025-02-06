import sqlite3

DB_PATH = "football_stats.db"  # Vérifie que le chemin est correct

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 🔥 Libère la base SQLite
    cursor.execute("PRAGMA wal_checkpoint(FULL);")  
    cursor.execute("PRAGMA journal_mode=WAL;")  # ✅ Active le mode WAL pour éviter les verrous
    conn.commit()
    conn.close()

    print("✅ Base SQLite libérée avec succès !")

except sqlite3.Error as e:
    print(f"❌ Erreur SQLite : {e}")