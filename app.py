from flask import Flask
from routes.upload_routes import upload_bp
from routes.data_routes import data_bp
from routes.model_routes import model_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(upload_bp)
app.register_blueprint(data_bp)
app.register_blueprint(model_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5001)