import sys
import unittest
from datetime import datetime
sys.path.append('./app')
if True:  # noqa: E402
    from src.classobj import Trainer, Learner, Administrator
    from src.classobj import Course, Classes, Application, enrolmentPeriod


# Group Member: TAN JIA LENG
class TestViewTrainers(unittest.TestCase):
    def setUp(self):
        self.trainer = Trainer('Anne', 'T001', 'anne@lms.com',
                               "Process Change Management, IT Support",
                               "8 years experience in IT operation",
                               "IS111, IS212, IS213, IS216")

    def tearDown(self):
        self.trainer = None

    # Check if trainer exists
    def test_existTrainer(self):
        self.assertEqual(self.trainer.json(), {
            'trainerName': 'Anne',
            'trainerID': 'T001',
            'trainerContact': 'anne@lms.com',
            'skills':
            ['Process Change Management', 'IT Support'],
            'experience':  ["8 years experience in IT operation"],
            'coursesTaught': ["IS111", "IS212", "IS213", "IS216"]}
        )


class TestViewEligibleCourses(unittest.TestCase):
    def setUp(self):
        self.learner = Learner(
            'Alivia', 'L001', 'alivia@lms.com', "IS111, IS213, IS215")
        self.course = Course('IS212', 'Software Project Management',
                             '...', "IS111, IS213", 2, "G1, G2]",
                             'Project Management')
        self.class1 = Classes("G1", "IS212", 20, "T001", datetime(
            2022, 1, 10), datetime(2022, 6, 30), 'FY20/21 Session 2')
        self.trainer = Trainer('Anne', 'T001', 'anne@lms.com',
                               "Process Change Management, IT Support",
                               "8 years experience in IT operation",
                               "IS111, IS212, IS213, IS216")

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

    # Check all field for classes exists and matches
    def test_existClasses(self):
        self.assertEqual(self.class1.json(), {
            'classID': "G1",
            'courseID': "IS212",
            'noOfSlots': 20,
            'trainerAssignedID': "T001",
            'startDate': datetime(2022, 1, 10),
            'endDate': datetime(2022, 6, 30),
            'enrolmentPeriodID': 'FY20/21 Session 2',
        })


class TestApplication(unittest.TestCase):

    def setUp(self):
        self.learner = Learner(
                'Alivia', 'L001', 'alivia@lms.com', "IS111, IS213, IS215")
        self.course = Course('IS212', 'Software Project Management', '...',
                             "IS111, IS213", 2, "G1, G2",
                             'Project Management')
        self.class1 = Classes("G1", "IS212", 20, "T001", datetime(
            2022, 1, 10), datetime(2022, 6, 30), 'FY20/21 Session 2')
        self.trainer = Trainer('Anne', 'T001', 'anne@lms.com',
                               "Process Change Management, IT Support",
                               "8 years experience in IT operation",
                               "IS111, IS212, IS213, IS216")
        self.application1 = Application(1, "L001", "G1", "IS212", "Processing",
                                        datetime(2021, 10, 20),
                                        'FY20/21 Session 2', "admin001")
        self.admin1 = Administrator('Estella', "admin001", "estella@lms.com")
        self.enrolmentPeriod = enrolmentPeriod('FY20/21 Session 2',
                                               datetime(2021, 10, 15),
                                               datetime(2021, 11, 30))

    def tearDown(self):
        self.learner = None
        self.course = None
        self.class1 = None
        self.trainer = None
        self.application1 = None
        self.admin1 = None
        self.enrolmentPeriod = None

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

    # cannot submit application after self-enrolment period
    def test_checkEnrolmentPeriod(self):
        try:
            self.assertTrue(self.application1.checkEnrolmentPeriod(
                self.enrolmentPeriod))
        except Exception as e:
            self.assertRaises(
                e, self.application1.checkEnrolmentPeriod,
                self.enrolmentPeriod)

    def test_class_for_currEnrolmentPeriod(self):
        self.assertEqual(
            self.class1.class_for_currEnrolmentPeriod(
                self.enrolmentPeriod.enrolmentEndDate,
                self.course, self.trainer), {
                    'courseID': self.course.courseID,
                    'classID': self.class1.classID,
                    'noOfSlots': self.class1.noOfSlots,
                    'trainerName': self.trainer.trainerName,
                    'startDate': self.class1.startDate,
                    'endDate': self.class1.endDate,
                    'courseName': self.course.courseName,
                    'courseDescription': self.course.courseDescription,
                    'subjectcategory': self.course.subjectcategory,
                    'enrolmentPeriodID': self.class1.enrolmentPeriodID}
                )


class TestEnrolmentPeriod(unittest.TestCase):

    def setUp(self):
        self.enrolmentPeriod = enrolmentPeriod('FY20/21 Session 2',
                                               datetime(2021, 10, 15),
                                               datetime(2021, 11, 30))

    def tearDown(self):
        self.learner = None
        self.course = None
        self.class1 = None
        self.trainer = None
        self.application1 = None
        self.admin1 = None

    def test_existEnrolmentPeriod(self):
        self.assertEqual(self.enrolmentPeriod.json(), {
            'enrolmentPeriodID': 'FY20/21 Session 2',
            'enrolmentStartDate': datetime(2021, 10, 15),
            'enrolmentEndDate': datetime(2021, 11, 30)}
        )


if __name__ == "__main__":
    unittest.main()
