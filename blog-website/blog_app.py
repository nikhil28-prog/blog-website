from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3

app = Flask(__name__)

# Create database and table
conn = sqlite3.connect("blog.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT
)
""")
conn.commit()
conn.close()

# HTML Template
html_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple Blog</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            padding: 20px;
        }
        .container {
            max-width: 700px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }
        input, textarea {
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            border-radius: 6px;
            border: 1px solid #ccc;
        }
        button {
            padding: 10px 15px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        .post {
            border-bottom: 1px solid #ddd;
            margin-bottom: 15px;
            padding-bottom: 10px;
        }
        a {
            margin-right: 10px;
        }
        .edit-box {
            background: #fff3cd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>📝 Simple Blog Website</h2>

        {% if edit_post %}
        <div class="edit-box">
            <h3>Edit Post</h3>
            <form method="post" action="/edit/{{ edit_post[0] }}">
                <input type="text" name="title" value="{{ edit_post[1] }}" required>
                <textarea name="content" required>{{ edit_post[2] }}</textarea>
                <button type="submit">Update Post</button>
            </form>
        </div>
        {% endif %}

        <form method="post" action="/add">
            <input type="text" name="title" placeholder="Post Title" required>
            <textarea name="content" placeholder="Write your post..." required></textarea>
            <button type="submit">Add Post</button>
        </form>

        <hr>

        {% for post in posts %}
        <div class="post">
            <h3>{{ post[1] }}</h3>
            <p>{{ post[2] }}</p>
            <a href="/edit/{{ post[0] }}">Edit</a>
            <a href="/delete/{{ post[0] }}">Delete</a>
        </div>
        {% endfor %}

    </div>
</body>
</html>
"""

@app.route('/')
def home():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = cursor.fetchall()
    conn.close()
    return render_template_string(html_page, posts=posts)

@app.route('/add', methods=['POST'])
def add_post():
    title = request.form['title']
    content = request.form['content']

    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute("UPDATE posts SET title=?, content=? WHERE id=?", (title, content, id))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))

    cursor.execute("SELECT * FROM posts WHERE id=?", (id,))
    post = cursor.fetchone()

    cursor.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = cursor.fetchall()
    conn.close()

    return render_template_string(html_page, posts=posts, edit_post=post)

@app.route('/delete/<int:id>')
def delete_post(id):
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
