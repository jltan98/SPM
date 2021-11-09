# from operator import pos
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)


class quiz(db.Model):
    __tablename__ = 'quiz'

    quizID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    # check if question correct or not
    questionStatus = db.Column(db.Boolean)
    attempted = db.Column(db.Boolean)
    maxMarks = db.Column(db.Integer)
    results = db.Column(db.Integer)

    def __init__(self,
                 quizID="",
                 title="",
                 questionStatus="",
                 attempted="",
                 maxMarks="",
                 results=""):
        self.quizID = quizID
        self.title = title
        self.questionStatus = questionStatus
        self.attempted = attempted
        self.maxMarks = maxMarks
        self.results = results

    def json(self):
        return{
            'quizID': self.quizID,
            'title': self.title,
            'questionsStatus': self.questionStatus,
            'attempted': self.attempted,
            'maxMarks': self.maxMarks,
            'results': self.results
        }

    def wrongquestiondict(self):
        wrongq = []
        i = 1
        # retrieve all the wrong qns tgt
        for y in self.questionStatus:
            if y is False:
                wrongq.append(i)
            i += 1
        return wrongq


class lesson(db.Model):
    __tablename__ = 'lesson'
    lessonID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    viewStatus = db.Column(db.Boolean)

    def __init__(self,
                 lessonID="",
                 title="",
                 viewStatus=""):
        self.lessonID = lessonID
        self.title = title
        self.viewStatus = viewStatus

    def json(self):
        return{
            'lessonID': self.lessonID,
            'title': self.title,
            'viewStatus': self.viewStatus,
        }

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def progress(self):
        a = 0
        for i in self.viewStatus:
            if i is True:
                a += 1
        progess = (a / (len(self.viewStatus))) * 100
        return progess


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
