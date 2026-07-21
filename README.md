# 🏢 ICT in Building Design — RES FLAT2, Larnaca
### Smart Building Optimization for a Residential Flat in Cyprus

A university project developed at **Politecnico di Torino** (A.Y. 2025/2026) for the ICT in Building Design course. The project applies data-driven ICT methods to optimize the energy performance and indoor comfort of a residential flat in Larnaca, Cyprus, covering surrogate-based design optimization, reinforcement learning control, energy prediction, and thermal analysis.

**Group 9:** Mattia Antonini (s344064) · Simone Peradotto (s343420) · Lorenzo Cavallaro (s346742) · Giovanni Grieco (s346012)

---

## 📋 Problem Statement

Buildings face three interconnected challenges:

1. **Energy & Environmental** — High energy consumption and significant carbon emissions alongside poor indoor environmental quality (thermal comfort, air quality, lighting).
2. **Integration & Control Complexity** — Building components, HVAC systems, and energy networks are difficult to integrate, limiting smart and climate-responsive operation.
3. **Need for Intelligent Optimization** — Advanced ICT solutions (digital building models, multi-level modeling, intelligent BMS algorithms) are required to optimize both design and real-time performance.

---

## 🏠 Building Description — RES FLAT2

| Parameter | Value |
|---|---|
| Location | Larnaca, Cyprus |
| Building type | Residential flat, 2nd floor |
| Thermal zones | 5 (4 conditioned rooms + 1 unconditioned stair) |
| Window U-factor | 1.96 W/m·K |
| Window SHGC | 0.69 |
| Heating setpoint | 20°C (max supply: 35°C) |
| Cooling setpoint | 26°C (min supply: 12°C) |
| Shading control | T > 24°C or Solar radiation > 120 W/m² |
| Mechanical ventilation | 0.1 L/s per m² (EN 16798-1), active all year |
| Natural ventilation | Summer only |
| Occupancy schedule | EN16798-1 RES (higher nights & weekends) |

---

## 🔬 Project Modules

### 1. Surrogate Design Optimization

**Goal:** Find the optimal set of building envelope and shading parameters to minimize energy consumption.

**Design parameters (8 variables):**
- Insulation Roof Thickness [m]
- Insulation Wall Thickness [m]
- U-Value [W/(m²·K)]
- Solar Heat Gain Coefficient (SHGC)
- Visible Transmittance
- Air Changes per Hour (ACH)
- Temperature Setpoint Shading [°C]
- Radiation Setpoint Shading [W/m²]

**Pipeline:**
1. 100 configurations sampled via **Latin Hypercube Sampling (LHS)**
2. All configurations simulated in **EnergyPlus** (3 objectives: electricity, cooling, heating demand)
3. **Gaussian Process Regression (GPR)** surrogate model trained (R² = 0.9, 6-fold cross-validation)
4. **NSGA-II** multi-objective optimization (10,000 evaluations, 5,000 individuals)
5. Best solution selected as the Pareto-optimal point with the smallest Euclidean distance to the ideal energy minimum

**Optimal parameters found:**

| Parameter | Optimal Value |
|---|---|
| Insulation Roof Thickness | 0.369 m |
| Insulation Wall Thickness | 0.199 m |
| U-Value | 1.106 W/(m²·K) |
| Solar Heat Gain Coefficient | 0.135 |
| Visible Transmittance | 0.355 |
| Air Changes per Hour (ACH) | 4 |
| Temperature Setpoint Shading | 21.859 °C |
| Radiation Setpoint Shading | 241.494 W/m² |

---

### 2. BMS Control — Shading Optimization

Two control strategies were implemented and compared for automated shading management, co-simulated via **EnergyPlus FMU** and Python.

#### Arbitrary Control (Rule-Based)
Shading is driven by a fixed rule on indoor temperature and direct normal irradiance (DNI):

```
a_i(t) = ON   if T_i(t) > 26°C
a_i(t) = ON   if T_i(t) ≤ 26°C and DNI(t) ≥ 150 W/m²
a_i(t) = OFF  if T_i(t) ≤ 26°C and DNI(t) < 150 W/m²
```

**Pros:** Easy to implement, immediate reconfiguration, user-understandable  
**Cons:** Arbitrary thresholds, manual tuning required, potential variable conflicts

#### Reinforcement Learning Control (PPO)
A **Proximal Policy Optimization (PPO)** agent trained to control per-window shading, balancing thermal comfort and energy use.

- **State space:** Indoor temperatures (4 zones) + outdoor temperature + DNI
- **Action space:** Shading position per window (0 = open, 5 = closed)
- **Reward function:** `r_t = -(c_t + λ_en · e_t)` where `c_t` is the comfort penalty and `e_t` the energy penalty
- **Comfort penalty:** Penalizes deviation from the 20–26°C comfort band when DNI exceeds a gate threshold
- **Energy penalty:** Sum of heating, cooling, and electricity demand

---

### 3. Telegram Bot — Real-Time Monitoring

A Telegram bot provides occupants with real-time building status and alerts.

**Automatic notifications:**
- **Comfort Alert** — Triggered when any zone exits the 20–26°C range (with flood-prevention cooldown)
- **HVAC Update** — Triggered on heating/cooling system state transitions

**Commands:**
- `/temperature` — Returns current indoor temperatures for all thermal zones
- `/shades` — Returns the current shading configuration for each zone

---

### 4. Energy Prediction Model (XGBoost)

An ML pipeline built with **XGBoost** to predict building energy consumption at 6-hour resolution.

**Four specialized models:**

| Model | Type | R² | MSE |
|---|---|---|---|
| Electricity | XGBoost Regressor | 0.977 | 8.78e-7 |
| Heating | XGBoost Regressor | 0.996 | 1.77e-7 |
| Cooling ON/OFF | XGBoost Classifier (threshold = 0.7) | — | — |
| Cooling Magnitude | XGBoost Regressor (ON samples only) | 0.971 | 4.39e-6 |
| **Total Primary Energy** | **Combined** | **0.981** | **5.04e-6** |

**Dataset:** 1,405 samples / 34 features, chronological 70/30 split (no shuffling)

**Key features:** thermal variables (Tin, Tout, ΔT), temporal encoding (sin/cos of hour and day-of-year), lagged consumption, rolling means, non-linear interactions (temperature × DNI)

**Key findings:**
- Energy demand is primarily driven by thermal inertia and historical load
- Electricity and heating behave as memory-based systems (strong autocorrelation)
- Cooling operates as a regime-switching process (ON/OFF + intensity)

---

### 5. Energy Signature — Thermal Sensitivity Analysis

The energy signature relates heating and cooling demand to the indoor-outdoor temperature difference (ΔT), identifying the building's thermal behavior under different climate conditions.

- **Hourly/Daily resolution** is recommended — filters short-term noise while preserving thermal physics
- **Weekly/Monthly aggregation** reduces sample size significantly, losing robustness
- Custom power thresholds (Qh: 20 W, Qc: 30 W) filter operational noise, accounting for Cyprus's high-intensity cooling patterns

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| EnergyPlus | Building energy simulation |
| Python | Optimization, ML, control logic |
| GPR (scikit-learn) | Surrogate model |
| NSGA-II (pymoo) | Multi-objective optimization |
| XGBoost | Energy prediction |
| Stable-Baselines3 (PPO) | Reinforcement learning control |
| FMU / EnergyPlus Python API | Co-simulation |
| InfluxDB | Simulation data storage |
| Telegram Bot API | Real-time monitoring |

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone <repo-url>
cd ict-building-design

# Install dependencies
pip install -r requirements.txt
```

Make sure EnergyPlus is installed and accessible. For the Telegram bot, set your bot token in a `.env` file:

```
TELEGRAM_BOT_TOKEN=your_token_here
```
