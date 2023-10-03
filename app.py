from flask import Flask, render_template

app = Flask(__name__)

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

@app.route("/login")
def login():
	return render_template("login.html")

if __name__ == '__main__':
	app.run(debug=True)