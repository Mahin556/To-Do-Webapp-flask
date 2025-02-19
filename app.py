from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        title = request.form.get('title')
        desc = request.form.get('desc')

        if title:  # Ensure valid input before adding to the database
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
            return redirect("/")  # Redirect to avoid form resubmission

    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)

@app.route("/show")
def show():
    alltodo = Todo.query.all()
    print(alltodo)
    return "Hello"

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
   if request.method == "POST":
        title = request.form.get('title')
        desc = request.form.get('desc')
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")  # Redirect to avoid form resubmission
       
   todo = Todo.query.filter_by(sno=sno).first()
   return render_template('update.html', todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    else:
        print(f"Todo with sno={sno} not found")
    
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
