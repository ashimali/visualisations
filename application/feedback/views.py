from flask import Blueprint, render_template

feedback = Blueprint("feedback", __name__, template_folder="templates")


@feedback.route("/feedback")
def index():
    return render_template("feedback.html")
