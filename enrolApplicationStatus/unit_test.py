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
    def test_ChangeStatus(self):
        # application status for the class of course exist
        application = Application("L001", "G2", "Processing", datetime(2021, 8, 1), datetime(2022, 8, 31), "Admin001")
        admin1 = Admin('HR', "Admin001", "hr@smu.edu.sg")
        appAdmin = application.adminID
        # administrator exist
        self.assertIs(admin1.get_id(), appAdmin)
        self.assertEqual(admin1.get_id(), appAdmin)
        # contact of L&D administrator exist
        self.assertEqual(admin1.get_contact(), "hr@smu.edu.sg")
        status = application.get_appStatus()
        # application status - "Processing" exist
        self.assertEqual(status, "Processing")
        # application change works, and status - "Withdrawn" exist
        status = application.changeStatus("Withdrawn")
        self.assertEqual(status, "Withdrawn")

    def test_viewApplication(self):
        # application details exists - name, contact, class, class start date, class end date, trainer assigned, and course
        application = Application("L001", "G2", "Processing", datetime(2021, 8, 1), datetime(2022, 8, 31), "Admin001")
        learner = Learner('Phris', "L001", "phris@smu.edu.sg", ["IS111","IS212", "IS213", "IS215"])
        class1 = Classes("G2", "IS212", 20, "T001", datetime(2021, 10, 27), datetime(2022, 1, 31), [])
        trainer = Trainer('Chris', "T001", "chris@smu.edu.sg", ["project management", "product services", "software development"], "3-years experience in customer service...", ["IS212", "IS213", "IS215"])
        course = Course('IS212', "Software Project Management", "Software project management is dedicated to the planning, scheduling, resource allocation, execution, tracking, and delivery of software and web projects.", ["IS111", "IS213"], 1, ["G1"], "Software Development")

        self.assertIs(application.get_appLearner(), learner.get_id())
        self.assertEqual(application.get_appLearner(), learner.get_id())
        self.assertEqual(learner.get_contact(), "phris@smu.edu.sg")
        self.assertIs(class1.get_classID(), application.get_appClassID())
        self.assertEqual(class1.get_classID(), application.get_appClassID())
        self.assertEqual(class1.get_startDate(), datetime(2021, 10, 27))
        self.assertEqual(class1.get_endDate(), datetime(2022, 1, 31))
        self.assertEqual(class1.get_trainerAssignedID(), "T001")
        self.assertIs(trainer.get_trainerID(), class1.get_trainerAssignedID())
        self.assertEqual(trainer.get_trainerID(), class1.get_trainerAssignedID())
        self.assertEqual(trainer.get_name(), "Chris")
        self.assertEqual(class1.get_courseID(), "IS212")
        self.assertIs(course.get_courseID(), class1.get_courseID())
        self.assertEqual(course.get_courseID(), class1.get_courseID())
        self.assertEqual(course.get_courseName(), "Software Project Management")

    def test_enrolApplication(self):
        # self-enrolment period for self-enrolment application exists
        application = Application("L001", "G2", "Draft", datetime(2021, 8, 1), datetime(2021, 8, 31), "Admin001")
        learner = Learner('Phris', "L001", "phris@smu.edu.sg", ["IS111","IS212", "IS213", "IS215"])
        course = Course('IS212', "Software Project Management", "Software project management is dedicated to the planning, scheduling, resource allocation, execution, tracking, and delivery of software and web projects.", ["IS111", "IS213"], 1, ["G1"], "Software Development")
        
        reg_startDate = application.get_regStartDate()
        reg_endDate = application.get_regEndDate()
        self.assertEqual(reg_startDate, datetime(2021, 8, 1))
        self.assertEqual(reg_endDate, datetime(2021, 8, 31))
        # application status is in "draft" status before submission
        self.assertEqual(application.get_appStatus(), "Draft")
        # course applied must be eligible for the learner
        prerequisite = course.get_prerequisite()
        self.assertEqual(learner.courseEligibility(prerequisite), learner.get_coursesTaken())
        # cannot submit application after self-enrolment period
        self.assertRaises(Exception, application.checkEnrolmentPeriod)

if __name__ == "__main__":
    unittest.main()
