# BreatheWise AI

## Personalized Weather & Air Quality Health Advisory

BreatheWise AI is a Streamlit-based environmental intelligence application that combines live weather conditions, air-quality information, a user exposure profile, deterministic risk scoring, and AI-generated guidance.

The goal is simple:

> **The same environmental conditions can affect different people differently.**

Instead of showing the user only a generic weather or AQI warning, BreatheWise AI considers factors such as age group, health sensitivity, and occupation/exposure type before presenting personalized environmental guidance.

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Solution](#solution)
3. [Key Features](#key-features)
4. [How the Application Works](#how-the-application-works)
5. [Application Architecture](#application-architecture)
6. [Technology Stack](#technology-stack)
7. [Repository Structure](#repository-structure)
8. [Project Modules](#project-modules)
9. [Data Flow](#data-flow)
10. [Risk Assessment](#risk-assessment)
11. [AI Advisory Layer](#ai-advisory-layer)
12. [Safety Layer](#safety-layer)
13. [Database](#database)
14. [Installation](#installation)
15. [Configuration](#configuration)
16. [Running the Application](#running-the-application)
17. [Testing](#testing)
18. [GitHub Setup](#github-setup)
19. [Deployment](#deployment)
20. [Hackathon Demo Flow](#hackathon-demo-flow)
21. [Limitations](#limitations)
22. [Future Enhancements](#future-enhancements)
23. [Medical and Safety Disclaimer](#medical-and-safety-disclaimer)
24. [License](#license)

---

## Problem Statement

Generic weather and AQI applications usually present the same threshold-based warning to everyone. However, environmental exposure and sensitivity can differ significantly between users.

For example, an indoor worker, an outdoor worker, and a person with higher environmental sensitivity may require different guidance even when they are in the same location and experiencing the same weather and air quality.

BreatheWise AI addresses this gap by combining live environmental information with a lightweight user profile and producing personalized, understandable guidance.

---

## Solution

BreatheWise AI follows this processing pipeline:

```text
User Profile
     +
Location
     ↓
Live Weather Data
     +
Live Air-Quality Data
     ↓
Data Validation
     ↓
Deterministic Risk Engine
     ↓
AI Personalization
     ↓
Safety Validation
     ↓
Personalized Advisory
     ↓
Alert + History + Trends
```

The risk score is calculated by deterministic application logic. The AI layer is used to turn the structured result into concise, plain-language guidance that is adapted to the user's profile.

---

## Key Features

### 1. Live Location-Based Weather

The application allows the user to search for a location and obtain coordinates. The selected coordinates are then used to retrieve environmental data.

Displayed weather information includes:

- Temperature
- Apparent/feels-like temperature
- Humidity
- Wind speed
- Wind gusts
- Precipitation
- Weather condition
- UV index
- Multi-day forecast

### 2. Live Air Quality

The application retrieves air-quality information for the selected coordinates.

Available information includes:

- AQI
- PM2.5
- PM10
- NO2
- O3
- SO2
- CO

### 3. Personalized User Profile

The user can define:

- Age group
- Health sensitivity category
- Occupation/exposure type
- Preferred location

The profile is stored locally in SQLite and reused by the risk engine and advisory system.

### 4. Personalized Risk Score

BreatheWise AI calculates a risk score from 0 to 100 using environmental and profile factors.

The score is separated into areas such as:

- Air-quality risk
- Weather risk
- Outdoor-exposure risk

The system also records the main factors contributing to the result.

### 5. AI-Generated Advisory

The application sends structured environmental and profile information to the AI advisory layer.

The generated guidance can contain:

- Personalized summary
- Practical recommendations
- Outdoor guidance
- Explanation of personalization

### 6. Safety Validation

AI-generated content passes through a validation layer before being shown to the user.

The safety layer is designed to prevent:

- Medical diagnosis
- Medication instructions
- Unsupported medical claims
- Inappropriate or unsafe advice

### 7. Environmental Alerts

The application can create alerts when the environmental risk is sufficiently high or changes meaningfully compared with previous stored assessments.

### 8. Alert History

Users can review previous alerts, their risk level, timestamps, and alert messages.

### 9. Environmental Trends

The application stores environmental snapshots and presents collected data through trend charts.

Supported trend views include:

- AQI
- PM2.5
- Temperature
- Humidity
- Stored risk information where available

### 10. Seven-Day Outlook

The dashboard displays available multi-day weather forecast information to help the user understand upcoming conditions.

---

## How the Application Works

### Step 1: User selects a location

The location service sends the search term to the geocoding service and receives latitude and longitude.

### Step 2: Weather data is retrieved

The weather service uses the selected coordinates to retrieve current conditions and forecast information.

### Step 3: Air-quality data is retrieved

The air-quality service uses the same coordinates to retrieve AQI and pollutant information.

### Step 4: Environmental data is processed

The application converts API responses into internal data structures used throughout the project.

### Step 5: Risk is calculated

The deterministic risk engine considers environmental values together with user profile information.

### Step 6: Personalized guidance is generated

The AI advisory layer receives the structured context and generates a human-readable recommendation.

### Step 7: Safety validation occurs

The generated response is validated before it is displayed.

### Step 8: Information is stored

Environmental readings, risk results, advisories, and alerts are written to SQLite.

### Step 9: Dashboard is updated

The user sees the live conditions, personalized risk, guidance, alerts, and trends.

---

## Application Architecture

```text
                         ┌──────────────────┐
                         │   Streamlit UI   │
                         └─────────┬────────┘
                                   │
                 ┌─────────────────┼─────────────────┐
                 │                 │                 │
                 ▼                 ▼                 ▼
          Profile Page       Dashboard        Trends/History
                 │                 │                 │
                 └─────────────────┼─────────────────┘
                                   ▼
                         ┌──────────────────┐
                         │ Location Service │
                         └─────────┬────────┘
                                   ▼
              ┌────────────────────┴────────────────────┐
              ▼                                         ▼
      Weather Service                            AQI Service
              │                                         │
              └────────────────────┬────────────────────┘
                                   ▼
                         ┌──────────────────┐
                         │ Validation      │
                         └─────────┬────────┘
                                   ▼
                         ┌──────────────────┐
                         │ Risk Engine      │
                         └─────────┬────────┘
                                   ▼
                         ┌──────────────────┐
                         │ Advisory Layer  │
                         └─────────┬────────┘
                                   ▼
                         ┌──────────────────┐
                         │ Safety Layer     │
                         └─────────┬────────┘
                                   ▼
                         ┌──────────────────┐
                         │ Alert Processing │
                         └─────────┬────────┘
                                   ▼
                         ┌──────────────────┐
                         │ SQLite Database  │
                         └──────────────────┘
```

---

## Technology Stack

| Area | Technology |
|---|---|
| Frontend | Streamlit |
| Programming Language | Python |
| Weather Data | Open-Meteo |
| Location Search | Open-Meteo Geocoding |
| Air Quality | Open-Meteo Air Quality API |
| AI Advisory | AI API integration through the project advisory service |
| Database | SQLite |
| Data Processing | Pandas |
| Visualization | Plotly |
| HTTP Requests | Requests |
| Testing | Pytest |
| Version Control | Git / GitHub |

---

## Repository Structure

```text
BreatheWise-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── GITHUB_SETUP.md
├── ALL_CODE.md
├── .gitignore
├── .env.example
│
├── .streamlit/
│   └── secrets.toml.example
│
├── agents/
│   ├── __init__.py
│   ├── advisory_agent.py
│   ├── risk_agent.py
│   ├── safety_agent.py
│   └── alert_agent.py
│
├── services/
│   ├── __init__.py
│   ├── weather_service.py
│   ├── aqi_service.py
│   └── location_service.py
│
├── models/
│   ├── __init__.py
│   └── schemas.py
│
├── database/
│   ├── __init__.py
│   └── database.py
│
├── utils/
│   ├── __init__.py
│   ├── constants.py
│   ├── formatting.py
│   ├── risk_rules.py
│   └── validators.py
│
├── components/
│   ├── __init__.py
│   ├── weather_card.py
│   ├── aqi_card.py
│   ├── risk_card.py
│   ├── advisory_card.py
│   └── charts.py
│
├── pages/
│   ├── dashboard.py
│   ├── profile.py
│   ├── trends.py
│   └── history.py
│
├── data/
│   └── sample_data.json
│
└── tests/
    ├── __init__.py
    ├── test_risk.py
    ├── test_advisory.py
    ├── test_services.py
    └── test_validators.py
```

---

## Project Modules

### `app.py`

Main application entry point.

Responsibilities:

- Configure Streamlit
- Load environment variables
- Initialize the database
- Register application pages
- Start Streamlit navigation

### `services/`

Contains all external data integrations.

#### `weather_service.py`

Handles weather requests, response processing, current conditions, and forecasts.

#### `aqi_service.py`

Handles air-quality requests and pollutant processing.

#### `location_service.py`

Handles location searches and coordinate lookup.

### `agents/`

Contains the decision and AI-processing layers.

#### `risk_agent.py`

Calculates the deterministic environmental risk assessment.

#### `advisory_agent.py`

Creates personalized natural-language guidance using the structured environmental context.

#### `safety_agent.py`

Checks the generated advisory and prevents unsafe content from being returned to the user.

#### `alert_agent.py`

Determines when an environmental alert should be created.

### `models/`

Contains internal data structures used to keep the different modules consistent.

### `database/`

Contains SQLite database connection and storage operations.

### `utils/`

Contains shared application rules, constants, validation, and formatting functions.

### `components/`

Contains reusable dashboard components and chart functions.

### `pages/`

Contains the Streamlit application pages:

- Dashboard
- Profile
- Trends
- History

### `tests/`

Contains automated tests for core services, validators, risk logic, and advisory behavior.

---

## Data Flow

```text
Location Input
      ↓
Location Service
      ↓
Latitude / Longitude
      ↓
┌─────────────────┬─────────────────┐
│ Weather Service │   AQI Service   │
└────────┬────────┴────────┬────────┘
         │                 │
         └────────┬────────┘
                  ↓
           Structured Data
                  ↓
            Risk Engine
                  ↓
         Personalized Risk
                  ↓
          Advisory Service
                  ↓
          Safety Validation
                  ↓
          Alert Processing
                  ↓
              SQLite
                  ↓
       Streamlit Dashboard
```

---

## Risk Assessment

The risk engine is intentionally deterministic rather than relying entirely on generated text.

It uses environmental and profile factors such as:

- AQI
- Temperature
- Humidity
- UV index
- Age group
- Health sensitivity
- Occupation
- Outdoor exposure

The result is converted into a risk score and level.

The application currently uses these broad levels:

| Score | Risk Level |
|---:|---|
| 0–29 | Low |
| 30–54 | Moderate |
| 55–74 | High |
| 75–100 | Very High |

These values are application rules for the prototype and should not be interpreted as a clinical risk scale.

---

## AI Advisory Layer

The advisory layer receives structured data from the application rather than directly reading arbitrary API responses.

The context includes:

- Location
- User profile
- Current weather
- Air quality
- Pollutants
- Calculated risk
- Main risk factors

The response is designed to contain:

- A concise summary
- Practical actions
- Outdoor guidance
- Personalization explanation

The application also has a deterministic fallback advisory so that the dashboard can still provide a useful basic response when AI generation is unavailable.

---

## Safety Layer

The safety layer is designed to keep the application within the scope of environmental guidance.

The application should not:

- Diagnose medical conditions
- Prescribe medicines
- Tell a user to stop a prescribed treatment
- Invent environmental measurements
- Present the generated guidance as a medical diagnosis

---

## Database

The application uses SQLite and creates the database automatically.

Database path:

```text
database/app.db
```

The application stores:

- User profiles
- Environmental readings
- Risk assessments
- AI advisories
- Alerts

The database is intentionally lightweight so the project can be developed and demonstrated without requiring a separate database server.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/BreatheWise-AI.git
cd BreatheWise-AI
```

### 2. Create a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\\Scripts\\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a local environment file:

```bash
cp .env.example .env
```

The application expects the AI service credentials through environment variables.

The main variable used by the current implementation is:

```text
AI_API_KEY=your_api_key_here
```

The application does not require a key for the Open-Meteo weather and air-quality endpoints used by the current project.

Never commit a real secret to GitHub.

For Streamlit deployment, use the deployment platform's secrets configuration rather than committing a local secret file.

---

## Running the Application

Start the application with:

```bash
streamlit run app.py
```

The browser should open the Streamlit application locally.

The main navigation contains:

```text
Dashboard
Profile
Trends
History
```

---

## Testing

Run the automated test suite with:

```bash
pytest -q
```

The tests cover core application logic including:

- Risk calculations
- Advisory validation
- Service response handling
- Input validation

Additional tests can be added as new functionality is introduced.

---

## GitHub Setup

Recommended repository:

```text
BreatheWise-AI
```

Basic workflow:

```bash
git init
git add .
git commit -m "Initial BreatheWise AI project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/BreatheWise-AI.git
git push -u origin main
```

For feature development:

```bash
git checkout -b feature/dashboard
```

After completing a feature:

```bash
git add .
git commit -m "Improve dashboard layout"
git push -u origin feature/dashboard
```

Merge the feature branch into `main` after testing.

---

## Deployment

The application is designed to be deployable as a Streamlit web application.

General deployment process:

1. Push the repository to GitHub.
2. Create a Streamlit deployment from the GitHub repository.
3. Set the application entry point to `app.py`.
4. Add required secrets through the deployment platform.
5. Deploy the application.
6. Test location search, weather, AQI, profile, risk, advisory, and history functionality.

Before deployment, verify that:

- `.env` is not committed.
- Real API keys are not present in the repository.
- `requirements.txt` contains all required dependencies.
- The database can be initialized automatically.
- API failures are handled gracefully.

---

## Hackathon Demo Flow

A strong demonstration should focus on personalization rather than only displaying weather data.

### Demonstration sequence

1. Open the application dashboard.
2. Select a location.
3. Show the live weather conditions.
4. Show the live AQI and pollutants.
5. Show the personalized risk score.
6. Show the generated advisory.
7. Change the user profile while keeping the location unchanged.
8. Show how the risk and guidance change.
9. Open the Trends page.
10. Open Alert History.

### Main presentation message

> **Same environmental conditions. Different people. Different advice.**

This demonstrates the main purpose of BreatheWise AI clearly and quickly.

---

## Limitations

This is a hackathon/prototype application and has several limitations:

- Environmental data depends on the availability and quality of the external data sources.
- Historical trends are based on snapshots collected by the application rather than a large preloaded historical dataset.
- Risk scoring is a prototype rules system, not a clinically validated risk model.
- AI-generated guidance may still require human review for production use.
- The application does not replace professional medical advice.
- Browser deployment may require additional configuration for persistent storage if long-term history is needed.

---

## Future Enhancements

Possible future development includes:

- More detailed location and station selection
- Improved environmental trend analysis
- Personalized outdoor-time recommendations
- Interactive pollution maps
- What-if profile simulations
- Push notifications or email alerts
- Authentication and multiple user profiles
- Cloud database support
- Improved accessibility and multilingual support
- More sophisticated risk calibration using validated public-health guidance
- Mobile-friendly progressive web application support

---

## Medical and Safety Disclaimer

BreatheWise AI provides general environmental information and personalized environmental guidance for demonstration and educational purposes.

It is **not a medical diagnostic system**, does not replace professional medical care, and should not be used to make medical decisions.

Users experiencing concerning or severe symptoms should seek appropriate professional medical assistance.

---

## License

Add the license selected by your team before publishing the project publicly.

For a hackathon repository, an MIT License is a common choice when the team wants a permissive open-source license.

---

## Acknowledgements

This project uses open and developer-friendly technologies and data services, including:

- Open-Meteo for weather and air-quality data
- Streamlit for the application interface
- Plotly for data visualization
- Pandas for data processing
- SQLite for local persistence

---

## Project Status

**Status:** Hackathon-ready prototype

The project is organized to support rapid development, demonstration, testing, and deployment while keeping the environmental data layer, risk engine, AI advisory layer, safety checks, database, and user interface separated into maintainable modules.
