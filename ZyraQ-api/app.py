from flask import Flask
from flask_cors import CORS
from flask import request
from jwt_utils import secret
from question import Question
from auth_token import require_token
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

if __name__ == "__main__":
    app.run()