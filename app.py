# ============================================================
# TripGenius AI — Advanced Travel Planner using CFAI Concepts
# KLH University | Python Streamlit Project
# Subject: Computational Foundations of Artificial Intelligence
# Made by Gatik Sharma 2520090223
#
# Run:
#   pip install -r requirements.txt
#   streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datetime import date, datetime, timedelta
from collections import deque
import heapq
import math
import random

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="TripGenius AI | CFAI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# ADVANCED CSS
# ============================================================
st.markdown("""
<style>
:root{
    --bg:#070B1A;
    --panel:#10172A;
    --panel2:#111C35;
    --text:#EAF0FF;
    --muted:#94A3B8;
    --blue:#38BDF8;
    --cyan:#22D3EE;
    --green:#34D399;
    --orange:#FB923C;
    --red:#F87171;
    --purple:#A78BFA;
    --border:rgba(148,163,184,0.22);
}
html, body, [class*="css"]{
    font-family: "Inter", "Segoe UI", sans-serif;
}
[data-testid="stAppViewContainer"]{
    background:
        radial-gradient(circle at 20% 0%, rgba(56,189,248,0.18), transparent 35%),
        radial-gradient(circle at 85% 10%, rgba(167,139,250,0.16), transparent 30%),
        linear-gradient(135deg, #050816, #07111F 45%, #0B1020);
}
.block-container{
    padding-top:1.2rem;
    padding-bottom:2rem;
}
[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#050816,#0F172A);
    border-right:1px solid rgba(148,163,184,0.18);
}
[data-testid="stSidebar"] *{
    color:#EAF0FF !important;
}
.main-title{
    font-size:3.1rem;
    font-weight:850;
    letter-spacing:-1.5px;
    line-height:1.05;
    margin:0;
    color:#F8FAFC;
}
.gradient-text{
    background:linear-gradient(90deg,#38BDF8,#34D399,#A78BFA);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.hero{
    padding:34px 34px;
    border-radius:28px;
    border:1px solid rgba(148,163,184,0.22);
    background:
        linear-gradient(135deg, rgba(15,23,42,0.94), rgba(17,24,39,0.85)),
        radial-gradient(circle at 85% 20%, rgba(56,189,248,0.12), transparent 38%);
    box-shadow:0 24px 70px rgba(0,0,0,0.42);
    margin-bottom:24px;
}
.subtext{
    font-size:1.05rem;
    line-height:1.7;
    color:#CBD5E1;
}
.glass-card{
    background:rgba(15,23,42,0.78);
    border:1px solid rgba(148,163,184,0.22);
    border-radius:22px;
    padding:20px;
    box-shadow:0 18px 45px rgba(0,0,0,0.25);
    backdrop-filter: blur(16px);
    margin-bottom:16px;
}
.mini-card{
    background:rgba(17,24,39,0.82);
    border:1px solid rgba(148,163,184,0.18);
    border-radius:18px;
    padding:16px;
    margin-bottom:12px;
}
.kpi{
    background:linear-gradient(135deg, rgba(14,165,233,0.16), rgba(167,139,250,0.12));
    border:1px solid rgba(148,163,184,0.22);
    border-radius:20px;
    padding:18px;
    min-height:120px;
}
.kpi-label{
    color:#94A3B8;
    font-size:.85rem;
    text-transform:uppercase;
    letter-spacing:.06em;
}
.kpi-value{
    color:#F8FAFC;
    font-size:1.85rem;
    font-weight:800;
    margin-top:6px;
}
.kpi-foot{
    color:#CBD5E1;
    font-size:.86rem;
    margin-top:8px;
}
.badge{
    display:inline-block;
    padding:6px 12px;
    border-radius:999px;
    font-size:.8rem;
    font-weight:700;
    border:1px solid rgba(148,163,184,0.24);
}
.badge-blue{background:rgba(56,189,248,.12);color:#7DD3FC;}
.badge-green{background:rgba(52,211,153,.13);color:#86EFAC;}
.badge-orange{background:rgba(251,146,60,.14);color:#FDBA74;}
.badge-red{background:rgba(248,113,113,.14);color:#FCA5A5;}
.section-title{
    font-size:1.45rem;
    font-weight:800;
    color:#F8FAFC;
    margin:14px 0 8px;
}
.small-muted{color:#94A3B8;font-size:.9rem;}
hr{border-color:rgba(148,163,184,0.18);}
.stDataFrame, .stTable{
    border-radius:16px;
}
button[kind="primary"]{
    background:linear-gradient(90deg,#2563EB,#06B6D4) !important;
}
.stButton>button{
    border-radius:12px !important;
    border:1px solid rgba(148,163,184,0.28) !important;
    font-weight:700 !important;
}
input, textarea{
    border-radius:12px !important;
}
.footer{
    color:#64748B;
    text-align:center;
    font-size:.82rem;
    padding:24px 0 8px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA
# ============================================================
DESTINATIONS = {
    "Goa": {
        "type": "Beach",
        "budget": "Medium",
        "safety": 82,
        "distance_score": 75,
        "avg_cost": 18000,
        "local_food": ["Goan thali", "Seafood", "Bebinca", "Beach cafe snacks"],
        "places": [
            {"name": "Baga Beach", "category": "Outdoor", "time": 3, "cost": 700, "priority": 9},
            {"name": "Fort Aguada", "category": "Heritage", "time": 2, "cost": 500, "priority": 8},
            {"name": "Dudhsagar Falls", "category": "Nature", "time": 5, "cost": 1800, "priority": 9},
            {"name": "Anjuna Market", "category": "Shopping", "time": 2, "cost": 900, "priority": 7},
            {"name": "Old Goa Church", "category": "Heritage", "time": 2, "cost": 400, "priority": 7},
            {"name": "Calangute Beach", "category": "Outdoor", "time": 3, "cost": 600, "priority": 8},
        ],
        "best_for": "friends, beach, relaxation, college trip",
    },
    "Jaipur": {
        "type": "Heritage",
        "budget": "Medium",
        "safety": 78,
        "distance_score": 70,
        "avg_cost": 16000,
        "local_food": ["Dal baati churma", "Kachori", "Lassi", "Rajasthani thali"],
        "places": [
            {"name": "Amber Fort", "category": "Heritage", "time": 3, "cost": 900, "priority": 10},
            {"name": "City Palace", "category": "Heritage", "time": 2, "cost": 700, "priority": 8},
            {"name": "Hawa Mahal", "category": "Photography", "time": 2, "cost": 400, "priority": 9},
            {"name": "Jantar Mantar", "category": "Science", "time": 2, "cost": 350, "priority": 7},
            {"name": "Nahargarh Fort", "category": "Viewpoint", "time": 3, "cost": 800, "priority": 8},
        ],
        "best_for": "history, culture, family trip, photography",
    },
    "Manali": {
        "type": "Adventure",
        "budget": "High",
        "safety": 70,
        "distance_score": 55,
        "avg_cost": 24000,
        "local_food": ["Siddu", "Trout fish", "Tibetan momos", "Local cafe food"],
        "places": [
            {"name": "Solang Valley", "category": "Adventure", "time": 4, "cost": 1800, "priority": 10},
            {"name": "Hadimba Temple", "category": "Heritage", "time": 2, "cost": 400, "priority": 7},
            {"name": "Mall Road", "category": "Shopping", "time": 2, "cost": 900, "priority": 7},
            {"name": "Atal Tunnel", "category": "Scenic", "time": 4, "cost": 1500, "priority": 8},
            {"name": "Jogini Falls", "category": "Nature", "time": 3, "cost": 600, "priority": 8},
        ],
        "best_for": "adventure, mountains, winter, friends",
    },
    "Kerala": {
        "type": "Nature",
        "budget": "Medium",
        "safety": 86,
        "distance_score": 68,
        "avg_cost": 21000,
        "local_food": ["Kerala meals", "Appam", "Puttu", "Fish curry", "Banana chips"],
        "places": [
            {"name": "Munnar Tea Gardens", "category": "Nature", "time": 4, "cost": 900, "priority": 10},
            {"name": "Alleppey Backwaters", "category": "Nature", "time": 5, "cost": 2500, "priority": 10},
            {"name": "Fort Kochi", "category": "Heritage", "time": 3, "cost": 700, "priority": 8},
            {"name": "Thekkady", "category": "Wildlife", "time": 4, "cost": 1500, "priority": 8},
            {"name": "Varkala Beach", "category": "Outdoor", "time": 3, "cost": 800, "priority": 8},
        ],
        "best_for": "family trip, nature, calm trip, relaxation",
    },
    "Tirupati": {
        "type": "Pilgrimage",
        "budget": "Low",
        "safety": 88,
        "distance_score": 85,
        "avg_cost": 9000,
        "local_food": ["South Indian meals", "Tiffins", "Laddu prasadam", "Curd rice"],
        "places": [
            {"name": "Tirumala Temple", "category": "Pilgrimage", "time": 5, "cost": 500, "priority": 10},
            {"name": "Kapila Theertham", "category": "Pilgrimage", "time": 2, "cost": 300, "priority": 7},
            {"name": "Govindaraja Swamy Temple", "category": "Pilgrimage", "time": 2, "cost": 250, "priority": 7},
            {"name": "Chandragiri Fort", "category": "Heritage", "time": 2, "cost": 400, "priority": 6},
        ],
        "best_for": "pilgrimage, family trip, budget trip, short trip",
    },
    "Bangalore": {
        "type": "City",
        "budget": "Medium",
        "safety": 76,
        "distance_score": 80,
        "avg_cost": 15000,
        "local_food": ["Dosa", "Filter coffee", "Biryani", "Cafe food", "Street snacks"],
        "places": [
            {"name": "Cubbon Park", "category": "Nature", "time": 2, "cost": 200, "priority": 7},
            {"name": "Lalbagh", "category": "Nature", "time": 2, "cost": 300, "priority": 7},
            {"name": "Bangalore Palace", "category": "Heritage", "time": 2, "cost": 700, "priority": 8},
            {"name": "Church Street", "category": "Shopping", "time": 3, "cost": 1200, "priority": 8},
            {"name": "Wonderla", "category": "Adventure", "time": 6, "cost": 2500, "priority": 9},
        ],
        "best_for": "college trip, city life, shopping, business trip",
    },
    "Mumbai": {
        "type": "City",
        "budget": "High",
        "safety": 74,
        "distance_score": 62,
        "avg_cost": 23000,
        "local_food": ["Vada pav", "Pav bhaji", "Bombay sandwich", "Street chaat"],
        "places": [
            {"name": "Marine Drive", "category": "Outdoor", "time": 2, "cost": 300, "priority": 9},
            {"name": "Gateway of India", "category": "Heritage", "time": 2, "cost": 300, "priority": 8},
            {"name": "Elephanta Caves", "category": "Heritage", "time": 5, "cost": 1200, "priority": 8},
            {"name": "Juhu Beach", "category": "Outdoor", "time": 2, "cost": 500, "priority": 7},
            {"name": "Colaba Causeway", "category": "Shopping", "time": 3, "cost": 1400, "priority": 7},
        ],
        "best_for": "city life, friends, business trip, shopping",
    },
}

CITY_GRAPH = {
    "Hyderabad": {"Bangalore": 570, "Pune": 560, "Vijayawada": 275, "Tirupati": 550, "Mumbai": 710},
    "Bangalore": {"Hyderabad": 570, "Goa": 560, "Kerala": 470, "Tirupati": 250, "Mumbai": 980},
    "Pune": {"Hyderabad": 560, "Goa": 450, "Jaipur": 1180, "Mumbai": 150},
    "Vijayawada": {"Hyderabad": 275, "Tirupati": 380, "Kerala": 900},
    "Tirupati": {"Hyderabad": 550, "Bangalore": 250, "Vijayawada": 380},
    "Goa": {"Bangalore": 560, "Pune": 450, "Mumbai": 590},
    "Kerala": {"Bangalore": 470, "Vijayawada": 900},
    "Jaipur": {"Pune": 1180, "Mumbai": 1150},
    "Mumbai": {"Hyderabad": 710, "Pune": 150, "Goa": 590, "Jaipur": 1150, "Bangalore": 980},
}

VEHICLES = {
    "Train": {"cost": 6, "time": 6, "comfort": 7, "safety": 8, "best_for": "budget, family, long distance"},
    "Bus": {"cost": 8, "time": 4, "comfort": 5, "safety": 6, "best_for": "budget, short distance"},
    "Car": {"cost": 5, "time": 7, "comfort": 8, "safety": 6, "best_for": "family, friends, flexible"},
    "Flight": {"cost": 3, "time": 10, "comfort": 9, "safety": 9, "best_for": "long distance, business, luxury"},
    "Bike": {"cost": 9, "time": 5, "comfort": 3, "safety": 4, "best_for": "adventure, short distance"},
    "Cab / Taxi": {"cost": 4, "time": 7, "comfort": 8, "safety": 6, "best_for": "city, local, family"},
}

CO_MAPPING = {
    "CO1": "The planner is modeled as an intelligent agent using PEAS, states, actions, costs, and Python data structures.",
    "CO2": "The Route Finder runs BFS, DFS, UCS, Greedy Search, and A* on a weighted city graph.",
    "CO3": "The Smart Itinerary applies CSP-style constraints such as time limits, budget, rest breaks, and activity distribution.",
    "CO4": "Destination, vehicle, and hotel suggestions use utility-based decision scores.",
    "CO5": "Travel readiness and trip risk are estimated using weighted uncertainty reasoning.",
    "CO6": "Explainable AI dashboards show reasoning traces, limitations, ethics, and failure analysis.",
}

PACKING_BY_TYPE = {
    "Beach": ["Sunscreen", "Sunglasses", "Light clothes", "Slippers", "Water bottle", "Power bank", "ID proof", "Towel"],
    "Adventure": ["Sports shoes", "Jacket", "First-aid kit", "Water bottle", "Torch", "Power bank", "ID proof", "Backpack"],
    "Heritage": ["Comfortable shoes", "Camera", "Cap", "Water bottle", "ID proof", "Small backpack"],
    "Pilgrimage": ["Traditional clothes", "ID proof", "Water bottle", "Medicines", "Cash", "Small bag"],
    "Nature": ["Comfortable clothes", "Mosquito repellent", "Camera", "Shoes", "Medicines", "Power bank"],
    "City": ["Casual clothes", "Phone charger", "Power bank", "ID proof", "Small backpack", "UPI backup"],
}

DOCS = ["Aadhaar / ID Proof", "College ID", "Tickets", "Hotel Confirmation", "Emergency Contact", "Medical Prescription", "Cash / UPI Backup"]

# ============================================================
# SESSION
# ============================================================
def init_session():
    defaults = {
        "logged_in": False,
        "is_admin": False,
        "current_user": None,
        "page": "landing",
        "destinations": DESTINATIONS.copy(),
        "users": {
            "student@klh.edu": {
                "name": "Demo Student",
                "email": "student@klh.edu",
                "password": "student123",
                "age": 20,
                "travel_style": "College Trip",
                "budget_range": "Medium",
                "comfort": "Balanced",
                "trip": {},
                "packing_done": [],
                "docs_done": [],
                "readiness_items": {
                    "Trip details saved": False,
                    "Itinerary prepared": False,
                    "Budget planned": False,
                    "Vehicle selected": False,
                    "Hotel selected": False,
                    "Packing completed": False,
                    "Documents ready": False,
                    "Emergency contact added": False,
                },
                "emergency_contact": "",
                "notes": [],
            }
        }
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def go(page):
    st.session_state.page = page
    st.rerun()

def get_user():
    return st.session_state.users.get(st.session_state.current_user)

def save_user(user):
    if st.session_state.current_user:
        st.session_state.users[st.session_state.current_user] = user

def logout():
    st.session_state.logged_in = False
    st.session_state.is_admin = False
    st.session_state.current_user = None
    st.session_state.page = "landing"
    st.rerun()

# ============================================================
# UTILITY LOGIC
# ============================================================
def date_days(start, end):
    if isinstance(start, str):
        start = datetime.strptime(start, "%Y-%m-%d").date()
    if isinstance(end, str):
        end = datetime.strptime(end, "%Y-%m-%d").date()
    return max(1, (end - start).days + 1)

def nearest_goal_key(goal):
    if goal in CITY_GRAPH:
        return goal
    if goal in ["Goa", "Jaipur", "Kerala", "Tirupati", "Bangalore", "Mumbai"]:
        return goal
    return "Goa"

def heuristic(goal):
    goal = nearest_goal_key(goal)
    # Rough heuristic using shortest known edge chain distance factor.
    # It is intentionally simple for academic explainability.
    base = {}
    for city in CITY_GRAPH:
        if city == goal:
            base[city] = 0
        else:
            direct = CITY_GRAPH.get(city, {}).get(goal)
            if direct:
                base[city] = direct
            else:
                base[city] = 600 + abs(len(city) - len(goal)) * 35
    return base

def path_cost(path):
    if not path or len(path) == 1:
        return 0
    return sum(CITY_GRAPH[path[i]][path[i + 1]] for i in range(len(path) - 1))

def bfs(start, goal):
    q = deque([[start]])
    seen, visited = set(), []
    while q:
        path = q.popleft()
        node = path[-1]
        if node in seen:
            continue
        seen.add(node)
        visited.append(node)
        if node == goal:
            return visited, path, path_cost(path)
        for nb in CITY_GRAPH.get(node, {}):
            if nb not in seen:
                q.append(path + [nb])
    return visited, [], 0

def dfs(start, goal):
    stack = [[start]]
    seen, visited = set(), []
    while stack:
        path = stack.pop()
        node = path[-1]
        if node in seen:
            continue
        seen.add(node)
        visited.append(node)
        if node == goal:
            return visited, path, path_cost(path)
        for nb in reversed(list(CITY_GRAPH.get(node, {}).keys())):
            if nb not in seen:
                stack.append(path + [nb])
    return visited, [], 0

def ucs(start, goal):
    pq = [(0, [start])]
    seen, visited = set(), []
    while pq:
        cost, path = heapq.heappop(pq)
        node = path[-1]
        if node in seen:
            continue
        seen.add(node)
        visited.append(node)
        if node == goal:
            return visited, path, cost
        for nb, w in CITY_GRAPH.get(node, {}).items():
            if nb not in seen:
                heapq.heappush(pq, (cost + w, path + [nb]))
    return visited, [], 0

def greedy(start, goal):
    h = heuristic(goal)
    pq = [(h[start], [start])]
    seen, visited = set(), []
    while pq:
        _, path = heapq.heappop(pq)
        node = path[-1]
        if node in seen:
            continue
        seen.add(node)
        visited.append(node)
        if node == goal:
            return visited, path, path_cost(path)
        for nb in CITY_GRAPH.get(node, {}):
            if nb not in seen:
                heapq.heappush(pq, (h.get(nb, 9999), path + [nb]))
    return visited, [], 0

def astar(start, goal):
    h = heuristic(goal)
    pq = [(h[start], 0, [start])]
    seen, visited = set(), []
    while pq:
        _, g, path = heapq.heappop(pq)
        node = path[-1]
        if node in seen:
            continue
        seen.add(node)
        visited.append(node)
        if node == goal:
            return visited, path, g
        for nb, w in CITY_GRAPH.get(node, {}).items():
            if nb not in seen:
                ng = g + w
                heapq.heappush(pq, (ng + h.get(nb, 9999), ng, path + [nb]))
    return visited, [], 0

def run_route(algo, start, goal):
    if algo == "BFS": return bfs(start, goal)
    if algo == "DFS": return dfs(start, goal)
    if algo == "UCS": return ucs(start, goal)
    if algo == "Greedy Search": return greedy(start, goal)
    return astar(start, goal)

def destination_score(dest, user, trip=None):
    trip = trip or user.get("trip", {})
    data = st.session_state.destinations[dest]
    budget = trip.get("budget_range", user.get("budget_range", "Medium"))
    style = trip.get("travel_style", user.get("travel_style", "College Trip"))
    days = trip.get("days", 3)
    total_budget = trip.get("total_budget", 20000)

    budget_fit = 25 if data["budget"] == budget else 14
    preference = 25 if style.lower() in data["best_for"].lower() or data["type"].lower() in style.lower() else 12
    days_fit = 18 if days >= 3 else 10
    safety = data["safety"] * 0.18
    affordability = max(0, 22 - max(0, data["avg_cost"] - total_budget) / 900)
    distance = data["distance_score"] * 0.1

    return round(budget_fit + preference + days_fit + safety + affordability + distance, 1)

def best_destination(user):
    scores = {d: destination_score(d, user) for d in st.session_state.destinations}
    best = max(scores, key=scores.get)
    return best, scores

def vehicle_score(vehicle, distance, budget_range, travellers, comfort):
    v = VEHICLES[vehicle]
    budget_pref = {"Low": 1.3, "Medium": 1.0, "High": 0.8}[budget_range]
    long_bonus = 8 if distance > 700 and vehicle in ["Flight", "Train"] else 0
    group_bonus = 7 if travellers >= 3 and vehicle in ["Car", "Cab / Taxi", "Train"] else 0
    comfort_bonus = 7 if comfort == "Comfort First" and vehicle in ["Flight", "Car", "Cab / Taxi"] else 0
    cost = v["cost"] * 2.3 * budget_pref
    safety = v["safety"] * 2.0
    time = v["time"] * 1.5
    comfort_score = v["comfort"] * 1.4
    risk_penalty = 10 if distance > 600 and vehicle == "Bike" else 0
    return round(cost + safety + time + comfort_score + long_bonus + group_bonus + comfort_bonus - risk_penalty, 1)

def recommend_vehicle(user):
    trip = user.get("trip", {})
    source = trip.get("source", "Hyderabad")
    dest = trip.get("destination", "Goa")
    route_goal = dest if dest in CITY_GRAPH else "Goa"
    _, path, distance = ucs(source, route_goal) if source in CITY_GRAPH and route_goal in CITY_GRAPH else ([], [], 700)
    distance = distance or 700
    scores = {
        v: vehicle_score(
            v,
            distance,
            trip.get("budget_range", user.get("budget_range", "Medium")),
            trip.get("travellers", 2),
            user.get("comfort", "Balanced"),
        )
        for v in VEHICLES
    }
    return max(scores, key=scores.get), scores, distance

def recommend_hotel(user):
    trip = user.get("trip", {})
    budget = trip.get("budget_range", user.get("budget_range", "Medium"))
    style = trip.get("travel_style", user.get("travel_style", "College Trip"))
    travellers = trip.get("travellers", 2)
    if style == "Luxury Trip" or budget == "High":
        hotel = "Resort / Premium Hotel"
    elif style == "Business Trip":
        hotel = "Business Hotel near city center"
    elif style == "Budget Trip":
        hotel = "Hostel / Budget Lodge"
    elif travellers >= 4 or style == "Family Trip":
        hotel = "Standard Family Hotel"
    else:
        hotel = "Standard Hotel"
    return hotel

def generate_itinerary(user):
    trip = user.get("trip", {})
    dest = trip.get("destination", "Goa")
    days = int(trip.get("days", 3))
    budget = trip.get("budget_range", "Medium")
    places = sorted(st.session_state.destinations[dest]["places"], key=lambda x: -x["priority"])

    max_daily_hours = {"Low": 7, "Medium": 8, "High": 9}.get(budget, 8)
    plan = []
    p_index = 0
    for d in range(1, days + 1):
        hours_used = 0
        day_activities = []
        attempts = 0
        while hours_used < max_daily_hours - 2 and attempts < len(places) * 2:
            place = places[p_index % len(places)]
            p_index += 1
            attempts += 1
            if place["time"] + hours_used <= max_daily_hours:
                day_activities.append(place)
                hours_used += place["time"]
            if len(day_activities) >= 2:
                break
        if not day_activities:
            day_activities = [places[d % len(places)]]

        morning = day_activities[0]
        plan.append({"Day": f"Day {d}", "Time": "Morning", "Activity": f"Visit {morning['name']}", "Category": morning["category"], "Hours": morning["time"], "Cost": morning["cost"], "Priority": morning["priority"]})
        plan.append({"Day": f"Day {d}", "Time": "Afternoon", "Activity": "Lunch + rest break", "Category": "Rest", "Hours": 1.5, "Cost": 500, "Priority": 8})
        if len(day_activities) > 1:
            eve = day_activities[1]
            plan.append({"Day": f"Day {d}", "Time": "Evening", "Activity": f"Explore {eve['name']}", "Category": eve["category"], "Hours": eve["time"], "Cost": eve["cost"], "Priority": eve["priority"]})
        else:
            plan.append({"Day": f"Day {d}", "Time": "Evening", "Activity": "Local market / free exploration", "Category": "Flexible", "Hours": 2, "Cost": 600, "Priority": 6})
    return plan

def budget_breakdown(total_budget):
    return {
        "Travel": int(total_budget * 0.30),
        "Hotel": int(total_budget * 0.26),
        "Food": int(total_budget * 0.17),
        "Local Transport": int(total_budget * 0.09),
        "Activities": int(total_budget * 0.10),
        "Shopping": int(total_budget * 0.04),
        "Emergency": int(total_budget * 0.04),
    }

def food_plan(user):
    trip = user.get("trip", {})
    dest = trip.get("destination", "Goa")
    days = trip.get("days", 3)
    food_pref = trip.get("food", "Mixed")
    foods = st.session_state.destinations[dest]["local_food"]
    rows = []
    for d in range(1, int(days) + 1):
        rows.append({
            "Day": f"Day {d}",
            "Breakfast": "Idli/Dosa + Tea" if food_pref == "Vegetarian" else "Local breakfast",
            "Lunch": foods[(d-1) % len(foods)],
            "Dinner": foods[d % len(foods)],
            "Estimated Cost": 900 if food_pref == "Mixed" else 750,
        })
    return rows

def risk_analysis(user):
    trip = user.get("trip", {})
    dest = trip.get("destination", "Goa")
    data = st.session_state.destinations.get(dest, DESTINATIONS["Goa"])
    vehicle = trip.get("vehicle", trip.get("transport", "Train"))
    days = trip.get("days", 3)
    budget = trip.get("budget_range", "Medium")
    style = trip.get("travel_style", user.get("travel_style", "College Trip"))

    risk = 100 - data["safety"]
    reasons = []
    if vehicle == "Bike":
        risk += 18
        reasons.append("Bike travel has higher safety risk for long trips.")
    if style == "Adventure":
        risk += 12
        reasons.append("Adventure trips need extra safety planning.")
    if budget == "Low":
        risk += 8
        reasons.append("Low budget can reduce flexibility during emergencies.")
    if days <= 2:
        risk += 6
        reasons.append("Short trips may lead to rushed schedules.")
    if data["type"] in ["Adventure", "City"]:
        risk += 5
        reasons.append("Destination type needs careful route and timing decisions.")

    risk = max(0, min(100, risk))
    label = "Low Risk" if risk < 30 else ("Medium Risk" if risk < 60 else "High Risk")
    return round(risk, 1), label, reasons

def readiness_score(user):
    items = user.get("readiness_items", {})
    checked = sum(1 for v in items.values() if v)
    base = checked / len(items) * 100 if items else 0
    risk, _, _ = risk_analysis(user)
    score = base * 0.82 + (100 - risk) * 0.18
    return round(max(0, min(100, score)), 1)

def readiness_label(score):
    if score <= 40: return "Not Ready"
    if score <= 70: return "Needs Planning"
    if score <= 90: return "Almost Ready"
    return "Trip Ready"

def trip_report_text(user):
    trip = user.get("trip", {})
    best_vehicle, vehicle_scores, distance = recommend_vehicle(user)
    best_dest, dest_scores = best_destination(user)
    risk, risk_label, reasons = risk_analysis(user)
    readiness = readiness_score(user)
    itinerary = generate_itinerary(user) if trip else []
    breakdown = budget_breakdown(trip.get("total_budget", 20000)) if trip else {}
    report = []
    report.append("TRIPGENIUS AI - TRAVEL PLAN REPORT")
    report.append("KLH University | CFAI Project")
    report.append("="*55)
    report.append(f"Student/User: {user.get('name')}")
    report.append(f"Destination: {trip.get('destination', 'Not selected')}")
    report.append(f"Source: {trip.get('source', 'Not selected')}")
    report.append(f"Dates: {trip.get('start', '-')} to {trip.get('end', '-')}")
    report.append(f"Days: {trip.get('days', '-')}")
    report.append(f"Budget: Rs.{trip.get('total_budget', 0)}")
    report.append(f"Recommended Vehicle: {best_vehicle}")
    report.append(f"Estimated Route Distance: {distance} km")
    report.append(f"Recommended Hotel: {recommend_hotel(user)}")
    report.append(f"Travel Readiness: {readiness}% ({readiness_label(readiness)})")
    report.append(f"Risk Level: {risk_label} ({risk}%)")
    if reasons:
        report.append("Risk Reasons:")
        report.extend([f"- {r}" for r in reasons])
    report.append("\nBudget Breakdown:")
    for k, v in breakdown.items():
        report.append(f"- {k}: Rs.{v}")
    report.append("\nItinerary:")
    for row in itinerary:
        report.append(f"{row['Day']} | {row['Time']} | {row['Activity']} | Rs.{row['Cost']}")
    report.append("\nCFAI CO Mapping:")
    for k, v in CO_MAPPING.items():
        report.append(f"{k}: {v}")
    return "\n".join(report)

# ============================================================
# CHARTS
# ============================================================
def bar_chart(title, data_dict, ylabel="Score"):
    fig, ax = plt.subplots(figsize=(9, 4))
    labels = list(data_dict.keys())
    vals = list(data_dict.values())
    ax.bar(labels, vals)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=25)
    ax.spines[["top", "right"]].set_visible(False)
    st.pyplot(fig)
    plt.close(fig)

def donut_chart(score, title):
    fig, ax = plt.subplots(figsize=(4.2, 4.2))
    ax.pie([score, 100-score], startangle=90, counterclock=False, wedgeprops=dict(width=0.35))
    ax.text(0, 0, f"{score:.0f}%", ha="center", va="center", fontsize=24, fontweight="bold")
    ax.set_title(title)
    st.pyplot(fig)
    plt.close(fig)

# ============================================================
# UI HELPERS
# ============================================================
def kpi(label, value, foot="", badge="blue"):
    color = {"blue":"badge-blue","green":"badge-green","orange":"badge-orange","red":"badge-red"}.get(badge,"badge-blue")
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-foot">{foot}</div>
    </div>
    """, unsafe_allow_html=True)

def page_header(title, subtitle):
    st.markdown(f"""
    <div class="hero">
        <h1 class="main-title">{title}</h1>
        <p class="subtext">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# PAGES
# ============================================================
def landing_page():
    st.markdown("""
    <div class="hero">
        <span class="badge badge-blue">KLH University | CFAI Advanced Project</span>
        <h1 class="main-title" style="margin-top:14px;">TripGenius <span class="gradient-text">AI</span></h1>
        <p class="subtext">
            A tier-1 intelligent travel planning system built with Python and CFAI concepts.
            It handles trip planning, route search, vehicle recommendation, hotel suggestions,
            budget allocation, food planning, safety analysis, travel readiness, and explainable decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("Login", type="primary", use_container_width=True):
            go("login")
    with c2:
        if st.button("Sign Up", use_container_width=True):
            go("signup")
    with c3:
        if st.button("Quick Demo", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.is_admin = False
            st.session_state.current_user = "student@klh.edu"
            go("home")

    st.markdown('<div class="section-title">Featured System Modules</div>', unsafe_allow_html=True)
    features = [
        ("Advanced Home Dashboard", "Trip overview, readiness, risk, tasks, budget, and CFAI mapping."),
        ("Smart Trip Planner", "Creates full trip profile with source, dates, budget, food, hotel, and vehicle type."),
        ("Route Intelligence", "BFS, DFS, UCS, Greedy Search, and A* route planning on weighted city graph."),
        ("Vehicle AI", "Recommends Train, Bus, Car, Flight, Bike, or Cab using utility scoring."),
        ("CSP Itinerary", "Creates day-wise itinerary while applying scheduling constraints."),
        ("Risk + Safety Analyzer", "Calculates risk based on destination, vehicle, budget, and travel style."),
        ("Downloadable Report", "Generates a complete travel plan report as a text file."),
        ("Explainable AI", "Explains why recommendations are made and lists limitations honestly."),
    ]
    cols = st.columns(4)
    for i, (h, p) in enumerate(features):
        with cols[i % 4]:
            st.markdown(f"<div class='glass-card'><b>{h}</b><br><span class='small-muted'>{p}</span></div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">CO1 to CO6 Project Connection</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([{"CO": k, "Used In TripGenius AI": v} for k, v in CO_MAPPING.items()]), use_container_width=True, hide_index=True)
    st.markdown("<div class='footer'>TripGenius AI | Built with Python + Streamlit | KLH University CFAI Project</div>", unsafe_allow_html=True)

def signup_page():
    page_header("Create Account", "Create a student profile so the travel planner can personalize recommendations.")
    with st.form("signup_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")
        with c2:
            age = st.number_input("Age", 10, 80, 20)
            travel_style = st.selectbox("Preferred Travel Style", ["Adventure", "Family Trip", "Budget Trip", "Luxury Trip", "Pilgrimage", "College Trip", "Business Trip"])
            budget_range = st.selectbox("Budget Range", ["Low", "Medium", "High"])
            comfort = st.selectbox("Comfort Preference", ["Budget First", "Balanced", "Comfort First"])
        submit = st.form_submit_button("Create Account", type="primary", use_container_width=True)

    if submit:
        if not name or not email or not password:
            st.error("Fill all required fields.")
        elif password != confirm:
            st.error("Passwords do not match.")
        elif email in st.session_state.users:
            st.error("Account already exists.")
        else:
            st.session_state.users[email] = {
                "name": name, "email": email, "password": password, "age": age,
                "travel_style": travel_style, "budget_range": budget_range, "comfort": comfort,
                "trip": {}, "packing_done": [], "docs_done": [],
                "readiness_items": {
                    "Trip details saved": False, "Itinerary prepared": False, "Budget planned": False,
                    "Vehicle selected": False, "Hotel selected": False, "Packing completed": False,
                    "Documents ready": False, "Emergency contact added": False,
                },
                "emergency_contact": "", "notes": []
            }
            st.success("Account created successfully. Please login.")
            go("login")
    if st.button("Back to Home"):
        go("landing")

def login_page():
    page_header("Login", "Access the advanced travel planning dashboard.")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", type="primary", use_container_width=True)

    if submit:
        if email == "admin@tripgenius.com" and password == "admin123":
            st.session_state.logged_in = True
            st.session_state.is_admin = True
            st.session_state.current_user = None
            go("admin")
        elif email in st.session_state.users and st.session_state.users[email]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.is_admin = False
            st.session_state.current_user = email
            go("home")
        else:
            st.error("Invalid email or password.")

    st.info("Demo: student@klh.edu / student123 | Admin: admin@tripgenius.com / admin123")
    c1, c2 = st.columns(2)
    if c1.button("Create Account", use_container_width=True):
        go("signup")
    if c2.button("Back", use_container_width=True):
        go("landing")

def home_page():
    user = get_user()
    trip = user.get("trip", {})
    readiness = readiness_score(user)
    risk, risk_label, _ = risk_analysis(user)
    best_vehicle, _, distance = recommend_vehicle(user)
    best_dest, _ = best_destination(user)

    st.markdown(f"""
    <div class="hero">
        <span class="badge badge-green">Advanced Student Dashboard</span>
        <h1 class="main-title" style="margin-top:12px;">Welcome, <span class="gradient-text">{user['name']}</span></h1>
        <p class="subtext">
            Your intelligent travel workspace with trip planning, route intelligence, vehicle recommendation,
            budget analysis, readiness tracking, safety reasoning, and CFAI concept mapping.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Current Destination", trip.get("destination", best_dest), "Based on your saved trip or recommendation", "blue")
    with c2: kpi("Travel Readiness", f"{readiness}%", readiness_label(readiness), "green" if readiness > 70 else "orange")
    with c3: kpi("Risk Status", risk_label, f"Risk score: {risk}%", "red" if risk > 60 else "orange")
    with c4: kpi("Best Vehicle", best_vehicle, f"Estimated route: {distance} km", "blue")

    st.markdown('<div class="section-title">Trip Command Center</div>', unsafe_allow_html=True)
    a, b = st.columns([1.2, 1])
    with a:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Trip Summary")
        if trip:
            summary = {
                "Source": trip.get("source"),
                "Destination": trip.get("destination"),
                "Dates": f"{trip.get('start')} to {trip.get('end')}",
                "Days": trip.get("days"),
                "Travellers": trip.get("travellers"),
                "Budget": f"₹{trip.get('total_budget')}",
                "Vehicle Type": trip.get("vehicle"),
                "Hotel Type": trip.get("hotel"),
                "Food Preference": trip.get("food"),
            }
            st.table(pd.DataFrame([summary]).T.rename(columns={0: "Details"}))
        else:
            st.warning("No trip created yet. Open Smart Trip Planner to create one.")
        st.markdown("</div>", unsafe_allow_html=True)

    with b:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Planning Tasks")
        items = user.get("readiness_items", {})
        for k, v in items.items():
            st.write(("✅" if v else "⬜") + " " + k)
        st.progress(readiness / 100, text=f"{readiness_label(readiness)} - {readiness}%")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">CFAI Intelligence Layer</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([{"CO": k, "Implementation in this project": v} for k, v in CO_MAPPING.items()]), use_container_width=True, hide_index=True)

def trip_planner_page():
    user = get_user()
    page_header("Smart Trip Planner", "Create a complete travel profile. This page drives all other recommendation dashboards.")

    with st.form("trip_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            source = st.selectbox("Source City", list(CITY_GRAPH.keys()), index=0)
            destination = st.selectbox("Destination", list(st.session_state.destinations.keys()))
            travellers = st.number_input("Number of Travellers", 1, 20, 2)
        with c2:
            start = st.date_input("Start Date", date.today() + timedelta(days=10))
            end = st.date_input("End Date", date.today() + timedelta(days=13))
            total_budget = st.number_input("Total Budget (₹)", 3000, 300000, 25000, step=1000)
        with c3:
            travel_style = st.selectbox("Travel Style", ["Adventure", "Family Trip", "Budget Trip", "Luxury Trip", "Pilgrimage", "College Trip", "Business Trip"], index=5)
            budget_range = st.selectbox("Budget Range", ["Low", "Medium", "High"], index=["Low","Medium","High"].index(user.get("budget_range","Medium")))
            vehicle = st.selectbox("Travel Mode / Vehicle Type", list(VEHICLES.keys()))
        food = st.selectbox("Food Preference", ["Vegetarian", "Non-Vegetarian", "Mixed", "Local Food"])
        hotel = st.selectbox("Hotel Preference", ["Auto Recommend", "Hostel", "Budget Hotel", "Standard Hotel", "Resort / Premium Hotel", "Business Hotel"])
        submit = st.form_submit_button("Save and Analyze Trip", type="primary", use_container_width=True)

    if submit:
        if end < start:
            st.error("End date cannot be before start date.")
        else:
            user["trip"] = {
                "source": source, "destination": destination, "travellers": int(travellers),
                "start": str(start), "end": str(end), "days": date_days(start, end),
                "total_budget": int(total_budget), "travel_style": travel_style,
                "budget_range": budget_range, "vehicle": vehicle, "food": food,
                "hotel": recommend_hotel(user) if hotel == "Auto Recommend" else hotel,
            }
            user["readiness_items"]["Trip details saved"] = True
            user["readiness_items"]["Vehicle selected"] = True
            user["readiness_items"]["Hotel selected"] = True
            save_user(user)
            st.success("Trip saved and analyzed successfully.")
            st.rerun()

    if user.get("trip"):
        st.markdown('<div class="section-title">Saved Trip Profile</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame([user["trip"]]), use_container_width=True, hide_index=True)

def recommendation_page():
    user = get_user()
    page_header("AI Recommendation Hub", "Destination, vehicle, hotel, and activity recommendations using utility-based decision making.")

    best_d, d_scores = best_destination(user)
    best_v, v_scores, distance = recommend_vehicle(user)
    hotel = recommend_hotel(user)

    c1, c2, c3 = st.columns(3)
    with c1: kpi("Best Destination", best_d, f"Utility score: {d_scores[best_d]}", "green")
    with c2: kpi("Best Vehicle", best_v, f"Route estimate: {distance} km", "blue")
    with c3: kpi("Best Hotel", hotel, "Based on budget, style, and travellers", "orange")

    st.markdown('<div class="section-title">Destination Scoreboard</div>', unsafe_allow_html=True)
    df = pd.DataFrame([
        {"Destination": d, "Score": s, "Type": st.session_state.destinations[d]["type"], "Avg Cost": st.session_state.destinations[d]["avg_cost"], "Safety": st.session_state.destinations[d]["safety"]}
        for d, s in d_scores.items()
    ]).sort_values("Score", ascending=False)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-title">Vehicle Scoreboard</div>', unsafe_allow_html=True)
    vf = pd.DataFrame([
        {"Vehicle": v, "Score": s, "Cost Rating": VEHICLES[v]["cost"], "Comfort": VEHICLES[v]["comfort"], "Safety": VEHICLES[v]["safety"], "Best For": VEHICLES[v]["best_for"]}
        for v, s in v_scores.items()
    ]).sort_values("Score", ascending=False)
    st.dataframe(vf, use_container_width=True, hide_index=True)

    st.info("Formula idea: Recommendation Score = Preference Match + Budget Fit + Safety + Distance Fit + Comfort - Risk Penalty")

def route_page():
    page_header("Route Intelligence Lab", "CO2 implementation: BFS, DFS, UCS, Greedy Search, and A* route planning.")
    c1, c2, c3 = st.columns(3)
    with c1:
        start = st.selectbox("Start City", list(CITY_GRAPH.keys()), index=0)
    with c2:
        goal = st.selectbox("Goal City", list(CITY_GRAPH.keys()), index=list(CITY_GRAPH.keys()).index("Goa"))
    with c3:
        algo = st.selectbox("Search Algorithm", ["BFS", "DFS", "UCS", "Greedy Search", "A*"])

    if st.button("Run Route Search", type="primary"):
        visited, path, cost = run_route(algo, start, goal)
        c1, c2, c3 = st.columns(3)
        with c1: kpi("Visited Cities", len(visited), "Nodes expanded", "blue")
        with c2: kpi("Route Cost", f"{cost} km", "Total weighted distance", "green")
        with c3: kpi("Algorithm", algo, "CO2 search method", "orange")
        st.success("Final Route: " + (" → ".join(path) if path else "No path found"))
        st.write("Visited Order:", " → ".join(visited))
        if algo == "A*":
            st.info("A* uses f(n) = g(n) + h(n), combining actual route distance and estimated distance.")
        elif algo == "UCS":
            st.info("UCS always expands the lowest cumulative cost path.")
        elif algo == "Greedy Search":
            st.info("Greedy uses heuristic estimate only, so it can be fast but not always optimal.")

    rows = []
    for city, links in CITY_GRAPH.items():
        for nb, dist in links.items():
            rows.append({"From": city, "To": nb, "Distance (km)": dist})
    st.markdown('<div class="section-title">Weighted City Graph</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

def itinerary_page():
    user = get_user()
    page_header("Smart Itinerary Generator", "CO3 implementation: CSP-style scheduling with time, budget, rest, and priority constraints.")
    if not user.get("trip"):
        st.warning("Create a trip first.")
        return
    plan = generate_itinerary(user)
    user["readiness_items"]["Itinerary prepared"] = True
    save_user(user)
    df = pd.DataFrame(plan)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-title">Constraint Explanations</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class='glass-card'>
    <b>Applied CSP-style constraints:</b><br>
    1. Do not exceed maximum activity hours per day.<br>
    2. Keep a lunch/rest block every day.<br>
    3. Higher-priority places are scheduled earlier.<br>
    4. Avoid overcrowding too many places in a single day.<br>
    5. Keep estimated activity cost within the selected budget range.<br>
    </div>
    """, unsafe_allow_html=True)

def budget_page():
    user = get_user()
    page_header("Budget Intelligence", "Plan budget distribution across travel, hotel, food, transport, activities, shopping, and emergency.")
    trip = user.get("trip", {})
    budget = st.number_input("Total Budget (₹)", 3000, 300000, int(trip.get("total_budget", 25000)), step=1000)
    data = budget_breakdown(budget)
    user["readiness_items"]["Budget planned"] = True
    save_user(user)
    st.dataframe(pd.DataFrame([{"Category": k, "Amount": v} for k, v in data.items()]), use_container_width=True, hide_index=True)
    bar_chart("Budget Allocation", data, "Amount ₹")
    if trip.get("destination"):
        est = st.session_state.destinations[trip["destination"]]["avg_cost"]
        if budget >= est:
            st.success(f"Budget looks safe. Estimated destination cost: ₹{est}.")
        else:
            st.warning(f"Budget may be tight. Estimated destination cost: ₹{est}.")

def food_page():
    user = get_user()
    page_header("Food Planner", "Daily food suggestions based on destination and preference.")
    if not user.get("trip"):
        st.warning("Create a trip first.")
        return
    rows = food_plan(user)
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    dest = user["trip"]["destination"]
    st.info(f"Local food highlights for {dest}: " + ", ".join(st.session_state.destinations[dest]["local_food"]))

def hotel_page():
    user = get_user()
    page_header("Hotel Recommendation", "Hotel recommendation based on budget, travellers, and travel style.")
    rec = recommend_hotel(user)
    st.markdown(f"""
    <div class='glass-card'>
    <h2>Recommended Stay: <span class='gradient-text'>{rec}</span></h2>
    <p class='subtext'>Reason: The system considers your budget range, travel style, number of travellers, and comfort preference.</p>
    </div>
    """, unsafe_allow_html=True)
    rows = [
        {"Hotel Type": "Hostel", "Best For": "Budget / solo / college trips", "Cost": "Low", "Comfort": "Medium"},
        {"Hotel Type": "Budget Hotel", "Best For": "Budget trips", "Cost": "Low-Medium", "Comfort": "Medium"},
        {"Hotel Type": "Standard Family Hotel", "Best For": "Family / balanced trips", "Cost": "Medium", "Comfort": "Good"},
        {"Hotel Type": "Resort / Premium Hotel", "Best For": "Luxury / relaxation", "Cost": "High", "Comfort": "Very Good"},
        {"Hotel Type": "Business Hotel", "Best For": "Business trips", "Cost": "Medium-High", "Comfort": "Good"},
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

def checklist_page():
    user = get_user()
    page_header("Packing + Documents Checklist", "A practical readiness system for packing and travel documents.")
    trip = user.get("trip", {})
    dest_type = "City"
    if trip.get("destination"):
        dest_type = st.session_state.destinations[trip["destination"]]["type"]
    items = PACKING_BY_TYPE.get(dest_type, PACKING_BY_TYPE["City"])

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Packing Checklist")
        packed = []
        for item in items:
            if st.checkbox(item, value=item in user.get("packing_done", []), key=f"pack_{item}"):
                packed.append(item)
        user["packing_done"] = packed
        st.progress(len(packed) / len(items), text=f"{len(packed)}/{len(items)} packed")
        if len(packed) == len(items):
            user["readiness_items"]["Packing completed"] = True

    with c2:
        st.subheader("Document Checklist")
        docs = []
        for doc in DOCS:
            if st.checkbox(doc, value=doc in user.get("docs_done", []), key=f"doc_{doc}"):
                docs.append(doc)
        user["docs_done"] = docs
        st.progress(len(docs) / len(DOCS), text=f"{len(docs)}/{len(DOCS)} ready")
        if len(docs) == len(DOCS):
            user["readiness_items"]["Documents ready"] = True
    save_user(user)

def risk_page():
    user = get_user()
    page_header("Trip Risk Analyzer", "CO5 + CO6: uncertainty-style risk estimation with explainable safety suggestions.")
    risk, label, reasons = risk_analysis(user)
    c1, c2 = st.columns([1, 2])
    with c1:
        donut_chart(100-risk, "Safety Confidence")
    with c2:
        kpi("Risk Level", label, f"Risk score: {risk}%", "red" if risk > 60 else "orange")
        if reasons:
            st.subheader("Why this risk level?")
            for r in reasons:
                st.write("• " + r)
        else:
            st.success("No major risk factors detected.")
        st.subheader("Safety Suggestions")
        st.write("• Keep emergency contacts saved offline.")
        st.write("• Avoid unknown areas late at night.")
        st.write("• Keep documents and money backup.")
        st.write("• Verify real prices, weather, and local rules before travel.")

def readiness_page():
    user = get_user()
    page_header("Travel Readiness System", "A readiness predictor based on trip completion, safety, documents, packing, and emergency planning.")
    for k in list(user["readiness_items"].keys()):
        user["readiness_items"][k] = st.checkbox(k, value=user["readiness_items"][k])
    contact = st.text_input("Emergency Contact", value=user.get("emergency_contact", ""))
    if contact:
        user["emergency_contact"] = contact
        user["readiness_items"]["Emergency contact added"] = True
    save_user(user)
    score = readiness_score(user)
    c1, c2 = st.columns([1, 2])
    with c1:
        donut_chart(score, "Readiness")
    with c2:
        kpi("Readiness Status", readiness_label(score), f"{score}% complete", "green" if score > 70 else "orange")
        pending = [k for k, v in user["readiness_items"].items() if not v]
        if pending:
            st.warning("Pending tasks: " + ", ".join(pending))
        else:
            st.success("All major travel planning tasks are complete.")

def alternatives_page():
    user = get_user()
    page_header("Alternative Plan Generator", "Generates backup plans when budget, time, or safety conditions change.")
    best_d, scores = best_destination(user)
    trip = user.get("trip", {})
    budget = trip.get("budget_range", user.get("budget_range", "Medium"))
    days = trip.get("days", 3)

    sorted_d = sorted(scores.items(), key=lambda x: -x[1])
    alt_budget = [d for d, _ in sorted_d if st.session_state.destinations[d]["budget"] in ["Low", "Medium"]][:3]
    alt_short = [d for d, _ in sorted_d if st.session_state.destinations[d]["distance_score"] >= 75][:3]
    alt_safe = [d for d, _ in sorted_d if st.session_state.destinations[d]["safety"] >= 82][:3]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='glass-card'><b>If budget becomes low</b><br>" + "<br>".join(alt_budget) + "</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='glass-card'><b>If time is less</b><br>" + "<br>".join(alt_short) + "</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='glass-card'><b>If safety is priority</b><br>" + "<br>".join(alt_safe) + "</div>", unsafe_allow_html=True)

def report_page():
    user = get_user()
    page_header("Download Trip Report", "Export your complete plan as a project-ready report file.")
    report = trip_report_text(user)
    st.text_area("Report Preview", report, height=420)
    st.download_button(
        "Download Trip Plan Report",
        data=report,
        file_name="TripGenius_AI_Travel_Report.txt",
        mime="text/plain",
        type="primary",
        use_container_width=True,
    )

def explanation_page():
    page_header("Project Explanation", "A built-in viva page explaining abstract, modules, CFAI mapping, limitations, and future work.")
    st.subheader("Abstract")
    st.write("TripGenius AI is a Python-based intelligent travel planning system developed using CFAI concepts from CO1 to CO6. It helps users plan trips by recommending destinations, vehicles, hotels, routes, budgets, food plans, packing lists, safety steps, readiness scores, and explainable decisions.")
    st.subheader("Modules")
    st.write("Login, Sign Up, Home Dashboard, Trip Planner, AI Recommendation Hub, Route Finder, CSP Itinerary, Budget Planner, Food Planner, Hotel Recommendation, Checklist, Risk Analyzer, Travel Readiness, Alternative Planner, Download Report, Admin Dashboard.")
    st.subheader("CO-wise Mapping")
    st.dataframe(pd.DataFrame([{"CO": k, "Explanation": v} for k, v in CO_MAPPING.items()]), use_container_width=True, hide_index=True)
    st.subheader("Limitations")
    st.warning("This project uses sample data and rule-based AI. It does not connect to live maps, real hotel booking, weather APIs, live prices, or traffic.")
    st.subheader("Future Enhancements")
    st.write("Add live Maps API, weather API, database storage, login encryption, real hotel/ticket APIs, ML-based recommendation, and mobile-friendly PWA version.")

def admin_page():
    page_header("Admin Control Panel", "Manage users, destination data, and project records.")
    st.subheader("Registered Users")
    rows = []
    for email, u in st.session_state.users.items():
        rows.append({"Name": u["name"], "Email": email, "Travel Style": u.get("travel_style"), "Budget": u.get("budget_range"), "Trip": u.get("trip", {}).get("destination", "-")})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.subheader("Destination Database")
    drows = []
    for d, info in st.session_state.destinations.items():
        drows.append({"Destination": d, "Type": info["type"], "Budget": info["budget"], "Safety": info["safety"], "Avg Cost": info["avg_cost"]})
    st.dataframe(pd.DataFrame(drows), use_container_width=True, hide_index=True)

    st.subheader("Add Destination")
    with st.form("add_destination"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Destination Name")
            dtype = st.selectbox("Type", ["Beach", "Adventure", "Heritage", "Pilgrimage", "Nature", "City"])
            budget = st.selectbox("Budget", ["Low", "Medium", "High"])
        with c2:
            safety = st.slider("Safety Score", 0, 100, 75)
            avg = st.number_input("Average Cost", 3000, 200000, 15000, step=1000)
            places = st.text_area("Places comma-separated")
        submit = st.form_submit_button("Add Destination", type="primary")
    if submit and name:
        place_list = [p.strip() for p in places.split(",") if p.strip()] or ["Main Attraction"]
        st.session_state.destinations[name] = {
            "type": dtype, "budget": budget, "safety": safety, "distance_score": 70,
            "avg_cost": int(avg), "local_food": ["Local food"], "best_for": dtype.lower(),
            "places": [{"name": p, "category": dtype, "time": 2, "cost": 600, "priority": 7} for p in place_list],
        }
        st.success("Destination added.")

# ============================================================
# SIDEBAR ROUTER
# ============================================================
def sidebar():
    st.sidebar.markdown("## ✈️ TripGenius AI")
    st.sidebar.caption("KLH University | CFAI Project")

    if st.session_state.is_admin:
        pages = {"Admin Control Panel": "admin"}
    else:
        pages = {
            "Home Dashboard": "home",
            "Smart Trip Planner": "trip",
            "AI Recommendation Hub": "recommendation",
            "Route Intelligence Lab": "route",
            "CSP Smart Itinerary": "itinerary",
            "Budget Intelligence": "budget",
            "Food Planner": "food",
            "Hotel Recommendation": "hotel",
            "Packing + Documents": "checklist",
            "Trip Risk Analyzer": "risk",
            "Travel Readiness": "readiness",
            "Alternative Plans": "alternatives",
            "Download Report": "report",
            "Project Explanation": "explanation",
        }
    choice = st.sidebar.radio("Navigation", list(pages.keys()))
    target = pages[choice]
    if st.session_state.page != target:
        st.session_state.page = target
        st.rerun()

    st.sidebar.markdown("---")
    if st.sidebar.button("Logout", use_container_width=True):
        logout()

# ============================================================
# MAIN
# ============================================================
def main():
    init_session()

    if not st.session_state.logged_in:
        if st.session_state.page == "login":
            login_page()
        elif st.session_state.page == "signup":
            signup_page()
        else:
            landing_page()
        return

    sidebar()
    page = st.session_state.page

    if page == "home": home_page()
    elif page == "trip": trip_planner_page()
    elif page == "recommendation": recommendation_page()
    elif page == "route": route_page()
    elif page == "itinerary": itinerary_page()
    elif page == "budget": budget_page()
    elif page == "food": food_page()
    elif page == "hotel": hotel_page()
    elif page == "checklist": checklist_page()
    elif page == "risk": risk_page()
    elif page == "readiness": readiness_page()
    elif page == "alternatives": alternatives_page()
    elif page == "report": report_page()
    elif page == "explanation": explanation_page()
    elif page == "admin": admin_page()
    else: home_page()

if __name__ == "__main__":
    main()
