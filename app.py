import os
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "super-secret-key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "cafes.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

ADMIN_PASSWORD = "admin123"


class Cafe(db.Model):
    __tablename__ = "cafe"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=True)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    search = request.args.get("search", "").strip()

    if search:
        cafes = Cafe.query.filter(
            Cafe.name.ilike(f"%{search}%") |
            Cafe.location.ilike(f"%{search}%")
        ).all()
    else:
        cafes = Cafe.query.all()

    return render_template(
        "index.html",
        cafes=cafes,
        search=search,
        is_admin=session.get("is_admin", False)
    )


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    if request.method == "POST":
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            seats=request.form.get("seats"),
            has_toilet=True if request.form.get("has_toilet") == "on" else False,
            has_wifi=True if request.form.get("has_wifi") == "on" else False,
            has_sockets=True if request.form.get("has_sockets") == "on" else False,
            can_take_calls=True if request.form.get("can_take_calls") == "on" else False,
            coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add_cafe.html", is_admin=session.get("is_admin", False))


@app.route("/edit/<int:cafe_id>", methods=["GET", "POST"])
def edit_cafe(cafe_id):
    if not session.get("is_admin"):
        flash("Only admin can edit cafes.")
        return redirect(url_for("home"))

    cafe = Cafe.query.get_or_404(cafe_id)

    if request.method == "POST":
        cafe.name = request.form.get("name")
        cafe.map_url = request.form.get("map_url")
        cafe.img_url = request.form.get("img_url")
        cafe.location = request.form.get("location")
        cafe.seats = request.form.get("seats")
        cafe.coffee_price = request.form.get("coffee_price")
        cafe.has_toilet = True if request.form.get("has_toilet") == "on" else False
        cafe.has_wifi = True if request.form.get("has_wifi") == "on" else False
        cafe.has_sockets = True if request.form.get("has_sockets") == "on" else False
        cafe.can_take_calls = True if request.form.get("can_take_calls") == "on" else False

        db.session.commit()
        flash("Cafe updated successfully.")
        return redirect(url_for("home"))

    return render_template("edit_cafe.html", cafe=cafe, is_admin=True)


@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    flash("Cafe deleted successfully.")
    return redirect(url_for("home"))


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            session["is_admin"] = True
            flash("Admin login successful.")
            return redirect(url_for("home"))
        else:
            flash("Incorrect admin password.")

    return render_template("admin_login.html", is_admin=session.get("is_admin", False))


@app.route("/logout")
def logout():
    session.pop("is_admin", None)
    flash("Logged out.")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)