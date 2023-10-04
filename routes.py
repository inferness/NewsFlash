from flask import Blueprint, render_template

# Create a Blueprint object
routes_bp = Blueprint("routes", __name__)

# Define your routes and their functions
@routes_bp.route("/")
@routes_bp.route("/home")
def home():
    return render_template("home.html")

@routes_bp.route("/library")
def library():
    return render_template("library.html")

@routes_bp.route("/team")
def team():
    return render_template("team.html")

@routes_bp.route("/login")
def login():
    return render_template("login.html")
