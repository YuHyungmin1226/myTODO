# -*- coding: utf-8 -*-
"""
MyTODO - 할 일 목록 관리 애플리케이션
UTF-8 인코딩으로 작성되었습니다.
"""

import sys
import locale
import codecs

# 시스템 인코딩 설정
if sys.platform.startswith('darwin'):  # macOS
    try:
        locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        except locale.Error:
            pass
elif sys.platform.startswith('win'):  # Windows
    try:
        locale.setlocale(locale.LC_ALL, 'Korean_Korea.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')
        except locale.Error:
            try:
                locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            except locale.Error:
                pass

# 표준 출력/입력 인코딩 설정
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import text
from datetime import datetime, timezone, timedelta
import os
import logging
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash

# 로깅 설정
if os.getenv('RAILWAY_ENVIRONMENT'):
    # Railway 환경에서는 파일 로깅 제외
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
else:
    # 로컬 환경에서는 파일과 콘솔 모두 로깅
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('mytodo.log', encoding='utf-8')
        ]
    )
logger = logging.getLogger(__name__)

# 한국 시간대 설정
KST = timezone(timedelta(hours=9))

# 데이터베이스 경로 설정
def get_db_path():
    """데이터베이스 경로를 반환합니다."""
    # Railway나 다른 클라우드 환경에서는 DATABASE_URL 사용
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        # Railway PostgreSQL URL을 SQLAlchemy 형식으로 변환
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return database_url
    
    # 로컬 환경에서는 SQLite 사용
    if getattr(sys, 'frozen', False):
        # PyInstaller로 빌드된 경우
        current_dir = os.path.dirname(sys.executable)
    else:
        # 일반 Python 실행의 경우
        current_dir = os.path.dirname(os.path.abspath(__file__))
    
    db_path = os.path.join(current_dir, "todo.db")
    return f'sqlite:///{db_path}'

# Flask 및 DB 설정
app = Flask('MyTODO')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_path()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 인코딩 설정
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Jinja2 템플릿 인코딩 설정
app.jinja_env.default_encoding = 'utf-8'
app.jinja_env.auto_reload = True

db = SQLAlchemy(app)

# Flask-Login 설정
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '이 페이지에 접근하려면 로그인이 필요합니다.'
login_manager.login_message_category = 'info'

# 사용자 모델
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(KST))
    
    # 사용자의 할 일 목록
    todos = db.relationship('Todo', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 할 일 모델
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(KST))
    completed_at = db.Column(db.DateTime, nullable=True)


class TodoForm(FlaskForm):
    content = StringField('할 일', validators=[DataRequired(), Length(min=1, max=200)])

class LoginForm(FlaskForm):
    username = StringField('사용자명', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('사용자명', validators=[DataRequired(), Length(min=3, max=80)])
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('비밀번호 확인', validators=[DataRequired(), EqualTo('password')])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 메인 대시보드
@app.route('/')
@login_required
def dashboard():
    form = TodoForm()
    filter_type = request.args.get('filter', 'all')
    query = Todo.query.filter_by(user_id=current_user.id)
    if filter_type == 'completed':
        query = query.filter_by(completed=True)
    elif filter_type == 'pending':
        query = query.filter_by(completed=False)
    todos = query.order_by(Todo.created_at.desc()).all()
    
    # 통계 계산 (현재 사용자의 할 일만)
    all_todos = Todo.query.filter_by(user_id=current_user.id).all()
    total_todos = len(all_todos)
    completed_todos = sum(1 for t in all_todos if t.completed)
    pending_todos = total_todos - completed_todos
    
    return render_template('dashboard.html', todos=todos, form=form, filter_type=filter_type, total_todos=total_todos, completed_todos=completed_todos, pending_todos=pending_todos)

# 할 일 관리
@app.route('/add_todo', methods=['POST'])
@login_required
def add_todo():
    form = TodoForm()
    if form.validate_on_submit():
        try:
            content = form.content.data
            todo = Todo(content=content, user_id=current_user.id)
            db.session.add(todo)
            db.session.commit()
            flash('할 일이 추가되었습니다.', 'success')
            logger.info(f"새 할 일 추가: {content[:50]}... (사용자: {current_user.username})")
        except Exception as e:
            db.session.rollback()
            logger.error(f"할 일 추가 중 오류: {e}")
            flash('할 일 추가 중 오류가 발생했습니다.', 'error')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{error}', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/edit_todo/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def edit_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first_or_404()
    form = TodoForm(obj=todo)
    if form.validate_on_submit():
        try:
            todo.content = form.content.data
            db.session.commit()
            flash('할 일이 수정되었습니다.', 'success')
            logger.info(f"할 일 수정: ID {todo_id}, 내용: {todo.content[:50]}... (사용자: {current_user.username})")
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"할 일 수정 중 오류: {e}")
            flash('할 일 수정 중 오류가 발생했습니다.', 'error')
    
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{error}', 'error')
    return render_template('edit_todo.html', todo=todo, form=form)

@app.route('/complete_todo/<int:todo_id>')
@login_required
def complete_todo(todo_id):
    try:
        todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first_or_404()
        todo.completed = True
        todo.completed_at = datetime.now(KST)
        db.session.commit()
        flash('할 일이 완료되었습니다.', 'success')
        logger.info(f"할 일 완료: ID {todo_id} (사용자: {current_user.username})")
        return redirect(url_for('dashboard'))
    except Exception as e:
        db.session.rollback()
        logger.error(f"할 일 완료 처리 중 오류: {e}")
        flash('할 일 완료 처리 중 오류가 발생했습니다.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/uncomplete_todo/<int:todo_id>')
@login_required
def uncomplete_todo(todo_id):
    try:
        todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first_or_404()
        todo.completed = False
        todo.completed_at = None
        db.session.commit()
        flash('할 일이 미완료로 변경되었습니다.', 'success')
        logger.info(f"할 일 미완료 변경: ID {todo_id} (사용자: {current_user.username})")
        return redirect(url_for('dashboard'))
    except Exception as e:
        db.session.rollback()
        logger.error(f"할 일 미완료 변경 중 오류: {e}")
        flash('할 일 미완료 변경 중 오류가 발생했습니다.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/delete_todo/<int:todo_id>')
@login_required
def delete_todo(todo_id):
    try:
        todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first_or_404()
        db.session.delete(todo)
        db.session.commit()
        flash('할 일이 삭제되었습니다.', 'success')
        logger.info(f"할 일 삭제: ID {todo_id} (사용자: {current_user.username})")
        return redirect(url_for('dashboard'))
    except Exception as e:
        db.session.rollback()
        logger.error(f"할 일 삭제 중 오류: {e}")
        flash('할 일 삭제 중 오류가 발생했습니다.', 'error')
        return redirect(url_for('dashboard'))

# 인증 관련 라우트
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'환영합니다, {user.username}님!', 'success')
            logger.info(f"사용자 로그인: {user.username}")
            return redirect(url_for('dashboard'))
        else:
            flash('사용자명 또는 비밀번호가 올바르지 않습니다.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # 사용자명 중복 확인
        if User.query.filter_by(username=form.username.data).first():
            flash('이미 사용 중인 사용자명입니다.', 'error')
            return render_template('register.html', form=form)
        
        # 이메일 중복 확인
        if User.query.filter_by(email=form.email.data).first():
            flash('이미 사용 중인 이메일입니다.', 'error')
            return render_template('register.html', form=form)
        
        try:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            
            login_user(user)
            flash(f'회원가입이 완료되었습니다! 환영합니다, {user.username}님!', 'success')
            logger.info(f"새 사용자 등록: {user.username} ({user.email})")
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"회원가입 중 오류: {e}")
            flash('회원가입 중 오류가 발생했습니다.', 'error')
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    flash(f'{username}님, 로그아웃되었습니다.', 'info')
    logger.info(f"사용자 로그아웃: {username}")
    return redirect(url_for('login'))

def find_available_port(start_port=5002, max_attempts=10):
    """사용 가능한 포트를 찾습니다."""
    import socket
    
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return None

def get_local_ip():
    """현재 시스템의 로컬 IP 주소를 반환합니다."""
    import socket
    try:
        # 호스트 이름을 통해 IP 주소 가져오기
        ip_address = socket.gethostbyname(socket.gethostname())
        # 127.0.0.1이거나, gethostbyname이 실패한 경우
        if ip_address == "127.0.0.1":
            # 모든 네트워크 인터페이스를 확인하여 127.0.0.1이 아닌 IP 찾기
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80)) # 외부 서버에 연결 시도 (실제 데이터 전송 없음)
            ip_address = s.getsockname()[0]
            s.close()
        return ip_address
    except Exception:
        return "127.0.0.1"

def check_database_connection():
    """데이터베이스 연결 상태를 확인합니다."""
    try:
        # 간단한 쿼리로 연결 테스트
        db.session.execute(text('SELECT 1'))
        db.session.commit()
        return True
    except Exception as e:
        logger.error(f"데이터베이스 연결 확인 실패: {e}")
        return False

if __name__ == '__main__':
    # PyInstaller 호환성을 위한 템플릿 폴더 설정
    if getattr(sys, 'frozen', False):
        template_folder = os.path.join(sys._MEIPASS, 'templates')
        app.template_folder = template_folder
    
    with app.app_context():
        try:
            db.create_all()
            logger.info("데이터베이스 테이블이 생성되었습니다.")
            
            # 데이터베이스 연결 확인
            if not check_database_connection():
                raise Exception("데이터베이스 연결에 실패했습니다.")
                
        except Exception as e:
            logger.error(f"데이터베이스 초기화 중 오류: {e}")
            print(f"데이터베이스 초기화 중 오류가 발생했습니다: {e}")
            input("엔터를 눌러 종료합니다...")
            sys.exit(1)
    
    # 포트 설정 (Railway 환경 지원)
    port = int(os.getenv('PORT', 5002))
    
    # Railway 환경에서는 포트 검색 불필요
    if not os.getenv('RAILWAY_ENVIRONMENT'):
        # 로컬 환경에서만 포트 검색
        port = find_available_port(5002)
        if port is None:
            logger.error("❌ 사용 가능한 포트를 찾을 수 없습니다. 다른 프로그램을 종료하고 다시 시도해주세요.")
            input("엔터를 눌러 종료합니다...")
            sys.exit(1)
    
    host = '0.0.0.0'
    
    # Railway 환경이 아닐 때만 로컬 IP 표시
    if not os.getenv('RAILWAY_ENVIRONMENT'):
        local_ip = get_local_ip()

    print("="*50)
    print("MyTODO 할 일 목록 애플리케이션")
    print("="*50)
    print(f"서버가 시작되었습니다!")
    
    if os.getenv('RAILWAY_ENVIRONMENT'):
        print(f"Railway 환경에서 실행 중")
    else:
        print(f"로컬:   http://127.0.0.1:{port}")
        if local_ip != '127.0.0.1':
            print(f"네트워크: http://{local_ip}:{port}")
    
    print("종료하려면 Ctrl+C를 누르세요")
    print("="*50)
    
    try:
        logger.info(f"서버 시작: {host}:{port}")
        app.run(debug=False, host=host, port=port, use_reloader=False)
    except KeyboardInterrupt:
        logger.info("사용자에 의해 서버가 종료되었습니다.")
        print("서버가 종료되었습니다.")
    except Exception as e:
        logger.error(f"서버 실행 중 오류가 발생했습니다: {e}")
        print(f"서버 실행 중 오류가 발생했습니다: {e}")
        input("엔터를 눌러 종료합니다...")
