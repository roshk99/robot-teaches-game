from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    trials = db.relationship("Trial", backref="author", lazy="dynamic")
    demos = db.relationship("Demo", backref="author", lazy="dynamic")
    consent = db.Column(db.Integer)
    training = db.Column(db.Integer)
    robot_teaching = db.Column(db.Integer)
    user_learning = db.Column(db.Integer)
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    ethnicity = db.Column(db.Integer)
    education = db.Column(db.Integer)
    robot = db.Column(db.Integer)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Trial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    trial_num = db.Column(db.Integer)
    card_num = db.Column(db.Integer)
    correct_bin = db.Column(db.Integer)
    chosen_bin = db.Column(db.Integer)
    feedback_given = db.Column(db.String(300))
    feedback_type = db.Column(db.String(20))
    rule_set = db.Column(db.String(300))


class Demo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    demo_num = db.Column(db.Integer)
    card_num = db.Column(db.Integer)
    correct_bin = db.Column(db.Integer)
    rule_set = db.Column(db.String(300))


