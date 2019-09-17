from flask import Flask, render_template, request, url_for, redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Person(db.Model):

    __tablename__='client'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birthday = db.Column(db.String)
    telephone = db.Column(db.String)
    email = db.Column(db.String)
    gender = db.Column(db.String)

    def __init__(self, name, birthday, telephone, email, gender):
        self.name = name
        self.birthday = birthday
        self.telephone = telephone
        self.email = email
        self.gender = gender

db.create_all()


@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/forms", methods=['GET','POST'])
def forms():
    if request.method == "POST":
        name = request.form.get("name")
        birthday = request.form.get("birthday")
        telephone = request.form.get("telephone")
        email = request.form.get("email")
        gender = request.form.get("gender")

        if (name and birthday and telephone and email and gender):
            p = Person(name, birthday, telephone, email, gender)
            db.session.add(p)
            db.session.commit()

    return redirect(url_for("index"))

@app.route("/list")
def list():
    people = Person.query.all()
    return render_template("list.html", people=people)

@app.route("/delete/<int:id>")
def delete(id):
    person = Person.query.filter_by(id=id).first()

    db.session.delete(person)
    db.session.commit()

    people = Person.query.all()
    return render_template("list.html", people=people)

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    person = Person.query.filter_by(id=id).first()

    if request.method == "POST":
        name = request.form.get("name")
        birthday = request.form.get("birthday")
        telephone = request.form.get("telephone")
        email = request.form.get("email")
        gender = request.form.get("gender")

        if name and birthday and telephone and email and gender:
            person.name = name
            person.birthday = birthday
            person.telephone = telephone
            person.email = email
            person.gender = gender

            db.session.commit()

            return redirect(url_for("list"))

    return render_template("edit.html", person=person)



if __name__ == '__main__':
    app.run(debug=True)
