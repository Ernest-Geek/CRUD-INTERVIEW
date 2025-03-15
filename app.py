from flask import Flask
from flask_jwt_extended import JWTManager
from usermanagementapi.routes.auth_routes import auth_routes
from usermanagementapi.config.config import SECRET_KEY

app = Flask(__name__)


app.config["JWT_SECRET_KEY"] = SECRET_KEY  

jwt = JWTManager(app)

app.register_blueprint(auth_routes, url_prefix="/api")

@app.route("/")
def home():
    return {"message": "Welcome to the User Management API"}

if __name__ == "__main__":
    app.run(debug=True)
