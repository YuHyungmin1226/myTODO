from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone, timedelta
import os
import sys
import logging
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

# 한국 시간대 설정
KST = timezone(timedelta(hours=9))

# 데이터베이스 경로 설정
def get_db_path():
    """데이터베이스 경로를 반환합니다."""
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
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24).hex())
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_path()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 할 일 모델
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(KST))
    completed_at = db.Column(db.DateTime, nullable=True)


class TodoForm(FlaskForm):
    content = StringField('할 일', validators=[DataRequired(), Length(min=1, max=200)])

# 메인 대시보드
@app.route('/')
def dashboard():
    form = TodoForm()
    filter_type = request.args.get('filter', 'all')
    query = Todo.query
    if filter_type == 'completed':
        query = query.filter_by(completed=True)
    elif filter_type == 'pending':
        query = query.filter_by(completed=False)
    todos = query.order_by(Todo.created_at.desc()).all()
    
    # 통계 계산
    all_todos = Todo.query.all()
    total_todos = len(all_todos)
    completed_todos = sum(1 for t in all_todos if t.completed)
    pending_todos = total_todos - completed_todos
    
    return render_template('dashboard.html', todos=todos, form=form, filter_type=filter_type, total_todos=total_todos, completed_todos=completed_todos, pending_todos=pending_todos)

# 할 일 관리
@app.route('/add_todo', methods=['POST'])
def add_todo():
    form = TodoForm()
    if form.validate_on_submit():
        content = form.content.data
        todo = Todo(content=content)
        db.session.add(todo)
        db.session.commit()
        flash('할 일이 추가되었습니다.', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{error}', 'error')
    return redirect(url_for('dashboard'))

@app.route('/edit_todo/<int:todo_id>', methods=['GET'])
def edit_todo_form(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    form = TodoForm(obj=todo)
    return render_template('edit_todo.html', todo=todo, form=form)

@app.route('/edit_todo/<int:todo_id>', methods=['POST'])
def edit_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    form = TodoForm()
    if form.validate_on_submit():
        todo.content = form.content.data
        db.session.commit()
        flash('할 일이 수정되었습니다.', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{error}', 'error')
    return redirect(url_for('dashboard'))

@app.route('/complete_todo/<int:todo_id>')
def complete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.completed = True
    todo.completed_at = datetime.now(KST)
    db.session.commit()
    flash('할 일이 완료되었습니다.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/uncomplete_todo/<int:todo_id>')
def uncomplete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.completed = False
    todo.completed_at = None
    db.session.commit()
    flash('할 일이 미완료로 변경되었습니다.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete_todo/<int:todo_id>')
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash('할 일이 삭제되었습니다.', 'success')
    return redirect(url_for('dashboard'))

def find_available_port(start_port=5002, max_attempts=10):
    """사용 가능한 포트를 찾습니다."""
    import socket

def get_local_ip():
    """현재 시스템의 로컬 IP 주소를 반환합니다."""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception:
        return "127.0.0.1"
    
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return None

if __name__ == '__main__':
    # PyInstaller 호환성을 위한 템플릿 폴더 설정
    if getattr(sys, 'frozen', False):
        template_folder = os.path.join(sys._MEIPASS, 'templates')
        app.template_folder = template_folder
    
    with app.app_context():
        db.create_all()
    
    # 사용 가능한 포트 찾기
    host = '127.0.0.1'
    port = find_available_port(5002)
    local_ip = get_local_ip()
    
    if port is None:
        app.logger.error("❌ 사용 가능한 포트를 찾을 수 없습니다. 다른 프로그램을 종료하고 다시 시도해주세요.")
        input("엔터를 눌러 종료합니다...")
        sys.exit(1)
    
    app.logger.info("="*50)
    app.logger.info("MyTODO 할 일 목록 애플리케이션")
    app.logger.info("="*50)
    app.logger.info(f"서버가 시작되었습니다!")
    app.logger.info(f"로컬:   http://{host}:{port}")
    if local_ip != '127.0.0.1':
        app.logger.info(f"네트워크: http://{local_ip}:{port}")
    app.logger.info("종료하려면 Ctrl+C를 누르세요")
    app.logger.info("="*50)
    
    try:
        app.run(debug=False, host=host, port=port, use_reloader=False)
    except KeyboardInterrupt:
        app.logger.info("\n서버가 종료되었습니다.")
    except Exception as e:
        app.logger.error(f"\n서버 실행 중 오류가 발생했습니다: {e}")
        input("엔터를 눌러 종료합니다...")
