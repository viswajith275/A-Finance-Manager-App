from .extensions import db
from flask_login import  UserMixin
from datetime import datetime

class User(db.Model,UserMixin):

    __tablename__ = 'user'

    uid = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    def get_id(self):
        return str(self.uid)

class Transaction(db.Model):

    __tablename__ = 'transactions'

    tid = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.uid"))
    type = db.Column(db.String(10))  # income / expense
    category = db.Column(db.String(50))
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    is_recurring = db.Column(db.Boolean, default=False)

class Budget(db.Model):

    __tablename__ = 'budget'

    bid = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.uid'))
    category = db.Column(db.String(50),nullable=False)
    month = db.Column(db.String(7), nullable=False) #format yyyy-mm
    amount = db.Column(db.Float, nullable=False)

    __table_args__ = (db.UniqueConstraint('user_id','category',name='unique_user_category'),)
class RecurringBills(db.Model):

    __tablename__ = 'recurringbills'

    rid = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.uid'))
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    next_due_date = db.Column(db.Date, nullable=False)
    active = db.Column(db.Boolean, default=True)

