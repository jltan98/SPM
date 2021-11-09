from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root' + \
                                        '@localhost:3308/lms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}


db = SQLAlchemy(app)

CORS(app)

class Classes(db.Model):
    __tablename__ = 'classes'
    classID = db.Column(db.String(64),primary_key=True)
    courseID = db.Column(db.String(64),primary_key=True)
    noOfSlots = db.Column(db.Integer())
    trainerAssignedID = db.Column(db.String(64))
    startDate = (db.DateTime())
    endDate = db.Column(db.DateTime())
    enrolmentPeriodID = db.Column(db.String(64))

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
    __tablename__ = 'quizInfo'
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
    app.run(host='0.0.0.0', port=5002, debug=True)