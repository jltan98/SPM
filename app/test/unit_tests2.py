from typing import List
import unittest
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date, datetime
import sys
sys.path.append('./app')
if True:  # noqa: E402
    from src.classobj import Learner, Trainer, Administrator, Classes, Course, Application, enrolmentPeriod

class TestLearner(unittest.TestCase):
    def setUp(self):
        self.Learner = Learner('Alivia','L003','alivia@lms.com','IS110,IS213,IS111','1234')
        self.Application = Application(1, "L001", "G1", "IS212", "Processing",
                                        datetime(2021, 10, 20),
                                        'FY20/21 Session 2', "admin001")
    def tearDown(self):
        self.Application = None
        self.Learner = None
        
    def test_getLearnerCurrentAppliedCoursesAsDictionary(self):
        learnerCurrentAppliedCourses = self.Learner.getLearnerCurrentAppliedCoursesAsDictionary()
        expectedValue = ['IS211']
        self.assertEqual(expectedValue,learnerCurrentAppliedCourses)

    def test_getCoursesTakenIDs(self):
        learnerCoursesTaken = self.Learner.getCoursesTakenIDs()
        expectedValue = ['IS110','IS213','IS111']
        self.assertEqual(expectedValue,learnerCoursesTaken)


if __name__ == "__main__":
    unittest.main()
