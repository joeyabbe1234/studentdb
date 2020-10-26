from flask import Flask, render_template, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'abonitalla123'
app.config['MYSQL_DB'] = 'student'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
Bootstrap(app)


class RegisterForm(FlaskForm):
    Firstname = StringField('Firstname', validators=[InputRequired()])
    Lastname = StringField('Lastname', validators=[InputRequired()])
    Course = StringField('Course', validators=[InputRequired()])
    StudentID = StringField('StudentID', validators=[InputRequired()])


class Searchform(FlaskForm):
    StudentID = StringField('StudentID', validators=[InputRequired()])


@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/students', methods=['GET'])
def students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student")
    studentdetails = cur.fetchall()
    return render_template('students.html', studentdetails=studentdetails)


@app.route('/addstudents', methods=['GET', 'POST'])
def addstudents():
    form = RegisterForm()
    if form.validate_on_submit():
        firstname = form.Firstname.data
        lastname = form.Lastname.data
        course = form.Course.data
        studentid = form.StudentID.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO student VALUES(%s, %s, %s, %s)", (firstname, lastname, course, studentid))
        mysql.connection.commit()
        cur.close()
        flash('Student added', 'success')
        return redirect(url_for('dashboard'))
    return render_template('addstudents.html', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = Searchform()
    if form.validate_on_submit():
        studentid = request.form['StudentID']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM student WHERE StudentID=%s", [studentid])
        if result > 0:
            student = cur.fetchone()
            return render_template('profile.html', student=student)
        else:
            flash('No Student found', 'danger')
        cur.close()
    return render_template('search.html', form=form)


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    form = RegisterForm()
    if request.method == 'POST':
        Firstname = request.form['Firstname']
        Lastname = request.form['Lastname']
        Course = request.form['Course']
        StudentID = request.form['StudentID']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE student SET Firstname=%s, Lastname=%s, Course=%s WHERE StudentID=%s", (Firstname, Lastname, Course, StudentID))
        flash("Data Updated Successfully", 'success')
        mysql.connection.commit()
        return render_template('dashboard.html')
    return render_template('edit.html', form=form)


@app.route('/delete/<string:StudentID>', methods = ['GET'])
def delete(StudentID):
    flash("Record Has Been Deleted Successfully",'success')
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM student WHERE StudentID=%s", (StudentID,))
    mysql.connection.commit()
    return redirect(url_for('students'))


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'secret'
    app.run(debug=True)
