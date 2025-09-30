import sqlite3 
import json

class Question():
    def __init__(self, title: str = "", text: str = "", image: str = "", position: int = 0, possibleAnswers: list = None):
        self.title = title
        self.text = text
        self.image = image
        self.position = position
        self.possibleAnswers = possibleAnswers if possibleAnswers is not None else []
    
    @staticmethod
    def save(question):
        conn = sqlite3.connect("bdd.db")
        try:
            cur = conn.cursor()
            print("laaaaaa")

            cur.execute("INSERT INTO Question (title, text, image, position) VALUES (?, ?, ?, ?)",
                        (question.title, question.text, question.image, question.position))
            
            print("iciii")
            question_id = cur.lastrowid
            
            # Insérer chaque réponse dans la table Answer
            for answer in question.possibleAnswers:
                if isinstance(answer, dict):
                    cur.execute("INSERT INTO Answer (question, text, isCorrect) VALUES (?, ?, ?)",
                                (question_id, answer.get('text', ''), answer.get('isCorrect', False)))
            
            # conn.commit()
            print("question_id:", question_id)
            return question_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    # Méthode pour convertir l'objet Python en dictionnaire JSON
    def to_json(self):
        return {
            "title": self.title,
            "text": self.text,
            "image": self.image,
            "position": self.position,
        }
    
    # Méthode statique pour créer un objet Question à partir d'un dictionnaire JSON
    @staticmethod
    def from_json(json_data):
        if not isinstance(json_data, dict):
            raise ValueError("JSON data must be a dictionary")
            
        return Question(
            title=json_data.get("title", ""),
            text=json_data.get("text", ""),
            image=json_data.get("image", ""),
            position=int(json_data.get("position", 0)) if json_data.get("position") is not None else 0,
            possibleAnswers=json_data.get("possibleAnswers", [])
        )