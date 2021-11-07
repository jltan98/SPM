from operator import and_, or_
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import query
from sqlalchemy.orm.query import Query 
from sqlalchemy.sql import case
from flask_cors import CORS
import json
from datetime import date, datetime

from sqlalchemy.sql.expression import false, true
from classObjects import ClassesStatus, Learner, Trainer, Administrator, Classes, Course, Application, ApplicationPeriod


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
    # adminID should be empty if self enroled
    if 'adminID' in data:
        adminID = data['adminID']

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
            # check if slots are still available
            slotsTaken = Application.query.filter(Application.applicationClassID==application.applicationClassID, Application.applicationCourseID==application.applicationCourseID,Application.enrolmentPeriodID==application.enrolmentPeriodID,Application.applicationStatus!='Unsuccessful',Application.applicationStatus!='Successful').count()
            noOfSlots = Classes.query.filter_by(classID=application.applicationClassID,courseID=application.applicationCourseID,enrolmentPeriodID=application.enrolmentPeriodID).first().noOfSlots
            if (noOfSlots - slotsTaken) > 0:
                try:
                    db.session.add(application,)
                    db.session.commit()
                except Exception:
                    return jsonify({
                        "message": "Unable to commit to database."
                    }), 500
                return jsonify(application.json()), 201
            else:
                return jsonify({
                "message": "No slots available."
                }), 404
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
    #get applications joined with Classes, Course, Learner. this will return only applications with matching data of joined classes
    #applications will return results even if the outer joins Administrator and Application period has no matching data
    applications = db.session.query(Application,Classes,Course,Learner,Administrator,ApplicationPeriod) \
            .join(Classes, \
                and_(Application.applicationClassID==Classes.classID, \
                and_(Application.applicationCourseID==Classes.courseID,Application.enrolmentPeriodID==Classes.enrolmentPeriodID))) \
            .join(Course,Application.applicationCourseID==Course.courseID) \
            .join(Learner,Application.applicationLearnerID==Learner.learnerID) \
            .outerjoin(Administrator,Application.adminID==Administrator.adminID) \
            .outerjoin(ApplicationPeriod,Application.enrolmentPeriodID==ApplicationPeriod.enrolmentPeriodID) \
        .filter(Application.applicationStatus==status)
            #.join(Classes,Application.applicationClassID==Classes.classID,isouter=true)
    #applications = db.session.query(Application,Classes).outerjoin(Classes, and_(Application.applicationClassID==Classes.classID,and_(Application.applicationCourseID==Classes.courseID,Application.enrolmentPeriodID==Classes.enrolmentPeriodID)))

    #create list to store applications
    apps=[]

    #iterate applications
    for ap in applications:
        #create dictionary for application
        #in db.session.query(Application,Classes,Course,Learner,Administrator,ApplicationPeriod), Classes=Application = 0
        dictApplications={}
        dictApplications["applicationID"]=ap[0].applicationID
        dictApplications["applicationClassID"]=ap[0].applicationClassID
        dictApplications["applicationCourseID"]=ap[0].applicationCourseID
        dictApplications["enrolmentPeriodID"]=ap[0].enrolmentPeriodID
        dictApplications["applicationLearnerID"]=ap[0].applicationLearnerID
        dictApplications["applicationStatus"]=ap[0].applicationStatus
        dictApplications["applicationDate"]=ap[0].applicationDate
        
        #in db.session.query(Application,Classes,Course,Learner,Administrator,ApplicationPeriod), Classes=1
        dictClass={}
        dictClass["classID"]=ap[1].classID
        dictClass["courseID"]=ap[1].courseID
        dictClass["noOfSlots"]=ap[1].noOfSlots
        dictClass["trainerAssignedID"]=ap[1].trainerAssignedID
        dictClass["startDate"]=ap[1].startDate
        dictClass["endDate"]=ap[1].endDate
        dictClass["enrolmentPeriodID"]=ap[1].enrolmentPeriodID
        dictApplications["class"]=dictClass

        #in db.session.query(Application,Classes,Course,Learner,Administrator,ApplicationPeriod), Course=2
        dictCourse={}
        dictCourse["courseID"] = ap[2].courseID
        dictCourse["courseName"] = ap[2].courseName
        dictCourse["courseDescription"] = ap[2].courseDescription
        dictCourse["prerequisite"] = ap[2].prerequisite
        dictCourse["noOfClasses"] = ap[2].noOfClasses
        dictCourse["subjectcategory"] = ap[2].subjectcategory
        dictApplications["course"]=dictCourse

        #in db.session.query(Application,Classes,Course,Learner,Administrator,ApplicationPeriod), learner=3
        dictLearner={}
        dictLearner["learnerID"] = ap[3].learnerID
        dictLearner["learnerName"] = ap[3].learnerName
        dictLearner["learnerContact"] = ap[3].learnerContact
        dictLearner["coursesTaken"] = ap[3].coursesTaken
        dictApplications["learner"]=dictLearner

        #in db.session.query(Application,Classes,Course,Learner,Administrator,ApplicationPeriod), Administrator=4
        dictAdministrator={}
        if "adminID" in ap:
            dictAdministrator["adminID"] = ap[4].adminID
            dictAdministrator["adminName"] = ap[4].adminName
            dictAdministrator["adminContact"] = ap[4].adminContact
        dictApplications["administrator"]=dictAdministrator       

         #in db.session.query(Application,Classes,Course,Learner,Administrator,ApplicationPeriod), ApplicationPeriod=4
        dictEnrolmentPeriod={}
        dictEnrolmentPeriod["enrolmentPeriodID"]=ap[5].enrolmentPeriodID
        dictEnrolmentPeriod["enrolmentStartDate"]=ap[5].enrolmentStartDate
        dictEnrolmentPeriod["enrolmentEndDate"]=ap[5].enrolmentEndDate
        dictApplications["enrolmentPeriod"]=dictEnrolmentPeriod
        apps.append(dictApplications)

    try:
        return jsonify(apps), 200
    except Exception as e:
        return jsonify({
            "message": "Applications not found."
        }), 404
@app.route("/viewapplications_old/<string:status>")
def viewapplications_old(status):
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
    #get all courses as dictionary, to be used later 
    dictCourses = Course.getAllCoursesAsDictionary()
    #get all classes with prerequisites as dictionary
    classesWithPrereq = Classes.GetClassesJoinCoursesAsDictionary(ClassesStatus.FUTURE)

    #get all learners
    learners=Learner.query.all()

    #create list of learners with information about classes learners are eligible to take
    #this list will be the primary data we will display in the html age
    learnersWithEligibleClasses=[]

    #iterate all learners
    for l in learners:
        #create dictionary to store learner details
        dictLearnerWithEligibleClasses={}

        #learner details
        dictLearnerWithEligibleClasses["learnerID"]=l.learnerID
        dictLearnerWithEligibleClasses["learnerName"]=l.learnerName
        dictLearnerWithEligibleClasses["learnerContact"]=l.learnerContact

        #add the list of courses taken to learner details
        dictLearnerWithEligibleClasses["coursesTaken"]=l.getCoursesTakenAsDictionary(dictCourses)
        #add the list of eligible classes to learner details
        dictLearnerWithEligibleClasses["eligibleClasses"]=l.getLearnerEligibleClassesAsDictionary(classesWithPrereq)

        #add the details of learner to list of learners
        learnersWithEligibleClasses.append(dictLearnerWithEligibleClasses)

    #return the list of learner after it is converted to json
    return jsonify(learnersWithEligibleClasses), 200
@app.route("/viewClasses")
def viewClasses():
    classes = Classes.GetClassesJoinCoursesAsDictionary(ClassesStatus.FUTURE)
    if classes:
        return jsonify(classes), 200
    else:
        return jsonify({
            "message": "Classes not found."
        }), 404

@app.route("/updateClassTrainer", methods=['POST', 'PUT'])
def updateClassTrainer():
    data = request.get_json()
    classID = data['classID']
    courseID = data['courseID']
    enrolmentPeriodID = data['enrolmentPeriodID']
    trainerAssignedID=data['trainerAssignedID']
    clas = Classes.query.filter(Classes.classID==classID,Classes.courseID==courseID,Classes.enrolmentPeriodID==enrolmentPeriodID).first()
    if clas:
        try:
            clas.trainerAssignedID = trainerAssignedID
            db.session.merge(clas)
            db.session.commit()
            return jsonify(clas.json()), 201
        except Exception as e:
            return jsonify({
                "message": "Unable to commit to database."
            }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
