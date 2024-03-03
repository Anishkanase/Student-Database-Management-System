from flask import Flask, render_template, request,redirect, url_for
import mysql.connector

app = Flask(__name__)



db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="studentdb"
)
cursor = db.cursor()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_student")
def add_student():
    return render_template("add_student.html")

@app.route("/saverecord", methods=["POST", "GET"])
def saveRecord():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            gender = request.form["gender"]
            contact = request.form["contact"]
            dob = request.form["dob"]
            address = request.form["address"]

            sql = "INSERT into Student_Info (name, email, gender, contact, dob, address) values (%s, %s, %s, %s, %s, %s)"
            val = (name, email, gender, contact, dob, address)

            cursor.execute(sql, val)
            db.commit()
            msg = "Student details successfully added"
            return render_template("success_record.html", msg=msg)

        except Exception as e:
            msg = f"We cannot add student details to the database. Error: {str(e)}"
            return render_template("success_record.html", msg=msg)

@app.route("/delete_student")
def delete_student():
    return render_template("delete_student.html")


@app.route("/student_info")
def student_info():
    try:
        cursor.execute("SELECT * FROM Student_Info")
        rows = cursor.fetchall()
        return render_template("student_info.html", rows=rows)

    except Exception as e:
        msg = f"Error fetching student details: {str(e)}"
        return render_template("error.html", error=msg)
    
    
@app.route("/deleterecord", methods=["POST"])
def deleterecord():
    try:
        id = request.form["id"]

        cursor.execute("SELECT * FROM Student_Info WHERE id=%s", (id,))
        rows = cursor.fetchall()

        if not rows:
            msg = "Student not found. Can't be deleted"
        else:
            cursor.execute("DELETE FROM Student_Info WHERE id = %s", (id,))
            db.commit()
            msg = "Student detail successfully deleted"

    except Exception as e:
        msg = f"Error deleting student details: {str(e)}"

    return render_template("delete_record.html", msg=msg)


@app.route("/update_student/<int:student_id>", methods=["GET", "POST"])
def update_student(student_id):
    
    try:
        if request.method == "GET":
            cursor.execute("SELECT * FROM Student_Info WHERE id=%s", (student_id,))
            student = cursor.fetchone()
            return render_template("update_student.html", student_id=student_id, student=student)

        elif request.method == "POST":
            
            try:
                name = request.form["name"]
                email = request.form["email"]
                gender = request.form["gender"]
                contact = request.form["contact"]
                dob = request.form["dob"]
                address = request.form["address"]

            
                sql = "UPDATE student_info SET name=%s, email=%s, gender=%s, contact=%s, dob=%s, address=%s WHERE id=%s"
                val = (name, email, gender, contact, dob, address, student_id)

                cursor.execute(sql, val)
                db.commit()

                msg = "Student details successfully updated"
                return redirect(url_for("student_info", student_id=student_id))
            except Exception as e:
                msg = f"We cannot update student details. Error: {str(e)}"
                return render_template("success_record.html", msg=msg)
    except Exception as e:
                msg = f"We cannot update student details. Error: {str(e)}"
                return render_template("success_record.html", msg=msg)

if __name__ == "__main__":
    app.run(debug=True)
