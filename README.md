# SMARTBIN -- Intelligent Waste Management System

## Overview

SMARTBIN is an intelligent waste-management prototype that monitors
SmartBin conditions, stores live data in Firebase, assigns collection
priorities, and generates a collection route.

For the hackathon, the physical IoT communication layer is simulated in
Python so the complete workflow can be demonstrated without physical
LoRaWAN hardware.

## Architecture

``` text
Virtual SmartBin
      ↓
Simulated LoRaWAN
      ↓
Virtual Municipal Gateway
      ↓
Firebase Realtime Database
      ↓
AI Agent
      ↓
Priority / Score
      ↓
Route Optimizer
      ↓
Streamlit Dashboard
```

## Features

-   Virtual SmartBin sensor simulation
-   Simulated LoRaWAN packet transmission
-   Virtual municipal gateway
-   Firebase Realtime Database integration
-   AI-based bin priority and scoring
-   Collection route optimization
-   Streamlit dashboard integration
-   GitHub-based team development

## Project Structure

``` text
SMARTBIN/
├── member3_ai/
│   ├── ai_agent.py
│   ├── firebase_config.py
│   ├── firebase_test.py
│   ├── main.py
│   └── route_optimizer.py
├── virtual/
│   ├── firebase_config.py
│   ├── gateway.py
│   ├── lora_simulator.py
│   └── simulator.py
├── .gitignore
├── README.md
├── req.txt
└── requirements.txt
```

## Data Flow

``` text
SmartBin
  ↓
Simulated LoRaWAN
  ↓
Virtual Gateway
  ↓
Firebase
  ↓
AI Agent
  ↓
Priority
  ↓
Route Optimization
```

Example Firebase path:

``` text
bins/BIN-001
```

Example data:

``` text
Fill Level: 47%
Battery: 94%
Status: NORMAL
Location: 12.8236, 80.0454
```

## Setup

### 1. Clone the repository

``` bash
git clone https://github.com/Pradozxy/SMARTBIN.git
cd SMARTBIN
```

### 2. Create and activate a virtual environment

Windows PowerShell:

``` powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

``` powershell
pip install -r requirements.txt
```

## Firebase Security

Firebase credentials must remain local.

Do **not** upload:

``` text
.env
serviceAccountKey.json
.venv/
```

The Firebase service-account JSON contains a private credential and must
never be committed to GitHub.

## Run the Prototype

### Virtual SmartBin + Gateway

``` powershell
python virtual\simulator.py
```

A successful transmission should show:

``` text
Packet transmitted successfully!
Firebase updated successfully!
```

Stop the simulator with:

``` text
Ctrl + C
```

### AI Agent

``` powershell
python member3_aii_agent.py
```

The AI layer reads bin information and produces a priority and score.

### Route Optimizer

``` powershell
python member3_aioute_optimizer.py
```

This produces a collection order based on the available priority
information.

## Two-Laptop Demo

``` text
Laptop 1
Virtual SmartBin
      ↓
Simulated LoRaWAN
      ↓
Virtual Gateway
      ↓
Firebase
      ↑
      │
Laptop 2
Streamlit Dashboard
```

The laptops communicate through Firebase rather than directly.

## Real-World Deployment

The hackathon prototype uses simulated LoRaWAN. A physical deployment
could replace the simulator with:

``` text
Smart Bin Sensors
      ↓
ESP32
      ↓
LoRaWAN
      ↓
Municipal LoRaWAN Gateway
      ↓
Cloud Database
      ↓
AI Agent
      ↓
Dashboard + Route Optimization
```

Possible future additions include real ultrasonic sensors, gas sensors,
solar power, historical trend analysis, predictive forecasting, live
maps, and municipal-scale deployment.

## Team

**Team:** Ctrl+C and Ctrl+V

**Project:** SMARTBIN -- Intelligent Waste Management System

**Track:** Open Innovation

## Hackathon Statement

SMARTBIN demonstrates an end-to-end intelligent waste-management
workflow from virtual sensing and long-range IoT communication to cloud
storage, AI-based prioritization, and collection-route optimization.
