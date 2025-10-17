class Answer:
    
    def __init__(self, question, text, isCorrect, id=None):
        self.id = id
        self.question = question  # must match Question.id
        self.text = text
        self.isCorrect = isCorrect  # 0 or 1

    def to_json(self):
        return {
            "id": self.id,
            "question": self.question,
            "text": self.text,
            "isCorrect": self.isCorrect
        }

    @staticmethod
    def from_json(data):
        return Answer(
            question=data.get("question"),
            text=data.get("text"),
            isCorrect=data.get("isCorrect")
        )

    @staticmethod
    def save(answer, conn):
        """
        Save an Answer instance to the database.
        """
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Answer (text, isCorrect, question_id) VALUES (?, ?, ?)",
            (answer.text, answer.isCorrect, answer.question)
        )

        conn.commit()
        answer.id = cur.lastrowid
        return answer
