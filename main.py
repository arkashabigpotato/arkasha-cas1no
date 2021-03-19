from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from flask import session
from flask import url_for
from flask import redirect


app = Flask(__name__)
app.debug = True
app.secret_key = "ljy4x^isv^@axcd&z&d-o1d)uu+_!%5atd=fx)6c$c#3x9=_)w"


@app.route("/index")
@app.route("/")
def index():
    name = "Artem"
    return render_template("index.html", name=name)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session['login'] = request.form['login']
        return redirect(url_for("index"))
    else:  # GET
        if session.get('login'):
            return redirect(url_for('index'))
        else:
            return render_template("login.html")


@app.route("/registration")
def register():
    return "Register page"


@app.route("/logout")
def logout():
    session.pop('login', None)
    return redirect(url_for('index'))


@app.route("/user/<user_id>")
def user(user_id):
    return "user id -" + str(user_id)


if __name__ == "__main__":
    app.run()

