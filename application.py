import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


from helpers import apology, login_required, lookup, usd

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
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "GET":
        current_cash = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])[0]['cash']
        id = session["user_id"]
        summary = db.execute("SELECT SUM(numberOfShares), stockname FROM purchases WHERE id = :id GROUP BY stockname", id = id)
        currentPrice = [];
        stockBalance = 0;
        for row in summary:
            row['currentPrice'] = round(lookup(row['stockname'])['price'], 2)
            row['total'] = round(lookup(row['stockname'])['price'] * row['SUM(numberOfShares)'], 2)
            stockBalance += lookup(row['stockname'])['price'] * row['SUM(numberOfShares)']
        stockBalance = round(stockBalance, 2)
        grandTotal = stockBalance + current_cash



        return render_template("index.html", current_cash = round(current_cash, 2), summary = summary, grandTotal = round(grandTotal,2), stockBalance = round(stockBalance,2))




@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        if lookup(request.form.get("symbol")) == None:
            return apology("Invalid symbol")
        elif not int(request.form.get("shares")) > 0:
            return apology("Invalid number of shares")
        else:
            row = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])
            username = row[0]["username"]
            id = session["user_id"]
            current_cash = row[0]["cash"]
            numberofshares = int(request.form.get("shares"))
            totalvalue = lookup(request.form.get("symbol"))['price'] * numberofshares
            stockname = lookup(request.form.get("symbol"))['symbol']
            stockprice = lookup(request.form.get("symbol"))['price']
            time = datetime.now()
            type = 'bought'
            if (totalvalue > current_cash):
                return apology("Insufficient Balance")
            else:
                db.execute("INSERT INTO purchases(time, id, stockname, numberOfShares, stockPrice, totalvalue, type) VALUES(:time, :id, :stockname,:numberofshares, :stockprice, :totalvalue, :type)", time = time, id = id,
                stockname = stockname, numberofshares = numberofshares, stockprice = stockprice, totalvalue=totalvalue, type = type)
                db.execute("UPDATE users SET cash = cash - :totalvalue WHERE id = :id", totalvalue = totalvalue, id = id)
                return redirect("/")




    elif request.method == "GET":
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    purchases = db.execute("SELECT * FROM purchases")
    for row in purchases:
        row['numberOfShares'] = abs(row['numberOfShares'])
    return render_template("history.html", purchases = purchases)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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
    """Get stock quote."""
    if request.method == "POST":

        if lookup(request.form.get("symbol")) == None:
            return apology("Invalid symbol")
        else:
            stockname = lookup(request.form.get("symbol"))['symbol']
            companyName = lookup(request.form.get("symbol"))['name']
            price = lookup(request.form.get("symbol"))['price']
            return render_template("quoted.html", stockname = stockname,price=price, companyName = companyName)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
     #select all rows from existing database of users
            rows = db.execute("SELECT * FROM users WHERE username = :username",
                              username=request.form.get("username"))
            #check if username exists
            if len(rows) != 0:
                return apology("Username already exists")
            elif not request.form.get("password") == request.form.get("confirmation"):
                return apology("Invalid Password")
            elif request.form.get("password") =="" or request.form.get("confirmation") =="":
                return apology("Invalid Password")
            else:
                db.execute("INSERT INTO users(username, hash) VALUES(:username, :password)", username = request.form.get("username"), password = generate_password_hash(request.form.get("password")))
                return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        number = int(request.form.get("shares"))
        symbol = request.form.get("symbol")
        id = session["user_id"]
        time  = datetime.now()
        currentPrice = lookup(symbol)['price']
        type = 'sold'
        totalvalue = number * currentPrice
        owned = db.execute("SELECT SUM(numberOfShares) FROM purchases WHERE stockname=:symbol AND id =:id", symbol=symbol, id=id)[0]['SUM(numberOfShares)']
        if owned == None:
            owned = 0
        if lookup(symbol) == None:
            return apology("Invalid symbol")
        elif not number > 0:
            return apology("Invalid number of shares")
        elif number > owned:
            return apology("Insufficient number of shares owned")
        else:
            db.execute("INSERT INTO purchases(time, id, stockname, numberOfShares, stockprice, 'totalvalue', 'type') VALUES(:time, :id, :stockname, :numberOfShares, :stockPrice, :totalValue, :type)",
            time = time, id = id, stockname = symbol, numberOfShares = -number, stockPrice = -currentPrice, totalValue = totalvalue, type = type)
            db.execute("UPDATE users SET cash = cash + :totalvalue WHERE id = :id", totalvalue = round(totalvalue, 2), id = id)
            return redirect("/")

    else:
        return render_template("sell.html")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
