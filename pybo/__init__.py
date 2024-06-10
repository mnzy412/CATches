# __init__.py
from flask import Flask, g
import secrets
from flask_apscheduler import APScheduler
import pymysql
from datetime import timedelta
from werkzeug.security import generate_password_hash
import random
import string

def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_urlsafe(16)
    app.permanent_session_lifetime = timedelta(hours=1)  # 기본 세션 유효 기간을 1시간으로 설정

    def get_db():
        if 'db' not in g:
            g.db = pymysql.connect(
                host='localhost',
                user='root',
                password='root',
                db='catchesdb',
                charset='utf8'
            )
        return g.db

    @app.teardown_appcontext
    def teardown_db(exception):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    scheduler = APScheduler()

    def generate_random_email(user_key):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        return f'deleted_{user_key}_{random_string}@example.com'

    def generate_dummy_password():
        return generate_password_hash('dummy_password')

    def finalize_withdrawals():
        with app.app_context():
            try:
                db = get_db()
                cursor = db.cursor()
                sql = "SELECT user_key FROM users WHERE status = 'deleted' AND TIMESTAMPDIFF(MINUTE, deleted_at, NOW()) >= 1"
                #TIMESTAMPDIFF(DAY, deleted_at, NOW()) >= 3 
                #테스트를 위해 1분으로 설정 
                cursor.execute(sql)
                deleted_users = cursor.fetchall()

                for user in deleted_users:
                    user_key = user[0]
                    random_email = generate_random_email(user_key)
                    dummy_password = generate_dummy_password()

                    update_sql = """
                    UPDATE users 
                    SET user_nick = '탈퇴한 회원',
                        email = %s,
                        password = %s,
                        user_phone = NULL,
                        user_name = NULL
                    WHERE user_key = %s
                    """
                    cursor.execute(update_sql, (random_email, dummy_password, user_key))

                db.commit()
                print(f"{cursor.rowcount} rows updated")
            except pymysql.MySQLError as e:
                db.rollback()
                print(f"Error finalizing withdrawals: {e}")
            finally:
                cursor.close()

    scheduler.add_job(id='finalize_withdrawals', func=finalize_withdrawals, trigger='interval', minutes=1)
    scheduler.start()

    from .views import main_views
    app.register_blueprint(main_views.bp)

    app.get_db = get_db

    return app
