import unittest
from datetime import datetime
from app import Trainer, Learner, Administrator, Course, Classes, Application


class TestViewTrainers(unittest.TestCase):

    def setUp(self):
        self.trainer = Trainer('Anne', 'T001', 'anne@lms.com', "Process Change Management, Aftersales IT Support, Software Development",
                               "8 years experience in IT operation", "IS111, IS212, IS213, IS216")

    def tearDown(self):
        self.trainer = None

    # Check if trainer exists >> ID, Name, list of courses taught, skills, experience
    def test_existTrainer(self):
        self.assertEqual(self.trainer.json(), {
            'trainerName': 'Anne',
            'trainerID': 'T001',
            'trainerContact': 'anne@lms.com',
            'skills': ['Process Change Management', 'Aftersales IT Support', 'Software Development'],
            'experience':  ["8 years experience in IT operation"],
            'coursesTaught': ["IS111", "IS212", "IS213", "IS216"]}
        )


class TestViewEligibleCourses(unittest.TestCase):

    def setUp(self):
        self.learner = Learner(
            'Alivia', 'L001', 'alivia@lms.com', "IS111, IS213, IS215")
        self.course = Course('IS212', 'Software Project Management',
                             '...', "IS111, IS213", 2, "G1, G2]", 'Project Management')
        self.class1 = Classes("G1", "IS212", 20, "T001", datetime(
            2021, 10, 1), datetime(2022, 11, 30), 'FY20/21 Session 2')
        self.trainer = Trainer('Anne', 'T001', 'anne@lms.com', "Process Change Management, Aftersales IT Support, Software Development",
                               "8 years experience in IT operation", "IS111, IS212, IS213, IS216")

    def tearDown(self):
        self.learner = None
        self.course = None
        self.class1 = None
        self.trainer = None

    # Check if learner is eligible for the course (cleared prerequisite)
    def testEligibility(self):
        prerequisite = self.course.prerequisite
        self.assertEqual(prerequisite, "IS111, IS213")
        # if prerequisite has been cleared
        self.assertEqual(self.learner.courseEligibility(
            prerequisite), self.learner.coursesTaken)
        self.assertRaises(
            Exception, self.learner.courseEligibility, 'IS200, IS111')
        self.assertRaises(Exception, self.learner.courseEligibility, 'IS200')

    # Check course must not be taken before by learner
    def test_courseTaken(self):
        # course must not be taken before
        self.assertTrue(self.course.courseID not in self.learner.coursesTaken)
        self.assertRaises(Exception, self.learner.checkCourseTaken, 'IS213')

    # Check all field for classes exists and matches
    def test_existClasses(self):
        self.assertEqual(self.class1.json(), {
            'classID': "G1",
            'courseID': "IS212",
            'noOfSlots': 20,
            'trainerAssignedID': "T001",
            'startDate': datetime(2021, 10, 1),
            'endDate': datetime(2022, 11, 30),
            'enrolmentPeriodID': 'FY20/21 Session 2',
        })


class TestApplication(unittest.TestCase):

    def setUp(self):
        self.learner = Learner(
            'Alivia', 'L001', 'alivia@lms.com', "IS111, IS213, IS215")
        self.course = Course('IS212', 'Software Project Management',
                             '...', "IS111, IS213", 2, "G1, G2]", 'Project Management')
        self.class1 = Classes("G1", "IS212", 20, "T001", datetime(
            2021, 10, 1), datetime(2022, 11, 30))
        self.trainer = Trainer('Anne', 'T001', 'anne@lms.com', "Process Change Management, Aftersales IT Support, Software Development",
                               "8 years experience in IT operation", "IS111, IS212, IS213, IS216")
        self.application1 = Application(1, "L001", "G1", "IS212", "Processing", datetime(
            2021, 10, 20), 'FY20/21 Session 2', "admin001")
        self.admin1 = Administrator('Estella', "admin001", "estella@lms.com")

    def tearDown(self):
        self.learner = None
        self.course = None
        self.class1 = None
        self.trainer = None
        self.application1 = None
        self.admin1 = None

    # check and match the fields for application
    def test_existApplication(self):
        self.assertEqual(self.application1.json(), {
            'applicationID': 1,
            'applicationLearnerID': "L001",
            'applicationClassID': "G1",
            'applicationCourseID': "IS212",
            'applicationStatus': "Processing",
            'applicationDate': datetime(2021, 10, 20),
            'enrolmentPeriodID': "FY20/21 Session 2",
            'adminID': "admin001"}
        )

    # check and match the fields for admin (mainly name, id and contact)
    def test_existAdministrator(self):
        self.assertEqual(self.admin1.json(), {
            'adminName': 'Estella',
            'adminID': "admin001",
            'adminContact': "estella@lms.com"}
        )

    # check that application to the same course can only be made once by the Learner in each enrolment period
    def test_checkApplication(self):
        pass

    # cannot submit application after self-enrolment period
    def test_checkEnrolmentPeriod(self):
        self.assertRaises(
            Exception, self.application1.checkEnrolmentPeriod, datetime.now())


if __name__ == "__main__":
    unittest.main()
