from flask import Flask
from flask_cors import CORS
from flask import request
from jwt_utils import secret
from question import Question
from auth_token import require_token
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
    try:
        json_data = request.get_json()
        # print("Received JSON data:", json_data)
        
        if not json_data:
            return {'error': 'No JSON data provided'}, 400
        
        # Validation basique des champs requis
        required_fields = ['text', 'title']
        missing_fields = [field for field in required_fields if not json_data.get(field)]
        
        if missing_fields:
            return {'error': f'Missing required fields: {", ".join(missing_fields)}'}, 400
        
        # Créer un objet Question à partir du JSON
        question = Question.from_json(json_data)
        print("Question created:", question.title)

        # Sauvegarder en base de données
        question_id = Question.save(question)
        print("Question saved with ID:", question_id)

        return {
            "id": question_id,
        }, 200

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
        
        # Validation des champs requis
        required_fields = ['playerName', 'answers']
        missing_fields = [field for field in required_fields if not json_data.get(field)]
        
        if missing_fields:
            return {'error': f'Missing required fields: {", ".join(missing_fields)}'}, 400
        
        # Créer un objet Player à partir du JSON (validation incluse)
        player = Player.from_json(json_data)
        
        # Sauvegarder en base de données
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

if __name__ == "__main__":
    app.run(debug=True)