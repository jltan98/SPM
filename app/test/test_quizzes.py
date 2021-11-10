import unittest
import flask_testing
import json
import sys
sys.path.append('./app')
if True:  # noqa: E402
    from src.quizzes import db, app


# Group Member: ALVIN NGOW FENG HAO
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


class TestQuizzes(TestApp):
    def test_create_quiz(self):
        request_body = {
                "quizID": 2,
                "classID": "IS111",
                "sectionID": "G6",
                "active": 1,
                "answer": "Chicken",
                "questionNumber": 1,
                "question": "What came first?",
                "selections": {"selection":
                               ["chicken",
                                "egg",
                                "hen",
                                "rooster"]}}

        response = self.client.post("/enter_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json,
                        {"quizID": 2,
                         "classID": "IS111",
                         "sectionID": "G6",
                         "active": 1,
                         "answer": "Chicken",
                         "questionNumber": 1,
                         "question": "What came first?",
                         "selections": {"selection":
                                        ["chicken",
                                         "egg",
                                         "hen",
                                         "rooster"]}})


if __name__ == '__main__':
    unittest.main()
