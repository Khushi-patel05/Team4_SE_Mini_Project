import sqlite3
from functools import wraps

from flask import (
    Blueprint,
    current_app,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    abort
)
from werkzeug.security import check_password_hash, generate_password_hash


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def get_auth_db_connection():
    """Connect to the application's configured SQLite database."""
    connection = sqlite3.connect(current_app.config["DATABASE"])
    connection.row_factory = sqlite3.Row
    return connection


def initialize_auth_database():
    """Create the users table without changing existing tables."""
    with get_auth_db_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK (
                    role IN ('Administrator', 'Doctor', 'Receptionist')
                ),
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


def create_user(username, password, role):
    """Create a user with a securely hashed password."""
    username = username.strip()

    allowed_roles = {
        "Administrator",
        "Doctor",
        "Receptionist",
    }

    if not username or not password:
        raise ValueError("Username and password are required.")

    if role not in allowed_roles:
        raise ValueError("Invalid user role.")

    password_hash = generate_password_hash(password)

    with get_auth_db_connection() as connection:
        connection.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
            """,
            (username, password_hash, role),
        )


def login_required(view):
    """Require an authenticated session before opening a protected page."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))

        return view(*args, **kwargs)

    return wrapped_view


def role_required(*allowed_roles):
    """Allow access only to authenticated users with permitted roles."""

    def decorator(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if "user_id" not in session:
                flash("Please log in to continue.", "warning")
                return redirect(url_for("auth.login"))

            if session.get("role") not in allowed_roles:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for("auth.dashboard"))

            return view(*args, **kwargs)

        return wrapped_view

    return decorator


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Enter both username and password.", "danger")
            return render_template("auth/login.html")

        with get_auth_db_connection() as connection:
            user = connection.execute(
                """
                SELECT id, username, password_hash, role
                FROM users
                WHERE username = ?
                """,
                (username,),
            ).fetchone()

        if user is None or not check_password_hash(
            user["password_hash"], password
        ):
            flash("Invalid username or password.", "danger")
            return render_template("auth/login.html")

        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]

        flash("Login successful.", "success")
        return redirect(url_for("auth.dashboard"))

    return render_template("auth/login.html")


@auth_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/manage-users", methods=["GET", "POST"])
@role_required("Administrator")
def manage_users():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "")

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "danger")
            return redirect(url_for("auth.manage_users"))

        try:
            create_user(username, password, role)
            flash(f"{role} account created successfully.", "success")
        except ValueError as error:
            flash(str(error), "danger")
        except sqlite3.IntegrityError:
            flash("That username already exists.", "danger")
        except sqlite3.Error:
            current_app.logger.exception("Staff account creation failed")
            flash("A database error prevented account creation.", "danger")

        return redirect(url_for("auth.manage_users"))

    return render_template("manage_users.html")
