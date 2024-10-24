from flask import Flask
from config import Config
from extensions import jwt, mail 
from routers.account_routes import account_bp
from routers.transaction_routes import transaction_bp
from routers.user_routes import user_bp
from flask_cors import CORS  
from datetime import timedelta

app = Flask(__name__)
app.config.from_object(Config)

mail.init_app(app)  
jwt.init_app(app)   

CORS(app)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(account_bp, url_prefix='/account')
app.register_blueprint(transaction_bp, url_prefix='/transaction')

if __name__ == '__main__':
    app.run(debug=True)
