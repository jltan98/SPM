from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from classObjects import Learner, Trainer, Administrator

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root' + \
                                        '@localhost:3306/LMS'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)


# APP ROUTING
@app.route("/login", methods=['POST'])
def login_verification():
    data = request.get_json()
    role = data['role']
    userid = data['userid']
    password = data['password']
    name = ""
    try:
        if (role == "learner"):
            user = Learner.query.filter_by(learnerID=userid).first()
            name = user.learnerName
        elif (role == "trainer"):
            user = Trainer.query.filter_by(trainerID=userid).first()
            name = user.trainerName
        elif (role == "administrator"):
            user = Administrator.query.filter_by(adminID=userid).first()
            name = user.adminName

        if (user.password == password):
            return name
        else:
            return "Invalid Password, please try again."
    except Exception:
        return "Invalid User ID, please try again."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
