# Import required modules
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

# Create a Flask application instance
app = Flask(__name__)

# Required for session and flash messages
app.secret_key = "secret_key"  # Should replace with a strong, random string

# MySQL configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "helpdesk_user"
app.config["MYSQL_PASSWORD"] = "StrongPassword123!"
app.config["MYSQL_DB"] = "helpdesk_db"

mysql = MySQL(app)

# Redirect root URL to login page
@app.route("/")
def home():
    return redirect(url_for("login"))

# login, logout, and register routes
# Login route handling both GET (show form) and POST (process login)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Open a cursor to run the DB query
        cur = mysql.connection.cursor()
        # Fetch the stored (hashed) password and role for the given username
        cur.execute("SELECT password, role FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        # Close the cursor to release DB resources
        cur.close()

        # Check if username exists and password matches
        if user and check_password_hash(
            user[0], password
        ): 
            session["username"] = username
            session["role"] = user[1]

            # Redirect based on role
            if user[1] == "Admin":
                return render_template("dashboard_admin.html")
            elif user[1] == "IT Support":
                return render_template("dashboard_it.html")
            else:
                return render_template("dashboard_user.html")
        else:
            # Show error message using flash and redirect to login page
            flash("Invalid username or password. Please try again.", "error")
            return redirect(url_for("login"))

    # GET request: show login form
    return render_template("login.html")

@app.route("/logout")
def logout():
    # Clear all session data
    session.clear()

    # Show a logout confirmation message
    flash("You have been logged out.", "success")

    # Redirect back to the login page
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        # Check if username already exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        existing_user = cur.fetchone()

        if existing_user:
            flash("Username already exists. Please choose a different one.", "error")
            cur.close()
            return redirect(url_for("register"))

        # Hash the password before storing
        hashed_password = generate_password_hash(password)

        # Insert into database
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, hashed_password, role),
        )
        mysql.connection.commit()
        cur.close()

        flash("Registration successful. You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# user routes
@app.route("/dashboard_user")
def dashboard_user():
    if "username" in session and session["role"] == "User":
        return render_template("dashboard_user.html")
    else:
        return redirect(url_for("login"))


@app.route("/submit_ticket", methods=["GET", "POST"])
def submit_ticket():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        category = request.form["category"]
        priority = request.form["priority"]

        # Get user ID from database
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s", (session["username"],))
        user = cur.fetchone()

        # Insert ticket
        cur.execute(
            """
            INSERT INTO tickets (user_id, title, description, category, priority)
            VALUES (%s, %s, %s, %s, %s)
        """,
            (user[0], title, description, category, priority),
        )
        mysql.connection.commit()
        cur.close()

        flash("Ticket submitted successfully.", "success")

    return render_template("submit_ticket.html")


@app.route("/my_tickets")
def my_tickets():
    # Only allow logged-in users with 'User' role
    if "username" not in session or session["role"] != "User":
        return redirect(url_for("login"))

    # Fetch tickets submitted by the current user
    cur = mysql.connection.cursor()
    cur.execute(
        """
        SELECT id, title, description, category, priority, status, created_at
        FROM tickets
        WHERE user_id = (
            SELECT id FROM users WHERE username = %s
        ) AND status != 'Closed'
    """,
        (session["username"],),
    )
    tickets = cur.fetchall()
    cur.close()

    return render_template("my_tickets.html", tickets=tickets)


@app.route("/my_ticket_history")
def my_ticket_history():
    # Only allow logged-in users with 'User' role
    if "username" not in session or session["role"] != "User":
        return redirect(url_for("login"))

    # Fetch tickets submitted by the current user
    cur = mysql.connection.cursor()
    cur.execute(
        """
        SELECT id, title, description, category, priority, status, created_at
        FROM tickets
        WHERE user_id = (
            SELECT id FROM users WHERE username = %s
        ) AND status = 'Closed'
    """,
        (session["username"],),
    )
    tickets = cur.fetchall()
    cur.close()

    return render_template("my_ticket_history.html", tickets=tickets)


# it support routes
@app.route("/dashboard_it")
def dashboard_it():
    if "username" in session and session["role"] == "IT Support":
        return render_template("dashboard_it.html")
    else:
        return redirect(url_for("login"))


@app.route("/manage_tickets", methods=["GET", "POST"])
def manage_tickets():
    # Only IT Support users can access this page
    if "username" not in session or session["role"] != "IT Support":
        return redirect(url_for("login"))

    # Open a DB cursor for queries/updates
    cur = mysql.connection.cursor()

    # Handle form submission to update ticket status/priority
    if request.method == "POST":
        # NOTE: validate/sanitize inputs as appropriate (e.g., ensure status/priority are allowed values)
        ticket_id = request.form["ticket_id"]
        new_status = request.form["status"]
        new_priority = request.form["priority"]

        # Parameterized query prevents SQL injection
        cur.execute(
            """
            UPDATE tickets
            SET status = %s, priority = %s
            WHERE id = %s 
        """,
            (new_status, new_priority, ticket_id),
        )
        mysql.connection.commit()
        flash("Ticket updated successfully.", "success")

    # Fetch all tickets to display to IT Support
    cur.execute(
        "SELECT id, title, description, category, priority, status, created_at FROM tickets"
    )
    tickets = cur.fetchall()

    # Close cursor to release DB resources
    cur.close()

    # Render the IT support ticket management template
    return render_template("manage_tickets.html", tickets=tickets)


# admin routes
@app.route("/dashboard_admin")
def dashboard_admin():
    if "username" in session and session["role"] == "Admin":
        return render_template("dashboard_admin.html")
    else:
        return redirect(url_for("login"))


@app.route("/manage_users")
def manage_users():
    if "role" in session and session["role"] == "Admin":
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, role FROM users")
        users = cur.fetchall()
        cur.close()

        return render_template("manage_users.html", users=users)
    else:
        return "Access Denied"


@app.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    # Ensure only Admins can delete users
    if "role" in session and session["role"] == "Admin":
        # Delete user by ID
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        cur.close()

        # Show success message
        flash("User deleted successfully.", "success")
        return redirect(url_for("manage_users"))
    else:
        return "Access Denied"


@app.route("/reset_password/<int:user_id>", methods=["POST"])
def reset_password(user_id):
    # Ensure only Admins can reset user passwords
    if "role" in session and session["role"] == "Admin":
        # Get new password from form
        # new_password = request.form.get("new_password")
        new_password = "password"
        if not new_password:
            flash("New password is required.", "error")
            return redirect(url_for("manage_users"))

        # Hash the password
        hashed_password = generate_password_hash(new_password)

        # Update password in DB
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET password=%s WHERE id=%s", (hashed_password, user_id))
        mysql.connection.commit()
        cur.close()

        # Show success message
        flash("Password reset successfully.", "success")
        return redirect(url_for("manage_users"))
    else:
        return "Access Denied"
