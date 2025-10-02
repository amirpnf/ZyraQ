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

    @staticmethod
    def save(question):
        conn = sqlite3.connect("bdd.db")
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Question (title, text, difficulty, image, position)
                VALUES (?, ?, ?, ?, ?)
            """, (question.title, question.text, question.difficulty, question.image, question.position))
            conn.commit()
            question.id = cur.lastrowid
        finally:
            conn.close()
        return question

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "text": self.text,
            "difficulty": self.difficulty,
            "image": base64.b64encode(self.image).decode("utf-8") if self.image else None,
            "position": self.position
        }

    @staticmethod
    def from_json(json_data):
        image_data = json_data.get("image")
        image_bytes = base64.b64decode(image_data) if image_data else None

        return Question(
            title=json_data.get("title", ""),
            text=json_data.get("text", ""),
            difficulty=json_data.get("difficulty", ""),
            image=image_bytes,
            position=json_data.get("position")
        )
