from services.utility import get_db, get_config_db

# ---------------- DATABASE ----------------

def create_tables():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS std_list (
            roll TEXT,
            name TEXT,
            branch TEXT,
            admission_year INTEGER,
            user_id INTEGER,
            PRIMARY KEY (roll, branch,user_id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS results (
            roll TEXT,
            branch TEXT,
            semester INTEGER,
            marks REAL,
            attendance REAL,
            percentage REAL,
            grade TEXT,
            performance TEXT,
            risk TEXT,
            user_id INTEGER,
            PRIMARY KEY (roll, semester, branch,user_id)
        )
    """)

    conn.commit()
    conn.close()

def create_config():
    conn = get_config_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS config (
            branch TEXT,
            semester INTEGER,
            total_marks INTEGER,
            user_id INTEGER,
            PRIMARY KEY (branch, semester)
        )
    """)

    conn.commit()
    conn.close()
    
def init_db():
	create_tables()
	create_config()