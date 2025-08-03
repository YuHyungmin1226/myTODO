from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
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
app.config['SECRET_KEY'] = os.urandom(24).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_path()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 할 일 모델 (사용자 연결 제거)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

# 메인 대시보드 (로그인 불필요)
@app.route('/')
def dashboard():
    filter_type = request.args.get('filter', 'all')
    query = Todo.query
    if filter_type == 'completed':
        query = query.filter_by(completed=True)
    elif filter_type == 'pending':
        query = query.filter_by(completed=False)
    todos = query.order_by(Todo.created_at.desc()).all()
    
    # 통계 한 번에 계산
    all_todos = Todo.query.all()
    total_todos = len(all_todos)
    completed_todos = sum(1 for t in all_todos if t.completed)
    pending_todos = total_todos - completed_todos
    
    return render_template('dashboard.html', todos=todos, filter_type=filter_type, total_todos=total_todos, completed_todos=completed_todos, pending_todos=pending_todos)

# 할 일 관리 (로그인 불필요)
@app.route('/add_todo', methods=['POST'])
def add_todo():
    content = request.form['content'].strip()
    if content:
        todo = Todo(content=content)
        db.session.add(todo)
        db.session.commit()
        flash('할 일이 추가되었습니다.', 'success')
    else:
        flash('할 일 내용을 입력해주세요.', 'error')
    return redirect(url_for('dashboard'))

@app.route('/edit_todo/<int:todo_id>', methods=['GET'])
def edit_todo_form(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    return render_template('edit_todo.html', todo=todo)

@app.route('/edit_todo/<int:todo_id>', methods=['POST'])
def edit_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    content = request.form['content'].strip()
    if content:
        todo.content = content
        db.session.commit()
        flash('할 일이 수정되었습니다.', 'success')
    else:
        flash('할 일 내용을 입력해주세요.', 'error')
    return redirect(url_for('dashboard'))

@app.route('/complete_todo/<int:todo_id>')
def complete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.completed = True
    todo.completed_at = datetime.utcnow()
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
    with app.app_context():
        db.create_all()
    if getattr(sys, 'frozen', False):
        template_folder = os.path.join(sys._MEIPASS, 'templates')
        app.template_folder = template_folder
    
    # 기존 MyTODO 프로세스 종료
    kill_existing_processes()
    
    # 고정 호스트 및 포트 사용
    host = '127.0.0.1'
    port = 5002
    print(f"포트 {port}를 사용합니다.")
    
    print("="*50)
    print("MyTODO 할 일 목록 애플리케이션")
    print("="*50)
    print(f"서버가 시작되었습니다! 브라우저에서 http://{host}:{port} 으로 접속하세요")
    print("종료하려면 Ctrl+C를 누르세요")
    print("="*50)
    
    try:
        # 개발 서버 경고 메시지 숨기기
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        app.run(debug=False, host=host, port=port, use_reloader=False)
    except KeyboardInterrupt:
        print("
서버가 종료되었습니다.")
    except OSError as e:
        if hasattr(e, 'errno') and e.errno in (98, 10048):  # 98: Linux/macOS, 10048: Windows
            print(f"
[오류] 포트 {port}가 이미 사용 중입니다.")
            print("다른 MyTODO 인스턴스가 실행 중이거나, 해당 포트를 사용하는 다른 프로그램이 있습니다.")
            print("기존 프로세스를 종료하거나 다른 포트를 사용하세요.")
            input("엔터를 눌러 종료합니다...")
        else:
            print(f"
서버 실행 중 오류가 발생했습니다: {e}")
            input("엔터를 눌러 종료합니다...")
        sys.exit(1)
    except Exception as e:
        print(f"
서버 실행 중 오류가 발생했습니다: {e}")
        input("엔터를 눌러 종료합니다...")
        sys.exit(1)
