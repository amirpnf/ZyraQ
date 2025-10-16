from flask import Flask
from flask_cors import CORS
from flask import request
from jwt_utils import secret
from question import Question
from auth_token import require_token
from answer import Answer
import sqlite3

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
	print("HIHIHHIHIHIHIHIHIHIHIH")
	return 'Unauthorized', 401

@app.route('/questions/<int:question_id>', methods=['GET'])
@require_token
def GetQuestionById(question_id):
	conn = get_db_connection()

	question_row = conn.execute(f"SELECT * FROM Question WHERE id = ?", (question_id,)).fetchone()

	if not question_row :
		conn.close()
		return {"error": "Question not found"}, 404
	
	conn.close()
	return {
		"id" : question_row["id"],
		"title" : question_row["title"],
		"text" : question_row["text"],
		"position" : question_row["position"],
		"image" : question_row["image"]
	}, 200

@app.route('/questions', methods=['GET'])
@require_token
def GetQuestionByPosition():
	position = request.args.get('position', type=int)

	if not position:
		return {"error" : "Missing 'position' query parameter"}, 400

	conn = get_db_connection()
	q = conn.execute("SELECT * FROM Question WHERE position = ?", (position,)).fetchone()
	conn.close()

	if not q:
		return {"error" : "No questions found at this position"}, 404
	
	return {
		"id" : q["id"],
		"title" : q["title"],
		"text" : q["text"],
		"position" : q["position"],
		"image" : q["image"]
	}, 200
	

@app.route('/questions', methods=['POST'])
@require_token
def PostQuestions():
	json_data = request.get_json()
	if not json_data:
		return 'Bad Request - No JSON data', 400
	
	try:
		# Créer un objet Question à partir du JSON
		question = Question.from_json(json_data)
		# Sauvegarder en base de données
		Question.save(question)
		print("Question saved:", question.title)
		return {"message": "Question saved successfully", "question": question.to_json()}, 201
		
	except Exception as e:
		return f'Error saving question: {str(e)}', 500
	
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
		return {"error" : "No JSON data provided"}, 400

	conn = get_db_connection()
	existing = conn.execute("SELECT * FROM Question WHERE id = ?", (question_id,)).fetchone()
	if not existing:
		return {"error" : "Question is not found"}, 400
	
	question = Question.from_json(json_data)
	fields, values = [], []
	for field in ["title", "text", "image", "difficulty", "position"]:
		if field in json_data:
			fields.append(f"{field} = ?")
			values.append(json_data[field])

	if not fields:
		conn.close()
		return {"error" : "No valid fields to update"}, 400

	values.append(question_id)
	conn.execute(f"UPDATE Question SET {', '.join(fields)} WHERE id = ?", values)
	conn.commit()

	modified = conn.execute("SELECT * FROM Question WHERE id = ?", (question_id,)).fetchone()
	conn.close()

	return {
		"id" : modified["id"],
		"title" : modified["title"],
		"text" : modified["text"],
		"difficulty" : modified["difficulty"],
		"image" : modified["image"],
		"position" : modified["position"]
	}, 200

@app.route("/questions/<int:question_id>", methods=["DELETE"])
@require_token
def DeleteQuestion(question_id):
	conn = get_db_connection()

	existing = conn.execute("SELECT * FROM Question WHERE id = ?", (question_id,)).fetchone()
	if not existing:
		conn.close()
		return {"error" : "Question not found"}, 404

	conn.execute("DELETE FROM Question WHERE id = ?", (question_id,))
	conn.commit()
	conn.close()

	return {"message" : "Question deleted successfully"}, 200

@app.route("/questions/all", methods=["DELETE"])
@require_token
def DeleteAllQuestions():
    conn = get_db_connection()
    
    try:
        conn.execute("DELETE FROM Question")
        conn.commit()
        conn.close()
        return {"message": "All questions deleted successfully"}, 200
    except Exception as e:
        conn.close()
        return {"error": str(e)}, 500



if __name__ == "__main__":
    app.run()