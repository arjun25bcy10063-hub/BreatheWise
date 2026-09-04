# BreatheWise AI

BreatheWise AI is a Streamlit application that combines live weather data, live air-quality data, a lightweight user profile, deterministic risk scoring, and AI-generated environmental guidance.

## Features

- Location search
- Live weather and seven-day forecast
- Live AQI and pollutant data
- User profile with age, sensitivity, and exposure type
- Deterministic personalized risk score
- AI-generated plain-language advisory
- Safety validation of generated guidance
- Persistent alert history
- Seven-day trend charts
- SQLite storage
- Streamlit multipage interface

## Project structure

See the repository tree for the complete modular structure.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your AI API key to `.env`.

Run:

```bash
streamlit run app.py
```

Test:

```bash
pytest -q
```

## Data sources

Weather and geocoding use Open-Meteo. Air-quality data uses the Open-Meteo Air Quality API.

## Architecture

```text
Location
   ↓
Weather + Air Quality Services
   ↓
Risk Engine
   ↓
AI Advisory
   ↓
Safety Validation
   ↓
Alert Agent
   ↓
SQLite
   ↓
Streamlit Dashboard
```

## Safety

This application provides environmental guidance and is not a medical diagnosis tool or a substitute for professional medical advice.
