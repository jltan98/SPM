from flask import Flask, jsonify
import os
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
sys.path.append('./app/src')
if True:  # noqa: E402
    from classobj import Classes


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}


db = SQLAlchemy(app)

CORS(app)


class Quizzes(db.Model):
    __tablename__ = 'quizzes'
    quizID = db.Column(db.Integer(), primary_key=True)
    classID = db.Column(db.String(5), primary_key=True)
    sectionID = db.Column(db.String(10))
    active = db.Column(db.Boolean)

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result


class QuizInfo(db.Model):
    __tablename__ = 'quizinfo'
    quizID = db.Column(db.Integer(), primary_key=True)
    questionNumber = db.Column(db.Integer(), primary_key=True)
    question = db.Column(db.Text())
    answer= db.Column(db.Text())
    selections = db.Column(db.JSON)

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result


@app.route("/quiz", methods=['GET'])
def get_quiz():
    quizzes = Quizzes.query.all()

    if quizzes:
            return jsonify({
                "data": [quiz.to_dict() for quiz in quizzes]
            }), 200
    else:
        return jsonify({
            "message": "Person not found."
        }), 404


@app.route("/quiz_info/<quizID>", methods=['GET'])
def get_quiz_info(quizID):
    quizzes = QuizInfo.query.filter_by(quizID=quizID).all()

    if quizzes:
            return jsonify({
                "data": [quiz.to_dict() for quiz in quizzes]
            }), 200
    else:
        return jsonify({
            "message": "Person not found."
        }), 404


@app.route("/classes/<trainerID>", methods=['GET'])
def get_classes(trainerID):
    classes = Classes.query.filter_by(trainerAssignedID=trainerID).all()
    

    if classes:
            return jsonify({
                "data": [clas.to_dict() for clas in classes]
            }), 200
    else:
        return jsonify({
            "message": "Person not found."
        }), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)