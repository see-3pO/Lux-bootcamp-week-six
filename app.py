from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

#///=Relative path
#////=Absolute path
#configuration for the FLASKALCHEMY extension
#
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#initializing the extension
db = SQLAlchemy(app)

#Todo class that inherits from the db.Model()
#class represents a table in the db with three columns id...
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


#hello function returns an html template rendered with data from the database
@app.route('/')
def hello():
    todo_list = Todo.query.all()
    return render_template("todoapp.html", todo_list=todo_list)

#adding new task to the database
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("hello"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("hello"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("hello"))

if __name__=='__main__':
    #creates an application context for the db session in the hello,add,update,delete functions
    #ensures code is executed within context of Flask application
    with app.app_context():
        #inside the if ___name to also ensure the schema is created within the context of the flask app
        db.create_all()
    app.run(host='0.0.0.0',port=80, debug=True)