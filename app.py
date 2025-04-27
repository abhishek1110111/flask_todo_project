from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) ## create an instance of the Flask class

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Todo(db.Model): ## create a class Todo which is a child class of db.Model
    Sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self) -> str:
        return f"<Todo {self.title} - {self.Sno}>"

@app.route("/", methods=["GET", "POST"]) ## home page
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc) ## create an object of the Todo class
        db.session.add(todo) ## add the object to the session
        db.session.commit() ## commit the session to the database
    all_todo = Todo.query.all()
    return render_template("index.html", all_todo=all_todo) ## render the template with the objects

@app.route("/delete/<int:Sno>") ## delete the object with the given Sno
def delete(Sno):
    delete_todo = Todo.query.filter_by(Sno=Sno).first() ## query all the objects of the Todo class
    print(delete_todo) ## print the objects in the console
    db.session.delete(delete_todo)
    db.session.commit() ## commit the session to the database
    return redirect("/")

@app.route("/update/<int:Sno>", methods=["GET", "POST"]) ## update the object with the given Sno
def update(Sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(Sno=Sno).first() ## query all the objects of the Todo class
        todo.title = title
        todo.desc = desc    ## update the object with the given Sno
        db.session.add(todo) ## add the object to the session
        db.session.commit() ## commit the session to the database
        return redirect("/")
    update_todo = Todo.query.filter_by(Sno=Sno).first() ## query all the objects of the Todo class
    return render_template("update.html", update_todo=update_todo) 

@app.route("/about-us") ## about us page
def about_us():
    return render_template("aboutus.html")

if __name__ == "__main__": ## main function
    with app.app_context():## create the database and tables
        db.create_all()
    app.run(debug=True, port=8000)