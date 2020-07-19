from flask import Flask, render_template, request ,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import EntryForm

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///details.db'
app.config['SECRET_KEY'] = 'ba94f676a536e224b8bc8e9b67ba6473'
db = SQLAlchemy(app)

class StudentDetails(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    roll_no = db.Column(db.Integer, nullable = False)
    phone = db.Column(db.Integer, nullable = False ,  default = 'N/A')
    date_enrolled = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)  

    def __repr__(self):
        return 'Student ' + str(self.id)


@app.route('/')
def home_page():
    return render_template('main.html')

@app.route('/details', methods=['GET', 'POST'])
def detail_page():
    form = EntryForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            flash(f"{form.name.data}'s data was stored", 'success')
            student_name = request.form['name']
            student_roll_no = request.form['roll_no']
            student_phone = request.form['phone']
            new_student = StudentDetails(name=student_name, roll_no= student_roll_no, phone= student_phone)
            db.session.add(new_student)
            db.session.commit()
            all_details= StudentDetails.query.order_by(StudentDetails.roll_no).all()
            return redirect('/details')
    else:
        all_details= StudentDetails.query.order_by(StudentDetails.roll_no).all()
        return render_template('detail.html', details=all_details, form=form)

@app.route('/details/delete/<int:id>')
def delete(id):
    detail = StudentDetails.query.get_or_404(id)
    flash(f"{StudentDetails.query.get(id).name}'s data was deleted", 'danger' )
    db.session.delete(detail)
    db.session.commit()
    
    return redirect('/details')

@app.route('/details/edit/<int:id>',methods=['GET','POST'])
def edit(id):

    detail = StudentDetails.query.get_or_404(id)
    form = EntryForm()
    if request.method == 'POST':
        flash(f"{form.name.data}'s data was edited", 'warning' )
        detail.name = request.form['name']
        detail.roll_no = request.form['roll_no']
        detail.phone = request.form['phone']
        db.session.commit()
        return redirect('/details')
    else:
        return render_template('edit.html', detail=detail, form=form)


if __name__=="__main__":
    app.run(debug=True)