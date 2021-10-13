import unittest
from unittest import mock
from datetime import datetime
from learner import Learner
from classes import Classes
from application import Application
from admin import Admin
from trainer import Trainer
from course import Course

# User Story 1e, 1f, 1g

class TestApplication(unittest.TestCase):

    def setUp(self):
        self.learner = Learner('Phris', "L001", "phris@smu.edu.sg", ["IS111", "IS213", "IS215"]) 
        self.course = Course('IS212', "Software Project Management", "Software project management is dedicated to the planning, scheduling, resource allocation, execution, tracking, and delivery of software and web projects.", ["IS111", "IS213"], 1, ["G1"], "Software Development")
        self.class1 = Classes("G1", "IS212", 20, "T001", datetime(2021, 10, 27), datetime(2022, 1, 31), [])
        self.trainer = Trainer('Chris', "T001", "chris@smu.edu.sg", ["project management", "product services", "software development"], "3-years experience in customer service...", ["IS212", "IS213", "IS215"])
        self.application1 = Application("L001", "G1", "Processing", datetime(2021, 8, 1), datetime(2021, 8, 31), "Admin001")
        self.application2 = Application("L001", "G1", "Draft", datetime(2021, 8, 1), datetime(2021, 8, 31), "Admin001")
        self.admin1 = Admin('HR', "Admin001", "hr@smu.edu.sg")

    def tearDown(self):
        self.learner = None
        self.course = None
        self.class1 = None
        self.trainer = None
        self.application1 = None
        self.application2 = None
        self.admin1 = None

    def test_ChangeStatus(self):
        # application status for the class of course exist
        appAdmin = self.application1.adminID
        # administrator exist
        self.assertIs(self.admin1.get_id(), appAdmin)
        self.assertEqual(self.admin1.get_id(), appAdmin)
        # contact of L&D administrator exist
        self.assertEqual(self.admin1.get_contact(), "hr@smu.edu.sg")
        status = self.application1.get_appStatus()
        # application status - "Processing" exist
        self.assertEqual(status, "Processing")
        # application change works, and status - "Withdrawn" exist
        status = self.application1.changeStatus("Withdrawn")
        self.assertEqual(status, "Withdrawn")

    def test_viewApplication(self):
        # application details exists - name, contact, class, class start date, class end date, trainer assigned, and course
        self.assertIs(self.application1.get_appLearner(), self.learner.get_id())
        self.assertEqual(self.application1.get_appLearner(), self.learner.get_id())
        self.assertEqual(self.learner.get_contact(), "phris@smu.edu.sg")
        self.assertIs(self.class1.get_classID(), self.application1.get_appClassID())
        self.assertEqual(self.class1.get_classID(), self.application1.get_appClassID())
        self.assertEqual(self.class1.get_startDate(), datetime(2021, 10, 27))
        self.assertEqual(self.class1.get_endDate(), datetime(2022, 1, 31))
        self.assertEqual(self.class1.get_trainerAssignedID(), "T001")
        self.assertIs(self.trainer.get_trainerID(), self.class1.get_trainerAssignedID())
        self.assertEqual(self.trainer.get_trainerID(), self.class1.get_trainerAssignedID())
        self.assertEqual(self.trainer.get_name(), "Chris")
        self.assertEqual(self.class1.get_courseID(), "IS212")
        self.assertIs(self.course.get_courseID(), self.class1.get_courseID())
        self.assertEqual(self.course.get_courseID(), self.class1.get_courseID())
        self.assertEqual(self.course.get_courseName(), "Software Project Management")

    def test_enrolApplication(self):
        # self-enrolment period for self-enrolment application exists
        reg_startDate = self.application2.get_regStartDate()
        reg_endDate = self.application2.get_regEndDate()
        self.assertEqual(reg_startDate, datetime(2021, 8, 1))
        self.assertEqual(reg_endDate, datetime(2021, 8, 31))
        # application status is in "draft" status before submission
        self.assertEqual(self.application2.get_appStatus(), "Draft")
        # course applied must be eligible for the learner
        prerequisite = self.course.get_prerequisite()
        self.assertEqual(self.learner.courseEligibility(prerequisite), self.learner.get_coursesTaken())
        # cannot submit application after self-enrolment period
        self.assertRaises(Exception, self.application2.checkEnrolmentPeriod, datetime.now())

if __name__ == "__main__":
    unittest.main()
