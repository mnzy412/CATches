from flask import Flask
import secrets

def create_app():
    app = Flask(__name__)
    
    # 임의의 고유한 secret_key 생성
    app.secret_key = secrets.token_urlsafe(16) 

    # 블루프린트
    from .views import main_views
    app.register_blueprint(main_views.bp)

    return app
