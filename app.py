from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Todo(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self) -> str:
        return f"<Todo {self.title} - {self.Sno}>"

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
    todo = Todo(title = title, desc = desc) ## create an object of the Todo class
    db.session.add(todo) ## add the object to the session
    db.session.commit() ## commit the session to the database
    all_todo = Todo.query.all()
    return render_template("index.html", all_todo=all_todo) ## render the template with the objects
@app.route("/show")
def products():
    all_todo = Todo.query.all() ## query all the objects of the Todo class
    print(all_todo) ## print the objects in the console
    return "<p>New products</p>"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)