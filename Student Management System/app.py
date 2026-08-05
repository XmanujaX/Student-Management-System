from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='student_db',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    cursor.close()
    conn.close()

    total_students = len(students)

    courses = [s['course'] for s in students if s.get('course')]
    total_courses = len(set(courses))

    ages = [s['age'] for s in students if s.get('age')]
    avg_age = round(sum(ages) / len(ages), 1) if ages else 0

    if courses:
        top_course = max(set(courses), key=courses.count)
    else:
        top_course = '-'

    return render_template(
        'index.html',
        students=students,
        total_students=total_students,
        total_courses=total_courses,
        avg_age=avg_age,
        top_course=top_course
    )

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    age = request.form['age']
    course = request.form['course']
    email = request.form['email']
    contact = request.form['contact']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name, age, course, email, contact) VALUES (%s, %s, %s, %s, %s)', (name, age, course, email, contact))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update_student():
    id = request.form['id']
    name = request.form['name']
    age = request.form['age']
    course = request.form['course']
    email = request.form['email']
    contact = request.form['contact']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE students SET name=%s, age=%s, course=%s, email=%s, contact=%s WHERE id=%s', (name, age, course, email, contact, id))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/delete/<string:id>', methods=['GET'])
def delete_student(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE id=%s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)