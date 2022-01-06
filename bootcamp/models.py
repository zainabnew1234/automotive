import datetime
from wtforms.fields import numeric
from bootcamp import db

class Cust(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    customer_name = db.Column(db.String(80),nullable=False)
    customer_mobile = db.Column(db.String(45),nullable=False)
    customer_email = db.Column(db.String(60),nullable=False)
    customer_username = db.Column(db.String(60),nullable=False)
    customer_password = db.Column(db.String(45),nullable=False)
    customer_address = db.Column(db.String(90),nullable=False)


class Book(db.Model):
    __tablename__='booking'    
    booking_id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    booking_customer_id =db.Column(db.Integer(),db.ForeignKey('customer.customer_id'))
    booking_title = db.Column(db.String(45),nullable=False)
    booking_type = db.Column(db.String(45),nullable=False)
    booking_ticket = db.Column(db.String(45),nullable=False)
    booking_date = db.Column(db.DateTime(),default=datetime.datetime.utcnow)
    booking_description = db.Column(db.String(45),nullable=False)
    b=db.relationship('Cust',backref='book')

class Car(db.Model):
    __tablename__='car'    
    car_id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    car_customer_id= db.Column(db.Integer(),db.ForeignKey('customer.customer_id'))
    car_number = db.Column(db.Float(45),nullable=False)
    car_company = db.Column(db.String(45),nullable=False)
    car_type = db.Column(db.String(50),nullable=False)
    car_description = db.Column(db.String(45),nullable=False)
    c =db.relationship('Cust',backref='car')

    

class Pay(db.Model):
    __tablename__=' payment'    
    payment_id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    payment_customer_id= db.Column(db.Integer(),db.ForeignKey('customer.customer_id'))
    payment_date = db.Column(db.DateTime(),default=datetime.datetime.utcnow)
    payment_type = db.Column(db.String(45),nullable=False)
    payment_ref = db.Column(db.String(45),nullable=False)
    payment_status = db.Column(db.String(45),nullable=False)
    payment_amt = db.Column(db.Float(),nullable=False)
    pay =db.relationship('Cust',backref='payment')



class Insure(db.Model):
    __tablename__='insurance'    
    insurance_id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    insurance_car_id= db.Column(db.Integer(),nullable=False)
    insurance_number= db.Column(db.Float(),nullable=False)
    insurance_date = db.Column(db.DateTime(),default=datetime.datetime)
    insurance_expiry = db.Column(db.DateTime(),default=datetime.datetime.utcnow)
    insurance_amount = db.Column(db.Numeric(10,3),nullable=False)
    insurance_type = db.Column(db.String(45),nullable=False)
    insurance_description = db.Column(db.String(45),nullable=False)


class Serve(db.Model):
    __tablename__='services'    
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    service_name = db.Column(db.String(200),nullable=False)
    service_price = db.Column(db.Float(45),nullable=False)
   
