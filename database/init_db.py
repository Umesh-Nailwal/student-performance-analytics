from services.utility import get_db, get_config_db
def create_tables():
    conn = get_db()
    # Enable Foreign Key support in SQLite
    conn.execute("PRAGMA foreign_keys = ON")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

   
    conn.execute("""
        CREATE TABLE IF NOT EXISTS std_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll TEXT  NOT NULL,
            name TEXT NOT NULL,
            branch TEXT NOT NULL,
            admission_year INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(roll, branch, admission_year, user_id) 
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS results (
            student_id INTEGER NOT NULL,
            semester INTEGER NOT NULL,
            marks REAL NOT NULL,
            attendance REAL NOT NULL,
            percentage REAL NOT NULL,
            grade TEXT NOT NULL,
            performance TEXT NOT NULL,
            risk TEXT NOT NULL,
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
            branch TEXT NOT NULL,
            semester INTEGER NOT NULL,
            total_marks INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            PRIMARY KEY (branch, semester, user_id)
        )
    """)
    conn.commit()
    conn.close()
def init_db():
	create_tables()
	create_config()