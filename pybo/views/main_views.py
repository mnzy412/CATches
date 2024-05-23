from flask import Blueprint, render_template

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return 'Hello, catches'


@bp.route('/')
def index():
    return render_template('home.html')


@bp.route('/register')
def register():
    return render_template('user_register.html')

@bp.route('/login')
def login():
    return render_template('user_login.html')

@bp.route('/mypage')
def mypage():
    return render_template('mypage.html')

@bp.route('/mypage/case')
def mypage_case():
    return render_template('mypage_case.html')

@bp.route('/mypage/pishing')
def mypage_pishing():
    return render_template('mypage_pishing.html')

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
