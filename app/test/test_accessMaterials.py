import unittest
import sys
sys.path.append('./app')
if True:  # noqa: E402
    from src.access_materials import quiz, lesson


# Group Member: C. SNEKHA
class testwrongquestions(unittest.TestCase):
    def setup(self):
        self.quiz = quiz(1,
                         "First Test",
                         [True, True, False],
                         "True", 3, 2)

    def tearDown(self):
        self.quiz = None

    def checkwrongquestion(self):
        wrongq = self.quiz.wrongquestiondict()
        self.assertEqual(wrongq, [3])


class testviewcontentlist(unittest.TestCase):
    def setup(self):
        self.lesson = lesson("1",
                             "First,Second,Third",
                             [True, True, False])

    def tearDown(self):
        self.lesson = None

    def checkcontentlist(self):
        self.assertEqual(self.lesson.json(), {
            'lessonID': 1,
            'title': "First,Second,Third",
            'viewStatus': [True, True, False]
        })


class testprogress(unittest.TestCase):
    def setup(self):
        self.lesson = lesson("1",
                             "First,Second,Third",
                             [True, True, False])

    def tearDown(self):
        self.lesson = None

    def checkprogress(self):
        progress = self.lesson.progress()
        self.assertEqual(progress, (2/3*100))


if __name__ == "__main__":
    unittest.main()
