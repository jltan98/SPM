from typing import List
import unittest
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date, datetime
from classObjects import Learner, Trainer, Administrator, Classes, Course, Application, ApplicationPeriod
from enrolment import learnersClasses, viewapplications
from enums import ClassesStatus

class TestViewApplications(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql+mysqlconnector://root:root' + \
                                                '@localhost:3306/LMSTest'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

        db = SQLAlchemy(self.app)
        db.init_app(self.app)
        self.app.app_context().push()
        self.expected = [{'adminID': 'admin001', 'applicationClassID': 'G1', 'applicationCourseID': 'IS212', 'applicationCourseName': 'Software Project Management', 'applicationDate': 'Sun, 31 Oct 2021 19:58:23 GMT', 'applicationID': 1, 'applicationLearnerID': 'L001', 'applicationStatus': 'Processing', 'applicationTrainerContact': 'anne@lms.com', 'applicationTrainerName': 'Anne', 'classEndDate': 'Thu, 30 Jun 2022 00:00:00 GMT', 'classStartDate': 'Mon, 10 Jan 2022 00:00:00 GMT', 'enrolmentPeriodID': 'FY20/21 Session 2'},
{'adminID': 'admin002', 'applicationClassID': 'G1', 'applicationCourseID': 'IS214', 'applicationCourseName': 'Analytics Foundation', 'applicationDate': 'Sun, 31 Oct 2021 19:58:23 GMT', 'applicationID': 2, 'applicationLearnerID': 'L002', 'applicationStatus': 'Processing', 'applicationTrainerContact': 'bill@lms.com', 'applicationTrainerName': 'Bill', 'classEndDate': 'Thu, 30 Jun 2022 00:00:00 GMT', 'classStartDate': 'Mon, 10 Jan 2022 00:00:00 GMT', 'enrolmentPeriodID': 'FY20/21 Session 2'},
{'adminID': 'admin003', 'applicationClassID': 'G3', 'applicationCourseID': 'IS213', 'applicationCourseName': 'Solution Development', 'applicationDate': 'Sun, 31 Oct 2021 19:58:23 GMT', 'applicationID': 3, 'applicationLearnerID': 'L003', 'applicationStatus': 'Processing', 'applicationTrainerContact': '', 'applicationTrainerName': '', 'classEndDate': '', 'classStartDate': '', 'enrolmentPeriodID': 'FY20/21 Session 2'}]

    def tearDown(self):
        self.app=None
        db=None

    def test_viewApplications2(self):
        applications = viewapplications("Processing")
       #a = applications
        self.assertEqual(applications[0].json["data"],self.expected)

class TestLearnersClasses(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root' + \
                                                '@localhost:3306/LMSTest'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

        db = SQLAlchemy(self.app)
        db.init_app(self.app)
        self.app.app_context().push()
        self.expected = [{'coursesTaken': [...], 'eligibleClasses': [...], 'learnerContact': 'alivia@lms.com', 'learnerID': 'L001', 'learnerName': 'Alivia'}, {'coursesTaken': [...], 'eligibleClasses': [...], 'learnerContact': 'stella@lms.com', 'learnerID': 'L002', 'learnerName': 'Stella'}, {'coursesTaken': [...], 'eligibleClasses': [...], 'learnerContact': 'natalie@lms.com', 'learnerID': 'L003', 'learnerName': 'Natalie'}, {'coursesTaken': [...], 'eligibleClasses': [...], 'learnerContact': 'lyndy@lms.com', 'learnerID': 'L004', 'learnerName': 'Lyndy'}, {'coursesTaken': [...], 'eligibleClasses': [...], 'learnerContact': 'mabel@lms.com', 'learnerID': 'L005', 'learnerName': 'Mabel'}]
    def tearDown(self):
        self.app=None
        db=None

    def test_learnersClasses(self):
        classes = learnersClasses()
        self.assertEqual(len(classes[0].json),len(self.expected))

class TestClasses(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root' + \
                                                '@localhost:3306/LMSTest'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

        db = SQLAlchemy(self.app)
        db.init_app(self.app)
        self.app.app_context().push()
        self.expected = [{'coursesTaken': [...], 'eligibleClasses': [...], 'learnerContact': 'alivia@lms.com', 'learnerID': 'L001', 'learnerName': 'Alivia'}, {'coursesTaken': [...], 'eligibleClasses': [...], 'learnerContact': 'stella@lms.com', 'learnerID': 'L002', 'learnerName': 'Stella'}, {'coursesTaken': [...], 'eligibleClasses': [...], 'learnerContact': 'natalie@lms.com', 'learnerID': 'L003', 'learnerName': 'Natalie'}, {'coursesTaken': [...], 'eligibleClasses': [...], 'learnerContact': 'lyndy@lms.com', 'learnerID': 'L004', 'learnerName': 'Lyndy'}, {'coursesTaken': [...], 'eligibleClasses': [...], 'learnerContact': 'mabel@lms.com', 'learnerID': 'L005', 'learnerName': 'Mabel'}]
    def tearDown(self):
        self.app=None
        db=None

    def test_Classes(self):
        classes = Classes.GetClassesJoinCoursesAsDictionary(ClassesStatus.FUTURE)
        c = classes
        self.assertEqual(len(classes[0].json),len(self.expected))



if __name__ == "__main__":
    unittest.main()
