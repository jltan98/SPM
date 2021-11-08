import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}


db = SQLAlchemy(app)

CORS(app)


class Quizzes(db.Model):
    __tablename__ = 'quizzes'
    quizID = db.Column(db.Integer, primary_key=True)
    classID = db.Column(db.String(5), primary_key=True)
    sectionID = db.Column(db.String(10))
    active = db.Column(db.Boolean)


class QuizInfo(db.Model):
    __tablename__ = 'quizInfo'
    quizInfoID = db.Column(db.Integer, db.ForeignKey(
        'quizzes.quizID'), primary_key=True)
    questionNumber = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text())
    answer = db.Column(db.Text())
    selections = db.Column(db.JSON)


@app.route("/enter_quiz", methods=['POST'])
def register():
    data = request.get_json()
    if not all(key in data.keys() for
               key in ('quizID', 'classID', 'sectionID', 'active',
                       'questionNumber', 'question',
                       'answer', 'selections')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500

    print(data['quizID'])

    quiz = Quizzes(
        quizID=data['quizID'],
        classID=data['classID'],
        sectionID=data['sectionID'],
        active=data['active']
    )

    quizInfo = QuizInfo(
        quizInfoID=data['quizID'],
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
