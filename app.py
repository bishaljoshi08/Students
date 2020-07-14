from flask import Flask, render_template, request ,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///details.db'
db = SQLAlchemy(app)

class StudentDetails(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    roll_no = db.Column(db.Integer, nullable = False)
    phone = db.Column(db.Integer, nullable = False ,  default = 'N/A')
    date_enrolled = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)  

    def __repr__(self):
        return 'Student ' + str(self.id)

all_details=[
    {
        'name': 'Bishal Joshi',
        'roll_no': '19',
        'phone': '9861292306'
    },
    {
        'name': 'Ramraj Chimouriya',
        'roll_no': '11'
    }
]

@app.route('/')
def home_page():
    return render_template('main.html')

@app.route('/details', methods=['GET', 'POST'])
def detail_page():
    if request.method == 'POST':
        student_name = request.form['name']
        student_roll_no = request.form['roll_no']
        new_student = StudentDetails(name=student_name, roll_no= student_roll_no)
        db.session.add(new_student)
        db.session.commit()
        return redirect('/posts')
    else:
        all_details= StudentDetails.query.order_by(StudentDetails.roll_no).all()
        return render_template('detail.html',detail_page=all_details)

if __name__=="__main__":
    app.run(debug=True)