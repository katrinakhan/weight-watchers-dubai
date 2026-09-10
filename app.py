import os
from pathlib import Path

import stripe
from flask import Flask, redirect, render_template, request, session, url_for
from flask_login import LoginManager, current_user, login_user, logout_user
from sqlalchemy import text

from models import User, db
from restaurants import (
    all_restaurants,
    cuisine_counts,
    cuisines,
    get_cuisine,
    get_restaurant,
    search_restaurants,
)

PLANS = {
    "3m": {"aed": 30, "days": 90, "label": "AED 30 for 3 months"},
    "6m": {"aed": 50, "days": 180, "label": "AED 50 for 6 months"},
    "1y": {"aed": 90, "days": 365, "label": "AED 90 for a year"},
}


def _database_uri() -> str:
    uri = os.environ.get("DATABASE_URL", "sqlite:///instance/whattoorder.db")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    return uri


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-on-render")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
os.makedirs(app.instance_path, exist_ok=True)
if os.environ.get("DATABASE_URL"):
    app.config["SQLALCHEMY_DATABASE_URI"] = _database_uri()
else:
    if os.environ.get("RENDER"):
        db_file = Path("/tmp/whattoorder.db")
    else:
        db_file = Path(app.instance_path) / "whattoorder.db"
    posix = str(db_file.resolve()).replace("\\", "/")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + posix

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Create a password after you subscribe, then log in."


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def _ensure_paid_until_column():
    for stmt in (
        'ALTER TABLE "user" ADD COLUMN paid_until DATETIME',
        'ALTER TABLE "user" ADD COLUMN is_admin BOOLEAN DEFAULT 0',
    ):
        try:
            with db.engine.connect() as conn:
                conn.execute(text(stmt))
                conn.commit()
        except Exception:
            pass


def _ensure_admin_user():
    email = (os.environ.get("ADMIN_EMAIL") or "").strip().lower()
    password = os.environ.get("ADMIN_PASSWORD") or ""
    if not email or "@" not in email:
        return
    user = User.query.filter_by(email=email).first()
    if user is None:
        if len(password) < 8:
            return
        user = User(email=email, is_admin=True)
        user.set_password(password)
        db.session.add(user)
    else:
        user.is_admin = True
    db.session.commit()


try:
    with app.app_context():
        db.create_all()
        _ensure_paid_until_column()
        _ensure_admin_user()
except Exception:
    app.logger.exception("Could not create the login database tables")
    raise


def _has_access() -> bool:
    return current_user.is_authenticated and current_user.has_access()


@app.context_processor
def inject_access():
    return {"has_access": _has_access(), "plans": PLANS}


def _filters():
    cuisine = request.args.get("cuisine", "all").strip() or "all"
    if cuisine != "all" and get_cuisine(cuisine) is None:
        cuisine = "all"
    restaurant_q = request.args.get("restaurant", "").strip()
    price = request.args.get("price", "all")
    if price not in ("all", "mid", "high"):
        price = "all"
    return cuisine, restaurant_q, price


def _grant_by_email(email: str, days: int) -> User | None:
    user = User.query.filter_by(email=email).first()
    if user is None:
        return None
    user.grant_days(days)
    db.session.commit()
    return user


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    error = None
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            error = "That email or password is not right."
        else:
            login_user(user)
            nxt = request.args.get("next") or url_for("index")
            if not nxt.startswith("/") or nxt.startswith("//"):
                nxt = url_for("index")
            return redirect(nxt)
    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    paid_email = (session.get("paid_email") or "").lower()
    error = None
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        confirm = request.form.get("confirm") or ""
        if "@" not in email or "." not in email.split("@")[-1]:
            error = "Enter a real email address."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        elif password != confirm:
            error = "The two passwords do not match."
        elif User.query.filter_by(email=email).first():
            error = "That email already has an account. Log in instead."
        else:
            user = User(email=email)
            user.set_password(password)
            if paid_email and email == paid_email:
                user.grant_days(int(session.pop("paid_days", 90)))
                session.pop("paid_email", None)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("index"))
    return render_template("register.html", error=error, paid_email=paid_email)


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("index"))


@app.route("/")
def index():
    cuisine, restaurant_q, price = _filters()
    results = search_restaurants(cuisine, restaurant_q, price)
    selected = get_cuisine(cuisine) if cuisine != "all" else None
    return render_template(
        "index.html",
        cuisines=cuisines(),
        counts=cuisine_counts(),
        restaurants=results,
        selected=selected,
        cuisine=cuisine,
        restaurant_q=restaurant_q,
        price=price,
        total=len(all_restaurants()),
        shown=len(results),
    )


@app.route("/restaurant/<slug>")
def restaurant(slug):
    if not _has_access():
        return redirect(url_for("subscribe"))
    row = get_restaurant(slug)
    if row is None:
        return render_template("not_found.html"), 404
    return render_template("restaurant.html", r=row)


@app.route("/how-this-works")
def how():
    return render_template("how.html", total=len(all_restaurants()))


@app.route("/subscribe")
def subscribe():
    if _has_access():
        return redirect(url_for("index"))
    return render_template("subscribe.html", error=None)


@app.route("/subscribe/checkout", methods=["POST"])
def subscribe_checkout():
    secret = os.environ.get("STRIPE_SECRET_KEY")
    if not secret:
        return render_template(
            "subscribe.html",
            error="Stripe is not connected yet. Add STRIPE_SECRET_KEY in Render Environment.",
        ), 503
    plan_key = request.form.get("plan") or "3m"
    plan = PLANS.get(plan_key, PLANS["3m"])
    stripe.api_key = secret
    checkout = stripe.checkout.Session.create(
        mode="payment",
        currency="aed",
        metadata={"plan": plan_key, "days": str(plan["days"])},
        line_items=[
            {
                "price_data": {
                    "currency": "aed",
                    "unit_amount": plan["aed"] * 100,
                    "product_data": {
                        "name": "Weight Watchers — subscribe to see what to order",
                        "description": plan["label"],
                    },
                },
                "quantity": 1,
            }
        ],
        success_url=url_for("subscribe_success", _external=True)
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=url_for("subscribe", _external=True),
    )
    return redirect(checkout.url, code=303)


@app.route("/subscribe/success")
def subscribe_success():
    secret = os.environ.get("STRIPE_SECRET_KEY")
    session_id = request.args.get("session_id") or ""
    if not secret or not session_id:
        return redirect(url_for("subscribe"))
    stripe.api_key = secret
    checkout = stripe.checkout.Session.retrieve(session_id)
    if checkout.payment_status != "paid":
        return redirect(url_for("subscribe"))
    email = (checkout.customer_details.email or "").strip().lower()
    if not email:
        return redirect(url_for("subscribe"))
    days = 90
    if checkout.metadata:
        days = int(checkout.metadata.get("days") or 90)
    user = _grant_by_email(email, days)
    if user is not None:
        login_user(user)
        return redirect(url_for("index"))
    session["paid_email"] = email
    session["paid_days"] = days
    return redirect(url_for("register"))


if __name__ == "__main__":
    app.run(debug=True, port=5055)
