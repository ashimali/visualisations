from flask import Blueprint, render_template

from application.utils import load_data

companies_house = Blueprint("companies_house", __name__, template_folder="templates")


def _parse_int(s):
    return int(s.replace(",", ""))


def _headline_figure(title, subtitle, current, previous):
    change = current - previous
    per_cent = round(change / previous * 100, 1)
    return {
        "title": title,
        "subtitle": subtitle,
        "current": current,
        "previous": previous,
        "change": change,
        "change_per_cent": per_cent,
        "direction": "down" if change < 0 else "up",
    }


@companies_house.route("/companies-house")
def index():
    records = load_data(
        "Companies_register_activities_April_2024_to_March_2025_table_A8.csv"
    )
    prev_year, curr_year = records[-2], records[-1]

    # turn "2024-25" -> "2025"
    curr_fye = "20" + curr_year["Year ending"].split("-")[1]
    prev_fye = "20" + prev_year["Year ending"].split("-")[1]

    formations = (
        _parse_int(curr_year["Incorporations"]),
        _parse_int(prev_year["Incorporations"]),
    )
    dissolutions = (
        _parse_int(curr_year["Dissolved"]),
        _parse_int(prev_year["Dissolved"]),
    )
    net = (formations[0] - dissolutions[0], formations[1] - dissolutions[1])

    headlines = [
        _headline_figure(
            "Company formations",
            f"New companies incorporated (FYE {curr_fye})",
            *formations,
        ),
        _headline_figure(
            "Company dissolutions",
            f"Companies removed from the register (FYE {curr_fye})",
            *dissolutions,
        ),
        _headline_figure(
            "Net register growth",
            f"Formations minus dissolutions (FYE {curr_fye})",
            *net,
        ),
    ]

    return render_template(
        "companies-house.html",
        headlines=headlines,
        curr_fye=curr_fye,
        prev_fye=prev_fye,
    )
