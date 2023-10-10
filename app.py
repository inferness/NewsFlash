from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import input_required, Length, ValidationError

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SECRET_KEY'] = "secretkey"
# initialize the app with the extension
db.init_app(app)

##Model schema
class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String, unique=True, nullable=False)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[input_required(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[input_required(), Length(min=8, max=80)])
    submit = SubmitField('Submit')

# Register the Blueprint with your app

# Routes
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/library")
def library():
    return render_template("library.html")

@app.route("/team")
def team():
    return render_template("team.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        print("login")
        user = User.query.filter_by(username=form.username.data).first()
        if(user):
            if(user.password == form.password.data):
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'), form=form)

    return render_template("login.html", form=form)

@app.route("/articles/<id>")
def articles(id):
    # Now you can use the article_id in your code
    return render_template("/articles/article" + id + ".html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
