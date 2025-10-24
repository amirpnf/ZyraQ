from flask import Flask
from flask_cors import CORS
from flask import request
from jwt_utils import secret
from question import Question
from auth_token import require_token
from answer import Answer
import sqlite3
from player import Player


app = Flask(__name__)
CORS(app)

DATABASE = "bdd.db"

def get_db_connection():
	conn = sqlite3.connect(DATABASE)
	conn.row_factory = sqlite3.Row
	return conn	

@app.route('/')
def hello_world():
    x = 'world'
    return f"Hello, {x}"


@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    return {"size": 0, "scores": []}, 200


@app.route('/login', methods=['POST'])
def PostLogin():
    payload = request.get_json()
    if payload and payload.get("password") == "OuiStiti":	
        return {"token": secret}, 200
    return 'Unauthorized', 401

@app.route('/questions/<int:question_id>', methods=['GET'])
@require_token
def GetQuestionById(question_id):
    conn = get_db_connection()

    question_row = conn.execute(
        "SELECT * FROM Question WHERE id = ?", (question_id,)
    ).fetchone()

    if not question_row:
        conn.close()
        return {"error": "Question not found"}, 404

    answers_rows = conn.execute(
        "SELECT * FROM Answer WHERE question_id = ? ORDER BY id",
        (question_id,)
    ).fetchall()


    possible_answers = [
        {"id": a["id"], "text": a["text"], "isCorrect": bool(a["isCorrect"])}
        for a in answers_rows
    ]


    conn.close()

    return {
        "id": question_row["id"],
        "title": question_row["title"],
        "text": question_row["text"],
        "position": question_row["position"],
        "image": question_row["image"],
        "possibleAnswers": possible_answers
    }, 200


@app.route('/questions', methods=['GET'])
@require_token
def GetQuestionByPosition():
    position = request.args.get('position', type=int)

    if position is None:
        return {"error": "Missing 'position' query parameter"}, 400

    conn = get_db_connection()

    q = conn.execute("SELECT * FROM Question WHERE position = ?", (position,)).fetchone()

    if not q:
        conn.close()
        return {"error": "No questions found at this position"}, 404

    answers = conn.execute("""
        SELECT text, isCorrect
        FROM Answer
        WHERE question_id = ?
        ORDER BY id ASC
    """, (q["id"],)).fetchall()

    conn.close()

    question_data = {
        "id": q["id"],
        "title": q["title"],
        "text": q["text"],
        "position": q["position"],
        "image": q["image"] if q["image"] is not None else "",
        "possibleAnswers": [
            {"text": a["text"], "isCorrect": bool(a["isCorrect"])} for a in answers
        ]
    }

    return question_data, 200

	

@app.route('/questions', methods=['POST'])
@require_token
def PostQuestions():
    try:
        json_data = request.get_json()
        
        if not json_data:
            return {'error': 'No JSON data provided'}, 400

        required_fields = ['text', 'title', 'position']
        missing_fields = [field for field in required_fields if not json_data.get(field)]
        if missing_fields:
            return {'error': f"Missing required fields: {', '.join(missing_fields)}"}, 400
        
        position = json_data['position']
        difficulty = json_data.get("difficulty", "easy")
        question = Question.from_json({**json_data, "difficulty": difficulty})
        print("Question created:", question.title)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if position already exists
        existing = cursor.execute(
            "SELECT id, position FROM Question WHERE position = ?", (position,)
        ).fetchone()

        if existing:
            # Swap positions
            temp_position = cursor.execute("SELECT MAX(position) FROM Question").fetchone()[0] or 0
            temp_position += 1
            cursor.execute("UPDATE Question SET position = ? WHERE id = ?", (temp_position, existing['id']))
            conn.commit()

        # Insert the new question
        cursor.execute(
            "INSERT INTO Question (title, text, position, image, difficulty) VALUES (?, ?, ?, ?, ?)",
            (question.title, question.text, position, question.image, question.difficulty)
        )
        new_id = cursor.lastrowid
        conn.commit()
        print(f"Inserted new question ID {new_id} at position {position}")

        # Insert possible answers if available
        if hasattr(question, "possibleAnswers") and question.possibleAnswers:
            for ans in question.possibleAnswers:
                # Each answer should have: text and isCorrect
                answer_text = ans.get("text")
                is_correct = ans.get("isCorrect", 0)
                cursor.execute(
                    "INSERT INTO Answer (text, isCorrect, question_id) VALUES (?, ?, ?)",
                    (answer_text, is_correct, new_id)
                )
            conn.commit()
            print(f"Inserted {len(question.possibleAnswers)} answers for question ID {new_id}")

        # Handle old position if we did a swap
        if existing:
            old_pos = json_data.get("old_position")
            if old_pos is not None:
                cursor.execute("UPDATE Question SET position = ? WHERE id = ?", (old_pos, existing['id']))
            else:
                cursor.execute("UPDATE Question SET position = ? WHERE id = ?", (temp_position, existing['id']))
            conn.commit()
            print(f"Swapped old question ID {existing['id']} back to position")

        conn.close()
        return {"id": new_id}, 200

    except ValueError as ve:
        print("Validation error:", str(ve))
        return {'error': f'Validation error: {str(ve)}'}, 400

    except Exception as e:
        print("Error saving question:", str(e))
        return {'error': f'Error saving question: {str(e)}'}, 500



@app.route('/participations', methods=['POST'])
def PostParticipations():
    try:
        json_data = request.get_json()
        
        if not json_data:
            return {'error': 'No JSON data provided'}, 400
        
        required_fields = ['playerName', 'answers']
        missing_fields = [field for field in required_fields if not json_data.get(field)]
        
        if missing_fields:
            return {'error': f'Missing required fields: {", ".join(missing_fields)}'}, 400
        
        player = Player.from_json(json_data)
        
        player_id = Player.save(player)
        
        return {
            "message": "Participation saved successfully",
            "player_id": player_id,
            "playerName": player.playerName,
            "score": player.score
        }, 200
        
    except ValueError as ve:
        return {'error': f'Validation error: {str(ve)}'}, 400
        
    except Exception as e:
        return {'error': f'Error saving participation: {str(e)}'}, 500

@app.route('/participations/all', methods=['DELETE'])
@require_token
def DeleteAllParticipations():
    try:
        rows_affected = Player.delete_all_participations()
        
        return {
            "players_deleted": rows_affected
        }, 204
        
    except Exception as e:
        return {'error': f'Error deleting participations: {str(e)}'}, 500
    
@app.route("/answers", methods=['POST'])
@require_token
def PostAnswers():

	json_data = request.get_json()
	if not json_data:
		return {"error" : "No JSON data provided"}, 400
	
	try:
		answer = Answer.from_json(json_data)
		if answer.isCorrect not in (0, 1):
			return {"error" : "isCorrect must be 0 or 1"}, 400
		if not answer.text or answer.question is None:
			return {"error" : "Missing text or question ID for the answer"}, 400
		
		conn = get_db_connection()

		q = conn.execute("SELECT id FROM Question WHERE id = ?", (answer.question,)).fetchone()
		if not q:
			conn.close()
			return {"error": "Question not found"}, 404
		
		saved_answer = Answer.save(answer, conn)
		conn.close()

		return {"message" : "Answers saved successfully", "answer" : saved_answer.to_json()}, 201
	
	except Exception as e:
		return {"error" : str(e)}, 500
	
@app.route("/questions/<int:question_id>", methods=["PUT"])
@require_token
def ModifyQuestion(question_id):
    json_data = request.get_json()
    if not json_data:
        return {"error": "No JSON data provided"}, 400

    conn = get_db_connection()
    cursor = conn.cursor()

    existing = cursor.execute("SELECT * FROM Question WHERE id = ?", (question_id,)).fetchone()
    if not existing:
        conn.close()
        return {"error": "Question not found"}, 404

    cursor.execute("DELETE FROM Answer WHERE question_id = ?", (question_id,))

    fields, values = [], []
    for field in ["title", "text", "image", "difficulty", "position"]:
        if field in json_data:
            fields.append(f"{field} = ?")
            values.append(json_data[field])

    if fields:
        values.append(question_id)
        cursor.execute(f"UPDATE Question SET {', '.join(fields)} WHERE id = ?", values)

    possible_answers = json_data.get("possibleAnswers", [])
    for ans in possible_answers:
        answer_text = ans.get("text")
        is_correct = int(ans.get("isCorrect", 0))
        cursor.execute(
            "INSERT INTO Answer (text, isCorrect, question_id) VALUES (?, ?, ?)",
            (answer_text, is_correct, question_id)
        )

    conn.commit()

    modified = cursor.execute("SELECT * FROM Question WHERE id = ?", (question_id,)).fetchone()

    answers = cursor.execute(
        "SELECT id, text, isCorrect FROM Answer WHERE question_id = ? ORDER BY id",
        (question_id,)
    ).fetchall()

    conn.close()

    return {
        "id": modified["id"],
        "title": modified["title"],
        "text": modified["text"],
        "difficulty": modified["difficulty"],
        "image": modified["image"],
        "position": modified["position"],
        "possibleAnswers": [
            {"id": a["id"], "text": a["text"], "isCorrect": bool(a["isCorrect"])} for a in answers
        ]
    }, 204


@app.route("/questions/<int:question_id>", methods=["DELETE"])
@require_token
def DeleteQuestion(question_id):
    with get_db_connection() as conn:
        existing = conn.execute("SELECT * FROM Question WHERE id = ?", (question_id,)).fetchone()
        if not existing:
            return {"error": "Question not found"}, 404

        conn.execute("DELETE FROM Answer WHERE question_id = ?", (question_id,))

        conn.execute("DELETE FROM Question WHERE id = ?", (question_id,))

        conn.commit()

    return {"message": "Question and its answers deleted successfully"}, 204


@app.route("/questions/all", methods=["DELETE"])
@require_token
def DeleteAllQuestions():
    conn = get_db_connection()
    
    try:
        conn.execute("DELETE FROM Question")
        conn.execute("DELETE FROM sqlite_sequence WHERE name='Question'")
        conn.execute("DELETE FROM Answer")
        conn.execute("DELETE FROM sqlite_sequence WHERE name='Answer'")

        conn.commit()
        conn.close()
        return {"message": "All questions deleted successfully"}, 204
    except Exception as e:
        conn.close()
        return {"error": str(e)}, 500

@app.route('/rebuild-db', methods=['POST'])
@require_token
def RebuildDatabase():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DROP TABLE IF EXISTS Answer")
        cursor.execute("DROP TABLE IF EXISTS Question")
        cursor.execute("DROP TABLE IF EXISTS Player")
        
        cursor.execute("""
            CREATE TABLE Question (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                text TEXT NOT NULL,
                difficulty TEXT NOT NULL DEFAULT 'easy',
                image BLOB,
                position INTEGER
            )
        """)
        
        cursor.execute("""
            CREATE TABLE Answer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                isCorrect INTEGER NOT NULL CHECK (isCorrect IN (0, 1)),
                text TEXT NOT NULL,
                FOREIGN KEY(question_id) REFERENCES Question(id) ON DELETE CASCADE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE Player (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                playerName TEXT NOT NULL,
                answers TEXT,
                score INTEGER DEFAULT 0
            )
        """)
        
        conn.commit()
        conn.close()
        return "Ok", 200

    except Exception as e:
        if conn:
            conn.close()
        return {"error": str(e)}, 500




if __name__ == "__main__":
    app.run(debug=True)