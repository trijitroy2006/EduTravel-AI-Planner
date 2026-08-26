import streamlit as st
import math
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="EduTravel | Student Exclusive", layout="wide", page_icon="🎓", initial_sidebar_state="collapsed")

# Professional Dark Mode SaaS CSS - Full Width
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* App Background (Dark Mode) */
    .stApp {
        background-color: #0F172A; /* Slate 900 */
        color: #F8FAFC;
    }
    
    header {visibility: hidden;}
    [data-testid="collapsedControl"] {display: none;}
    
    /* Login / Register Card */
    .auth-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 8vh;
    }
    .auth-card {
        background-color: #1E293B;
        border: 1px solid #3B82F6;
        border-radius: 12px;
        padding: 3rem;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3);
        width: 100%;
        max-width: 500px;
        margin: 0 auto;
    }
    .auth-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #F8FAFC;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .auth-subheader {
        font-size: 0.95rem;
        color: #94A3B8;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Main Dashboard Styling */
    .app-header {
        font-size: 2rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.25rem;
        margin-top: -3rem;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .app-subheader {
        font-size: 1rem;
        color: #94A3B8;
        margin-bottom: 2rem;
        border-bottom: 1px solid #334155;
        padding-bottom: 15px;
    }
    .student-badge {
        background: #3B82F6;
        color: white;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        vertical-align: middle;
        margin-left: 10px;
    }

    .control-panel {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px -1px rgba(0,0,0, 0.3);
    }

    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
    }
    .kpi-title {
        color: #94A3B8;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        color: #F8FAFC;
        font-size: 2.25rem;
        font-weight: 700;
        line-height: 1.2;
    }
    .kpi-trend-positive { color: #10B981; font-size: 0.875rem; margin-top: 0.5rem; font-weight: 500;}
    .kpi-trend-neutral { color: #F59E0B; font-size: 0.875rem; margin-top: 0.5rem; font-weight: 500;}

    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #E2E8F0;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #334155;
    }
    
    .streamlit-expanderHeader { background-color: #1E293B !important; color: #F8FAFC !important; border-radius: 8px; }
    div[data-testid="stExpanderDetails"] { background-color: #0F172A !important; border: 1px solid #334155 !important; border-top: none; }
    p, li, .stMarkdown, .stText { color: #CBD5E1 !important; }
    strong { color: #F8FAFC !important; }
    .map-container { border-radius: 12px; overflow: hidden; border: 1px solid #334155; }
</style>
""", unsafe_allow_html=True)

# Application State Management
if 'users' not in st.session_state:
    st.session_state['users'] = {'student@edu.com': {'password': 'password123', 'name': 'Demo Student', 'uni': 'Global University'}}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'auth_mode' not in st.session_state:
    st.session_state['auth_mode'] = 'login' # 'login' or 'register'

# Mock Data Generation (Domestic + International)
def generate_mock_pois(destination, interests):
    cities = {
        "Jaipur": [
            {"name": "Amer Fort", "cost": 500, "student_cost": 250, "lat": 26.9855, "lon": 75.8513, "category": "Historical Study", "value": 9},
            {"name": "City Palace", "cost": 300, "student_cost": 150, "lat": 26.9258, "lon": 75.8237, "category": "Historical Study", "value": 8},
            {"name": "Bapu Bazaar", "cost": 500, "student_cost": 500, "lat": 26.9189, "lon": 75.8242, "category": "Thrift & Budget Markets", "value": 7},
            {"name": "Nahargarh Fort", "cost": 200, "student_cost": 100, "lat": 26.9373, "lon": 75.8155, "category": "Nature & Relaxation", "value": 8},
        ],
        "Delhi": [
            {"name": "Red Fort", "cost": 500, "student_cost": 250, "lat": 28.6562, "lon": 77.2410, "category": "Historical Study", "value": 9},
            {"name": "Chandni Chowk", "cost": 300, "student_cost": 300, "lat": 28.6505, "lon": 77.2303, "category": "Student Hangouts & Food", "value": 8},
            {"name": "Sarojini Nagar", "cost": 1000, "student_cost": 1000, "lat": 28.5776, "lon": 77.1968, "category": "Thrift & Budget Markets", "value": 7},
        ],
        "Paris (France)": [
            {"name": "The Louvre", "cost": 1500, "student_cost": 0, "lat": 48.8606, "lon": 2.3376, "category": "Historical Study", "value": 10}, 
            {"name": "Eiffel Tower (Stairs)", "cost": 1000, "student_cost": 500, "lat": 48.8584, "lon": 2.2945, "category": "Historical Study", "value": 9},
            {"name": "Latin Quarter Eats", "cost": 1200, "student_cost": 1200, "lat": 48.8488, "lon": 2.3434, "category": "Student Hangouts & Food", "value": 8},
            {"name": "Luxembourg Gardens", "cost": 0, "student_cost": 0, "lat": 48.8462, "lon": 2.3372, "category": "Nature & Relaxation", "value": 7},
        ],
        "Tokyo (Japan)": [
            {"name": "Senso-ji Temple", "cost": 0, "student_cost": 0, "lat": 35.7148, "lon": 139.7967, "category": "Historical Study", "value": 9},
            {"name": "Akihabara District", "cost": 2000, "student_cost": 2000, "lat": 35.6983, "lon": 139.7731, "category": "Student Hangouts & Food", "value": 8},
            {"name": "Ueno Park & Museums", "cost": 600, "student_cost": 300, "lat": 35.7141, "lon": 139.7736, "category": "Historical Study", "value": 7},
            {"name": "Shibuya Crossing", "cost": 0, "student_cost": 0, "lat": 35.6595, "lon": 139.7001, "category": "Nature & Relaxation", "value": 7},
        ],
        "Bali (Indonesia)": [
            {"name": "Uluwatu Temple", "cost": 300, "student_cost": 150, "lat": -8.8291, "lon": 115.0886, "category": "Historical Study", "value": 9},
            {"name": "Ubud Monkey Forest", "cost": 450, "student_cost": 450, "lat": -8.5194, "lon": 115.2600, "category": "Nature & Relaxation", "value": 8},
            {"name": "Canggu Surf & Eat", "cost": 800, "student_cost": 800, "lat": -8.6478, "lon": 115.1385, "category": "Student Hangouts & Food", "value": 8},
            {"name": "Campuhan Ridge Walk", "cost": 0, "student_cost": 0, "lat": -8.5036, "lon": 115.2536, "category": "Nature & Relaxation", "value": 7},
        ]
    }
    all_pois = cities.get(destination, cities["Jaipur"])
    for poi in all_pois:
        if poi["category"] in interests:
            poi["value"] += 2
    return all_pois

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def knapsack_optimization(budget, pois):
    n = len(pois)
    scale = 10
    scaled_budget = int(budget // scale)
    dp = [[0 for _ in range(scaled_budget + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, scaled_budget + 1):
            cost = int(pois[i-1]["student_cost"] // scale)
            if cost <= w:
                dp[i][w] = max(pois[i-1]['value'] + dp[i-1][w-cost], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    res = dp[n][scaled_budget]
    w = scaled_budget
    selected = []
    for i in range(n, 0, -1):
        if res <= 0: break
        if res == dp[i-1][w]: continue
        else:
            selected.append(pois[i-1])
            res -= pois[i-1]['value']
            w -= int(pois[i-1]["student_cost"] // scale)
    return selected

def tsp_nearest_neighbor(pois):
    if not pois: return []
    unvisited = pois.copy()
    current = unvisited.pop(0)
    route = [current]
    while unvisited:
        nearest = min(unvisited, key=lambda p: haversine(current["lat"], current["lon"], p["lat"], p["lon"]))
        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest
    return route

def generate_ai_narrative(day, pois):
    themes = set([p['category'] for p in pois])
    if "Historical Study" in themes: return f"Educational heritage tour — perfect for academic enrichment."
    elif "Student Hangouts & Food" in themes: return f"Local culture and budget-friendly street food hopping."
    elif "Nature & Relaxation" in themes: return f"Post-exam relaxation and scenic outdoor retreats."
    else: return f"A highly optimized mix of study breaks and sightseeing."

def auth_screen():
    st.markdown("<div class='auth-container'><div class='auth-card'>", unsafe_allow_html=True)
    st.markdown("<div class='auth-header'>🎓 EduTravel Secure Portal</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-subheader'>Verified University Student Access</div>", unsafe_allow_html=True)
    
    if st.session_state['auth_mode'] == 'login':
        with st.form("login_form"):
            email = st.text_input("University Email (.edu / .ac.in)")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login to Workspace", use_container_width=True)
            
            if submitted:
                if email in st.session_state['users'] and st.session_state['users'][email]['password'] == password:
                    st.session_state['logged_in'] = True
                    st.session_state['current_user'] = st.session_state['users'][email]
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
                    
        st.write("")
        if st.button("New student? Create an account", type="tertiary"):
            st.session_state['auth_mode'] = 'register'
            st.rerun()
            
    else:
        with st.form("register_form"):
            new_name = st.text_input("Full Name")
            new_uni = st.text_input("University / College Name")
            new_email = st.text_input("University Email")
            new_password = st.text_input("Password", type="password")
            registered = st.form_submit_button("Register Account", use_container_width=True)
            
            if registered:
                if new_email in st.session_state['users']:
                    st.error("Email already registered!")
                elif not new_email or not new_password or not new_uni:
                    st.error("Please fill all fields.")
                else:
                    st.session_state['users'][new_email] = {'password': new_password, 'name': new_name, 'uni': new_uni}
                    st.success("Registration successful! Please login.")
                    st.session_state['auth_mode'] = 'login'
                    st.rerun()
                    
        st.write("")
        if st.button("Already registered? Back to login", type="tertiary"):
            st.session_state['auth_mode'] = 'login'
            st.rerun()
            
    st.markdown("</div></div>", unsafe_allow_html=True)

def dashboard_screen():
    user = st.session_state['current_user']
    
    # ---------- FULL WIDTH HEADER ----------
    col_h1, col_h2 = st.columns([4, 1])
    with col_h1:
        st.markdown(f"<div class='app-header'><span style='color:#3B82F6;'>🎓</span> Welcome {user['name']}! <span class='student-badge'>VERIFIED</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='app-subheader'>EduTravel Global Academic Travel Optimization Engine • {user['uni']}</div>", unsafe_allow_html=True)
    with col_h2:
        if st.button("Log Out", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # ---------- HORIZONTAL CONTROL PANEL ----------
    st.markdown("<div class='control-panel'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("**1. Travel Scale**")
        travel_type = st.radio("Travel Category", ["Domestic (India)", "International (Global)"], horizontal=True)
        if travel_type == "Domestic (India)":
            destination = st.selectbox("Destination City", ["Jaipur", "Delhi"])
        else:
            destination = st.selectbox("Global Destination", ["Paris (France)", "Tokyo (Japan)", "Bali (Indonesia)"])
            
    with col2:
        st.markdown("**2. Trip Parameters**")
        days = st.slider("Semester Break Duration (Days)", 1, 7, 3)
        travelers = st.number_input("Study Group Size", min_value=1, max_value=20, value=2)
        
    with col3:
        st.markdown("**3. Student Financials (INR Eqv.)**")
        budget_input = st.number_input("Max Budget Per Student (₹)", min_value=1000, max_value=50000, value=5000, step=1000)
        total_budget = budget_input * travelers
        interests = st.multiselect(
            "Vibe & Interests", 
            ["Historical Study", "Nature & Relaxation", "Student Hangouts & Food", "Thrift & Budget Markets"],
            default=["Historical Study", "Nature & Relaxation"]
        )
        
    st.write("")
    generate_btn = st.button(f"Generate Optimized Route for {destination}", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- PROCESSING ----------
    if generate_btn:
        with st.spinner(f"Verifying {user['uni']} ISIC status & mapping {destination}..."):
            all_pois = generate_mock_pois(destination, interests)
            selected_pois = knapsack_optimization(total_budget, all_pois)
            ordered_pois = tsp_nearest_neighbor(selected_pois)
            
            if not ordered_pois:
                st.error("Constraint Violation: Your budget cap is too low to survive in this city. Increase budget.")
                st.stop()
                
            pois_per_day = max(1, len(ordered_pois) // days)
            st.session_state['itinerary'] = []
            st.session_state['ordered_pois'] = ordered_pois
            actual_total_cost = 0
            base_total_cost = 0
            
            for day in range(days):
                start_idx = day * pois_per_day
                end_idx = start_idx + pois_per_day if day < days - 1 else len(ordered_pois)
                day_pois = ordered_pois[start_idx:end_idx]
                
                day_actual_cost = sum(p["student_cost"] for p in day_pois)
                day_base_cost = sum(p['cost'] for p in day_pois)
                actual_total_cost += day_actual_cost
                base_total_cost += day_base_cost
                
                st.session_state['itinerary'].append({
                    "day": day + 1,
                    "pois": day_pois,
                    "cost": day_actual_cost,
                    "narrative": generate_ai_narrative(day + 1, day_pois)
                })
                
            st.session_state['savings'] = base_total_cost - actual_total_cost
            st.session_state['actual_total_cost'] = actual_total_cost
            st.session_state['total_budget'] = total_budget
            st.session_state['destination'] = destination

    # ---------- FULL-WIDTH RESULTS VIEW ----------
    if 'itinerary' in st.session_state:
        st.markdown(f'''
            <div class="dashboard-grid">
                <div class="kpi-card">
                    <div class="kpi-title">Verified Group Expenditure</div>
                    <div class="kpi-value">₹{st.session_state['actual_total_cost']:,}</div>
                    <div class="kpi-trend-positive">
                        <span>✅</span> Within strict {user['uni']} student limits
                    </div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">ISIC / College ID Savings</div>
                    <div class="kpi-value">₹{st.session_state['savings']:,}</div>
                    <div class="kpi-trend-neutral">
                        <span>🎓</span> Saved on international entry fees
                    </div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Optimized Study Break Waypoints</div>
                    <div class="kpi-value">{len(st.session_state['ordered_pois'])}</div>
                    <div class="kpi-trend-neutral">
                        <span>🗺️</span> TSP transit routing active
                    </div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
        
        col_left, col_right = st.columns([1, 1.5], gap="large")
        
        with col_left:
            st.markdown(f"<div class='section-title'>Generated Itinerary — {st.session_state['destination']}</div>", unsafe_allow_html=True)
            for day_plan in st.session_state['itinerary']:
                with st.expander(f"Day {day_plan['day']} Output  —  Cost: ₹{day_plan['cost']}", expanded=True):
                    st.caption(f"Vibe: {day_plan['narrative']}")
                    st.write("")
                    for i, poi in enumerate(day_plan['pois']):
                        has_discount = poi['cost'] > poi['student_cost']
                        discount_badge = " • 🏷️ `[STUDENT FREE/DISCOUNT]`" if has_discount else ""
                        st.markdown(f"**{i+1}. {poi['name']}**")
                        st.markdown(f"<span style='color:#94A3B8; font-size:14px;'>{poi['category']} | Price: ₹{poi['student_cost']} <span style='color:#3B82F6;'>{discount_badge}</span></span>", unsafe_allow_html=True)
            
            st.markdown("<br><div class='section-title'>Daily Capital Drain</div>", unsafe_allow_html=True)
            chart_df = pd.DataFrame([
                {"Timeline": f"Day {d['day']}", "Student Cost (₹)": d['cost']}
                for d in st.session_state['itinerary']
            ])
            st.bar_chart(chart_df.set_index("Timeline")["Student Cost (₹)"], color="#10B981", height=250)

        with col_right:
            st.markdown("<div class='section-title'>Global Geospatial Routing</div>", unsafe_allow_html=True)
            ordered_pois = st.session_state['ordered_pois']
            if ordered_pois:
                avg_lat = sum(p['lat'] for p in ordered_pois) / len(ordered_pois)
                avg_lon = sum(p['lon'] for p in ordered_pois) / len(ordered_pois)
                m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12, tiles="CartoDB dark_matter")
                
                primary_color = '#3B82F6'
                for day_plan in st.session_state['itinerary']:
                    route_coords = []
                    for i, poi in enumerate(day_plan['pois']):
                        route_coords.append((poi['lat'], poi['lon']))
                        folium.CircleMarker(
                            location=[poi['lat'], poi['lon']],
                            radius=7,
                            popup=f"Day {day_plan['day']}: {poi['name']}",
                            tooltip=f"{poi['name']}",
                            color=primary_color,
                            fill=True,
                            fill_color="#0F172A",
                            fill_opacity=1,
                            weight=2
                        ).add_to(m)
                    
                    if len(route_coords) > 1:
                        folium.PolyLine(route_coords, color=primary_color, weight=2.5, opacity=0.8).add_to(m)
                
                st.markdown("<div class='map-container'>", unsafe_allow_html=True)
                st_folium(m, width="100%", height=750, returned_objects=[])
                st.markdown("</div>", unsafe_allow_html=True)

def main():
    if not st.session_state['logged_in']:
        auth_screen()
    else:
        dashboard_screen()

if __name__ == '__main__':
    main()
