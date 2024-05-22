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

@bp.route('/case_info')
def case_info():
    return render_template('case_info.html')

@bp.route('/phishing_info')
def phishing_info():
    return render_template('phishing_info.html')
