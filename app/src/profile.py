import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from classobj import Learner, Course, Application, enrolmentPeriod

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)


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
    period = enrolmentPeriod.query.all()

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
    courses = Course.query.all()

    if courses:
        return jsonify({
            "data": [course.to_dict() for course in courses]
        }), 200
    else:
        return jsonify({
            "message": "Person not found."
        }), 404


@app.route("/applications/<learnerID>", methods=['GET'])
def get_applications(learnerID):
    applications = Application.query.filter_by(
        applicationLearnerID=learnerID).all()

    if applications:
        return jsonify({
            "data": [application.to_dict() for application in applications]
        }), 200
    else:
        return jsonify({
            "message": "Person not found."
        }), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
