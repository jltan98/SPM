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

class Courses(db.Model):
    __tablename__ = 'course'
    CourseID = db.Column(db.String(50), primary_key=True)
    courseName = db.Column(db.String(50))
    courseDescription = db.Column(db.Text)
    prerequisite = db.Column(db.Text)
    noOfClasses = db.Column(db.Integer)
    classes = db.Column(db.Text)
    subjectcategory = db.Column(db.String(50))

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

class Enrol_Period(db.Model):
    __tablename__ = 'enrolmentperiod'
    enrolmentPeriodID = db.Column(db.String(50), primary_key=True)
    enrolmentStartDate = db.Column(db.String(50))
    enrolmentEndDate = db.Column(db.String(50))

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

class Learner(db.Model):
    __tablename__ = 'learner'
    learnerID = db.Column(db.Integer, primary_key=True)
    learnerName = db.Column(db.String(50))
    learnerContact = db.Column(db.String(50))
    coursesTaken = db.Column(db.Text)

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

@app.route("/learner/<name>", methods=['GET'])
def get_course(name):
    learner = Learner.query.filter_by(learnerName=name).first()

    if learner:
        return jsonify({
            "data": learner.to_dict()
        }), 200
    else:
        return jsonify({
            "message": "Person not found."
        }), 404

@app.route("/enrolDates")
def get_enrolment_period():
    period = Enrol_Period.query.all()

    if period:
        return jsonify({
            "data": [periods.to_dict() for periods in period]
        }), 200
    else:
        return jsonify({
            "message": "Person not found."
        }), 404

@app.route("/courses")
def get_courses():
    courses = Courses.query.all()

    if courses:
        return jsonify({
            "data": [course.to_dict() for course in courses]
        }), 200
    else:
        return jsonify({
            "message": "Person not found."
        }), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)