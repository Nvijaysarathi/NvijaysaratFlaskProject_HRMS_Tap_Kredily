from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = 'employees'  # Specify the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    date_of_joining = db.Column(db.Date, nullable=False)
    attendances = db.relationship('Attendance', backref='employee', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'designation': self.designation,
            'department': self.department,
            'date_of_joining': self.date_of_joining.strftime('%Y-%m-%d')
        }


class Attendance(db.Model):
    __tablename__ = 'attendances'  # Specify the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)  # Correct the foreign key reference

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'attendance_date': self.attendance_date.strftime('%Y-%m-%d'),
            'employee_id': self.employee_id
        }
