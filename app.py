from flask import Flask, render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# DUMMY DATA [WILL DELETE] ------------------------------------------------------------- #

applications = [
    
    # 01
        {
        'application_id' : '0001',
        'learner_id' : '1234',
        'learner_name' : 'Naruto Uzamaki',
        'course_id' : 'COR123',
        'course_name' : 'How to Be Hokage'
         },

     # 02
        {
        'application_id' : '0002',
        'learner_id' : '4321',
        'learner_name' : 'Sasuke Uchiha',
        'course_id' : 'COR101',
        'course_name' : 'Avenging Your Clan 101'
         },

    # 03
        {
        'application_id' : '0003',
        'learner_id' : '2341',
        'learner_name' : 'Kakashi Hatake',
        'course_id' : 'COR600',
        'course_name' : 'Icha Icha'
         }     
    ]


# ROUTING ------------------------------------------------------------- #
@app.route("/")
def welcome():
    return "welcome to Admin page"

@app.route("/pending")
def home():
    return render_template('pending_list.html', title = "Pending Applications", applications = applications)

@app.route("/success")
def approve():
    return "APPROVED!"

@app.route("/reject")
def reject():
    return "REJECTED!"


@app.route("/courses/")
def courses():
    return render_template('courses_list.html', title = "Courses Information")

@app.route("/name/")
def name():
    return render_template()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)