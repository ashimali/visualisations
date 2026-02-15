import json

from flask import Blueprint, render_template

from application.utils import load_data, timestamp_ms

bank_rate = Blueprint("bank_rate", __name__, template_folder="templates")


@bank_rate.route("/bank-rate")
def index():
    records = load_data("Bank Rate history and data  Bank of England Database.csv")

    # CSV is already reverse chronological, most recent first, so we reverse to get oldest first
    records.reverse()

    series_data = [
        [timestamp_ms(r["Date Changed"], fmt="%d %b %y"), float(r["Rate"])]
        for r in records
    ]

    return render_template(
        "bank-rate.html",
        series_data=json.dumps(series_data),
    )
