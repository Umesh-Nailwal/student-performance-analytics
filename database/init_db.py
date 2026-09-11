from services.utility import get_db, get_config_db
def create_tables():
    conn = get_db()
    # Enable Foreign Key support in SQLite
    conn.execute("PRAGMA foreign_keys = ON")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

   
    conn.execute("""
        CREATE TABLE IF NOT EXISTS std_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll TEXT,
            name TEXT,
            branch TEXT,
            admission_year INTEGER,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(roll, branch, admission_year, user_id) 
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS results (
            student_id INTEGER ,
            semester INTEGER,
            marks REAL,
            attendance REAL,
            percentage REAL,
            grade TEXT,
            performance TEXT,
            risk TEXT,
            PRIMARY KEY (student_id, semester),
            FOREIGN KEY (student_id) REFERENCES std_list(id) ON DELETE CASCADE
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
            PRIMARY KEY (branch, semester, user_id)
        )
    """)
    conn.commit()
    conn.close()
def init_db():
	create_tables()
	create_config()