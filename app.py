from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_NAME = "portfolio.db"

# ------------------ DATABASE INITIALIZATION ------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create projects table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            image TEXT NOT NULL
        )
    """)
    
    # Create messages table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

# Run DB init at startup
init_db()


# ------------------ ROUTES ------------------
@app.route("/")
def home():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, image FROM projects")
    projects = cursor.fetchall()
    conn.close()
    return render_template("index.html", projects=projects)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        image = request.form["image"]

        cursor.execute("INSERT INTO projects (title, description, image) VALUES (?, ?, ?)",
                       (title, description, image))
        conn.commit()

    cursor.execute("SELECT id, title, description, image FROM projects")
    projects = cursor.fetchall()
    conn.close()

    return render_template("admin.html", projects=projects)


@app.route("/delete/<int:project_id>")
def delete(project_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects WHERE id=?", (project_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/skills")
def skills():
    return render_template("skills.html")


@app.route("/projects")
def projects():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, image FROM projects")
    all_projects = cursor.fetchall()
    conn.close()
    return render_template("projects.html", projects=all_projects)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    success = False
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
                       (name, email, message))
        conn.commit()
        conn.close()
        
        referer = request.headers.get('Referer', '')
        if '/#contact' in referer or referer.endswith('/'):
            return redirect("/?success=1#contact")
        else:
            success = True
    
    return render_template("contact.html", success=success)


@app.route("/submit-contact", methods=["POST"])
def submit_contact():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
                   (name, email, message))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "message": "Thank you! Your message has been sent successfully."})


@app.route("/works")
def works():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, image FROM projects")
    projects = cursor.fetchall()
    conn.close()
    return render_template("works.html", projects=projects)


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/messages")
def messages():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, message, created_at FROM messages ORDER BY created_at DESC")
    all_messages = cursor.fetchall()
    conn.close()
    return render_template("messages.html", messages=all_messages)


@app.route("/delete-message/<int:message_id>")
def delete_message(message_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE id=?", (message_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("contact"))


# ------------------ RUN SERVER ------------------
if __name__ == "__main__":
    app.run(debug=True)
