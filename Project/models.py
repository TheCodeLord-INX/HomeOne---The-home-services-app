from flask_login import UserMixin
from . import db
from flask import current_app
from datetime import datetime, timezone

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(100))  # Ensure this field exists
    password = db.Column(db.String(100))
    role = db.Column(db.Integer(), nullable=False)  # Ensure it's not nullable
    pdf_filename = db.Column(db.String(100))  # Ensure this field exists
    expy = db.Column(db.String(100))  # Ensure this field exists
    service = db.Column(db.String(100))  # Ensure this field exists
    status = db.Column(db.String(20), nullable=True)  # Add status field
    
    @staticmethod
    def create_dummy_admin():
        with current_app.app_context():
            user = User(name='admin', username='admin', password='admin', role=0)
            db.session.add(user)
            db.session.commit()
            
            
    @staticmethod
    def create_dummy_user():
        with current_app.app_context():
            user = User(name='user', username='user', address='Location Y', password='user', role=2)
            db.session.add(user)
            db.session.commit()

    @staticmethod
    def create_dummy_professionals():
        with current_app.app_context():
            professionals = [
                {'name': 'prof', 'username': 'prof', 'password': 'prof', 'role': 1, 'expy': '6', 'service': 'HVAC'},
                {'name': 'prof1', 'username': 'prof1', 'password': 'prof1', 'role': 1, 'expy': '5', 'service': 'Sink'},
                {'name': 'prof2', 'username': 'prof2', 'password': 'prof2', 'role': 1, 'expy': '3', 'service': 'Plumbing'},
                {'name': 'prof3', 'username': 'prof3', 'password': 'prof3', 'role': 1, 'expy': '7', 'service': 'Electrical'},
                {'name': 'prof4', 'username': 'prof4', 'password': 'prof4', 'role': 1, 'expy': '2', 'service': 'Carpentry'},
                {'name': 'prof5', 'username': 'prof5', 'password': 'prof5', 'role': 1, 'expy': '4', 'service': 'Painting'}
            ]
            for prof in professionals:
                user = User(name=prof['name'], username=prof['username'], password=prof['password'], role=prof['role'], expy=prof['expy'], service=prof['service'])
                db.session.add(user)
            db.session.commit()

class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    bp = db.Column(db.Numeric(10, 2), nullable=False)  # Set precision to 2 decimal places
    desc = db.Column(db.String(), nullable=True)  # Added 'desc' field
    rating = db.Column(db.Numeric(2, 1), nullable=True)  # Added 'ratings' field
    pin = db.Column(db.String(), nullable=True)  # Added 'pin' field
    location = db.Column(db.String(), nullable=True)  # Added 'location' field
    status = db.Column(db.String(), nullable=True)  # Added 'status' field
    reqDate = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  # Added 'reqDate' field

    # @staticmethod
    # def create_service():
    #     with current_app.app_context():
    #         # Ensure there is at least one user in the User table
    #         # user = User.query.first()
    #         # if not user:
    #         #     user = User(name='dummy_user', username='dummy', password='dummy', role=2, address='123 Dummy St')
    #         #     db.session.add(user)
    #         #     db.session.commit()
            
    #         service = Services(
    #             name='Sink',
    #             bp=100,
    #             desc='Sink installation and repair',
    #             rating=4.5,
    #             pin='12345',
    #             location='Dummy Location',
    #             status='Pending'
    #         )
    #         db.session.add(service)
    #         db.session.commit()
            
    @staticmethod
    def create_services():
        with current_app.app_context():
            services = [
                {'name': 'Sink', 'bp': 100, 'desc': 'Sink installation and repair', 'rating': 4.5, 'pin': '12345', 'location': 'Location 1', 'status': 'Pending'},
                {'name': 'HVAC', 'bp': 200, 'desc': 'HVAC maintenance', 'rating': 4.7, 'pin': '12346', 'location': 'Location 2', 'status': 'Pending'},
                {'name': 'Plumbing', 'bp': 150, 'desc': 'Plumbing services', 'rating': 4.6, 'pin': '12347', 'location': 'Location 3', 'status': 'Pending'},
                {'name': 'Electrical', 'bp': 180, 'desc': 'Electrical repairs', 'rating': 4.8, 'pin': '12348', 'location': 'Location 4', 'status': 'Pending'},
                {'name': 'Carpentry', 'bp': 130, 'desc': 'Carpentry work', 'rating': 4.4, 'pin': '12349', 'location': 'Location 5', 'status': 'Pending'},
                {'name': 'Painting', 'bp': 120, 'desc': 'Painting services', 'rating': 4.3, 'pin': '12350', 'location': 'Location 6', 'status': 'Pending'},
                {'name': 'Cleaning', 'bp': 110, 'desc': 'House cleaning', 'rating': 4.2, 'pin': '12351', 'location': 'Location 7', 'status': 'Pending'},
                {'name': 'Gardening', 'bp': 140, 'desc': 'Gardening services', 'rating': 4.1, 'pin': '12352', 'location': 'Location 8', 'status': 'Pending'}
            ]
            for service in services:
                new_service = Services(
                    name=service['name'],
                    bp=service['bp'],
                    desc=service['desc'],
                    rating=service['rating'],
                    pin=service['pin'],
                    location=service['location'],
                    status=service['status']
                )
                db.session.add(new_service)
            db.session.commit()
            
class ServiceRemarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    contact_no = db.Column(db.String(), nullable=False)
    prof_uname = db.Column(db.String(), nullable=False)
    prof_name = db.Column(db.String(), nullable=False)
    service_rating = db.Column(db.Numeric(2, 1), nullable=False)
    remarks = db.Column(db.String(), nullable=False)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'))  # Add foreign key to ServiceRequests table

    @staticmethod
    def create_service_remarks():
        with current_app.app_context():
            service_remarks = ServiceRemarks(
                service_name='Sink',
                description='Sink installation and repair',
                date=datetime.utcnow(),
                contact_no='1234567890',
                prof_uname='prof',
                prof_name='prof',
                service_rating=4.5,
                remarks='Good service'
            )
            db.session.add(service_remarks)
            db.session.commit()
            
class ServiceRequests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    bp = db.Column(db.Numeric(10, 2), nullable=False)  # Set precision to 2 decimal places
    desc = db.Column(db.String(), nullable=True)  # Added 'desc' field
    rating = db.Column(db.Numeric(2, 1), nullable=True)  # Added 'ratings' field
    pin = db.Column(db.String(), nullable=True)  # Added 'pin' field
    location = db.Column(db.String(), nullable=True)  # Added 'location' field
    status = db.Column(db.String(), nullable=True)  # Added 'status' field
    reqDate = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  # Added 'reqDate' field
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Add foreign key to User table
    user = db.relationship('User', backref=db.backref('service_requests', lazy=True))  # Add relationship to User
    assigned_prof = db.Column(db.String(), nullable=True)  # Added 'assigned_prof' field
    remarks = db.relationship('ServiceRemarks', backref='service_request', lazy=True)  # Add relationship to ServiceRemarks



