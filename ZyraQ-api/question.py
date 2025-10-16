<<<<<<< HEAD
import sqlite3 
import json

class Question():
    def __init__(self, title: str = "", text: str = "", image: str = "", position: int = 0, possibleAnswers: list = None):
        self.title = title
        self.text = text
        self.image = image
        self.position = position
        self.possibleAnswers = possibleAnswers if possibleAnswers is not None else []
    
=======
import sqlite3
import base64

class Question:
    def __init__(self, title: str, text: str, difficulty: str, image: bytes = None, position: int = None, id: int = None):
        self.id = id   
        self.title = title
        self.text = text
        self.difficulty = difficulty
        self.image = image 
        self.position = position

>>>>>>> Amir_beta
    @staticmethod
    def save(question):
        conn = sqlite3.connect("bdd.db")
        try:
            cur = conn.cursor()
<<<<<<< HEAD
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
            
            conn.commit()
            print("question_id:", question_id)
            return question_id
        except Exception as e:
            conn.rollback()
            raise e
=======
            cur.execute("""
                INSERT INTO Question (title, text, difficulty, image, position)
                VALUES (?, ?, ?, ?, ?)
            """, (question.title, question.text, question.difficulty, question.image, question.position))
            conn.commit()
            question.id = cur.lastrowid
>>>>>>> Amir_beta
        finally:
            conn.close()
        return question

    def to_json(self):
        return {
<<<<<<< HEAD
            "title": self.title,
            "text": self.text,
            "image": self.image,
            "position": self.position,
=======
            "id": self.id,
            "title": self.title,
            "text": self.text,
            "difficulty": self.difficulty,
            "image": base64.b64encode(self.image).decode("utf-8") if self.image else None,
            "position": self.position
>>>>>>> Amir_beta
        }

    @staticmethod
    def from_json(json_data):
<<<<<<< HEAD
        if not isinstance(json_data, dict):
            raise ValueError("JSON data must be a dictionary")
            
        return Question(
            title=json_data.get("title", ""),
            text=json_data.get("text", ""),
            image=json_data.get("image", ""),
            position=int(json_data.get("position", 0)) if json_data.get("position") is not None else 0,
            possibleAnswers=json_data.get("possibleAnswers", [])
        )
=======
        image_data = json_data.get("image")
        image_bytes = base64.b64decode(image_data) if image_data else None

        return Question(
            title=json_data.get("title", ""),
            text=json_data.get("text", ""),
            difficulty=json_data.get("difficulty", ""),
            image=image_bytes,
            position=json_data.get("position")
        )
>>>>>>> Amir_beta
