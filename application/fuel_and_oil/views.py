from flask import Blueprint, render_template

from application.utils import load_data

PETROL_FIELD_NAME = (
    "Motor spirit:\nPremium unleaded / ULSP\n(Pence per litre)\n[Note 1, 4]"
)
DIESEL_FIELD_NAME = "Derv: Diesel / ULSD\n(Pence per litre)\n[Note 1, 5]"

fuel_and_oil = Blueprint("fuel_and_oil", __name__, template_folder="templates")


@fuel_and_oil.route("/fuel-and-oil-prices")
def index():
    records = load_data("4.1.2-Table 1.csv")

    # select last n years - arbitrarily
    n = 10
    last_n_years = records[-n:]

    petrol = [
        [record["Year"], float(record[PETROL_FIELD_NAME])] for record in last_n_years
    ]
    diesel = [
        [record["Year"], float(record[DIESEL_FIELD_NAME])] for record in last_n_years
    ]

    series = [
        {"name": "Premium unleaded petrol", "data": petrol},
        {"name": "Ultra low sulphur diesel", "data": diesel},
    ]

    return render_template("fuel-and-oil-prices.html", series=series)
