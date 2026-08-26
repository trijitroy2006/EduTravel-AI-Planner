# EduTravel AI Planner 🎓✈️

An AI-powered, budget-optimized travel routing engine built exclusively for university students. EduTravel ensures you maximize your travel experience without exceeding your strict student budget by applying mathematical optimization and mapping algorithms.

## 🌟 Key Features

* **Strict Budget Optimization:** Utilizes a 0/1 Knapsack Dynamic Programming algorithm to allocate your exact budget across the highest-value Points of Interest (POIs).
* **Geospatial Transit Routing:** Implements the Nearest-Neighbor Traveling Salesperson Problem (TSP) algorithm using Haversine distances to create an efficient, seamless travel itinerary.
* **Student Concession Integration:** Dynamically switches pricing tiers for verified students, taking advantage of free entries and ISIC/College ID discounts.
* **Interactive Mapping:** Features an immersive Dark Mode geospatial route visualization using Folium.
* **Global Support:** Handles both Domestic (India) and International (Paris, Tokyo, Bali) study breaks.

## 🛠️ Tech Stack

* **Frontend Framework:** [Streamlit](https://streamlit.io/) (Pure Python)
* **Geospatial Mapping:** [Folium](https://python-visualization.github.io/folium/) & `streamlit-folium`
* **Data Processing:** Pandas & Math (Standard Library)
* **Algorithms:** DP Knapsack, Nearest-Neighbor TSP

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/trijitroy2006/EduTravel-AI-Planner.git
   cd EduTravel-AI-Planner
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the application:**
   ```bash
   streamlit run app.py
   ```

4. **Access the Dashboard:**
   Once running, the app will instantly be available at your local host link:
   👉 **[http://localhost:8501](http://localhost:8501)**

## 🔐 Test Credentials

Use the following credentials to bypass the Student Authentication portal:
* **Email:** `student@edu.com`
* **Password:** `password123`

---
*Built with ❤️ for student backpackers and budget travelers.*
