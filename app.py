from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Employee, Attendance
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employeedatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/', endpoint='home_page')
def home():
    return render_template('welcome.html')

# ---------------------------------------------------------------------------------------------------------------

@app.route('/home')
def home():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

# ---------------------------------------------------------------------------------------------------------------

@app.route('/add_employee_form', methods=['GET'])
def add_employee_form():
    return render_template('add_employee.html')

@app.route('/add_employee', methods=['POST'])
def add_employee():
    name = request.form['name']
    designation = request.form['designation']
    department = request.form['department']
    date_of_joining_str = request.form['date_of_joining']
    
    # Convert the date string to a datetime.date object
    date_of_joining = datetime.strptime(date_of_joining_str, '%Y-%m-%d').date()
    
    new_employee = Employee(name=name, designation=designation, department=department, date_of_joining=date_of_joining)
    db.session.add(new_employee)
    db.session.commit()
    
    return redirect(url_for('home'))

# ---------------------------------------------------------------------------------------------------------------

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([e.serialize() for e in employees])

# ---------------------------------------------------------------------------------------------------------------

@app.route('/mark_attendance_form/<int:employee_id>', methods=['GET'])
def mark_attendance_form(employee_id):
    employee = Employee.query.get(employee_id)
    return render_template('mark_attendance.html', employee=employee)


@app.route('/mark_attendance/<int:employee_id>', methods=['POST'])
def mark_attendance(employee_id):
    status = request.form['status']
    attendance_date = datetime.strptime(request.form['attendance_date'], '%Y-%m-%d').date()
    employee = Employee.query.get(employee_id)
    
    if employee:
        new_attendance = Attendance(status=status, name=employee.name, attendance_date=attendance_date, employee=employee)
        db.session.add(new_attendance)
        db.session.commit()
    
    return redirect(url_for('home'))

# ---------------------------------------------------------------------------------------------------------------

@app.route('/employee/<int:employee_id>')
def employee_detail(employee_id):
    employee = Employee.query.get(employee_id)
    return render_template('employee_detail.html', employee=employee)

# ---------------------------------------------------------------------------------------------------------------

@app.route('/attendance_report')
def attendance_report():
    attendance_summary = db.session.query(
        Employee.id, 
        Employee.name, 
        Employee.department,
        db.func.count(db.case([(Attendance.status == 'Present', 1)])).label('present_count'),
        db.func.count(db.case([(Attendance.status == 'Absent', 1)])).label('absent_count'),
        db.func.count(db.case([(Attendance.status == 'Leave', 1)])).label('leave_count')
    ).join(Attendance, Employee.id == Attendance.employee_id)\
     .group_by(Employee.id, Employee.name, Employee.department)\
     .all()

    return render_template('attendance_report.html', attendance_summary=attendance_summary)


if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()  # Be careful: this will delete existing data
        db.create_all()  # This will create the new tables
    app.run(debug=True)

