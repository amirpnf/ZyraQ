from flask import Flask
from flask_cors import CORS
from flask import request
from jwt_utils import secret
from question import Question
from auth_token import require_token

app = Flask(__name__)
CORS(app)

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