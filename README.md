# TripGenius AI — Advanced Travel Planner using CFAI Concepts

A Python Streamlit web application developed for KLH University CFAI project.

## Project Description

TripGenius AI is an advanced travel planning web application that applies CFAI concepts from CO1 to CO6. It helps users create trip plans, get destination recommendations, compare vehicle types, find routes using search algorithms, generate CSP-style itineraries, manage budget, plan food, select hotels, track packing/documents, analyze trip risk, calculate travel readiness, generate alternative plans, and download a full trip report.

## Major Features

- Advanced Login and Sign Up
- Home Dashboard / Command Center
- Smart Trip Planner
- AI Recommendation Hub
- Route Intelligence Lab
- Vehicle / Travel Mode Recommendation
- CSP Smart Itinerary Generator
- Budget Intelligence
- Food Planner
- Hotel Recommendation
- Packing and Document Checklist
- Trip Risk Analyzer
- Travel Readiness System
- Alternative Plan Generator
- Downloadable Trip Report
- Project Explanation / Viva Page
- Admin Control Panel

## Technologies Used

- Python
- Streamlit
- Pandas
- Matplotlib
- Heapq
- Collections
- Datetime

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Demo Login

Student:

```text
Email: student@klh.edu
Password: student123
```

Admin:

```text
Email: admin@tripgenius.com
Password: admin123
```

## CO-wise Mapping

| CO | CFAI Concept | Project Implementation |
|---|---|---|
| CO1 | Agent model, PEAS, problem formulation, Python data structures | Travel planner as intelligent agent |
| CO2 | BFS, DFS, UCS, Greedy Search, A* | Route Intelligence Lab |
| CO3 | CSP, constraints, scheduling | Smart Itinerary Generator |
| CO4 | Utility functions and decision making | Destination, vehicle, and hotel recommendations |
| CO5 | Probability and uncertainty | Risk analyzer and travel readiness score |
| CO6 | Hybrid AI, explainability, ethics | Explainable AI dashboard, limitations, and reasoning traces |

## Limitations

- Uses sample destination and route data.
- Does not connect to live maps, weather, traffic, or hotel APIs.
- Recommendations are rule-based and explainable, not machine-learning based.
- Readiness and risk scores are estimates for academic demonstration.

## Future Enhancements

- Add real-time Maps API.
- Add weather API.
- Add database storage.
- Add user authentication security.
- Add live hotel/ticket API integration.
- Add ML-based destination recommendation.
