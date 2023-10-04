from flask import Flask
from routes import routes_bp  # Import the routes Blueprint

app = Flask(__name__)

# Register the Blueprint with your app
app.register_blueprint(routes_bp)

if __name__ == '__main__':
    app.run(debug=True)
