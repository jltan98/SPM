from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import date, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root' + \
                                        '@localhost:3306/learningmanagementsystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}


db = SQLAlchemy(app)

CORS(app)


class Learner(db.Model):
    __tablename__ = 'learner'

    learnerName = db.Column(db.String(64))
    learnerID = db.Column(db.String(64), primary_key=True)
    learnerContact = db.Column(db.String(255))
    coursesTaken = db.Column(db.Text)

    def __init__(self,
                 learnerName="",
                 learnerID="",
                 learnerContact="",
                 coursesTaken=[]):
        self.learnerName = learnerName
        self.learnerID = learnerID
        self.learnerContact = learnerContact
        self.coursesTaken = coursesTaken

    def json(self):
        return {
            'name': self.learnerName,
            'id': self.learnerID,
            'contact': self.learnerContact,
            'coursesTaken': self.coursesTaken,
        }


class Trainer(db.Model):
    __tablename__ = 'trainer'

    trainerName = db.Column(db.String(64))
    trainerID = db.Column(db.String(64), primary_key=True)
    trainerContact = db.Column(db.String(255))
    skills = db.Column(db.Text)
    experience = db.Column(db.Text)
    coursesTaught = db.Column(db.Text)

    def __init__(self,
                 trainerName="",
                 trainerID="",
                 trainerContact="",
                 skills=[],
                 experience="",
                 coursesTaught=[]):
        self.trainerName = trainerName
        self.trainerID = trainerID
        self.trainerContact = trainerContact
        self.skills = skills
        self.experience = experience
        self.coursesTaught = coursesTaught

    def json(self):
        return {
            'trainerName': self.trainerName,
            'trainerID': self.trainerID,
            'trainerContact': self.trainerContact,
            'skills': self.skills,
            'experience': self.experience,
            'coursesTaught': self.coursesTaught,
        }

class Course(db.Model):
    __tablename__ = 'course'

    courseID = db.Column(db.String(64), primary_key=True)
    courseName = db.Column(db.String(64))
    courseDescription = db.Column(db.Text)
    prerequisite = db.Column(db.Text)
    noOfClasses = db.Column(db.Integer, default=0)
    classes = db.Column(db.Text)
    subjectcategory = db.Column(db.String(255))

    def __init__(self,
                 courseID="",
                 courseName="",
                 courseDescription="",
                 prerequisite=[],
                 noOfClasses=0,
                 classes = [],
                 subjectcategory=""):
        self.courseID = courseID
        self.courseName = courseName
        self.courseDescription = courseDescription
        self.prerequisite = prerequisite
        self.noOfClasses = noOfClasses
        self.classes = classes
        self.subjectcategory = subjectcategory

    def json(self):
        return {
            'courseID': self.courseID,
            'courseName': self.courseName,
            'courseDescription': self.courseDescription,
            'prerequisite': self.prerequisite,
            'noOfClasses': self.noOfClasses,
            'classes': self.classes,
            'subjectcategory': self.subjectcategory,
        }

class Classes(db.Model):
    __tablename__ = 'classes'

    classID = db.Column(db.String(64), primary_key=True)
    courseID = db.Column(db.Integer, db.ForeignKey('course.courseID'))
    noOfSlots = db.Column(db.Integer, default=0)
    trainerAssignedID = db.Column(db.Integer, db.ForeignKey('trainer.trainerID'))
    startDate = db.Column(db.DateTime)
    endDate = db.Column(db.DateTime)

    def __init__(self,
                 classID="",
                 courseID="",
                 noOfSlots=0,
                 trainerAssignedID="",
                 startDate='',
                 endDate = ''
                 ):
        self.classID = classID
        self.courseID = courseID
        self.noOfSlots = noOfSlots
        self.trainerAssignedID = trainerAssignedID
        self.startDate = startDate
        self.endDate = endDate

    def json(self):
        return {
            'classID': self.classID,
            'courseID': self.courseID,
            'noOfSlots': self.noOfSlots,
            'trainerAssignedID': self.trainerAssignedID,
            'startDate': self.startDate,
            'endDate': self.endDate,
        }


@app.route("/learners/<string:learnerID>")
def learner_by_id(learnerID):
    learner = Learner.query.filter_by(learnerID=learnerID).first()
    if learner:
        return jsonify({
            "data": learner.json()
        }), 200
    else:
        return jsonify({
            "message": "Learner ID not found."
        }), 404

@app.route("/trainers/<string:trainerID>")
def trainer_by_id(trainerID):
    trainer = Trainer.query.filter_by(trainerID=trainerID).first()
    if trainer:
        return jsonify({
            "data": trainer.json()
        }), 200
    else:
        return jsonify({
            "message": "Trainer ID not found."
        }), 404

@app.route("/courses/<string:courseID>")
def course_by_id(courseID):
    course = Course.query.filter_by(courseID=courseID).first()
    if course:
        return jsonify({
            "data": course.json()
        }), 200
    else:
        return jsonify({
            "message": "Course ID not found."
        }), 404

@app.route("/<string:courseID>/<string:classID>")
def class_by_id(classID, courseID):
    class_n = Classes.query.filter_by(classID=classID, courseID=courseID).first()
    if class_n:
        return jsonify({
            "data": class_n.json()
        }), 200
    else:
        return jsonify({
            "message": "Class ID not found."
        }), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
