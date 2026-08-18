# NutriTrackPro QA Automation

Automated API testing framework for NutriTrackPro using Python, Pytest, and Requests.

The project validates core application APIs and generates machine-readable test results that are transformed into a web-based QA dashboard.

## Features

- Automated REST API testing
- Authentication API validation
- Profile API testing
- Meal API testing
- Health API testing
- Pytest-based test execution
- JUnit XML test reporting
- Automated JSON report generation
- QA dashboard with test statistics
- One-command QA execution

## Project Structure


```text
NutriTrackPro-QA/
│
├── automation/
│   └── api/
│       ├── test_auth.py
│       ├── test_health.py
│       ├── test_meals.py
│       └── test_profile.py
│
├── dashboard/
│   ├── data/
│   │   └── test-results.json
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── reports/
│   └── test-results.xml
│
├── scripts/
│   ├── generate_report.py
│   └── run_qa.sh
│
├── test data/
│
├── .gitignore
├── requirements.txt
└── README.md

## Tech Stack


