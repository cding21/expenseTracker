import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, aud

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["aud"] = aud

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///expenses.db")




@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rows = db.execute("""
        SELECT id, category, notes, SUM(amount), date
        FROM history
        WHERE user_id = ?
        GROUP BY category
        ORDER BY id;
    """, session["user_id"])

    historys = []
    percentages = []
    total = 0
    for row in rows:
        historys.append({
            "id": row["id"],
            "category": row["category"],
            "notes": row["notes"],
            "amount": aud(row["SUM(amount)"]),
            "date": row["date"]
        })
        total += row["SUM(amount)"]
    for row in rows:
        percentages.append({
            "category": row["category"],
            "percentage": round(100 * row["SUM(amount)"] / total)
        })


    return render_template("index.html", historys=historys, total=aud(total), percentages = percentages)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """TODO"""
    if request.method == "POST":
        if not request.form.get("category"):
            return apology("Category must be included")
        elif not request.form.get("amount"):
            return apology("Amount must be included")
        elif not request.form.get("amount").isdigit:
            return apology("Invalid amount")
        else:
            category = request.form.get("category")
            notes = request.form.get("notes")
            amount = request.form.get("amount")
            db.execute("""INSERT INTO history (user_id, category, notes, amount) VALUES(?,?,?,?)""", session["user_id"], category, notes, amount)
            return redirect("/")


    else:
        return render_template("add.html")


@app.route("/history")
@login_required
def history():
    """Show portfolio of stocks"""
    rows = db.execute("""
        SELECT id, category, notes, amount, date
        FROM history
        WHERE user_id = ?
        GROUP BY category;
    """, session["user_id"])

    historys = []
    total = 0
    count = 1
    for row in rows:
        historys.append({
            "id": row["id"],
            "category": row["category"],
            "notes": row["notes"],
            "amount": aud(row["amount"]),
            "time": row["date"]
        })
        total += row["amount"]
    return render_template("history.html", historys=historys, total=aud(total), count=count)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """TODO"""


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password must match", 400)

        rows = db.execute("SELECT username FROM users")
        for row in rows:
            if request.form.get("username") == row["username"]:
                return apology("Username already taken", 400)

        else:
            username = request.form.get("username")
            password = request.form.get("password")

            hashed_password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashed_password)

            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """TODO"""

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)