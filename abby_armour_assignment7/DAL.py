import sqlite3 as sqlite

class DAL:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_tables()

    def _connect(self):
        return sqlite.connect(self.db_path)

    def _ensure_tables(self):
        with self._connect() as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT NOT NULL,
                Description TEXT NOT NULL,
                ImageFileName TEXT NOT NULL
            )''')
            conn.commit()

    def get_all_projects(self):
        with self._connect() as conn:
            c = conn.cursor()
            c.execute("SELECT id, Title, Description, ImageFileName FROM projects ORDER BY id DESC")
            return c.fetchall()

    def add_project(self, title, description, image_filename):
        with self._connect() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO projects (Title, Description, ImageFileName) VALUES (?, ?, ?)", (title, description, image_filename))
            conn.commit()
            return c.lastrowid

    def delete_project(self, project_id):
        with self._connect() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            conn.commit()
