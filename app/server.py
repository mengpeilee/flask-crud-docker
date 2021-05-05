import os
from flask_sqlalchemy import SQLAlchemy
from flask import redirect
from flask import request
from flask import render_template
from flask import Flask


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(
    os.path.join(project_dir, "title.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Titles(db.Model):
    title = db.Column(db.String(80), unique=True,
                      nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)


@app.route("/", methods=["GET", "POST"])
def home():
    titles = None
    if request.form:
        try:
            title = Titles(title=request.form.get("title"))
            db.session.add(title)
            db.session.commit()
        except Exception as e:
            print("Failed to add title")
            print(e)
    titles = Titles.query.all()
    return render_template("home.html", titles=titles)


@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        titles = Titles.query.filter_by(title=oldtitle).first()
        titles.title = newtitle
        db.session.commit()
    except Exception as e:
        print("Couldn't update title")
        print(e)
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    titles_data = Titles.query.filter_by(title=title).first()
    db.session.delete(titles_data)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=34567, debug=True)
