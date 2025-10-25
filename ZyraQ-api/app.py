from flask import Flask
from flask_cors import CORS
from flask import request
from jwt_utils import secret, build_token
from question import Question
from auth_token import require_token
from rebuild_db import rebuild_database
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
    conn = get_db_connection()
    
    questions = conn.execute("SELECT id, title, position FROM Question ORDER BY position ASC").fetchall()
    
    scores = conn.execute("""
        SELECT playerName, score
        FROM Player
        ORDER BY score DESC
    """).fetchall()
    
    conn.close()

    quiz_info = {
        "size": len(questions),
        "scores": [
            {"playerName": s["playerName"], "score": s["score"]} for s in scores
        ]
    }

    return quiz_info, 200


@app.route('/login', methods=['POST'])
def PostLogin():
    payload = request.get_json()
    if payload and payload.get("password") == "OuiStiti":	
        token = build_token()
        return {"token": token}, 200
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
        "SELECT id, text, isCorrect FROM Answer WHERE question_id = ? ORDER BY rowid ASC",
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
        SELECT id, text, isCorrect
        FROM Answer
        WHERE question_id = ?
        ORDER BY rowid ASC
    """, (q["id"],)).fetchall()

    conn.close()

    question_data = {
        "id": q["id"],
        "title": q["title"],
        "text": q["text"],
        "position": q["position"],
        "image": q["image"] if q["image"] is not None else "",
        "possibleAnswers": [
            {"id": a["id"], "text": a["text"], "isCorrect": bool(a["isCorrect"])} for a in answers
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
        
        possible_answers = json_data.get("possibleAnswers", [])

        question = Question.from_json({**json_data, "difficulty": difficulty})
        
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE Question SET position = position + 1 WHERE position >= ?",
            (position,)
        )

        cursor.execute(
            "INSERT INTO Question (title, text, position, image, difficulty) VALUES (?, ?, ?, ?, ?)",
            (question.title, question.text, position, question.image, question.difficulty)
        )
        new_id = cursor.lastrowid

        for ans in possible_answers:
            if "text" not in ans or ans["text"] is None:
                continue  
            is_correct = int(ans.get("isCorrect", 0))
            cursor.execute(
                "INSERT INTO Answer (text, isCorrect, question_id) VALUES (?, ?, ?)",
                (ans["text"], is_correct, new_id)
            )

        conn.commit()
        conn.close()
        return {"id": new_id}, 200

    except Exception as e:
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

    old_position = existing["position"]
    new_position = json_data.get("position", old_position)

    if new_position != old_position:
        if new_position < old_position:
            cursor.execute(
                "UPDATE Question SET position = position + 1 WHERE position >= ? AND position < ?",
                (new_position, old_position)
            )
        else:
            cursor.execute(
                "UPDATE Question SET position = position - 1 WHERE position <= ? AND position > ?",
                (new_position, old_position)
            )

    fields, values = [], []
    for field in ["title", "text", "image", "difficulty", "position"]:
        if field in json_data:
            fields.append(f"{field} = ?")
            values.append(json_data[field])

    if fields:
        values.append(question_id)
        cursor.execute(f"UPDATE Question SET {', '.join(fields)} WHERE id = ?", values)

    if "possibleAnswers" in json_data:
        cursor.execute("DELETE FROM Answer WHERE question_id = ?", (question_id,))
        for ans in json_data["possibleAnswers"]:
            if "text" not in ans or ans["text"] is None:
                continue
            is_correct = int(ans.get("isCorrect", 0))
            cursor.execute(
                "INSERT INTO Answer (text, isCorrect, question_id) VALUES (?, ?, ?)",
                (ans["text"], is_correct, question_id)
            )

    conn.commit()

    modified = cursor.execute("SELECT * FROM Question WHERE id = ?", (question_id,)).fetchone()
    answers = cursor.execute(
        "SELECT id, text, isCorrect FROM Answer WHERE question_id = ? ORDER BY rowid ASC",
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
    conn = get_db_connection()
    cursor = conn.cursor()

    q = cursor.execute("SELECT * FROM Question WHERE id = ?", (question_id,)).fetchone()
    if not q:
        conn.close()
        return {"error": "Question not found"}, 404

    deleted_position = q["position"]

    cursor.execute("DELETE FROM Answer WHERE question_id = ?", (question_id,))
    cursor.execute("DELETE FROM Question WHERE id = ?", (question_id,))

    cursor.execute(
        "UPDATE Question SET position = position - 1 WHERE position > ?",
        (deleted_position,)
    )

    conn.commit()
    conn.close()

    return {"message": "Question deleted successfully"}, 204





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
        success = rebuild_database()
        if success:
            return "Ok", 200
        else:
            return {"error": "Failed to rebuild database."}, 500
    except Exception as e:
        return {"error": str(e)}, 500




if __name__ == "__main__":
    app.run(debug=True)