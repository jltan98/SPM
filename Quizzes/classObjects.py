

class Submission:
    def __init__(self, courseID='', section='', trainerID='', selected_answers=[]):
        self.courseID = courseID
        self.section = section
        self.trainerID = trainerID
        self.selected_answers = selected_answers

    def get_selected_answers(self):
        return self.selected_answers

class Question:
    def __init__(self, title='', type='', options=[], correct_answer=''):
        self.title = title
        self.type = type
        self.options = options
        self.correct_answer = correct_answer
    
    def get_title(self):
        return self.title

    def get_type(self):
        return self.type

    def get_options(self):
        return self.options

    def get_correct_answer(self):
        return self.correct_answer

class Quiz:
    def __init__(self, submission=None):
        self.submission = submission
        self.questions = []
    
    def get_questions(self):
        return self.questions
    
    def add_question(self, question):
        self.questions.append(question)

    def remove_question(self, question):
        self.questions.remove(question)
    
    def get_num_of_questions(self):
        return len(self.questions)

    def get_total_score(self):
        total = 0
        total += len(self.questions)
        return total
        # to edit later: for question in questions -> total += score weightage
    
    def calculate_score(self, answer=[]):
        score = 0

        for i in range(len(self.questions)):
            if answer[i] == self.questions[i].get_correct_answer():
                score += 1 #change this to score weightage later
        
        return score
        
    