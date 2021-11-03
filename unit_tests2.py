from typing import List
import unittest
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date, datetime
from classObjects import Learner, Trainer, Administrator, Classes, Course, Application, ApplicationPeriod
from enrolment import learnersClasses, viewapplications

class TestViewApplications(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root' + \
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
        self.expected = [{'adminID': 'admin001', 'applicationClassID': 'G1', 'applicationCourseID': 'IS212', 'applicationCourseName': 'Software Project Management', 'applicationDate': 'Sun, 31 Oct 2021 19:58:23 GMT', 'applicationID': 1, 'applicationLearnerID': 'L001', 'applicationStatus': 'Processing', 'applicationTrainerContact': 'anne@lms.com', 'applicationTrainerName': 'Anne', 'classEndDate': 'Thu, 30 Jun 2022 00:00:00 GMT', 'classStartDate': 'Mon, 10 Jan 2022 00:00:00 GMT', 'enrolmentPeriodID': 'FY20/21 Session 2'},
{'adminID': 'admin002', 'applicationClassID': 'G1', 'applicationCourseID': 'IS214', 'applicationCourseName': 'Analytics Foundation', 'applicationDate': 'Sun, 31 Oct 2021 19:58:23 GMT', 'applicationID': 2, 'applicationLearnerID': 'L002', 'applicationStatus': 'Processing', 'applicationTrainerContact': 'bill@lms.com', 'applicationTrainerName': 'Bill', 'classEndDate': 'Thu, 30 Jun 2022 00:00:00 GMT', 'classStartDate': 'Mon, 10 Jan 2022 00:00:00 GMT', 'enrolmentPeriodID': 'FY20/21 Session 2'},
{'adminID': 'admin003', 'applicationClassID': 'G3', 'applicationCourseID': 'IS213', 'applicationCourseName': 'Solution Development', 'applicationDate': 'Sun, 31 Oct 2021 19:58:23 GMT', 'applicationID': 3, 'applicationLearnerID': 'L003', 'applicationStatus': 'Processing', 'applicationTrainerContact': '', 'applicationTrainerName': '', 'classEndDate': '', 'classStartDate': '', 'enrolmentPeriodID': 'FY20/21 Session 2'}]

    def tearDown(self):
        self.app=None
        db=None

    def test_learnersClasses(self):
        classes = learnersClasses()
        c = classes
       #a = applications
        #self.assertEqual(applications[0].json["data"],self.expected)

# class TestApproveApplications(unittest.TestCase):
#     def setUp(self):
#         self.url = 'http://localhost:5001/approveApplications'
#         self.selected=[1,2]
#         self.status = "Approve"
#         self.adminID="admin001"
#         self.data={'selected':self.selected,'status':self.status,'adminID':self.adminID}

#         self.app = Flask(__name__)
#         self.c = self.app.test_client()

#     def tearDown(self):
#         self.app=None

#     def test_viewApplications2(self):
#         x = self.c.post(self.url,data=self.data)
#         y=x

if __name__ == "__main__":
    unittest.main()
