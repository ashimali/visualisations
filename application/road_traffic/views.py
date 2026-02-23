import json

from flask import Blueprint, render_template

from application.utils import load_data

road_traffic = Blueprint("road_traffic", __name__, template_folder="templates")

VEHICLE_TYPE_FILE = "tra2501-miles-by-vehicle-type_TRA2501a.csv"
ROAD_CLASS_FILE = "tra2502-miles-by-road-class_TRA2502a.csv"


@road_traffic.route("/road-traffic")
def index():
    # Chart 1: Traffic by vehicle type (latest rolling annual period)
    vehicle_records = load_data(VEHICLE_TYPE_FILE)
    latest_vehicle = vehicle_records[-1]
    total_vehicle = float(latest_vehicle["All Motor Vehicles"])
    vehicle_period = latest_vehicle["Year ending [note 1]"]

    vehicle_labels = ["Cars and taxis", "Vans", "Lorries", "Other vehicles"]
    vehicle_values = [
        round(float(latest_vehicle[cat]) / total_vehicle * 100, 1)
        for cat in [
            "Cars and Taxis",
            "Light Commercial Vehicles [note 3]",
            "Heavy Goods Vehicles [note 4]",
            "Other Vehicles [note 5]",
        ]
    ]

    # Chart 2: Traffic by road type (latest rolling annual period)
    road_records = load_data(ROAD_CLASS_FILE)
    latest_road = road_records[-1]
    total_road = float(latest_road["All Roads"])
    road_period = latest_road["Year ending [note 1]"]

    motorways = float(latest_road["Major Roads: Motorways"])
    a_roads = float(latest_road["Major Roads: Rural 'A' Roads [note 3]"]) + float(
        latest_road["Major Roads: Urban 'A' Roads [note 3]"]
    )
    minor_roads = float(latest_road["Minor Roads: Rural [note 3]"]) + float(
        latest_road["Minor Roads: Urban [note 3]"]
    )

    road_labels = ["Motorways", "'A' roads", "Minor roads"]
    road_values = [
        round(v / total_road * 100, 1) for v in [motorways, a_roads, minor_roads]
    ]

    return render_template(
        "road-traffic.html",
        vehicle_period=vehicle_period,
        vehicle_labels=json.dumps(vehicle_labels),
        vehicle_values=json.dumps(vehicle_values),
        road_period=road_period,
        road_labels=json.dumps(road_labels),
        road_values=json.dumps(road_values),
    )
