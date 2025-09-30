import sqlite3 

class Question():
    def __init__(self, title: str):
        self.title = title
    
    @staticmethod
    def save(question):
        conn = sqlite3.connect("bdd.db")
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO Question (title) VALUES (?)", (question.title,))
            conn.commit()
        finally:
            conn.close()
            
    # Méthode pour convertir l'objet Python en dictionnaire JSON
    def to_json(self):
        return {
            "title": self.title
        }
    
    # Méthode statique pour créer un objet Question à partir d'un dictionnaire JSON
    @staticmethod
    def from_json(json_data):
        return Question(
            title=json_data.get("title", "")
        )