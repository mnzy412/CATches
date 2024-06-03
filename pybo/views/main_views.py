# main_views.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g, current_app
import random
import string
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import pymysql

bp = Blueprint('main', __name__, url_prefix='/')

def get_db():
    if 'db' not in g:
        g.db = current_app.get_db()
    return g.db

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

        db = get_db()
        cursor = db.cursor()
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
        
        db = get_db()
        cursor = db.cursor()
        try:
            sql = "SELECT * FROM users WHERE email = %s AND status = 'active'"
            cursor.execute(sql, (email,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user[2], password):  # user[2]가 해시된 비밀번호
                session['user_id'] = user[0]  # user[0]이 사용자 ID
                session['user_nick'] = user[5]  # user[5]가 사용자 닉네임
                session['user_email'] = user[1]  # user[1]이 사용자 이메일
                if remember:
                    session.permanent = True
                    current_app.permanent_session_lifetime = timedelta(hours=3)  # 3시간 동안 세션 유지
                else:
                    session.permanent = True
                    current_app.permanent_session_lifetime = timedelta(hours=1)  # 1시간 동안 세션 유지
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
    #if 'user_id' not in session:
        #flash('로그인이 필요합니다.', 'danger')
        #return redirect(url_for('main.login'))
    #return render_template('mypage_case.html')
    if 'user_id' in session:
            user_id = session['user_id']
            db = get_db()
            cursor = db.cursor()
            case_list = []
            try:
                sql = """
                SELECT ci.case_key, b.bank_account, b.bank_nickname, cd.case_type, ci.case_date, s.suspect_status 
                FROM case_info ci 
                JOIN case_detail cd ON ci.case_key = cd.case_key 
                JOIN suspects s ON ci.case_key = s.case_key 
                JOIN bank_info b ON ci.bank_key = b.bank_key 
                WHERE ci.user_key = %s
                """
                cursor.execute(sql, (user_id,))
                cases = cursor.fetchall()
                
                for case in cases:
                    case_dict = {
                        'case_key': case[0],
                        'bank_account': case[1],
                        'bank_nickname': case[2],
                        'case_type': case[3],
                        'case_date': case[4],
                        'suspect_status': case[5],
                    }
                    case_list.append(case_dict)
            except pymysql.MySQLError as e:
                flash(f"Database error: {str(e)}", "danger")
            finally:
                cursor.close()
            
            return render_template('mypage_case.html', cases=case_list)
    
@bp.route('/mypage/phishing')
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
    db = get_db()
    cursor = db.cursor()
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
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('main.login'))
      
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        db = get_db()
        cursor = db.cursor()
        try:
            sql = "SELECT * FROM users WHERE email = %s AND status = 'active'"
            cursor.execute(sql, (email,))
            user = cursor.fetchone()
            
            if user and user[1] == session.get('user_email') and check_password_hash(user[2], password):
                return render_template('withdraw_confirm.html', email=email)
            else:
                flash('현재 로그인된 계정의 이메일 또는 비밀번호가 잘못되었습니다.', 'danger')
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
        db = get_db()
        cursor = db.cursor()
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

    db = get_db()
    cursor = db.cursor()
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

    db = get_db()
    cursor = db.cursor()
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

@bp.route('/case_list', methods=['GET'])
def case_list():
    case_info = request.args.get('caseInfo', '')

    if not case_info:
        flash('검색어를 입력해주세요.', 'danger')
        return redirect(url_for('main.case_search'))

    try:
        if case_info.isdigit() and len(case_info) == 11:
            # 11자리 숫자인 경우 suspects 테이블 조회
            sql = """
                SELECT i.case_key, b.bank_account, b.bank_nickname, d.case_type, i.case_date, s.suspect_status
                FROM case_info i
                JOIN bank b ON i.bank_key = b.bank_key
                JOIN case_detail d ON i.case_key = d.case_key
                JOIN suspects s ON b.suspect_key = s.suspect_key
                WHERE s.suspect_phone = %s
            """
            cursor.execute(sql, (case_info,))
        else:
            # 다른 경우 bank 테이블 조회
            sql = """
                SELECT i.case_key, b.bank_account, b.bank_nickname, d.case_type, i.case_date, s.suspect_status
                FROM case_info i
                JOIN bank b ON i.bank_key = b.bank_key
                JOIN case_detail d ON i.case_key = d.case_key
                JOIN suspects s ON b.suspect_key = s.suspect_key
                WHERE b.bank_account = %s OR b.bank_nickname = %s
            """
            cursor.execute(sql, (case_info, case_info))
        
        cases = cursor.fetchall()
        
        case_list = []
        for case in cases:
            case_dict = {
                'case_key': case[0],
                'bank_account': case[1],
                'bank_nickname': case[2],
                'case_type': case[3],
                'case_date': case[4],
                'suspect_status': case[5],
            }
            case_list.append(case_dict)
        
        return render_template('case_list.html', cases=case_list, caseInfo=case_info)
    except pymysql.MySQLError as e:
        flash(f"검색 중 오류가 발생했습니다: {e}", 'danger')
        return redirect(url_for('main.case_search'))



@bp.route('/case_detail/<int:case_key>')
def case_detail(case_key):
    try:
        sql = """
            SELECT i.case_key, b.bank_account, b.bank_nickname, d.case_type, i.case_date, s.suspect_status, 
                   s.suspect_phone, s.suspect_sex, s.suspect_age, s.suspect_credit, s.suspect_country, 
                   p.platform_name, p.platform_url, d.case_item, d.case_price, d.bank_date, d.case_content,
                   po.police_name, po.police_location
            FROM case_info i
            JOIN bank b ON i.bank_key = b.bank_key
            JOIN case_detail d ON i.case_key = d.case_key
            JOIN suspects s ON b.suspect_key = s.suspect_key
            JOIN platform p ON i.platform_key = p.platform_key
            LEFT JOIN polices po ON s.police_key = po.police_key
            WHERE i.case_key = %s
        """
        cursor.execute(sql, (case_key,))
        case = cursor.fetchone()

        if not case:
            flash("해당 사례를 찾을 수 없습니다.", 'danger')
            return redirect(url_for('main.case_list'))

        case_info = {
            'case_key': case[0],
            'bank_account': case[1],
            'bank_nickname': case[2],
            'case_type': case[3],
            'case_date': case[4],
            'suspect_status': case[5],
            'suspect_phone': case[6],
            'suspect_sex': case[7],
            'suspect_age': case[8],
            'suspect_credit': case[9],
            'suspect_country': case[10],
            'platform_name': case[11],
            'platform_url': case[12],
            'case_item': case[13],
            'case_price': case[14],
            'bank_date': case[15],
            'case_content': case[16],
            'police_name': case[17],
            'police_location': case[18]
        }

        if case_info['suspect_status'] == 'arrested':
            return render_template('case_detail_arrested.html', case=case_info)
        else:
            return render_template('case_detail_unarrested.html', case=case_info)

    except pymysql.MySQLError as e:
        flash(f"상세 조회 중 오류가 발생했습니다: {e}", 'danger')
        return redirect(url_for('main.case_list'))


@bp.route('/phishing_detail')
def phishing_detail():
    return render_template('phishing_detail.html')
