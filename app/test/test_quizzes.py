import unittest
import flask_testing
import json
import sys
sys.path.append('./app')
if True:  # noqa: E402
    from src.quizzes import app, db, Quizzes, QuizInfo

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
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
        q = Quizzes(quizID="2", 
                    classID='IS111', 
                    sectionID='G6', 
                    active=1)

        qi = QuizInfo(quizInfoID="2", 
                      questionNumber=1,
                      answer='Chicken', 
                      question="What came first?", 
                      selections={
                                    "selection": [
                                        "chicken",
                                        "egg",
                                        "hen",
                                        "rooster"
                                    ]})
        db.session.add(q)
        db.session.add(qi)
        db.session.commit()

        request_body = {
            'quizID': q.quizID,
            'classID': q.classID,
            'sectionID': q.sectionID,
            'active': q.active,
            'answer': qi.answer,
            'questionNumber': qi.questionNumber,
            'question': qi.question,
            'selections': qi.selections,
        }

        response = self.client.post("/enter_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            'quizID': 2,
            'classID': "IS111",
            'sectionID': "G6",
            'active': 1,
            'questionNumber': 1,
            'question': "What came first?",
            'selections' :{
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