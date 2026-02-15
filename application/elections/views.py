import json

from flask import Blueprint, render_template

from application.utils import load_data

elections = Blueprint("elections", __name__, template_folder="templates")


@elections.route("/elections")
def index():
    records = load_data("parties-general-election-04-07-2024.csv", encoding="utf-8-sig")

    # Only parties that won at least one seat
    with_seats = [r for r in records if int(r["Constituencies won"]) > 0]
    with_seats.sort(key=lambda r: int(r["Constituencies won"]), reverse=True)

    parties = [r["Party name"] for r in with_seats]
    seats_won = [int(r["Constituencies won"]) for r in with_seats]
    vote_shares = [round(float(r["Vote share"]), 1) for r in with_seats]

    # For the seats vs votes comparison, express both as percentages
    total_seats = sum(int(r["Constituencies won"]) for r in records)
    seat_shares = [
        round(int(r["Constituencies won"]) / total_seats * 100, 1) for r in with_seats
    ]

    return render_template(
        "elections.html",
        parties=json.dumps(parties),
        seats_won=json.dumps(seats_won),
        vote_shares=json.dumps(vote_shares),
        seat_shares=json.dumps(seat_shares),
    )
