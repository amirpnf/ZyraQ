import sqlite3
import json

class Player():
    def __init__(self, playerName: str = "", answers: list = None, score: int = 0):
        self.playerName = playerName
        self.answers = answers if answers is not None else []
        self.score = score
    
    @staticmethod
    def calculate_score(answers):
        """Calcule le score en comparant les réponses du joueur aux bonnes réponses"""
        conn = sqlite3.connect("bdd.db", timeout=20.0)
        try:
            cur = conn.cursor()
            
            cur.execute("""
                SELECT q.id
                FROM Question q
                ORDER BY q.id
            """)
            
            questions = cur.fetchall()
            score = 0
            
            for i, (question_id,) in enumerate(questions):
                if i < len(answers):
                    player_choice = answers[i]  
                    
                    cur.execute("""
                        SELECT id, isCorrect
                        FROM Answer
                        WHERE question_id = ?
                        ORDER BY id
                    """, (question_id,))
                    
                    question_answers = cur.fetchall()
                    print(question_answers)
                    
                    
                    if 1 <= player_choice <= len(question_answers):
                        answer_id, is_correct = question_answers[player_choice - 1] 
                        if is_correct:
                            score += 1
            
            return score
        finally:
            conn.close()
    
    @staticmethod
    def save(player):
        conn = sqlite3.connect("bdd.db", timeout=20.0)
        try:
            cur = conn.cursor()
            
            player.score = Player.calculate_score(player.answers)
            
            answers_json = json.dumps(player.answers)
            
            cur.execute("INSERT INTO Player (playerName, answers, score) VALUES (?, ?, ?)",
                        (player.playerName, answers_json, player.score))

            player_id = cur.lastrowid
            conn.commit()
            return player_id
        except Exception as e:
            print("except")

            conn.rollback()
            raise e
        finally:
            print("final")

            conn.close()
    
    @staticmethod
    def delete_all_participations():
        """Supprime tous les utilisateurs/joueurs de la base de données"""
        conn = sqlite3.connect("bdd.db", timeout=20.0)
        try:
            cur = conn.cursor()
            
            cur.execute("DELETE FROM Player")
            
            rows_affected = cur.rowcount
            conn.commit()
            return rows_affected
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def to_json(self):
        return {
            "playerName": self.playerName,
            "answers": self.answers,
            "score": self.score
        }
    
    @staticmethod
    def from_json(json_data):
        if not isinstance(json_data, dict):
            raise ValueError("JSON data must be a dictionary")
        
        answers = json_data.get("answers", [])
        if not isinstance(answers, list):
            raise ValueError("answers must be a list")
        
        if len(answers) != 10:
            raise ValueError(f"answers must contain exactly 10 elements, got {len(answers)}")
            
        return Player(
            playerName=json_data.get("playerName", ""),
            answers=answers,
            score=json_data.get("score", 0)
        )