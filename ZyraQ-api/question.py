import sqlite3 
import json

class Question():
    def __init__(self, title: str = "", text: str = "", image: str = "", position: int = 0, difficulty: str = "easy", possibleAnswers: list = None):
        self.title = title
        self.text = text
        self.image = image
        self.position = position
        self.difficulty = difficulty
        self.possibleAnswers = possibleAnswers if possibleAnswers is not None else []
    
    @staticmethod
    def save(question):
        conn = sqlite3.connect("bdd.db")
        try:
            cur = conn.cursor()
            
            cur.execute(
                "INSERT INTO Question (title, text, image, position, difficulty) VALUES (?, ?, ?, ?, ?)",
                (question.title, question.text, question.image, question.position, question.difficulty)
            )
            
            question_id = cur.lastrowid
            
            for answer in question.possibleAnswers:
                if isinstance(answer, dict):
                    cur.execute(
                        "INSERT INTO Answer (questionID, text, isCorrect) VALUES (?, ?, ?)",
                        (question_id, answer.get('text', ''), int(answer.get('isCorrect', False)))
                    )
            
            conn.commit()
            return question_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def to_json(self):
        return {
            "title": self.title,
            "text": self.text,
            "image": self.image,
            "position": self.position,
            "difficulty": self.difficulty,
            "possibleAnswers": self.possibleAnswers
        }

    @staticmethod
    def from_json(json_data):
        if not isinstance(json_data, dict):
            raise ValueError("JSON data must be a dictionary")
            
        return Question(
            title=json_data.get("title", ""),
            text=json_data.get("text", ""),
            image=json_data.get("image", ""),
            position=int(json_data.get("position", 0)) if json_data.get("position") is not None else 0,
            difficulty=json_data.get("difficulty", "easy"),
            possibleAnswers=json_data.get("possibleAnswers", [])
        )
