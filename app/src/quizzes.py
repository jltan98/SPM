import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import sys
sys.path.append('./app/src')
if True:  # noqa: E402
    from quiz import Quizzes, QuizInfo


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}


db = SQLAlchemy(app)

CORS(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


# class Quizzes(db.Model):
#     __tablename__ = 'quizzes'

#     quizID = db.Column(db.Integer, primary_key=True)
#     classID = db.Column(db.String(5))
#     sectionID = db.Column(db.String(10))
#     active = db.Column(db.Boolean)


# class QuizInfo(db.Model):
#     __tablename__ = 'quizInfo'

#     quizID = db.Column(db.Integer, primary_key=True)
#     questionNumber = db.Column(db.Integer, primary_key=True)
#     question = db.Column(db.Text())
#     answer = db.Column(db.Text())
#     selections = db.Column(db.JSON)


@app.route("/enterquiz", methods=['POST'])
def enterQuiz():
    data = request.json
    print(data)
    if not all(key in data.keys() for
               key in ('quizID', 'classID', 'sectionID', 'active',
                       'questionNumber', 'question',
                       'answer', 'selections')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500

    quiz = Quizzes(
        quizID=data['quizID'],
        classID=data['classID'],
        sectionID=data['sectionID'],
        active=data['active']
    )

    quizInfo = QuizInfo(
        quizID=data['quizID'],
        questionNumber=data['questionNumber'],
        question=data['question'],
        answer=data['answer'],
        selections=data['selections']
    )

    db.session.add(quiz)
    db.session.add(quizInfo)
    db.session.commit()
    return data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
