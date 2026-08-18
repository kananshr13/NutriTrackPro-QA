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
```

## Tech Stack

- Python
- Pytest
- Requests
- python-dotenv
- REST APIs
- JUnit XML
- HTML/CSS/JavaScript

## Test Coverage

| Area | Tests |
|---|---:|
| Authentication | 2 |
| Health | 1 |
| Meals | 2 |
| Profile | 2 |
| **Total** | **7** |

## Running the Tests

Create and activate the virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the complete QA pipeline:

```bash
./scripts/run_qa.sh
```

The script:

1. Executes all Pytest API tests.
2. Generates a JUnit XML report.
3. Converts the XML results into dashboard JSON data.

## Test Results

A successful run currently produces:

```text
7 passed
0 failed
0 skipped
0 errors
100% pass rate
```

## QA Dashboard

The dashboard uses the generated:

```text
dashboard/data/test-results.json
```

to display the latest automated test results.

Open `dashboard/index.html` in a browser to view the dashboard.

## Environment Variables

API configuration is stored in a local `.env` file.

Example:

```env
BASE_URL=your_api_url
```

Do not commit `.env` or expose API credentials in the repository.

## Reporting Flow

```text
Pytest API Tests
       ↓
JUnit XML
       ↓
generate_report.py
       ↓
test-results.json
       ↓
QA Dashboard
```

## Future Improvements

- GitHub Actions CI/CD
- Automatic test execution on every push
- GitHub Secrets
- Dashboard deployment
- Historical test runs
- Defect tracking
- API response metrics
- Playwright E2E testing
- UI testing
- Database testing
- Security and authentication testing



