import sys
import unittest
import flask_testing
from datetime import datetime
sys.path.append('./app')
if True:  # noqa: E402
    from src.classobj import Learner, Trainer, Administrator
    from src.classobj import Classes, Course, Application, enrolmentPeriod
    from src.enums import ClassesStatus
    from src.classobj import db, app, Learner, Application
    import src.enrolment


class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestLearner(unittest.TestCase):
    def test_getLearnerCurrentAppliedCoursesAsDictionary(self):
        learner = Learner('Alivia', 'L003', 'alivia@lms.com',
                          'IS110,IS213,IS111', '1234')
        application = Application(1, "L001", "G1", "IS212", "Processing",
                                  datetime(2021, 10, 20),
                                  'FY20/21 Session 2', "admin001")
        db.session.add(learner)
        db.session.add(application)
        db.session.commit()

        response = self.client.get("/learnerCurrAppliedCourse/" + learner.learnerID)
        # learnerCurrentAppliedCourses = self.Learner.getLearnerCurrentAppliedCoursesAsDictionary()
        learnerCurrentAppliedCourses = response.data
        print(learnerCurrentAppliedCourses)
        expectedValue = ['IS211']
        self.assertEqual(expectedValue, learnerCurrentAppliedCourses)

    def test_getCoursesTakenIDs(self):
        self.learner = Learner('Alivia', 'L003', 'alivia@lms.com',
                          'IS110,IS213,IS111', '1234')

        learnerCoursesTaken = self.learner.getCoursesTakenIDs()
        expectedValue = ['IS110', 'IS213', 'IS111']
        self.assertEqual(expectedValue, learnerCoursesTaken)


if __name__ == "__main__":
    unittest.main()
