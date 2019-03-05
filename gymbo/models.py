from gymbo import db, loginManager
from flask_login import UserMixin

#Manages login session data
@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#DB models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #lifts = db.relationship('UserLift', backref='name', lazy=True)

    def __repr__(self):
        return "User('{}', '{}', '{}')".format(self.username, self.email, self.profile_pic)

class Lift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lift = db.Column(db.String(60), unique=True, nullable=False)
    #new_lift = db.relationship('UserLift', backref='curr_lift', lazy=True)

    def __repr__(self):
        return "Lift('{}')".format(self.lift)

class UserLift(db.Model):
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    #user = db.relationship('User')
    liftid = db.Column(db.Integer, db.ForeignKey('lift.id'), primary_key=True, nullable=False)
    #lift = db.relationship('Lift')
    max_lift = db.Column(db.Integer, nullable=False, default=0)
    current_lift = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return "UserLift('{}', '{}', '{}', '{}')".format(self.userid, self.liftid, self.current_lift, self.max_lift)
