from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.query import Query 
from sqlalchemy.sql import case
from flask_cors import CORS
import json
from datetime import date, datetime
from classObjects import Learner, Trainer, Administrator, Classes, Course, Application, ApplicationPeriod


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
        period = ApplicationPeriod.query.filter_by(enrolmentPeriodID = app.enrolmentPeriodID).first()
        course = Course.query.filter_by(
            courseID=app.applicationCourseID).first()
        class_n = Classes.query.filter_by(
            classID=app.applicationClassID, courseID=app.applicationCourseID, enrolmentPeriodID=period.enrolmentPeriodID).first()
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
        if (application.applicationCourseID, application.applicationClassID) not in appList and (application.applicationStatus == "Processing"):
            appList.append((application.applicationCourseID,
                           application.applicationClassID))

    for session in classes:
        period = ApplicationPeriod.query.filter_by(enrolmentPeriodID=session.enrolmentPeriodID).first()
        enddate = period.enrolmentEndDate
        course = Course.query.filter_by(courseID=session.courseID).first()
        try:
            if (learner.courseEligibility(course.prerequisite) == learner.coursesTaken) and (learner.checkCourseTaken(session.courseID) == learner.coursesTaken):
                trainer = Trainer.query.filter_by(
                    trainerID=session.trainerAssignedID).first()
                output = Classes.class_for_currEnrolmentPeriod(session, enddate, course, trainer)
                if (output != "False"):
                    outputList.append(output)
        except:
            pass

    for output in outputList:
        if (output['courseID'], output['classID']) not in appList and (output not in filteredOutputList):
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
      
    enrolmentPeriod = ApplicationPeriod.query.filter_by(enrolmentPeriodID = enrolmentPeriodID).first()
    # application needs to be within the enrolment Period
    check = application.checkEnrolmentPeriod(enrolmentPeriod)

    if (check == True):
        # there should not be application for the same course in the same term
        dupcheck = application.query.filter_by(
            applicationLearnerID=applicationLearnerID, applicationCourseID=applicationCourseID, enrolmentPeriodID=enrolmentPeriodID, applicationStatus=applicationStatus).count()

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
                "message": "Duplicated application. Not allowed to apply for same course in the same enrolment period."
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

@app.route("/viewapplications/<string:status>")
def viewapplications(status):
    applications = Application.query.filter_by(
        applicationStatus=status)
    combined = []
    for app in applications:
        period = ApplicationPeriod.query.filter_by(enrolmentPeriodID = app.enrolmentPeriodID).first()
        course = Course.query.filter_by(
            courseID=app.applicationCourseID).first()
        class_n = Classes.query.filter_by(
            classID=app.applicationClassID, courseID=app.applicationCourseID, enrolmentPeriodID=period.enrolmentPeriodID).first()
        if class_n == None:
            trainer=None
        else:
            trainer = Trainer.query.filter_by(
                trainerID=class_n.trainerAssignedID).first()
        output = Application.display_json(app, course, class_n, trainer)
        combined.append(output)

    try:
        return jsonify({
            "data": combined
        }), 200
    except Exception as e:
        return jsonify({
            "message": "Applications not found."
        }), 404

    # if len(combined) > 0:
    #     return jsonify({
    #         "data": combined
    #     }), 200
    # else:
    #     return jsonify({
    #         "message": "Applications not found."
    #     }), 404

@app.route("/approveApplications", methods=['POST', 'PUT'])
def approveApplications():
    data = request.get_json()
    selected = data['selected']
    status = data['status']
    adminId = data['adminID']
    applications = Application.query.filter(Application.applicationID.in_(selected))
    if applications.count()>0:
        try:
            db.session.query(Application).filter(Application.applicationID.in_(selected)) \
            .update({
                Application.applicationStatus:status,
                Application.adminID:adminId
                },synchronize_session=False)
            db.session.commit()
            return jsonify({"message":"updated"}), 201
        except Exception as e:
            return jsonify({
                "message": e
           }), 500
    
@app.route("/learnersClasses")
def learnersClasses():
    classes = db.session.query(Classes,Course).filter(Classes.courseID==Course.courseID)
    classesWithPrereq=[]
    for c in classes:
        dictClassWithPrereq={}
        #class
        dictClassWithPrereq["classID"]=c[0].classID
        dictClassWithPrereq["courseID"]=c[0].courseID
        dictClassWithPrereq["noOfSlots"]=c[0].noOfSlots
        dictClassWithPrereq["trainerAssignedID"]=c[0].trainerAssignedID
        dictClassWithPrereq["enrolmentPeriodID"]=c[0].enrolmentPeriodID
        dictClassWithPrereq["startDate"]=c[0].startDate
        dictClassWithPrereq["endDate"]=c[0].endDate
        dictClassWithPrereq["coursePrereq"]=c[1].prerequisite.split(',')
        #course
        dictCourse={}
        dictCourse["courseID"]=c[1].courseID
        dictCourse["courseName"]=c[1].courseName
        dictCourse["courseDescription"]=c[1].courseDescription
        dictCourse["subjectcategory"]=c[1].subjectcategory
        dictCourse["prerequisite"]=c[1].prerequisite.split(',')
        dictClassWithPrereq["courses"]=dictCourse
        classesWithPrereq.append(dictClassWithPrereq)

    learners=Learner.query.all()
    learnersWithEligibleClasses=[]
    for l in learners:
        dictLearnerWithEligibleClasses={}
        dictLearnerWithEligibleClasses["learnerID"]=l.learnerID
        dictLearnerWithEligibleClasses["learnerName"]=l.learnerName
        dictLearnerWithEligibleClasses["learnerContact"]=l.learnerContact
        
        coursesTakenIds=[]
        #remove before and after blank spaces
        for ctId in l.coursesTaken.split(','):
            coursesTakenIds.append(ctId.strip())

        coursesTaken=[]
        for cid in coursesTakenIds:
            ct = Course.query.filter(Course.courseID==cid.strip()).first()
            if ct != None:
                dictCourse={}
                dictCourse["courseID"]=ct.courseID
                dictCourse["courseName"]=ct.courseName
                dictCourse["courseDescription"]=ct.courseDescription
                dictCourse["subjectcategory"]=ct.subjectcategory
                dictCourse["prerequisite"]=ct.prerequisite.split(',')
                coursesTaken.append(dictCourse)
        dictLearnerWithEligibleClasses["coursesTaken"]=coursesTaken
        eligibleClasses=[]

        for c in classesWithPrereq:
            if (c['courseID'] not in coursesTakenIds and c['coursePrereq'] == [''])or \
                (c['courseID'] not in coursesTakenIds and set(c['coursePrereq']).issubset(set(coursesTakenIds))):
                eligibleClasses.append(c)
        dictLearnerWithEligibleClasses["eligibleClasses"]=eligibleClasses
        learnersWithEligibleClasses.append(dictLearnerWithEligibleClasses)
    return jsonify(learnersWithEligibleClasses), 200
    #return learnersWithEligibleClasses
    # if learner:
    #     return jsonify({
    #         "data": learner.json()
    #     }), 200
    # else:
    #     return jsonify({
    #         "message": "Learner ID not found."
    #     }), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
