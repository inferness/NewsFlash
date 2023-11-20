from flask import Flask, render_template, request, redirect, url_for, session, jsonify
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
# configure the SQLite database
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

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[input_required(), Length(min=4, max=15)])
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[
        validators.DataRequired(),
        validators.Length(min=8),
        validators.EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')

LoggedInUser = User()

# Routes
@app.route("/")
@app.route("/home")
def home():
    logged_in_user = session.get('LoggedInUser', None)
    print(logged_in_user)
    return render_template("home.html", user=logged_in_user)

@app.route("/team")
def team():
    return render_template("team.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    global LoggedInUser
    print(LoggedInUser)
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if(user):
            if(user.password == form.password.data):
                user_dict = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
                session['LoggedInUser'] = user_dict
                return redirect(url_for('home'))
        else:
            return redirect(url_for('login'), form=form)

    return render_template("login.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # Create a new user instance with form data
        existing_user = User.query.filter(
            (User.email == form.email.data) | (User.username == form.username.data)
        ).first()

        if (existing_user):
            return render_template('register.html', form=form)
            
        else: 
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )

            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            # Redirect to a success page or login page
            return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/articles/<id>")
def articles(id):
    # Now you can use the article_id in your code
    logged_in_user = session.get('LoggedInUser', None)
    return render_template("/articles/article" + id + ".html", user=logged_in_user)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
