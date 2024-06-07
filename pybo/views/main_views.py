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
global_cursor = db.cursor()

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
            cursor = db.cursor()
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
            cursor = db.cursor()
            sql = "SELECT * FROM users WHERE email = %s"
            cursor.execute(sql, (email,))
            user = cursor.fetchone()

            if user and check_password_hash(user[2], password):
                user_status = user[4]
                if user_status == 'deleted':  # user[5]는 상태(status)
                    deleted_at = user[7]  # user[7]는 deleted_at 컬럼
                    if deleted_at and (datetime.now() - deleted_at).days <= 3:
                        # 3일 이내이면 상태를 active로 변경
                        cursor.execute("UPDATE users SET status = 'active', deleted_at = NULL WHERE user_key = %s", (user[0],))
                        db.commit()
                        user_status = 'active'  # 상태 업데이트

                elif user_status == 'active':
                    session['user_id'] = user[0]
                    session['user_nick'] = user[6]
                    session['user_email'] = user[1]
                    session.permanent = True
                    session_lifetime = timedelta(days=30) if remember else timedelta(hours=1)
                    session.permanent_session_lifetime = session_lifetime
                    #flash('로그인 성공!', 'success')
                    return redirect(url_for('main.index'))
                else:
                    flash('계정이 비활성화 상태입니다.', 'danger')
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

    user_id = session['user_id']

    case_list = []
    try:
        cursor = db.cursor()
        sql = """
        SELECT ci.case_key, b.bank_account, b.bank_nickname, cd.case_type, ci.case_date, s.suspect_status 
        FROM case_info ci 
        JOIN case_detail cd ON ci.case_key = cd.case_key 
        JOIN bank b ON ci.bank_key = b.bank_key 
        JOIN suspects s ON b.suspect_key = s.suspect_key 
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

    user_id = session['user_id']

    phishing_list = []
    try:
        cursor = db.cursor()
        sql = """
        SELECT pi.phishing_key, pd.site_name, pi.phishing_url, pd.site_type, pi.phishing_date 
        FROM phishing_info pi 
        JOIN phishing_detail pd ON pi.phishing_key = pd.phishing_key 
        WHERE pi.user_key = %s
        """
        cursor.execute(sql, (user_id,))
        phishing_sites = cursor.fetchall()
        
        for site in phishing_sites:
            site_dict = {
                'phishing_key': site[0],
                'platform_name': site[1],
                'platform_url': site[2],
                'phishing_type': site[3],
                'phishing_date': site[4],
            }
            phishing_list.append(site_dict)
    except pymysql.MySQLError as e:
        flash(f"Database error: {str(e)}", "danger")
    finally:
        cursor.close()
    
    return render_template('mypage_phishing.html', phishing_sites=phishing_list)

@bp.route('/user_info')
def user_info():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    try:
        cursor = db.cursor()
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

    user_id = session['user_id']
    user_email = session['user_email']

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email != user_email:
            flash('입력된 이메일이 로그인한 계정과 일치하지 않습니다.', 'danger')
            return redirect(url_for('main.user_withdraw'))

        try:
            cursor = db.cursor()
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
            cursor = db.cursor()
            sql = "UPDATE users SET status = 'deleted', deleted_at = %s WHERE user_key = %s"
            cursor.execute(sql, (datetime.now(), user_id))
            db.commit()
            #flash('회원 탈퇴가 성공적으로 처리되었습니다. 3일 내에 로그인하면 계정이 활성화됩니다.', 'success')
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
@bp.route('/case_info', methods=["POST", "GET"])
def case_info():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        user_id = session['user_id']
        bank_name = request.form['bank_name']
        bank_account = request.form['bank_account']
        bank_nickname = request.form['bank_nickname']
        suspect_phone = request.form['suspect_phone']
        bank_date = request.form['case_date']
        case_price = request.form['case_price']
        case_type = request.form['case_type']
        case_item = request.form['case_item']
        platform_name = request.form['platform_type']
        suspect_id = request.form['suspect_key']
        platform_url = request.form['phishing_url']
        case_content = request.form['case_description']
        current_time = datetime.now()
        case_date = current_time.strftime("%Y-%m-%d %H:%M:%S")

        try:
            cursor = db.cursor()
            
            # Suspect insertion
            suspect_sql = "INSERT INTO suspects (suspect_phone, suspect_status) VALUES (%s, 'unarrested');"
            cursor.execute(suspect_sql, (suspect_phone,))
            suspect_pk = cursor.lastrowid

            # Platform insertion
            platform_sql = "INSERT INTO platform (platform_name, platform_url, suspent_id) VALUES (%s, %s, %s);"
            cursor.execute(platform_sql, (platform_name, platform_url, suspect_id))
            platform_pk = cursor.lastrowid

            # Check if the bank name already exists in bank_code
            bank_code_sql = "SELECT bank_code FROM bank_code WHERE bank_name = %s"
            cursor.execute(bank_code_sql, (bank_name,))
            bank_code_result = cursor.fetchone()

            if bank_code_result:
                bank_code_pk = bank_code_result[0]
            else:
                # If bank name does not exist, insert new bank code
                bank_code_sql = "INSERT INTO bank_code (bank_name) VALUES (%s)"
                cursor.execute(bank_code_sql, (bank_name,))
                bank_code_pk = cursor.lastrowid

            # Bank insertion
            bank_sql = "INSERT INTO bank (suspect_key, bank_account, bank_nickname, bank_code) VALUES (%s, %s, %s, %s);"
            cursor.execute(bank_sql, (suspect_pk, bank_account, bank_nickname, bank_code_pk))
            bank_pk = cursor.lastrowid

            # Case info insertion
            info_sql = "INSERT INTO case_info (user_key, platform_key, bank_key, case_date, case_status) VALUES (%s, %s, %s, %s, 'continue');"
            cursor.execute(info_sql, (user_id, platform_pk, bank_pk, case_date))
            info_pk = cursor.lastrowid

            # Case detail insertion
            detail_sql = "INSERT INTO case_detail (case_key, case_type, case_item, case_price, bank_date, case_content) VALUES (%s, %s, %s, %s, %s, %s);"
            cursor.execute(detail_sql, (info_pk, case_type, case_item, case_price, bank_date, case_content))
            
            db.commit()
            flash('피해사례 등록이 성공적으로 완료되었습니다.', 'success')
            return redirect(url_for('main.index'))
        except pymysql.MySQLError as e:
            db.rollback()
            flash(f"피해사례 등록 중 오류가 발생했습니다: {e}", 'danger')
    elif request.method == 'GET':
        return render_template('case_info.html')


@bp.route('/phishing_info', methods=["POST", "GET"])
def phishing_info():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('main.login'))
    if request.method == 'POST':
        user_id = session['user_id']
        phishing_url = request.form['site_url']
        site_name = request.form['site_name']
        site_type = request.form['case_type']
        site_content = request.form['site_content']
        phishing_count = 0
        current_time = datetime.now()
        phishing_date = current_time.strftime("%Y-%m-%d %H:%M:%S")

        try:
            cursor = db.cursor()
            # Insert into phishing_info table
            phishing_sql = "INSERT INTO phishing_info (user_key, phishing_count, phishing_date, phishing_url) VALUES (%s, %s, %s, %s)"
            cursor.execute(phishing_sql, (user_id, phishing_count, phishing_date, phishing_url))
            phishing_pk = cursor.lastrowid

            # Insert into phishing_detail table (assuming the table is named phishing_detail)
            phishing_detail_sql = "INSERT INTO phishing_detail (phishing_key, site_type, site_name, site_content) VALUES (%s, %s, %s, %s)"
            cursor.execute(phishing_detail_sql, (phishing_pk, site_type, site_name, site_content))

            db.commit()
            flash('피싱사이트 등록이 성공적으로 완료되었습니다.', 'success')
            return redirect(url_for('main.index'))
        except pymysql.MySQLError as e:
            db.rollback()
            flash(f"피싱사이트 등록 중 오류가 발생했습니다: {e}", 'danger')
    elif request.method == 'GET':
        return render_template('phishing_info.html')

@bp.route('/case_list', methods=['GET'])
def case_list():
    case_info = request.args.get('caseInfo', '')

    if not case_info:
        flash('검색어를 입력해주세요.', 'danger')
        return redirect(url_for('main.case_search'))

    try:
        cursor = db.cursor()
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
        cursor = db.cursor()
        sql = """
            SELECT i.case_key, b.bank_account, b.bank_nickname, d.case_type, i.case_date, s.suspect_status, 
                   s.suspect_phone, s.suspect_sex, s.suspect_age, s.suspect_credit, s.suspect_country, 
                   p.platform_name, p.platform_url, d.case_item, d.case_price, d.bank_date, d.case_content,
                   po.police_name, po.police_location, bc.bank_name, s.suspect_key
            FROM case_info i
            JOIN bank b ON i.bank_key = b.bank_key
            JOIN bank_code bc ON b.bank_code = bc.bank_code
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
            'police_location': case[18],
            'bank_name' : case[19]
        }
        print(case[5])
        if case_info['suspect_status'] == 'arrested':
            sql2 = """
                SELECT p.police_name, p.police_location, s.suspect_sex, s.suspect_age, s.suspect_country, s.suspect_credit
                FROM suspects s
                JOIN polices p ON s.police_key = p.police_key
                WHERE s.suspect_key = %s
            """
            cursor.execute(sql2, (case[20]))
            case2 = cursor.fetchone()
            print(case2)
            if not case2:
                print("사례 검거 정보가 없습니다.")
                case2_info = {
                    'police_name': "홍길동",
                    'police_location': "노원",
                    'suspect_sex': "여",
                    'suspect_age': "30",
                    'suspect_country': "한국",
                    'suspect_credit': "3"
                }
            else:
                case2_info = {
                    'police_name': case2[0],
                    'police_location': case2[1],
                    'suspect_sex': case2[2],
                    'suspect_age': case2[3],
                    'suspect_country': case2[4],
                    'suspect_credit': case2[5]
                }

            return render_template('case_detail_arrested.html', case=case_info, case2=case2_info)
        else:
            return render_template('case_detail_unarrested.html', case=case_info)

    except pymysql.MySQLError as e:
        flash(f"상세 조회 중 오류가 발생했습니다: {e}", 'danger')
        return redirect(url_for('main.case_list'))

@bp.route('/phishing_detail', methods=['GET'])
def phishing_detail():
    phishing_key = request.args.get('phishing_key')
    phishing_info = request.args.get('phishingInfo')
    try:
        cursor = db.cursor()
        sql = """
            SELECT pi.phishing_key, pi.phishing_url, pd.site_name, pd.site_type, pd.site_content, pi.phishing_date, pi.phishing_count
            FROM phishing_info pi
            JOIN phishing_detail pd ON pi.phishing_key = pd.phishing_key
            WHERE pi.phishing_url = %s OR pd.site_name = %s OR pi.phishing_key = %s
        """
        cursor.execute(sql, (phishing_info, phishing_info, phishing_key))
        phishing_detail = cursor.fetchone()

        if phishing_detail:
            phishing_data = {
                'phishing_key': phishing_detail[0],
                'site_url': phishing_detail[1],
                'site_name': phishing_detail[2],
                'site_type': phishing_detail[3],
                'site_content': phishing_detail[4],
                'phishing_date': phishing_detail[5],
                'phishing_count': phishing_detail[6]
            }

            # 조회 수 증가
            update_sql = "UPDATE phishing_info SET phishing_count = phishing_count + 1 WHERE phishing_key = %s"
            cursor.execute(update_sql, (phishing_data['phishing_key'],))
            db.commit()

            return render_template('phishing_detail.html', phishing_data=phishing_data)
        else:
            flash('해당 피싱 사이트 정보를 찾을 수 없습니다.', 'danger')
            return redirect(url_for('main.phishing_search'))
    
    except pymysql.MySQLError as e:
        db.rollback()
        flash(f"피싱 사이트 조회 중 오류가 발생했습니다: {e}", 'danger')
        return redirect(url_for('main.phishing_search'))

@bp.route('/case_delete/<int:case_key>', methods=['POST'])
def case_delete(case_key):
    print('사례 삭제 시작')
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('main.login'))

    try:
        cursor = db.cursor()

        # 해당 case_key에 연결된 bank_key, platform_key, suspect_key를 가져옵니다.
        sql_get_keys = """
        SELECT ci.bank_key, ci.platform_key, b.suspect_key
        FROM case_info ci
        JOIN bank b ON ci.bank_key = b.bank_key
        WHERE ci.case_key = %s
        """

        sql_bank_code = """
        SELECT bc.bank_code
        FROM bank_code bc
        JOIN bank b ON bc.bank_code = b.bank_code
        WHERE b.bank_key = %s
        """

        cursor.execute(sql_get_keys, (case_key,))
        result = cursor.fetchone()
        if not result:
            print('해당 사례를 찾을 수 없습니다.', 'danger')
            return redirect(url_for('main.case_search'))

        bank_key, platform_key, suspect_key = result

        cursor.execute(sql_bank_code, (bank_key,))
        bc_result = cursor.fetchone()
        if not bc_result:
            print('해당 뱅크 코드 없음')
            return redirect(url_for('main.case_search'))

        bank_code = bc_result[0]

        # 관련 데이터를 삭제
        sql_delete_case_detail = "DELETE FROM case_detail WHERE case_key = %s"
        sql_delete_case_info = "DELETE FROM case_info WHERE case_key = %s"
        sql_delete_bank = "DELETE FROM bank WHERE bank_key = %s"
        sql_delete_platform = "DELETE FROM platform WHERE platform_key = %s"
        sql_delete_suspect = "DELETE FROM suspects WHERE suspect_key = %s"

        cursor.execute(sql_delete_case_detail, (case_key,))
        cursor.execute(sql_delete_case_info, (case_key,))
        cursor.execute(sql_delete_bank, (bank_key,))
        cursor.execute(sql_delete_platform, (platform_key,))
        cursor.execute(sql_delete_suspect, (suspect_key,))

        sql_bank_code = "SELECT bank_key FROM bank WHERE bank_code = %s"
        cursor.execute(sql_bank_code, (bank_code))
        is_bc = cursor.fetchone()
        if not is_bc:
            sql_delete_bank_code = "DELETE FROM bank_code WHERE bank_code = %s"
            cursor.execute(sql_delete_bank_code, (bank_code,))

        db.commit()
        print('사례가 성공적으로 삭제되었습니다.', 'success')
    except pymysql.MySQLError as e:
        db.rollback()
        print(f"사례 삭제 중 오류가 발생했습니다: {e}", 'danger')
    
    return redirect(url_for('main.case_search'))


@bp.route('/phishing_delete/<int:phishing_key>', methods=['POST'])
def phishing_delete(phishing_key):
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('main.login'))
    try:
        cursor = db.cursor()
        # 피싱 사이트 관련 데이터를 삭제
        sql_delete_phishing_detail = "DELETE FROM phishing_detail WHERE phishing_key = %s"
        sql_delete_phishing_info = "DELETE FROM phishing_info WHERE phishing_key = %s"
        
        cursor.execute(sql_delete_phishing_detail, (phishing_key,))
        cursor.execute(sql_delete_phishing_info, (phishing_key,))
        
        db.commit()
        print('피싱 사이트가 성공적으로 삭제되었습니다.', 'success')
    except pymysql.MySQLError as e:
        db.rollback()
        print(f"피싱 사이트 삭제 중 오류가 발생했습니다: {e}", 'danger')

    return redirect(url_for('main.phishing_search'))
