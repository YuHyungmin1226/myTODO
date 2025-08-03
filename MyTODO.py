from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import sys
import platform

# 공유 DB 경로 설정




def get_db_path():
    """데이터베이스 경로를 반환합니다."""
    # 실행 파일과 같은 디렉토리에 DB 저장
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "todo.db")
    return f'sqlite:///{db_path}'

# Flask 및 DB 설정
app = Flask('MyTODO')
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_path()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# 사용자 모델
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    todos = db.relationship('Todo', backref='user', lazy=True)

# 할 일 모델
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# 인증 라우트
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('비밀번호가 일치하지 않습니다.', 'error')
            return render_template('register.html')
        if User.query.filter_by(username=username).first():
            flash('이미 존재하는 사용자명입니다.', 'error')
            return render_template('register.html')
        if User.query.filter_by(email=email).first():
            flash('이미 존재하는 이메일입니다.', 'error')
            return render_template('register.html')
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        flash('회원가입이 완료되었습니다. 로그인해주세요.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('로그인되었습니다.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('사용자명 또는 비밀번호가 올바르지 않습니다.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('로그아웃되었습니다.', 'success')
    return redirect(url_for('login'))

# 대시보드 및 할 일 관리
@app.route('/dashboard')
@login_required
def dashboard():
    filter_type = request.args.get('filter', 'all')
    query = Todo.query.filter_by(user_id=current_user.id)
    if filter_type == 'completed':
        query = query.filter_by(completed=True)
    elif filter_type == 'pending':
        query = query.filter_by(completed=False)
    todos = query.order_by(Todo.created_at.desc()).all()
    # 통계 한 번에 계산
    all_todos = Todo.query.filter_by(user_id=current_user.id).all()
    total_todos = len(all_todos)
    completed_todos = sum(1 for t in all_todos if t.completed)
    pending_todos = total_todos - completed_todos
    return render_template('dashboard.html', todos=todos, filter_type=filter_type, total_todos=total_todos, completed_todos=completed_todos, pending_todos=pending_todos)

@app.route('/add_todo', methods=['POST'])
@login_required
def add_todo():
    content = request.form['content'].strip()
    if content:
        todo = Todo(content=content, user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
        flash('할 일이 추가되었습니다.', 'success')
    else:
        flash('할 일 내용을 입력해주세요.', 'error')
    return redirect(url_for('dashboard'))

# 수정 폼(GET) + 처리(POST) 분리
@app.route('/edit_todo/<int:todo_id>', methods=['GET'])
@login_required
def edit_todo_form(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id != current_user.id:
        flash('권한이 없습니다.', 'error')
        return redirect(url_for('dashboard'))
    return render_template('edit_todo.html', todo=todo)

@app.route('/edit_todo/<int:todo_id>', methods=['POST'])
@login_required
def edit_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id != current_user.id:
        flash('권한이 없습니다.', 'error')
        return redirect(url_for('dashboard'))
    content = request.form['content'].strip()
    if content:
        todo.content = content
        db.session.commit()
        flash('할 일이 수정되었습니다.', 'success')
    else:
        flash('할 일 내용을 입력해주세요.', 'error')
    return redirect(url_for('dashboard'))

@app.route('/complete_todo/<int:todo_id>')
@login_required
def complete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id == current_user.id:
        todo.completed = True
        todo.completed_at = datetime.utcnow()
        db.session.commit()
        flash('할 일이 완료되었습니다.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/uncomplete_todo/<int:todo_id>')
@login_required
def uncomplete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id == current_user.id:
        todo.completed = False
        todo.completed_at = None
        db.session.commit()
        flash('할 일이 미완료로 변경되었습니다.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete_todo/<int:todo_id>')
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id == current_user.id:
        db.session.delete(todo)
        db.session.commit()
        flash('할 일이 삭제되었습니다.', 'success')
    return redirect(url_for('dashboard'))

def kill_existing_processes():
    """기존에 실행 중인 MyTODO 프로세스를 종료합니다."""
    import subprocess
    import os
    import platform
    
    try:
        system = platform.system()
        
        if system == "Windows":
            # Windows에서는 taskkill 사용
            result = subprocess.run(['taskkill', '/f', '/im', 'MyTODO.exe'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("기존 MyTODO.exe 프로세스가 종료되었습니다.")
            else:
                print("실행 중인 MyTODO.exe 프로세스가 없습니다.")
            
            # MyTODO 관련 Python 프로세스만 종료 (현재 프로세스는 제외)
            current_pid = os.getpid()
            result = subprocess.run(['wmic', 'process', 'where', f'name="python.exe" and commandline like "%MyTODO.py%" and processid!={current_pid}', 'call', 'terminate'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("기존 MyTODO Python 프로세스가 종료되었습니다.")
            else:
                print("실행 중인 MyTODO Python 프로세스가 없습니다.")
        else:
            # macOS/Linux에서는 pkill 사용
            result = subprocess.run(['pkill', '-f', 'MyTODO'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("기존 MyTODO 프로세스가 종료되었습니다.")
            else:
                print("실행 중인 MyTODO 프로세스가 없습니다.")
        
        import time
        time.sleep(2)  # 프로세스 종료 대기 시간 증가
            
    except Exception as e:
        print(f"기존 프로세스 종료를 시도했지만 실패했습니다: {e}")



if __name__ == '__main__':
    import argparse
    
    # 명령행 인수 파싱
    parser = argparse.ArgumentParser(description='MyTODO 할 일 목록 애플리케이션')
    parser.add_argument('--host', default='127.0.0.1', help='호스트 주소 (기본값: 127.0.0.1)')
    args = parser.parse_args()
    
    with app.app_context():
        db.create_all()
    if getattr(sys, 'frozen', False):
        template_folder = os.path.join(sys._MEIPASS, 'templates')
        app.template_folder = template_folder
    
    # 기존 MyTODO 프로세스 종료
    kill_existing_processes()
    
    # 5002 포트 고정 사용
    port = 5002
    print(f"포트 5002를 사용합니다.")
    
    print("="*50)
    print("MyTODO 할 일 목록 애플리케이션")
    print("="*50)
    print("서버가 시작되었습니다!")
    print(f"브라우저에서 http://{args.host}:{port} 으로 접속하세요")
    print("종료하려면 Ctrl+C를 누르세요")
    print("="*50)
    
    try:
        # 개발 서버 경고 메시지 숨기기
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        
        app.run(debug=False, host=args.host, port=port, use_reloader=False)
    except KeyboardInterrupt:
        print("\n서버가 종료되었습니다.")
    except Exception as e:
        print(f"\n서버 실행 중 오류가 발생했습니다: {e}")
        print("포트 5002가 이미 사용 중일 수 있습니다.")
        sys.exit(1) 