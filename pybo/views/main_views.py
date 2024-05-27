from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import pymysql
import random
import string
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime


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

# 닉네임 생성 로직 수정
nick_prefixes = ["더보이즈", "투바투", "엔시티", "스키즈", "제베원", "투어스", "라이즈", "보넥도", "뉴진스", "에스파"]

def generate_random_nick():
    prefix = random.choice(nick_prefixes)
    suffix = ''.join(random.choices(string.digits, k=4))
    return prefix + suffix

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
                session['user_nick'] = user[5]  # user[5]가 사용자 닉네임이라고 가정
                session['user_email'] = user[1]  # user[1]이 사용자 이메일이라고 가정
                if remember:
                    session.permanent = True
                    bp.permanent_session_lifetime = timedelta(days=30)  # 30일 동안 세션 유지
                #flash('로그인 성공!', 'success')
                return redirect(url_for('main.index'))  # 로그인 성공 시 마이페이지로 리다이렉트
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
    #flash('로그아웃되었습니다.', 'success')
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

@bp.route('/mypage/pishing')
def mypage_phishing():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('main.login'))
    return render_template('mypage_phishing.html')

@bp.route('/user_info')
def user_info():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    try:
        sql = "SELECT user_name, user_phone FROM users WHERE user_key = %s"
        cursor.execute(sql, (user_id,))
        user = cursor.fetchone()
        if user:
            return {'user_name': user[0], 'user_phone': user[1]}, 200
        else:
            return {'error': 'User not found'}, 404
    except pymysql.MySQLError as e:
        return {'error': str(e)}, 500

@bp.route('/withdraw', methods=['GET', 'POST'])
def user_withdraw():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            sql = "SELECT * FROM users WHERE email = %s AND status = 'active'"
            cursor.execute(sql, (email,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user[2], password):
                return render_template('withdraw_confirm.html', email=email)
            else:
                flash('이메일 또는 비밀번호가 잘못되었습니다.', 'danger')
        except pymysql.MySQLError as e:
            flash(f"탈퇴 처리 중 오류가 발생했습니다: {e}", 'danger')
    
    return render_template('user_withdraw.html')

@bp.route('/withdraw_confirm', methods=['POST'])
def withdraw_confirm():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('main.login'))
    
    if 'agree' in request.form:
        user_id = session['user_id']
        try:
            sql = "UPDATE users SET status = 'deleted', deleted_at = %s WHERE user_key = %s"
            cursor.execute(sql, (datetime.now(), user_id))
            db.commit()
            flash('회원 탈퇴가 성공적으로 처리되었습니다. 3일 내에 로그인하면 계정이 활성화됩니다.', 'success')
            return redirect(url_for('main.logout'))
        except pymysql.MySQLError as e:
            db.rollback()
            flash(f"탈퇴 처리 중 오류가 발생했습니다: {e}", 'danger')
    else:
        flash('탈퇴를 완료하려면 동의해주셔야 합니다.', 'danger')

    return redirect(url_for('main.user_withdraw'))

@bp.route('/search/c')
def case_search():
    return render_template('case_search.html')

@bp.route('/search/p')
def phishing_search():
    return render_template('phishing_search.html')

@bp.route('/case_info')
def case_info():
    return render_template('case_info.html')

@bp.route('/phishing_info')
def phishing_info():
    return render_template('phishing_info.html')

@bp.route('/case_list')
def case_list():
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
