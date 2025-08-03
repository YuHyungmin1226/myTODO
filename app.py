from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import sys
import platform

# 공유 DB 경로 설정
def get_shared_db_path():
    """Windows와 macOS 간에 공유할 DB 경로를 반환합니다."""
    home_dir = os.path.expanduser("~")
    
    # 플랫폼별 공유 폴더 설정
    if platform.system() == "Windows":
        # Windows: 사용자 홈 디렉토리 내 MyTODO 폴더
        shared_dir = os.path.join(home_dir, "MyTODO")
    else:
        # macOS: 사용자 홈 디렉토리 내 MyTODO 폴더
        shared_dir = os.path.join(home_dir, "MyTODO")
    
    # 공유 폴더가 없으면 생성
    if not os.path.exists(shared_dir):
        try:
            os.makedirs(shared_dir)
            print(f"공유 폴더가 생성되었습니다: {shared_dir}")
        except Exception as e:
            print(f"공유 폴더 생성 실패: {e}")
            # 폴더 생성 실패 시 현재 디렉토리 사용
            return 'sqlite:///todo.db'
    
    db_path = os.path.join(shared_dir, "todo.db")
    return f'sqlite:///{db_path}'

# Flask 및 DB 설정
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = get_shared_db_path()
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
    return User.query.get(int(user_id))

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
    
    try:
        # pkill을 사용하여 MyTODO 프로세스 종료
        result = subprocess.run(['pkill', '-f', 'MyTODO'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("🔄 기존 MyTODO 프로세스가 종료되었습니다.")
            import time
            time.sleep(1)  # 프로세스 종료 대기
        else:
            print("실행 중인 MyTODO 프로세스가 없습니다.")
            
    except Exception as e:
        print(f"기존 프로세스 종료를 시도했지만 실패했습니다: {e}")

def find_available_port(start_port=5001, end_port=5010):
    """사용 가능한 포트를 찾습니다."""
    import socket
    
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return None

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    if getattr(sys, 'frozen', False):
        template_folder = os.path.join(sys._MEIPASS, 'templates')
        app.template_folder = template_folder
    
    # 기존 MyTODO 프로세스 종료
    kill_existing_processes()
    
    # 사용 가능한 포트 찾기
    port = find_available_port()
    if port is None:
        print("오류: 5001-5010 포트가 모두 사용 중입니다.")
        print("다른 프로그램을 종료하고 다시 시도하세요.")
        sys.exit(1)
    
    print("="*50)
    print("MyTODO 할 일 목록 애플리케이션")
    print("="*50)
    print("서버가 시작되었습니다!")
    print(f"브라우저에서 http://localhost:{port} 으로 접속하세요")
    print("종료하려면 Ctrl+C를 누르세요")
    print("="*50)
    
    try:
        # 개발 서버 경고 메시지 숨기기
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        
        app.run(debug=False, host='127.0.0.1', port=port, use_reloader=False)
    except KeyboardInterrupt:
        print("\n서버가 종료되었습니다.") 