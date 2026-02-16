import json
from collections import defaultdict

from flask import Blueprint, render_template

from application.utils import load_data

house_prices = Blueprint("house_prices", __name__, template_folder="templates")

HIGHER_LEVEL_ADMIN_REGIONS = {"England and Wales", "Great Britain", "United Kingdom"}


@house_prices.route("/house-prices")
def index():
    records = load_data("Average-price-seasonally-adjusted-2025-11.csv")
    by_region = defaultdict(list)
    for r in records:
        by_region[r["Region_Name"]].append([r["Date"], int(r["Average_Price_SA"])])

    # Chart 1: individual regions (exclude England & Wales, GB and UK)
    all_regions_series = [
        {"name": name, "data": data}
        for name, data in sorted(by_region.items())
        if name not in HIGHER_LEVEL_ADMIN_REGIONS
    ]

    # Chart 2: nations
    nations_series = [
        {"name": name, "data": by_region[name]}
        for name in ["England", "Wales", "Scotland", "United Kingdom"]
    ]

    # Chart 3: latest month snapshot for regions
    latest_date = max(r["Date"] for r in records)
    latest = [
        r
        for r in records
        if r["Date"] == latest_date
        and r["Region_Name"] not in HIGHER_LEVEL_ADMIN_REGIONS
    ]
    latest.sort(key=lambda r: int(r["Average_Price_SA"]), reverse=True)
    bar_categories = [r["Region_Name"] for r in latest]
    bar_values = [int(r["Average_Price_SA"]) for r in latest]

    return render_template(
        "house-prices.html",
        all_regions_series=json.dumps(all_regions_series),
        nations_series=json.dumps(nations_series),
        bar_categories=json.dumps(bar_categories),
        bar_values=json.dumps(bar_values),
        latest_date=latest_date,
    )
