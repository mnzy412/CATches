from flask import Flask
import secrets
from flask_apscheduler import APScheduler
import pymysql

def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_urlsafe(16)

    db = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='catchesdb',
        charset='utf8'
    )

    scheduler = APScheduler()

    def finalize_withdrawals():
        with app.app_context():
            try:
                cursor = db.cursor()
                sql = """
                UPDATE users
                SET user_name = '탈퇴한 회원',
                    email = CONCAT('deleted_', user_key, '@example.com'),
                    password = '',
                    user_phone = NULL,
                    user_nick = NULL
                WHERE status = 'deleted' AND TIMESTAMPDIFF(DAY, deleted_at, NOW()) >= 3;
                """
                cursor.execute(sql)
                db.commit()
            except pymysql.MySQLError as e:
                print(f"Error finalizing withdrawals: {e}")

    scheduler.add_job(id='finalize_withdrawals', func=finalize_withdrawals, trigger='interval', hours=1)
    scheduler.start()

    from .views import main_views
    app.register_blueprint(main_views.bp)

    return app