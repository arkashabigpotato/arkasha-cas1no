from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///casino.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
app.secret_key = "ljy4x^isv^@axcd&z&d-o1d)uu+_!%5atd=fx)6c$c#3x9=_)w"
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Float, default=1000)
    is_admin = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    date_of_birth = db.Column(db.DateTime, default=datetime.utcnow)
    user_games = db.Column(db.Integer, db.ForeignKey('game.id'))


class Slot(db.Model):
    __tablename__ = "slot"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    win_rate = db.Column(db.Float, default=0.25)
    is_active = db.Column(db.Boolean, default=True)
    slot_games = db.Column(db.Integer, db.ForeignKey('game.id'))


class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    slot = db.relationship('Slot', backref='game', uselist=False)
    bid = db.Column(db.Float, nullable=False)
    is_win = db.Column(db.Boolean, nullable=False)
    payoff = db.Column(db.Float, nullable=False)
    user = db.relationship('User', backref='game', uselist=False)


@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        logged_user = User.query.filter_by(email=email).first()

        if logged_user:
            if hashlib.sha1(password.encode()).hexdigest() == logged_user.password:
                session['email'] = request.form['email']
                return redirect(url_for("index"))
            else:
                return redirect(url_for("login"))
        else:
            return redirect(url_for('register'))

    else:  # GET
        if session.get('email'):
            return redirect(url_for('index'))
        else:
            return render_template("login.html")


@app.route("/registration", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if request.form['password'] == request.form['2_password']:
            email = request.form['email']
            password = request.form['password']

            new_user = User(email=email, password=hashlib.sha1(password.encode()).hexdigest())

            try:
                db.session.add(new_user)
                db.session.commit()
            except:
                session['email'] = request.form['email']
                return "registration error"
            return redirect(url_for('index'))
        else:
            return redirect(url_for('register'))
    else:  # GET
        if session.get('email'):
            return redirect(url_for('index'))
        else:
            return render_template("registration.html")


@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route("/user/<user_id>")
def user(user_id):
    return "user id -" + str(user_id)


@app.route("/admin/")
def admin():
    return render_template("admin.html")


@app.route("/admin/users")
def admin_users():
    users = User.query.all()
    return render_template("admin_users.html", users=users)


@app.route("/admin/slots")
def admin_slots():
    return 'admin slots'





if __name__ == "__main__":
    app.run()
