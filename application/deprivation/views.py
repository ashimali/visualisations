import json
from collections import defaultdict

from flask import Blueprint, render_template

from application.utils import load_data

deprivation = Blueprint("deprivation", __name__, template_folder="templates")

LAD_CODE = "Local Authority District code (2024)"
LAD_NAME = "Local Authority District name (2024)"
IMD_RANK = "Index of Multiple Deprivation (IMD) Rank"


@deprivation.route("/deprivation")
def index():
    records = load_data(
        "reference/IoD-2025-custom_data_download-LAD.csv", encoding="utf-8-sig"
    )
    region_lookup = load_data(
        "reference/Local_Authority_District_to_Region_(April_2025)_Lookup_in_EN_v2.csv",
        encoding="utf-8-sig",
    )
    code_to_region = {r["LAD25CD"]: r["RGN25NM"] for r in region_lookup}

    for r in records:
        r[IMD_RANK] = int(r[IMD_RANK])

    total_lads = len(records)
    sorted_by_rank = sorted(records, key=lambda r: r[IMD_RANK])

    # Chart 1: 20 most deprived (lowest rank numbers)
    most_deprived = sorted_by_rank[:20]
    most_deprived_categories = [r[LAD_NAME] for r in most_deprived]
    most_deprived_values = [r[IMD_RANK] for r in most_deprived]

    # Chart 2: 20 least deprived (highest rank numbers)
    least_deprived = sorted_by_rank[-20:]
    least_deprived.reverse()
    least_deprived_categories = [r[LAD_NAME] for r in least_deprived]
    least_deprived_values = [r[IMD_RANK] for r in least_deprived]

    # Chart 3: average rank by region
    region_ranks = defaultdict(list)
    for r in records:
        region = code_to_region.get(r[LAD_CODE])
        if region:
            region_ranks[region].append(r[IMD_RANK])

    region_averages = [
        {"name": region, "average": round(sum(ranks) / len(ranks))}
        for region, ranks in region_ranks.items()
    ]
    region_averages.sort(key=lambda r: r["average"])
    region_categories = [r["name"] for r in region_averages]
    region_values = [r["average"] for r in region_averages]

    return render_template(
        "deprivation.html",
        total_lads=total_lads,
        most_deprived_categories=json.dumps(most_deprived_categories),
        most_deprived_values=json.dumps(most_deprived_values),
        least_deprived_categories=json.dumps(least_deprived_categories),
        least_deprived_values=json.dumps(least_deprived_values),
        region_categories=json.dumps(region_categories),
        region_values=json.dumps(region_values),
    )
