# 🛰 OrbitWatch India

> **A Space Situational Awareness (SSA) platform for monitoring, tracking, analyzing, and predicting the positions of Indian satellites using real-time orbital data.**

OrbitWatch India is an interactive web application that visualizes Indian satellites on a live world map, provides comprehensive satellite information, delivers analytical insights into India's satellite fleet, and predicts future satellite positions using orbital mechanics. The platform leverages publicly available Two-Line Element (TLE) data to deliver an intuitive and educational satellite monitoring experience.

---

## ✨ Features

### 🗺️ Live Satellite Map & Explorer
- Visualize Indian satellites in real time on an interactive world map.
- Search and locate satellites instantly.
- Filter satellites by mission type, orbit type, and operational status.
- View detailed information by selecting a satellite.
- Display current latitude, longitude, altitude, and orbital information.

### 📊 Analytics Dashboard
Gain meaningful insights into India's satellite fleet through interactive visualizations.

Includes:
- Total satellites tracked
- Active vs inactive satellites
- Mission type distribution
- Orbit type distribution
- Operational status analysis
- Average orbital altitude
- Altitude distribution
- Mission-wise satellite statistics
- Interactive charts and graphs

### 🔮 Orbit Predictor
Predict future satellite positions using orbital propagation.

Features:
- Select any Indian satellite
- Predict future position for a selected date and time
- Future latitude, longitude, and altitude
- Ground-track visualization
- Based on Skyfield and SGP4 orbital propagation

---

## 🎯 Objectives

OrbitWatch India aims to:

- Demonstrate Space Situational Awareness (SSA) concepts.
- Visualize India's satellite infrastructure.
- Provide educational insights into satellite missions and orbital mechanics.
- Enable interactive exploration of Indian satellites.
- Predict future satellite positions using real orbital data.
- Promote awareness of India's growing presence in space technology.

---

## 📂 Dataset

The project uses a curated dataset containing Indian satellites with fields including:

- Satellite Name
- Mission Type
- Orbit Type
- Operational Status
- Latitude
- Longitude
- Mean Altitude
- Two-Line Element (TLE)

The orbital positions are computed dynamically from the latest available TLE data.

---

## 🛠 Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### Libraries
- Pandas
- NumPy
- Skyfield
- SGP4
- Plotly
- PyDeck / Folium

---

## 📁 Project Structure

```
OrbitWatch/
│
├── Home.py
│
├── assets/
│   ├── earth_background.jpg
│   └── asset_utils.py
│
├── data/
│   └── indian_satellites.csv
│
├── pages/
│   ├── Live_Map.py
│   ├── Analytics.py
│   └── Orbit_Predictor.py
│
├── services/
│   ├── data_utils.py
│   ├── tle_utils.py
│   ├── analytics_utils.py
│   ├── map_utils.py
│   └── prediction_utils.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/OrbitWatch.git
```

Navigate into the project:

```bash
cd OrbitWatch
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run Home.py
```

---

## Application Workflow

```
Indian Satellite Dataset
          │
          ▼
 Load Satellite Information
          │
          ▼
  Retrieve Latest TLE Data
          │
          ▼
 Skyfield + SGP4 Propagation
          │
          ▼
 Current Satellite Positions
          │
          ▼
 ┌─────────────────────────┐
 │ Live Map & Explorer     │
 │ Analytics Dashboard     │
 │ Orbit Predictor         │
 └─────────────────────────┘
```

---

## 📊 Analytics

The Analytics dashboard provides insights such as:

- Fleet Overview
- Active Satellite Count
- Mission Distribution
- Orbit Distribution
- Operational Status Analysis
- Average Altitude
- Altitude Histogram
- Mission-wise Statistics
- Orbit-wise Statistics
- Interactive Charts

---

## 🔮 Orbit Prediction

OrbitWatch India predicts future satellite positions using:

- Skyfield
- SGP4 Orbital Propagator
- Two-Line Element (TLE) data

Unlike machine learning approaches, the prediction is based on real orbital mechanics, making it suitable for accurate short-term satellite position estimation.

---

## 🔄 Future Enhancements

Planned improvements include:

- Space debris visualization
- Close approach monitoring
- Collision risk estimation
- Historical orbit playback
- 3D Earth visualization
- Automatic TLE updates
- Ground station visualization
- Satellite coverage footprints
- Launch history timeline
- Notification system

---

---

## Acknowledgements

This project makes use of publicly available data and open-source software.

Special thanks to:

- **CelesTrak** for providing Two-Line Element (TLE) orbital data.
- **Skyfield** for satellite orbit propagation.
- **SGP4** for orbital mechanics implementation.
- **ISRO** public information for satellite mission references.
- The Python open-source community for the libraries used in this project.

---

## ⚠️ Disclaimer

OrbitWatch India is an independent educational and research project developed for learning and demonstration purposes.

This project is **not affiliated with, endorsed by, or officially associated with ISRO, CelesTrak, or any government organization.**

Satellite positions are computed using publicly available TLE data and should **not** be used for mission-critical, navigational, or operational decision-making.

---

## 👨‍💻 Author

**Shaukat Muchukota**

GitHub: https://github.com/Shaukat2896/OrbitWatch

LinkedIn: https://linkedin.com/in/shaukat-muchukota-024048322

Email: shaukat2896@gmail.com

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

Your support helps improve the project and encourages further development.

---

**Made with ❤️ for Space Technology, Satellite Tracking, and Space Situational Awareness (SSA).**