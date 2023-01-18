#Creating web page with TODO list
# ADD what to do
# What is the list active
# List completed
# Adding Due Date


from flask import Flask, render_template, jsonify, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import random
from flask_bootstrap import Bootstrap
from datetime import datetime, date

from sqlalchemy import func, desc

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)
Bootstrap(app)


class Note(db.Model):
   id = db.Column(db.Integer(), primary_key = True)
   text = db.Column(db.String(100))
   complete = db.Column(db.Boolean())
   date = db.Column(db.DateTime(timezone=True), default=func.now())

   def __repr__(self):
       return self.text


@app.route("/", methods=["GET", "POST"])
def home():
    # if request.method == "POST":
    #     task = request.form.get("taskname")
    #     print(task)
    # return render_template("index.html")
    incomplete = Note.query.filter_by(complete=False).order_by(desc(Note.complete)).all()
    done = Note.query.filter_by(complete=True).order_by(desc(Note.complete)).all()
    return render_template("index.html", incomplete=incomplete, complete=done)


@app.route('/add', methods=['POST'])
def add():
    note = Note(text=request.form['taskname'], complete=False)
    db.session.add(note)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/complete/<id>')
def complete(id):
    note = Note.query.filter_by(id=int(id)).first()
    note.complete = True
    db.session.commit()

    return redirect(url_for('home'))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Note.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Note.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))



if __name__ == '__main__':
    app.run(debug=True)