from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from classObjects import Learner, Trainer, Administrator
from classObjects import Classes, Course, Application, ApplicationPeriod


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root' + \
                                        '@localhost:3306/LMS'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


# APP ROUTING
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


@app.route("/trainers")
def trainers():
    trainers = Trainer.query.all()
    if trainers:
        return jsonify({
            "data": [trainer.json() for trainer in trainers]
        }), 200
    else:
        return jsonify({
            "message": "Trainer ID not found."
        }), 404


@app.route("/admins/<string:adminID>")
def admin_by_id(adminID):
    admin = Administrator.query.filter_by(adminID=adminID).first()
    if admin:
        return jsonify({
            "data": admin.json()
        }), 200
    else:
        return jsonify({
            "message": "Admin ID not found."
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


@app.route("/courses")
def courses():
    courses = Course.query.all()
    if courses:
        return jsonify({
            "data": [course.json() for course in courses]
        }), 200
    else:
        return jsonify({
            "message": "Courses not found."
        }), 404


@app.route("/<string:courseID>/<string:classID>")
def class_by_id(classID, courseID):
    class_n = Classes.query.filter_by(
        classID=classID, courseID=courseID).first()
    if class_n:
        return jsonify({
            "data": class_n.json()
        }), 200
    else:
        return jsonify({
            "message": "Class ID not found."
        }), 404


@app.route("/classes")
def classes():
    classes = Classes.query.all()
    if classes:
        return jsonify({
            "data": [class_n.json() for class_n in classes]
        }), 200
    else:
        return jsonify({
            "message": "Classes not found."
        }), 404


@app.route("/applications/<string:applicationLearnerID>")
def applicationStatus(applicationLearnerID):
    applications = Application.query.filter_by(
        applicationLearnerID=applicationLearnerID)
    combined = []
    for app in applications:
        period = ApplicationPeriod.query.filter_by(
            enrolmentPeriodID=app.enrolmentPeriodID).first()
        course = Course.query.filter_by(
            courseID=app.applicationCourseID).first()
        class_n = Classes.query.filter_by(
            classID=app.applicationClassID,
            courseID=app.applicationCourseID,
            enrolmentPeriodID=period.enrolmentPeriodID).first()
        trainer = Trainer.query.filter_by(
            trainerID=class_n.trainerAssignedID).first()
        output = Application.display_json(app, course, class_n, trainer)
        combined.append(output)

    if len(combined) > 0:
        return jsonify({
            "data": combined
        }), 200
    else:
        return jsonify({
            "message": "Applications not found."
        }), 404


@app.route("/viewEligibleCourses/<string:learnerID>")
def viewEligibleCourses(learnerID):
    learner = Learner.query.filter_by(learnerID=learnerID).first()
    classes = Classes.query.all()
    applications = Application.query.filter_by(applicationLearnerID=learnerID)
    appList = []
    filteredOutputList = []
    outputList = []

    for application in applications:
        if ((application.applicationCourseID, application.applicationClassID)
                not in appList and
                application.applicationStatus == "Processing"):
            appList.append((application.applicationCourseID,
                           application.applicationClassID))

    for session in classes:
        period = ApplicationPeriod.query.filter_by(
            enrolmentPeriodID=session.enrolmentPeriodID).first()
        enddate = period.enrolmentEndDate
        course = Course.query.filter_by(
            courseID=session.courseID).first()
        if (learner.courseEligibility(course.prerequisite)
                == learner.coursesTaken and
                learner.checkCourseTaken(session.courseID)
                == learner.coursesTaken):
            trainer = Trainer.query.filter_by(
                trainerID=session.trainerAssignedID).first()
            output = Classes.class_for_currEnrolmentPeriod(
                session, enddate, course, trainer)
            if (output != "False"):
                outputList.append(output)

    for output in outputList:
        if ((output['courseID'], output['classID']) not in appList
                and output not in filteredOutputList):
            filteredOutputList.append(output)

    if len(outputList) > 0:
        return jsonify({
            "data": filteredOutputList
        }), 200
    else:
        return jsonify({
            "message": "Learner ID does not exist or no eligible courses."
        }), 404


@app.route("/create_applications", methods=['POST'])
def create_application():
    data = request.get_json()

    applicationID = None
    applicationLearnerID = data['applicationLearnerID']
    applicationClassID = data['applicationClassID']
    applicationCourseID = data['applicationCourseID']
    applicationStatus = data['applicationStatus']
    enrolmentPeriodID = data['enrolmentPeriodID']
    applicationDate = datetime.now()
    adminID = ""

    application = Application(
        applicationID=applicationID,
        applicationLearnerID=applicationLearnerID,
        applicationClassID=applicationClassID,
        applicationCourseID=applicationCourseID,
        applicationStatus=applicationStatus,
        applicationDate=applicationDate,
        enrolmentPeriodID=enrolmentPeriodID,
        adminID=adminID
    )

    enrolmentPeriod = ApplicationPeriod.query.filter_by(
        enrolmentPeriodID=enrolmentPeriodID).first()
    # application needs to be within the enrolment Period
    check = application.checkEnrolmentPeriod(enrolmentPeriod)

    if (check is True):
        # there should not be application for the same course in the same term
        dupcheck = application.query.filter_by(
            applicationLearnerID=applicationLearnerID,
            applicationCourseID=applicationCourseID,
            enrolmentPeriodID=enrolmentPeriodID,
            applicationStatus=applicationStatus).count()

        if (dupcheck == 0):
            try:
                db.session.add(application)
                db.session.commit()
            except Exception:
                return jsonify({
                    "message": "Unable to commit to database."
                }), 500
            return jsonify(application.json()), 201

        else:
            return jsonify({
                "message":
                    "Duplicated application." +
                    "Not allowed to apply for same course."
            }), 404
    else:
        return jsonify({
            "message": check
        }), 404


@app.route("/updateApplicationStatus", methods=['POST', 'PUT'])
def updateApplicationStatus():
    data = request.get_json()
    applicationID = data['applicationID']
    application = Application.query.filter_by(
        applicationID=applicationID).first()

    if application:
        try:
            application.applicationStatus = data["applicationStatus"]
            db.session.merge(application)
            db.session.commit()
            return jsonify(application.json()), 201
        except Exception:
            return jsonify({
                "message": "Unable to commit to database."
            }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
