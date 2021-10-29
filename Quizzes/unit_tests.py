import unittest
from classObjects import *

class TestQuiz(unittest.TestCase):
    def setUp(self):
        self.q1 = Question("Please select 'true'.", "TF", ['True', 'False'], 'True')
        self.q2 = Question("question test 2", "MS", ['1', 2, '3', '4'], 2)
        self.s = Submission('SPM', 'G9', '012345', ['True', 2])

    def tearDown(self):
        self.q1 = None
        self.q2 = None
        self.course = None

    def test_calculatequizscore(self):
        x = Quiz(self.s)
        x.add_question(self.q1)
        x.add_question(self.q2)
        selected_answers = self.s.get_selected_answers()
        score_test = x.calculate_score(selected_answers)
        
        self.assertEqual(score_test, 2)

if __name__== "__main__":
    unittest.main()
