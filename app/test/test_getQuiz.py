import sys
import unittest
import flask_testing
import json
from datetime import datetime
sys.path.append('./app')
if True:  # noqa: E402
    from src.quiz import db, app, Quizzes


# Group Member: GABRIEL GOH ZONG LIN
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


class TestLearner(TestApp):
    def test_getQuizzes(self):
        quizzes = Quizzes(quizID=2,
                          classID='IS111',
                          sectionID='G6',
                          active=1)
        db.session.add(quizzes)
        db.session.commit()

        url = "/quiz"
        response = self.client.get(url)
        quiz_dict = response.data.decode('utf8')
        returnVal = json.loads(quiz_dict)
        expectedValue = bytes({'quizID': 2,
                         'classID': "IS111",
                         'sectionID': "G6",
                         'active': 'true',
                        })
        self.assertEqual(expectedValue, returnVal)


if __name__ == "__main__":
    unittest.main()
