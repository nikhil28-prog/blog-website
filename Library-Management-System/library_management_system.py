from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3

app = Flask(__name__)

def connect_db():
    return sqlite3.connect("library.db")

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

create_table()

@app.route("/")
def index():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()

    html = """
    <h2>Library Management System</h2>
    <a href='/add'>Add Book</a>
    <table border=1>
        <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Author</th>
            <th>Status</th>
            <th>Actions</th>
        </tr>
        {% for book in books %}
        <tr>
            <td>{{book[0]}}</td>
            <td>{{book[1]}}</td>
            <td>{{book[2]}}</td>
            <td>{{book[3]}}</td>
            <td>
                <a href='/issue/{{book[0]}}'>Issue</a>
                <a href='/return/{{book[0]}}'>Return</a>
                <a href='/delete/{{book[0]}}'>Delete</a>
            </td>
        </tr>
        {% endfor %}
    </table>
    """
    return render_template_string(html, books=books)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, status) VALUES (?, ?, ?)",
            (title, author, "Available")
        )
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    html = """
    <h2>Add Book</h2>
    <form method="POST">
        Title: <input type="text" name="title"><br><br>
        Author: <input type="text" name="author"><br><br>
        <input type="submit" value="Add Book">
    </form>
    """
    return render_template_string(html)

@app.route("/issue/<int:id>")
def issue_book(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE books SET status='Issued' WHERE id=?",
        (id,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

@app.route("/return/<int:id>")
def return_book(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE books SET status='Available' WHERE id=?",
        (id,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete_book(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM books WHERE id=?",
        (id,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)