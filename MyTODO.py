from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import sys

# 데이터베이스 경로 설정
def get_db_path():
    """데이터베이스 경로를 반환합니다."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "todo.db")
    return f'sqlite:///{db_path}'

# Flask 및 DB 설정
app = Flask('MyTODO')
app.config['SECRET_KEY'] = os.urandom(24).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_path()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 할 일 모델
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

# 메인 대시보드
@app.route('/')
def dashboard():
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
    
    return render_template('dashboard.html', todos=todos, filter_type=filter_type, total_todos=total_todos, completed_todos=completed_todos, pending_todos=pending_todos)

# 할 일 관리
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

if __name__ == '__main__':
    # PyInstaller 호환성을 위한 템플릿 폴더 설정
    if getattr(sys, 'frozen', False):
        template_folder = os.path.join(sys._MEIPASS, 'templates')
        app.template_folder = template_folder
    
    with app.app_context():
        db.create_all()
    
    # 서버 시작
    host = '127.0.0.1'
    port = 5002
    
    print("="*50)
    print("MyTODO 할 일 목록 애플리케이션")
    print("="*50)
    print(f"서버가 시작되었습니다! 브라우저에서 http://{host}:{port} 으로 접속하세요")
    print("종료하려면 Ctrl+C를 누르세요")
    print("="*50)
    
    try:
        app.run(debug=False, host=host, port=port, use_reloader=False)
    except KeyboardInterrupt:
        print("\n서버가 종료되었습니다.")
    except Exception as e:
        print(f"\n서버 실행 중 오류가 발생했습니다: {e}")
        input("엔터를 눌러 종료합니다...")
