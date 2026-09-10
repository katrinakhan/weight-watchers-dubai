import os

from flask import Flask, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from models import User, db
from restaurants import (
    all_restaurants,
    cuisine_counts,
    cuisines,
    get_cuisine,
    get_restaurant,
    search_restaurants,
)


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
    db_path = os.path.join(app.instance_path, "whattoorder.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path.replace("\\", "/")

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Log in with your email to open the restaurant guides."


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


with app.app_context():
    db.create_all()


def _filters():
    cuisine = request.args.get("cuisine", "all").strip() or "all"
    if cuisine != "all" and get_cuisine(cuisine) is None:
        cuisine = "all"
    restaurant_q = request.args.get("restaurant", "").strip()
    price = request.args.get("price", "all")
    if price not in ("all", "mid", "high"):
        price = "all"
    return cuisine, restaurant_q, price


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
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("index"))
    return render_template("register.html", error=error)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/")
@login_required
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
@login_required
def restaurant(slug):
    row = get_restaurant(slug)
    if row is None:
        return render_template("not_found.html"), 404
    return render_template("restaurant.html", r=row)


@app.route("/how-this-works")
@login_required
def how():
    return render_template("how.html", total=len(all_restaurants()))


if __name__ == "__main__":
    app.run(debug=True, port=5055)
