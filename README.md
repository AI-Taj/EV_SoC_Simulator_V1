# EV_SoC_Simulator_V1

**Electric Vehicle Battery State of Charge (SoC) Simulator**

This project aims to generate realistic, multi-year synthetic datasets of EV battery behavior (SoC, Current, Voltage, Temperature) based on real-world trip data (TripA/TripB). It supports both physical modeling and AI-based sequence generation.

---

## 🔍 Key Features

- 📊 Uses real trip data as a foundation
- ⚙️ Coulomb counting, CC-CV charging, thermal models
- 🧠 LSTM/GAN-based trip synthesis (future phases)
- 🗓️ Daily to multi-year simulation
- 📦 Output formats: CSV, HDF5
- 🖥️ GUI application planned for researchers

---

## 📁 Project Structure

```plaintext
EV_SoC_Simulator_V1/
│
├── Data/                     # Raw, processed, synthetic data
├── Models/                  # Trained models (LSTM, GAN, etc.)
├── Validation/              # Error metrics, plots, logs
├── App/                     # GUI app and export tools
├── Scripts/                 # Simulation and generation scripts by phase
├── Notebooks/               # Exploratory analysis and reports
├── Figures/                 # Publication figures
├── Docs/                    # Publications and documentation
├── requirements.txt         # Python dependencies
├── .gitignore               # Ignore raw data, caches, etc.
├── README.md                # Project overview
```

---

## 🚀 Phased Development Plan & Publications

This simulator is structured in phases, each with its own goals, methods, outputs, and publishable research opportunities.

### 🔵 Phase 0 — Real Data Analysis & Feature Extraction
**Objective**: Analyze and tag real-world trip data from TripA/TripB.

**Key Tasks**:
- Clean/filter raw data
- Extract trip features (duration, SoC delta)
- Tag trip styles (calm, aggressive)
- Generate metadata

**Publication**:
- 📄 “Statistical Characterization of Real-World EV Trip Data for Synthetic Simulation”

---

### 🔵 Phase 1 — Physical Daily Generator
**Objective**: Build 24h EV timelines using physical models.

**Key Tasks**:
- Trip stitching with rest/charging
- SoC via Coulomb counting
- Voltage & Temp modeling

**Publication**:
- 📄 “A Physically-Inspired Framework for Daily Synthetic EV Battery Data Generation”

---

### 🔵 Phase 2 — Profile-Driven Month-Level Simulator
**Objective**: Generate month-long behavior with profile control.

**Key Tasks**:
- Driver & day type logic
- SoC continuity
- Charging behavior variation

**Publications**:
- 📄 “Behaviorally-Constrained EV Battery Data Generation Over Calendar-Driven Scenarios”
- 📄 “Driver Profile Effects on EV Energy Use”

---

### 🔵 Phase 3 — AI-Based Trip Generator (LSTM/GAN)
**Objective**: Use ML to synthesize realistic trips.

**Key Tasks**:
- Train LSTM & GAN on real/synthetic data
- Generate plausible I/V/T/SoC
- Conditional context (profile, time)

**Publications**:
- 📄 “LSTM-Based Generation of Realistic EV Load Curves”
- 📄 “Comparison of LSTM and GANs for Battery Profile Synthesis”

---

### 🔵 Phase 4 — Long-Term Simulation Engine
**Objective**: Build year-scale synthetic EV usage.

**Key Tasks**:
- Calendar logic
- Ambient temp modeling
- Battery aging (SoH drift)

**Publications**:
- 📄 “Modeling Long-Term EV Battery Behavior Using Calendar-Driven Engine”
- 📄 “Aging-Aware Synthetic Battery Dataset Generation”

---

### 🔵 Phase 5 — Validation and Benchmarking
**Objective**: Validate realism and benchmark against tasks.

**Key Tasks**:
- Physics checks, stats comparisons
- Visual similarity (t-SNE, PCA)
- SoC model training on synthetic data

**Publications**:
- 📄 “Validating Synthetic EV Battery Time Series”
- 📄 “Benchmarking SoC Estimation with Synthetic Data”

---

### 🔵 Phase 6 — Application Packaging and Release
**Objective**: Build the GUI tool and dataset exporter.

**Key Tasks**:
- GUI options: profile, days, format
- Export: CSV, JSON, HDF5
- Documentation

**Publication**:
- 📄 “OpenBatterySim: A Modular Simulator for Long-Term EV Battery Data Generation”

---

## 📚 Additional Research Extensions

- Hybrid SoC Modeling: Physical + LSTM
- Digital Twin of EV Battery
- Regenerative Braking Pattern Generator
- Sim-to-Real Transfer of Battery AI
- Fault Injection and Anomaly Detection

---

## 📬 Contact & Contribution

Lead: **Taj Eddine KHALILI**  
GitHub: [github.com/AI-Taj](https://github.com/AI-Taj)

Pull requests and collaboration are welcome in future public releases.
