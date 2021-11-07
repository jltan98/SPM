import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('dbURL')
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

    def getCoursesTakenIDs(self):
        coursesTakenIDs = []
        coursesTakenIDs = list(map(str.strip,
                                   self.coursesTaken.split(',')))
        return coursesTakenIDs

    def getCoursesTakenAsDictionary(self, dictCourses):
        coursesTaken = []
        coursesTakenIDs = self.getCoursesTakenIDs()
        # create list of courses taken by the learner.
        # this will store the entire course details, not just ID
        # iterate all courses taken
        for cid in coursesTakenIDs:
            # get the course information from the all courses
            # dictionary we created on top
            if cid in dictCourses:
                ct = dictCourses[cid]
                if ct is not None:
                    # create dictionary to store the details
                    dictCourseTaken = {}
                    dictCourseTaken["courseID"] = ct['courseID']
                    dictCourseTaken["courseName"] = ct['courseName']
                    dictCourseTaken["courseDescription"] = ct[
                                                        'courseDescription']
                    dictCourseTaken["subjectcategory"] = ct[
                                                        'subjectcategory']
                    prerequisite = ct['prerequisite'].split(',')
                    dictCourseTaken["prerequisite"] = prerequisite

                    # add the details to list of courses taken
                    coursesTaken.append(dictCourseTaken)
        return coursesTaken

    def getLearnerCurrentAppliedCoursesAsDictionary(self):
        # create list of learner applied courses
        learnerCurrentAppliedCourses = []

        # get all outstanding applications by learner
        # (status != successful and unsuccessful)
        learnerOutstandingApplications = Application.query.filter(
            Application.applicationLearnerID == self.learnerID,
            Application.applicationStatus != 'Successful',
            Application.applicationStatus != 'Unsuccessful')

        # iterate learners current applications
        for learnerApplication in learnerOutstandingApplications:
            learnerCurrentAppliedCourses.append(
                learnerApplication.applicationCourseID)
        return learnerCurrentAppliedCourses

    def getLearnerEligibleClassesAsDictionary(self, classesWithPrereq):
        appliedCourse_dict = self.getLearnerCurrentAppliedCoursesAsDictionary()
        learnerCurrentAppliedCourses = appliedCourse_dict
        coursesTakenIDs = self.getCoursesTakenIDs()
        # create list of eligible classes for the learner
        eligibleClasses = []
        # iterate all classes with prerequisites
        for c in classesWithPrereq:
            if datetime.now() >= c["startDate"]:
                continue
            # the learner is eligible to class if the course assigned to class
            # if course is not in the list of courses taken by learner
            # and the course has no prerequisite
            # or course is not in the list of courses taken by learner
            # and all prerequisites are already taken
            if (c['courseID'] not in coursesTakenIDs
                    and c['coursePrereq'] == ['']) or \
                    (c['courseID'] not in coursesTakenIDs
                        and set(c['coursePrereq']).issubset(
                                                set(coursesTakenIDs))):
                eligibleClassesDetails = {}
                eligibleClassesDetails["class"] = c
                inprogress = False
                if c['courseID'] in learnerCurrentAppliedCourses:
                    inprogress = True
                eligibleClassesDetails["inprogress"] = inprogress
                eligibleClasses.append(eligibleClassesDetails)
        return eligibleClasses


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

    def getAllCoursesAsDictionary():
        allCourses = Course.query.all()
        dictCourses = {}
        for course in allCourses:
            dictCourseDetail = {}
            dictCourseDetail["courseID"] = course.courseID
            dictCourseDetail["courseName"] = course.courseName
            dictCourseDetail["courseDescription"] = course.courseDescription
            dictCourseDetail["subjectcategory"] = course.subjectcategory
            dictCourseDetail["prerequisite"] = course.prerequisite
            # assign the current course to the course id in dictionary
            dictCourses[course.courseID] = dictCourseDetail
        return dictCourses


class enrolmentPeriod(db.Model):
    __tablename__ = 'enrolmentPeriod'

    enrolmentPeriodID = db.Column(db.String(64), primary_key=True)
    enrolmentStartDate = db.Column(db.DateTime)
    enrolmentEndDate = db.Column(db.DateTime)

    def __init__(self,
                 enrolmentPeriodID="",
                 enrolmentStartDate="",
                 enrolmentEndDate=""):
        self.enrolmentPeriodID = enrolmentPeriodID
        self.enrolmentStartDate = enrolmentStartDate
        self.enrolmentEndDate = enrolmentEndDate

    def json(self):
        return {
            'enrolmentPeriodID': self.enrolmentPeriodID,
            'enrolmentStartDate': self.enrolmentStartDate,
            'enrolmentEndDate': self.enrolmentEndDate,
        }

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
        'enrolmentPeriod.enrolmentPeriodID'), primary_key=True)

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

    def class_for_currEnrolmentPeriod(self, enddate, course, trainer):
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

    def GetClassesByStatus(classesStatus):
        from src.enums import ClassesStatus
        if classesStatus == ClassesStatus.FUTURE:
            classes = db.session.query(Classes, Course).filter(
                Classes.courseID == Course.courseID,
                Classes.startDate > datetime.now())
            return classes
        elif classesStatus == ClassesStatus.PAST:
            classes = db.session.query(Classes, Course).filter(
                Classes.courseID == Course.courseID,
                Classes.endDate < datetime.now())
            return classes
        elif classesStatus == ClassesStatus.STARTED:
            classes = db.session.query(Classes, Course).filter(
                Classes.courseID == Course.courseID,
                Classes.startDate <= datetime.now(),
                Classes.endDate >= datetime.now())
            return classes
        else:
            # all classes past present future
            classes = db.session.query(Classes, Course).filter(
                Classes.courseID == Course.courseID)
            return classes

    def GetClassesJoinCoursesAsDictionary(classesStatus):
        from src.enums import ClassesStatus
        classesStatus = ClassesStatus.ALL
        classes = Classes.GetClassesByStatus(classesStatus)
        db.session.close()
        classesWithPrereq = []
        for c in classes:
            dictClassWithPrereq = {}
            # class details. c[0] is for Classes, c[1] is for Course.
            # db.session.query(Classes,Course),Classes_index=0,Course_index=1
            dictClassWithPrereq["classID"] = c[0].classID
            dictClassWithPrereq["courseID"] = c[0].courseID
            dictClassWithPrereq["noOfSlots"] = c[0].noOfSlots
            dictClassWithPrereq["trainerAssignedID"] = c[0].trainerAssignedID
            dictClassWithPrereq["enrolmentPeriodID"] = c[0].enrolmentPeriodID
            dictClassWithPrereq["startDate"] = c[0].startDate
            dictClassWithPrereq["endDate"] = c[0].endDate
            # split the string to an array
            dictClassWithPrereq["coursePrereq"] = c[1].prerequisite.split(',')
            # create dictionary to store the course details
            dictCourse = {}
            # course details
            dictCourse["courseID"] = c[1].courseID
            dictCourse["courseName"] = c[1].courseName
            dictCourse["courseDescription"] = c[1].courseDescription
            dictCourse["subjectcategory"] = c[1].subjectcategory
            dictCourse["prerequisite"] = c[1].prerequisite.split(',')
            # add the details to course in class details
            dictClassWithPrereq["course"] = dictCourse
            # create dictionary to store the EnrolmentPeriod. Get from [2]
            dictEnrolmentPeriod = {}
            dictEnrolmentPeriod["enrolmentPeriodID"] = c[2].enrolmentPeriodID
            dictEnrolmentPeriod["enrolmentStartDate"] = c[2].enrolmentStartDate
            dictEnrolmentPeriod["enrolmentEndDate"] = c[2].enrolmentEndDate
            dictClassWithPrereq["enrolmentPeriod"] = dictEnrolmentPeriod
            # add the class details to the class list
            classesWithPrereq.append(dictClassWithPrereq)
        return classesWithPrereq


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
        'enrolmentPeriod.enrolmentPeriodID'))
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
            'classEndDate': class_n.endDate}

    def checkEnrolmentPeriod(self, appPeriod):
        if (self.enrolmentPeriodID == appPeriod.enrolmentPeriodID):
            if (self.applicationDate > appPeriod.enrolmentStartDate and
                    self.applicationDate < appPeriod.enrolmentEndDate):
                return True
            else:
                raise Exception("Enrolment Period has passed.")
        else:
            raise Exception("Enrolment period does not match up.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
