import unittest

from flask.json import jsonify
import flask_testing
import json
import sys
import os
sys.path.append('./app')
if True:  # noqa: E402
    from src.quiz import app, db, Quizzes, QuizInfo


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
        q = Quizzes(quizID=2,
                    classID='IS111',
                    sectionID='G6',
                    active=1)

        qi = QuizInfo(quizID=2,
                      questionNumber=1,
                      answer='Chicken',
                      question="What came first?",
                      selections={"options": ["chicken","egg","hen","rooster"]}
                      )

        db.session.add(q)
        db.session.add(qi)
        db.session.commit()

        request_body = {
            {
                "quizID": 2,
                "classID": "IS111",
                "sectionID": "G6",
                "active": 1,
                "answer": "Chicken",
                "questionNumber": 1,
                "question": "What came first?",
                "selections":{"options": ["chicken","egg","hen","rooster"]}
            }
        }

        response = self.client.post("/enter_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        print(response)
        print(response.json)
        self.assertEqual(response.json, {
            'quizID': 2,
            'classID': "IS111",
            'sectionID': "G6",
            'active': 1,
            'questionNumber': 1,
            'question': "What came first?",
            'selections': {
                "selection": [
                    "chicken",
                    "egg",
                    "hen",
                    "rooster"
                ]
            }
        })


if __name__ == '__main__':
    unittest.main()
