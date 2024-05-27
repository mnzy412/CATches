from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import pymysql
import random
import string
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from datetime import datetime

bp = Blueprint('main', __name__, url_prefix='/')

# 데이터베이스 연결 설정
db = pymysql.connect(
    host='localhost', 
    user='root', 
    password='root', 
    db='catchesdb', 
    charset='utf8'
)
cursor = db.cursor()

def generate_random_nick():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

@bp.route('/hello')
def hello_pybo():
    return 'Hello, catches'

@bp.route('/')
def index():
    return render_template('home.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_phone = request.form['user_phone']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])  # 비밀번호 해시화
        user_nick = generate_random_nick()

        try:
            sql = "INSERT INTO users (email, password, user_name, status, user_nick, user_phone) VALUES (%s, %s, %s, 'active', %s, %s)"
            cursor.execute(sql, (email, password, user_name, user_nick, user_phone))
            db.commit()
            flash('회원가입이 성공적으로 완료되었습니다.', 'success')
            return redirect(url_for('main.login'))
        except pymysql.MySQLError as e:
            db.rollback()
            flash(f"회원가입 중 오류가 발생했습니다: {e}", 'danger')

    return render_template('user_register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = request.form.get('remember')
        
        try:
            sql = "SELECT * FROM users WHERE email = %s AND status = 'active'"
            cursor.execute(sql, (email,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user[2], password):  # user[2]가 해시된 비밀번호라고 가정
                session['user_id'] = user[0]  # user[0]이 사용자 ID라고 가정
                session['user_nick'] = user[4]  # user[4]가 사용자 닉네임이라고 가정
                session['user_email'] = user[1]  # user[1]이 사용자 이메일이라고 가정
                if remember:
                    session.permanent = True
                    bp.permanent_session_lifetime = timedelta(days=30)  # 30일 동안 세션 유지
                flash('로그인 성공!', 'success')
                return redirect(url_for('main.mypage'))  # 로그인 성공 시 마이페이지로 리다이렉트
            else:
                flash('이메일 또는 비밀번호가 잘못되었습니다.', 'danger')
        except pymysql.MySQLError as e:
            flash(f"로그인 중 오류가 발생했습니다: {e}", 'danger')
    
    return render_template('user_login.html')

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_nick', None)
    session.pop('user_email', None)
    flash('로그아웃되었습니다.', 'success')
    return redirect(url_for('main.index'))


@bp.route('/mypage')
def mypage():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('main.login'))
    user_nick = session.get('user_nick')
    user_email = session.get('user_email')
    return render_template('mypage.html', user_nick=user_nick, user_email=user_email)

@bp.route('/mypage/case')
def mypage_case():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('main.login'))
    return render_template('mypage_case.html')

@bp.route('/mypage/phishing')
def mypage_phishing():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('main.login'))
    return render_template('mypage_phishing.html')

@bp.route('/search/c')
def case_search():
    return render_template('case_search.html')

@bp.route('/search/p')
def phishing_search():
    return render_template('phishing_search.html')

@bp.route('/case_info')
def case_info():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('main.login'))
    
    user_id = session['user_id']
    bank_name = request.args.get('bank_name')
    bank_account = request.args.get('bank_account')
    bank_nickname = request.args.get('bank_nickname')
    suspect_phone = request.args.get('suspect_phone')
    bank_date = request.args.get('case_date')
    case_price = request.args.get('case_price')
    case_type = request.args.get('case_type')
    case_item = request.args.get('case_item')
    platform_name = request.args.get('platform_type')
    suspect_id = request.args.get('suspect_key')
    platform_url = request.args.get('phishing_url')
    case_content = request.args.get('case_description')
    current_time = datetime.now()
    case_date = current_time.strftime("%Y-%m-%d %H:%M:%S")

    try:
        suspect_sql = "INSERT INTO suspects (suspect_phone, suspect_status) VALUES (%s,'unarrested')"
        cursor.execute(suspect_sql, (suspect_phone))
        suspect_pk = cursor.lastrowid

        platform_sql = "INSERT INTO platform (platform_name, platform_url, suspent_id) VALUES (%s, %s, %s)"
        cursor.execute(platform_sql, (platform_name, platform_url, suspect_id))
        platform_pk = cursor.lastrowid

        bank_code_sql = "INSERT INTO bank_code (bank_name) VALUES (%s)"
        cursor.execute(bank_code_sql, (bank_name))
        bank_code_pk = cursor.lastrowid

        bank_sql = "INSERT INTO bank (suspect_key, bank_account, bank_nickname, bank_code) VALUES (%s, %s, %s, %s)"
        cursor.execute(bank_sql, (suspect_pk, bank_account, bank_nickname, bank_code_pk))
        bank_pk = cursor.lastrowid

        info_sql = "INSERT INTO case_info (user_key, platform_key, bank_key, case_date, case_status) VALUES (%s, %s, %s, %s, 'continue')"
        cursor.execute(info_sql, (user_id, platform_pk, bank_pk, case_date))
        info_pk = cursor.lastrowid

        detail_sql = "INSERT INTO case_detail (case_key, case_type, case_item, case_price, bank_date, case_content) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(detail_sql, (info_pk, case_type, case_item, case_price, bank_date, case_content))
        db.commit()
        flash('피해사례 등록이 성공적으로 완료되었습니다.', 'success')
        return redirect(url_for('main.index'))  # 변경: url_for('main.index')로 수정합니다.
        
    except pymysql.MySQLError as e:
        db.rollback()
        flash(f"피해사례 등록 중 오류가 발생했습니다: {e}", 'danger')

    return render_template('case_info.html')

@bp.route('/phishing_info')
def phishing_info():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('main.login'))
    
    user_id = session['user_id']
    phishing_url = request.args.get('site_url')
    site_name = request.args.get('site_name')
    site_type = request.args.get('case_type')
    site_content = request.args.get('site_content')
    phishing_count = 0
    current_time = datetime.now()
    phishing_date = current_time.strftime("%Y-%m-%d %H:%M:%S")

    try:
        phishing_sql = "INSERT INTO phishing_info (user_key, phishing_count, phishing_date, phishing_url) VALUES (%s, %s, %s, %s)"
        cursor.execute(phishing_sql, (user_id, phishing_count, phishing_date, phishing_url))
        phishing_pk = cursor.lastrowid

        phishing_detail_sql = "INSERT INTO phishing_info (phishing_key, site_type, site_name, site_content) VALUES (%s, %s, %s, %s)"
        cursor.execute(phishing_detail_sql, (phishing_pk, site_type, site_name, site_content))

        db.commit()
        flash('피싱사이트 등록이 성공적으로 완료되었습니다.', 'success')
        return redirect(url_for('main.index'))  # 변경: url_for('main.index')로 수정합니다.

    except pymysql.MySQLError as e:
        db.rollback()
        flash(f"피해사례 등록 중 오류가 발생했습니다: {e}", 'danger')


    return render_template('phishing_info.html')

@bp.route('/case_list')
def case_list():
    caseList = request.form['caseList']
    if caseList == '계좌 정보':
        table_name = 'suspects'
    return render_template('case_list.html')

@bp.route('/case_detail')
def case_detail():
    return render_template('case_detail.html')

@bp.route('/check_case_detail')
def check_case_detail():
    return render_template('check_case_detail.html')

@bp.route('/solve_case_detail')
def solve_case_detail():
    return render_template('solve_case_detail.html')

@bp.route('/phishing_detail')
def phishing_detail():
    return render_template('phishing_detail.html')
