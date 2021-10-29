from logging import raiseExceptions
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from datetime import date, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root' + \
                                        '@localhost:3306/LMS'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}


db = SQLAlchemy(app)

CORS(app)


class Learner(db.Model):
    __tablename__ = 'learner'

    learnerName = db.Column(db.String(64))
    learnerID = db.Column(db.String(64), primary_key=True)
    learnerContact = db.Column(db.String(256))
    coursesTaken = db.Column(db.Text)
    password = db.Column(db.String(256))

    def __init__(self,
                 learnerName="",
                 learnerID="",
                 learnerContact="",
                 coursesTaken="",
                 password=""):
        self.learnerName = learnerName
        self.learnerID = learnerID
        self.learnerContact = learnerContact
        self.coursesTaken = coursesTaken
        self.password = password

    def json(self):
        return {
            'name': self.learnerName,
            'id': self.learnerID,
            'contact': self.learnerContact,
            'coursesTaken': self.coursesTaken.split(", ")
        }

    def courseEligibility(self, prerequisite):
        check = "True"
        prerequisiteList = prerequisite.split(", ")
        for courseID in prerequisiteList:
            if (courseID not in self.coursesTaken):
                check = "False"

        if (check == "True"):
            return self.coursesTaken
        else:
            raise Exception("Ineligible - did not fulfil prerequisite")

    def checkCourseTaken(self, courseID):
        if (courseID not in self.coursesTaken):
            return self.coursesTaken
        else:
            raise Exception("Course already taken before")


class Trainer(db.Model):
    __tablename__ = 'trainer'

    trainerName = db.Column(db.String(64))
    trainerID = db.Column(db.String(64), primary_key=True)
    trainerContact = db.Column(db.String(256))
    skills = db.Column(db.Text)
    experience = db.Column(db.Text)
    coursesTaught = db.Column(db.Text)
    password = db.Column(db.String(256))

    def __init__(self,
                 trainerName="",
                 trainerID="",
                 trainerContact="",
                 skills="",
                 experience="",
                 coursesTaught="",
                 password=""):
        self.trainerName = trainerName
        self.trainerID = trainerID
        self.trainerContact = trainerContact
        self.skills = skills
        self.experience = experience
        self.coursesTaught = coursesTaught
        self.password = password

    def json(self):
        return {
            'trainerName': self.trainerName,
            'trainerID': self.trainerID,
            'trainerContact': self.trainerContact,
            'skills': self.skills.split(", "),
            'experience': self.experience.split(", "),
            'coursesTaught': self.coursesTaught.split(", "),
        }


class Administrator(db.Model):
    __tablename__ = 'administrator'

    adminName = db.Column(db.String(64))
    adminID = db.Column(db.String(64), primary_key=True)
    adminContact = db.Column(db.String(256))
    password = db.Column(db.String(256))

    def __init__(self,
                 adminName="",
                 adminID="",
                 adminContact="",
                 password=""):
        self.adminName = adminName
        self.adminID = adminID
        self.adminContact = adminContact
        self.password = password

    def json(self):
        return {
            'adminName': self.adminName,
            'adminID': self.adminID,
            'adminContact': self.adminContact
        }


class Course(db.Model):
    __tablename__ = 'course'

    courseID = db.Column(db.String(64), primary_key=True)
    courseName = db.Column(db.String(64))
    courseDescription = db.Column(db.Text)
    prerequisite = db.Column(db.Text)
    noOfClasses = db.Column(db.Integer, default=0)
    classes = db.Column(db.Text)
    subjectcategory = db.Column(db.String(256))

    def __init__(self,
                 courseID="",
                 courseName="",
                 courseDescription="",
                 prerequisite="",
                 noOfClasses=0,
                 classes="",
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
            'prerequisite': self.prerequisite.split(", "),
            'noOfClasses': self.noOfClasses,
            'classes': self.classes.split(", "),
            'subjectcategory': self.subjectcategory,
        }


class Classes(db.Model):
    __tablename__ = 'classes'

    classID = db.Column(db.String(64), primary_key=True)
    courseID = db.Column(db.Integer, db.ForeignKey(
        'course.courseID'), primary_key=True)
    noOfSlots = db.Column(db.Integer, default=0)
    trainerAssignedID = db.Column(
        db.Integer, db.ForeignKey('trainer.trainerID'))
    startDate = db.Column(db.DateTime)
    endDate = db.Column(db.DateTime)
    enrolmentPeriodID = db.Column(db.String(64), db.ForeignKey(
        'enrolmentperiod.enrolmentPeriodID'), primary_key=True)

    def __init__(self,
                 classID="",
                 courseID="",
                 noOfSlots=0,
                 trainerAssignedID="",
                 startDate=datetime,
                 endDate=datetime,
                 enrolmentPeriodID='',
                 ):
        self.classID = classID
        self.courseID = courseID
        self.noOfSlots = noOfSlots
        self.trainerAssignedID = trainerAssignedID
        self.startDate = startDate
        self.endDate = endDate
        self.enrolmentPeriodID = enrolmentPeriodID

    def json(self):
        return {
            'classID': self.classID,
            'courseID': self.courseID,
            'noOfSlots': self.noOfSlots,
            'trainerAssignedID': self.trainerAssignedID,
            'startDate': self.startDate,
            'endDate': self.endDate,
            'enrolmentPeriodID': self.enrolmentPeriodID,
        }

    def class_for_currEnrolmentPeriod(self, enddate ,course, trainer):
        if (self.startDate > enddate):
            return {
                'courseID': self.courseID,
                'classID': self.classID,
                'noOfSlots': self.noOfSlots,
                'trainerName': trainer.trainerName,
                'startDate': self.startDate,
                'endDate': self.endDate,
                'courseName': course.courseName,
                'courseDescription': course.courseDescription,
                'subjectcategory': course.subjectcategory,
                'enrolmentPeriodID': self.enrolmentPeriodID,
            }
        return "False"

class Application(db.Model):
    __tablename__ = 'application'

    applicationID = db.Column(db.Integer, primary_key=True)  # auto increment
    applicationLearnerID = db.Column(
        db.String(64), db.ForeignKey('learner.learnerID'))
    applicationClassID = db.Column(
        db.String(64), db.ForeignKey('classes.classID'))
    applicationCourseID = db.Column(
        db.String(64), db.ForeignKey('classes.courseID'))
    applicationStatus = db.Column(db.String(64))
    applicationDate = db.Column(db.DateTime, default=datetime.now())
    enrolmentPeriodID = db.Column(db.String(64), db.ForeignKey(
        'enrolmentperiod.enrolmentPeriodID'))
    adminID = db.Column(db.String(64), db.ForeignKey('administrator.adminID'))

    def __init__(self,
                 applicationID=0,
                 applicationLearnerID="",
                 applicationClassID="",
                 applicationCourseID="",
                 applicationStatus="",
                 applicationDate="",
                 enrolmentPeriodID="",
                 adminID=""):
        self.applicationID = applicationID
        self.applicationLearnerID = applicationLearnerID
        self.applicationClassID = applicationClassID
        self.applicationCourseID = applicationCourseID
        self.applicationStatus = applicationStatus
        self.applicationDate = applicationDate
        self.enrolmentPeriodID = enrolmentPeriodID
        self.adminID = adminID

    def json(self):
        return {
            'applicationID': self.applicationID,
            'applicationLearnerID': self.applicationLearnerID,
            'applicationClassID': self.applicationClassID,
            'applicationCourseID': self.applicationCourseID,
            'applicationStatus': self.applicationStatus,
            'applicationDate': self.applicationDate,
            'enrolmentPeriodID': self.enrolmentPeriodID,
            'adminID': self.adminID
        }
    
    def display_json(self, course, class_n, trainer):
        return {
            'applicationID': self.applicationID,
            'applicationLearnerID': self.applicationLearnerID,
            'applicationClassID': self.applicationClassID,
            'applicationCourseID': self.applicationCourseID,
            'applicationStatus': self.applicationStatus,
            'applicationDate': self.applicationDate,
            'enrolmentPeriodID': self.enrolmentPeriodID,
            'adminID': self.adminID,
            'applicationCourseName': course.courseName,
            'applicationTrainerContact': trainer.trainerContact,
            'applicationTrainerName': trainer.trainerName,
            'classStartDate': class_n.startDate,
            'classEndDate': class_n.endDate
        }     

    def checkEnrolmentPeriod(self, applicationPeriod):
        if (self.enrolmentPeriodID == applicationPeriod.enrolmentPeriodID):
            if (self.applicationDate > applicationPeriod.enrolmentStartDate) and (self.applicationDate < applicationPeriod.enrolmentEndDate):
                return True
            else:
                raise Exception ("Enrolment Period has passed, not allowed to submit applications.")
        else: 
            raise Exception ("Enrolment period does not match up. Please check with your administrator.")


class ApplicationPeriod(db.Model):
    __tablename__ = 'enrolmentperiod'

    enrolmentPeriodID = db.Column(db.String(64), primary_key=True)
    enrolmentStartDate = db.Column(db.DateTime)
    enrolmentEndDate = db.Column(db.DateTime)

    def __init__(self, enrolmentPeriodID="", enrolmentStartDate="", enrolmentEndDate=""):
        self.enrolmentPeriodID = enrolmentPeriodID
        self.enrolmentStartDate = enrolmentStartDate
        self.enrolmentEndDate = enrolmentEndDate

    def json(self):
        return {
            'enrolmentPeriodID': self.enrolmentPeriodID,
            'enrolmentStartDate': self.enrolmentStartDate,
            'enrolmentEndDate': self.enrolmentEndDate,
        }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
