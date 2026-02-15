import json

from flask import Blueprint, render_template

from application.utils import load_data

charities = Blueprint("charities", __name__, template_folder="templates")

CHARTS = [
    {
        "type": "INCOME",
        "column": "Income - Total",
        "title": "Charities by income",
        "unit": "bn",
    },
    {
        "type": "EXPENDITURE",
        "column": "Expenditure - Total",
        "title": "Charities by expenditure",
        "unit": "bn",
    },
    {
        "type": "INCOME_GROWTH",
        "column": "Income - growth",
        "title": "Charities by income growth",
        "unit": "m",
    },
    {
        "type": "EXPENDITURE_GROWTH",
        "column": "Expenditure - Growth",
        "title": "Charities by expenditure growth",
        "unit": "m",
    },
]


@charities.route("/charities")
def index():
    records = load_data("Top Charites.csv")

    charts = []
    for chart in CHARTS:
        rows = [r for r in records if r["type"] == chart["type"]]
        rows.sort(key=lambda r: int(r["order_no"]))
        names = [r["charity_name"].title() for r in rows]
        values = [int(r[chart["column"]]) for r in rows]
        charts.append(
            {
                "title": chart["title"],
                "categories": json.dumps(names),
                "data": json.dumps(values),
                "unit": chart["unit"],
            }
        )

    return render_template("charities.html", charts=charts)
