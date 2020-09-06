from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

# create the users database model
class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    major = db.Column(db.String(100))
    courses = db.Column(db.String(100))
    number = db.Column(db.String(100))
    
    def __init__(self, name, major, courses, number):
        self.name = name
        self.major = major
        self.courses = courses
        self.number = number

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    # save the name, major, courses, and number in the database
    if request.method == "POST":
        session.permanent = True  #makes the permanent session
        
        name = request.form["name"]
        major = request.form["major"]
        courses = request.form["courses"]
        number = request.form["number"]

        if name == "admin":
            return redirect(url_for("admin"))

        # error handling
        if not name or not major or not courses or not number:
            return render_template("apology.html")

        # save the name, major, courses, and number in the database
        usr = users(name, major, courses, number)
        db.session.add(usr)
        db.session.commit()
        flash("Info entered successfuly!")
        return redirect(url_for("view"))

    # request.method == "GET"
    else:
        return render_template("register.html")

# use this route to delete users
@app.route("/admin", methods=["POST", "GET"])
def admin():
    # delete the user
    if request.method == "POST":
        name = request.form["name"]
        session["name"] = name
        found_user = users.query.filter_by(name=name).delete()
        if not name or not found_user:
            flash(name + " not found!")
            return redirect(url_for("view"))
        else:
            db.session.commit()
            flash(name + " succesfuly deleted!")
            return redirect(url_for("view"))

    # request.method == "GET"
    # enter the information to be deleted
    else:
        return render_template("admin.html")

if __name__ == "__main__":
    db.create_all() 
    app.run(debug=True)
