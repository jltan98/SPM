import unittest
from unittest import mock
from datetime import datetime
from learner import Learner
from trainer import Trainer
from course import Course
from classes import Classes
# from enrolment import Learner, Trainer, Course, Classes

class TestViewEligibleCourses(unittest.TestCase):
    # Check if learner is eligible for the course
    def test_eligibility(self):
        learner = Learner("Phris", "phris@smu.edu.sg", ["IS111","IS212", "IS213", "IS215"])
        course = Course('IS212', "Software Project Management", "Software project management is dedicated to the planning, scheduling, resource allocation, execution, tracking, and delivery of software and web projects.", ["IS111", "IS213"], 1, ["G1"], "Software Development")
        prerequisite = course.get_prerequisite()
        check = learner.courseEligibility(prerequisite)
        self.assertTrue(check)

    # number of slots available for registration
    def test_existSlots(self):
        class1 = Classes("G1", "IS213", 20, "T001", datetime(2021, 10, 27), datetime(2022, 1, 31), [])
        slots = class1.get_noOfSlots()
        # evaluate true if number of slots is more than 0
        self.assertTrue(slots > 0)
        # check if exception is raised for negative number of slots
        self.assertRaises(Exception, slots, -1)
        # check if exception is raised for 0 slots
        self.assertRaises(Exception, slots, 0)

    # start and end date of classes are stipulated
    def test_existPeriod(self):
        class1 = Classes("G1", "IS213", 20, "T001", datetime(2021, 10, 27), datetime(2022, 1, 31), [])
        startdate = class1.get_startDate()
        enddate = class1.get_endDate()
        self.assertEqual(startdate, datetime(2021, 10, 27))
        self.assertEqual(enddate, datetime(2022, 1, 31))

    # course description is indicated
    def test_existDescription(self):
        course = Course('IS212', "Software Project Management", "Software project management is dedicated to the planning, scheduling, resource allocation, execution, tracking, and delivery of software and web projects.", ["IS111", "IS213"], 1, ["G1"], "Software Development")
        desc = course.get_courseDescription()
        self.assertEqual(desc, "Software project management is dedicated to the planning, scheduling, resource allocation, execution, tracking, and delivery of software and web projects.")

    # sort by earliest start date of classes of courses
    # check if this is needed since it seems more of a UI tasks
    def test_sortClasses(self):
        pass

    # assigned trainer is indicated for each classes
    def test_existTrainer(self):
        trainer = Trainer('Chris', "T001", "chris@smu.edu.sg", ["project management", "product services", "software development"], "3-years experience in customer service...", ["IS212", "IS213", "IS215"])
        class1 = Classes("G1", "IS213", 20, "T001", datetime(2021, 10, 27), datetime(2022, 1, 31), [])
        trainerID = trainer.get_trainerID()
        assignedtrainer = class1.get_trainerAssignedID()
        self.assertEqual(assignedtrainer, "T001")
        self.assertEqual(trainerID, assignedtrainer)

    # check if subject categories for courses exist
    def test_existSubjectCat(self):
        course = Course('IS212', "Software Project Management", "Software project management is dedicated to the planning, scheduling, resource allocation, execution, tracking, and delivery of software and web projects.", ["IS111", "IS213"], 1, ["G1"], "Software Development")
        subjectCat = course.get_subjectcategory()
        self.assertEqual(subjectCat, "Software Development")

if __name__ == "__main__":
    unittest.main()


