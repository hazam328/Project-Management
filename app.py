from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from sqlalchemy import create_engine
# from sqlalchemy.engine import url
# from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
# url = "https:cms.mlcs.xyz/api/view/teaching_staff/all/"
# batches_sessions= request.gets("https:cms.mlcs.xyz/api/view/bscs_2017/all/")
# teachers= request.get("https:cms.mlcs.xyz/api/view/teaching_staff/all/")

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///project_management.db'
app.config['SECRET_KEY'] = "Ebounesgg+328@"
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False

db.init_app(app)


# engine = create_engine("mysql+pymysql://root:Pashtoon-328@localhost:3306/project_management")
# db = scoped_session(sessionmaker(bind=engine))
class Students(db.Model):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    roll_no = db.Column(db.Integer, nullable=False)
    team_member1 = db.Column(db.String(100), nullable=False)
    team_member2 = db.Column(db.String(100), nullable=False)
    final_project = db.Column(db.String(200), nullable=False)
    supervisor = db.Column(db.String(100), unique=True)
    batch = db.Column(db.String(100), nullable=False)
    sessions = db.Column(db.Integer, nullable=False)
    # date_created = db.Column(db.DATE, default=datetime.now())


@app.route("/", methods=["GET"])
def main():
    if session.get == " username ":
        return render_template("admin_form.html", session=session)
    else:
        return render_template('login.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username.lower() == "admin" and password == "12345":
            session["username"] = "admin"
            return render_template("admin_form.html")
        else:
            msg = "Incorrect username or password"
            return render_template('login.html', msg=msg)
    else:
        return render_template('login.html', )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('admin_form'))


@app.route("/admin_form", methods=["GET", 'POST'])
def admin():

        if request.method == 'POST':
            name = request.form.get("name")
            rollno = request.form.get("rollno")
            team1 = request.form.get("team1")
            team2 = request.form.get("team2")
            fproject = request.form.get("fproject")
            supervisor = request.form.get("supervisor")
            batch = request.form.get("batch")
            sessions = request.form.get("sessions")
            stud = Students(name=name, roll_no=rollno, team_member1=team1,
                            team_member2=team2, final_project=fproject,
                            supervisor=supervisor, batch=batch, sessions=sessions)
            db.session.add(stud)
            db.session.commit()
            return render_template("admin_form.html", project=Students)
        # db.execute("INSERT into project(name, roll_no, team_member1, team_member2, supervisor, batch, session)"
        #            " VALUES(:name, :roll_no, :team_member1, :team_member2, :supervisor, :batch, session)",
        #            {"name": name, "roll_no": rollno, "team_member1": team1, "team_member2": team2,
        #             "supervisor": supervisor, "batch": batch, "session:": session})
        # db.commit()
        else:
            return render_template("admin_form.html")


@app.route("/batch/<bt>", methods=['GET'])
def batch_filter(bt):
    batch = Students.query.filter(Students.batch == bt).all()
    return render_template("output.html", batch=batch)


@app.route("/batches_sessions", methods=["GET"])
def batches_sessions():

        from urllib.request import urlopen
        import json
        url = "https://cms.mlcs.xyz/api/view/program_sessions/all/"

        response = urlopen(url)
    
        data_json = json.loads(response.read())
        batches = []
        for i in data_json:
            batches.append(i['Session_Title'])
        print(batches)
        return render_template("batches_sessions.html", batches=batches)



@app.route("/teachers", methods=["GET"])
def teachers():
        import json
        from urllib.request import urlopen
        url = "https://cms.mlcs.xyz/api/view/teaching_staff/all/"

        response = urlopen(url)
        data_json = json.loads(response.read())

        teach = []
        for a in data_json:
            teach.append(a['teacher_name'])
            teach.append(a['teacher_designation'])
        print(teach)
        return render_template('teachers.html', teach=teach)


@app.route("/output", methods=["GET", "POST"])
def output():

        project = Students.query.all()

        return render_template("output.html", project=project)


@app.route("/delete/<int:id>/", methods=["POST", "GET"])
def delete(id):
    if request.method == "GET":
        stud = Students.query.filter_by(id=id).first()
        db.session.delete(stud)
        db.session.commit()
        return redirect(url_for('output'))

    return render_template("admin_form.html", id=id)


@app.route("/update/<int:id>/", methods=["POST","GET"])
def update (id):
    if request.method == "POST":
        name = request.form.get("name")
        rollno = request.form.get("rollno")
        team1 = request.form.get("team1")
        team2 = request.form.get("team2")
        fproject = request.form.get("fproject")
        supervisor = request.form.get("supervisor")
        batch = request.form.get("batch")
        sessions = request.form.get("sessions")

        stud = Students.query.filter_by(id = id).first()
        stud.name=name
        stud.roll_no=rollno
        stud.team_member1=team1
        stud.team_member2=team2
        stud.final_project=fproject
        stud.supervisor=supervisor
        stud.batch=batch
        stud.sessions=sessions

        db.session.commit()
        flash("Record Successfully Updated!")
        return redirect(url_for("output"))
    else:
        stud = Students.query.filter_by(id=id).first()
        return render_template("update.html", stud=stud, id=id)


if __name__ == '__main__':
    app.run(debug=True)
