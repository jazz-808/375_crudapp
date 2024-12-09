from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

# Function to connect to the database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database with a table if it doesn't exist
def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)
        db.commit()

# Routes
@app.route('/')
def index():
    db = get_db()
    tasks = db.execute('SELECT * FROM tasks').fetchall()
    return render_template('index.html', tasks=tasks)

# Create task (AJAX request)
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    db = get_db()
    db.execute('INSERT INTO tasks (title, description) VALUES (?, ?)', (title, description))
    db.commit()
    return redirect(url_for('index'))

# Edit task (GET and POST request)
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    db = get_db()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        # Update the task in the database
        db.execute('UPDATE tasks SET title = ?, description = ? WHERE id = ?', (title, description, task_id))
        db.commit()

        return jsonify({'status': 'success'})

    # For GET request, render the edit page with the current task data
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    return render_template('edit.html', task=task)



# Delete task (AJAX request)
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    db.commit()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

