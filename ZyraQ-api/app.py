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

if __name__ == "__main__":
    app.run(debug=True)