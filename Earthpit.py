import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Elevator Earthpit Calculator", layout="wide")

# Title and Introduction
st.title("🛠️ Elevator Earthpit Calculator")
st.markdown("""
This tool helps calculate the recommended earthpit dimensions and components for elevator grounding systems,
based on international and Indian standards such as IEC 62305-3, IEEE Std 80/81, and IS 3043.
""")

# Sidebar for standards reference
with st.sidebar:
    st.header("Standards Reference")
    st.markdown("""
    - **IEC 62305-3:2011**: Earth resistance ≤ 10 ohms
    - **IEEE Std 80 & 81**: Soil resistivity measurement methods
    - **IS 3043:1987 & 2018**: Indian earthing practices
    """)

# Input section
st.header("Input Parameters")

# First row of inputs
col1, col2, col3 = st.columns(3)

with col1:
    pit_type = st.selectbox("Select Pit Type", [
        "Regular Pit",
        "Chemical Earthing Pit",
        "Maintenance-Free Pit"
    ])
    
with col2:
    plate_material = st.selectbox("Select Plate Material", ["GI (Galvanized Iron)", "Copper"])
    
with col3:
    soil_type = st.selectbox("Soil Type", [
        "Loamy Soil",
        "Clay Soil",
        "Sandy Soil",
        "Rocky Soil",
        "Black Cotton Soil"
    ])

# Second row of inputs
col4, col5, col6 = st.columns(3)

with col4:
    resistivity = st.number_input("Soil Resistivity (Ω·m)", 
                                min_value=1.0, 
                                value=100.0,
                                help="Typical range: Loamy: 50-100, Clay: 100-200, Sandy: 200-1000, Rocky: 1000+")
with col5:
    desired_resistance = st.number_input("Desired Earth Resistance (Ω)", 
                                       min_value=0.1, 
                                       value=5.0,
                                       help="As per standards, should be ≤ 10 ohms")
with col6:
    strip_length = st.number_input("Strip Length (m)", 
                                  min_value=1.0, 
                                  value=10.0,
                                  help="Connecting strip length from pit to equipment")

# Calculation section
st.header("📐 Calculated Outputs")

# Material properties
if plate_material == "GI (Galvanized Iron)":
    plate_size = "500 mm x 500 mm x 10 mm"
    material_factor = 1.0  # Base factor for GI
    strip_type = "GI"
    conductivity = "16%"  # Relative to copper
else:  # Copper
    plate_size = "600 mm x 600 mm x 3 mm"
    material_factor = 0.5  # Copper has better conductivity
    strip_type = "Copper"
    conductivity = "100%"

# Soil type factors
soil_factors = {
    "Loamy Soil": 1.0,
    "Clay Soil": 1.2,
    "Sandy Soil": 1.5,
    "Rocky Soil": 2.0,
    "Black Cotton Soil": 0.8
}

# Pit type configurations
pit_configs = {
    "Regular Pit": {
        "depth_factor": 1.0,
        "filling": "Coal/Salt/Sand mixture in 1:1:1 ratio",
        "lifetime": "3-5 years",
        "maintenance": "Regular watering and periodic maintenance required"
    },
    "Chemical Earthing Pit": {
        "depth_factor": 0.7,  # Chemical treatment improves conductivity
        "filling": "Conductive chemical compound with minerals",
        "lifetime": "10-15 years",
        "maintenance": "Periodic chemical refilling every 5-7 years"
    },
    "Maintenance-Free Pit": {
        "depth_factor": 0.8,
        "filling": "Highly conductive copper oxide compound",
        "lifetime": "15-20 years",
        "maintenance": "No regular maintenance required"
    }
}

# Calculate pit depth considering all factors
base_depth = (resistivity * material_factor * soil_factors[soil_type]) / (4 * math.pi * desired_resistance)
pit_depth = round(base_depth * pit_configs[pit_type]["depth_factor"], 2)

# Display calculations and recommendations
st.subheader("📏 Dimensions and Materials")
st.markdown(f"**Recommended Earthpit Depth:** `{pit_depth} meters`")
st.markdown(f"**Standard {plate_material} Plate Size:** `{plate_size}`")
st.markdown(f"**{strip_type} Strip Required:** `{strip_length} meters`")

st.subheader("⚡ Electrical Properties")
st.markdown(f"**Material Conductivity:** `{conductivity}`")
st.markdown(f"**Soil Type Factor:** `{soil_factors[soil_type]}`")
st.markdown(f"**Expected Resistance:** `{round(desired_resistance * pit_configs[pit_type]['depth_factor'], 2)} Ω`")

st.subheader("🏗️ Pit Specifications")
st.markdown(f"**Pit Type:** `{pit_type}`")
st.markdown(f"**Filling Material:** `{pit_configs[pit_type]['filling']}`")
st.markdown(f"**Expected Lifetime:** `{pit_configs[pit_type]['lifetime']}`")
st.markdown(f"**Maintenance Requirements:** `{pit_configs[pit_type]['maintenance']}`")

# Cost Estimation Section
st.subheader("💰 Cost Estimation")
base_costs = {
    "Regular Pit": {
        "GI (Galvanized Iron)": 15000,
        "Copper": 25000
    },
    "Chemical Earthing Pit": {
        "GI (Galvanized Iron)": 20000,
        "Copper": 30000
    },
    "Maintenance-Free Pit": {
        "GI (Galvanized Iron)": 25000,
        "Copper": 35000
    }
}

# Calculate additional costs based on depth and soil type
depth_cost = pit_depth * 1000  # Additional cost per meter depth
soil_complexity = {
    "Loamy Soil": 1.0,
    "Clay Soil": 1.2,
    "Sandy Soil": 1.3,
    "Rocky Soil": 1.8,
    "Black Cotton Soil": 1.4
}

base_cost = base_costs[pit_type][plate_material]
total_cost = base_cost + (depth_cost * soil_complexity[soil_type])

st.markdown(f"**Base Installation Cost:** `₹{base_cost:,.2f}`")
st.markdown(f"**Additional Depth Cost:** `₹{depth_cost:,.2f}`")
st.markdown(f"**Soil Complexity Factor:** `{soil_complexity[soil_type]}`")
st.markdown(f"**Estimated Total Cost:** `₹{total_cost:,.2f}`")

# Visual Representation
st.subheader("🎯 Visual Representation")
col_vis1, col_vis2 = st.columns([2, 1])

with col_vis1:
    # Create a visual representation of the earthing pit
    st.markdown(f"""
    ```
    Ground Level
    ─────────────────────────────────────────
    │                                       │
    │   Strip ({strip_type})                │
    │   Length: {strip_length}m             │
    │                                       │
    │   ┌───────────────────┐              │
    │   │    {plate_material}    │          │
    │   │    Plate          │ {pit_depth}m  │
    │   │    {plate_size}   │              │
    │   └───────────────────┘              │
    │                                       │
    │   Filling: {pit_configs[pit_type]['filling']}
    │                                       │
    └───────────────────────────────────────┘
    ```
    """)

with col_vis2:
    # Display a checklist of installed components
    st.markdown("**Installation Checklist:**")
    components = {
        "Earthing Plate": True,
        f"{strip_type} Strip": True,
        "Filling Material": True,
        "Moisture Control": pit_type != "Maintenance-Free Pit",
        "Chemical Compound": pit_type == "Chemical Earthing Pit",
        "Inspection Chamber": True
    }
    
    for component, installed in components.items():
        st.markdown(f"{'✅' if installed else '❌'} {component}")

# Additional Technical Details
st.subheader("🔧 Technical Specifications")
tech_col1, tech_col2 = st.columns(2)

with tech_col1:
    st.markdown("**Material Properties:**")
    material_props = {
        "GI (Galvanized Iron)": {
            "Tensile Strength": "380-550 MPa",
            "Zinc Coating": "610 g/m²",
            "Thickness": "10 mm",
            "Life Expectancy": "15-20 years"
        },
        "Copper": {
            "Tensile Strength": "220-250 MPa",
            "Purity": "99.9%",
            "Thickness": "3 mm",
            "Life Expectancy": "30-50 years"
        }
    }
    for prop, value in material_props[plate_material].items():
        st.markdown(f"- {prop}: `{value}`")

with tech_col2:
    st.markdown("**Pit Environment:**")
    environment_factors = {
        "pH Value": "6.5-7.5",
        "Moisture Content": "10-15%",
        "Temperature Range": "10-45°C",
        "Backfill Resistivity": "< 50 Ω·m"
    }
    for factor, value in environment_factors.items():
        st.markdown(f"- {factor}: `{value}`")

# Weather Impact Analysis
st.subheader("🌦️ Weather Impact Analysis")
weather_impact = {
    "Rainy Season": "Optimal performance, natural moisture maintenance",
    "Summer": "May require additional watering" if pit_type == "Regular Pit" else "Stable performance",
    "Winter": "Slightly increased resistance due to lower ground temperature",
    "Monsoon": "Enhanced performance, monitor for flooding"
}

for season, impact in weather_impact.items():
    st.markdown(f"**{season}:** {impact}")

# Inspection Schedule Generator
st.subheader("📅 Recommended Inspection Schedule")
current_year = datetime.now().year
inspection_schedule = []

if pit_type == "Regular Pit":
    frequency = 3  # months
elif pit_type == "Chemical Earthing Pit":
    frequency = 6  # months
else:  # Maintenance-Free Pit
    frequency = 12  # months

for month in range(1, 13, frequency):
    inspection_date = f"{current_year}-{month:02d}-01"
    inspection_schedule.append({
        "Date": inspection_date,
        "Activities": [
            "Visual Inspection",
            "Resistance Measurement",
            "Connection Check"
        ] + (["Moisture Check", "Salt/Coal Level Check"] if pit_type == "Regular Pit" else [])
          + (["Chemical Compound Check"] if pit_type == "Chemical Earthing Pit" else [])
    })

st.markdown("**Inspection Dates and Activities:**")
for inspection in inspection_schedule:
    st.markdown(f"**{inspection['Date']}**")
    for activity in inspection['Activities']:
        st.markdown(f"- {activity}")

# Maintenance Guidelines
st.header("🧰 Maintenance Guidelines")

if pit_type == "Regular Pit":
    st.markdown("""
    #### Regular Pit Maintenance:
    - 🌧️ Regular watering (weekly in dry season)
    - 🧂 Annual replenishment of salt/charcoal mixture
    - 🔍 Quarterly inspection for corrosion
    - 📏 Bi-annual earth resistance measurement
    - ⚡ Tightening of connections annually
    """)
elif pit_type == "Chemical Earthing Pit":
    st.markdown("""
    #### Chemical Pit Maintenance:
    - 🧪 Chemical compound check every 2 years
    - 🔄 Refilling of chemical compound every 5-7 years
    - 🔍 Annual inspection of connections
    - 📏 Annual earth resistance measurement
    - 💧 No regular watering required
    """)
else:  # Maintenance-Free Pit
    st.markdown("""
    #### Maintenance-Free Pit Care:
    - 🔍 Annual visual inspection
    - 📏 Annual earth resistance measurement
    - ⚡ Check connections every 2 years
    - 🛡️ No chemical refilling required
    - 💧 No watering required
    """)

# Footer
st.markdown("---")
st.markdown("For assistance write to services@serinthomas.in")