# NutriTrackPro QA Automation

API test automation framework for NutriTrackPro, a nutrition and meal-tracking application. The project validates core backend functionality through automated API tests using Python, Pytest, and Requests.

The test suite covers authentication, profile management, meal logging, authorization, validation, boundary-value testing, and API availability.

## Live Dashboard 

* https://nutritrackpro-qa.vercel.app/
* NutriTrackPro : https://nutri-track-pro-six.vercel.app

### Dashboard Preview 

![Main Page 1](screenshots/Screenshot%202026-08-19%20at%2012.59.06 AM.png)

![Main Page 2](screenshots/Screenshot%202026-08-19%20at%2012.59.41 AM.png)

![Main Page 3](screenshots/Screenshot%202026-08-19%20at%2012.59.55 AM.png)

## Project Overview

NutriTrackPro is a nutrition tracking application with APIs for:

* User authentication
* User profile management
* Meal logging
* Daily meal retrieval
* Nutrition and calorie evaluation
* User authorization

This repository focuses on testing the backend APIs rather than the frontend application.

## Tech Stack

| Technology     | Purpose                         |
| -------------- | ------------------------------- |
| Python         | Test automation language        |
| Pytest         | Test framework                  |
| Requests       | HTTP/API testing                |
| FastAPI        | Backend API being tested        |
| pytest markers | Test categorization             |
| GitHub Actions | Continuous integration          |
| XML reports    | Automated test result reporting |
| Render         | Deployed API environment        |

## Project Structure

```text
NutriTrackPro-QA/
│
├── automation/
│   └── api/
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_health.py
│       ├── test_meals.py
│       └── test_profile.py
│
├── reports/
│   └── test-results.xml
│
├── pytest.ini
├── requirements.txt
└── README.md
```

## Test Coverage

### Authentication

Tests cover:

* Successful login with valid credentials
* Login with invalid credentials
* Missing username
* Missing password
* Empty credentials
* Access token generation
* Token type validation

### Profile

Tests cover:

* Retrieving an authenticated user's profile
* Accessing the profile without authentication
* Invalid authentication token
* Malformed authorization header
* Updating user profile
* Profile calorie target calculation
* Unrealistic profile values
* Unauthorized profile updates

### Meal API

Tests cover:

* Logging a meal
* Retrieving today's meals
* Verifying logged meal data
* Missing required meal fields
* Negative calorie values
* Calorie boundary conditions
* Meals above the calorie threshold
* Unauthorized meal logging

### Health Check

The test suite verifies that the deployed API health endpoint is available and returns the expected HTTP status.

```text
GET /health
Expected: 200 OK
```

## Boundary Value Testing

The meal API includes boundary-value testing around the application's calorie classification logic.

The test suite validates values including:

```text
0
100
400
699
700
701
800
1000
```

The current application behavior classifies:

```text
Calories <= 700  -> healthy
Calories > 700   -> unhealthy
```

The tests verify both sides of the boundary rather than testing only normal values.

## Test Categorization

Tests are organized using Pytest markers.

```ini
[pytest]
markers =
    smoke: Critical tests that verify core application functionality
    regression: Full regression test suite
    negative: Tests that verify invalid inputs and error handling
```

### Smoke Tests

Critical tests covering core functionality such as:

* API availability
* Valid authentication
* Profile retrieval
* Profile updates
* Meal logging

Run smoke tests with:

```bash
pytest -m smoke -v
```

### Regression Tests

Run the complete regression suite with:

```bash
pytest -m regression -v
```

### Negative Tests

Run validation and error-handling tests with:

```bash
pytest -m negative -v
```

## Authentication Fixture

The test framework uses a session-scoped Pytest fixture to authenticate once and reuse the generated access token across tests.

This avoids repeatedly logging in before every test and reduces unnecessary API requests.

The credentials are loaded through environment variables:

```text
QA_USERNAME
QA_PASSWORD
```

Credentials are not stored directly in the test source code.

## Configuration

The API base URL is maintained separately from the test cases.

Example:

```python
BASE_URL = "https://nutritrackpro-api.onrender.com"
```

This allows the tests to target the deployed backend without hardcoding URLs throughout individual test files.

## Running the Tests

### 1. Clone the repository

```bash
git clone <repository-url>
cd NutriTrackPro-QA
```

### 2. Create a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure credentials

Set the required environment variables:

```bash
export QA_USERNAME="your_test_username"
export QA_PASSWORD="your_test_password"
```

### 5. Run the complete API test suite

```bash
pytest automation/api -v
```

### 6. Generate the test report

```bash
pytest automation/api -v --junitxml=reports/test-results.xml
```

## CI/CD

The project is configured to execute API tests through GitHub Actions.

The CI pipeline:

1. Sets up the Python environment
2. Installs project dependencies
3. Loads test credentials through GitHub Secrets
4. Executes the API automation suite
5. Generates an XML test report
6. Fails the workflow when an automated test fails

This ensures that backend changes can be automatically validated rather than relying only on manual testing.

## Defects Identified During Testing

The automation suite was also used to identify backend validation issues.

One example was negative calorie input.

The API initially accepted:

```json
{
    "calories": -100
}
```

with a successful response.

The test identified this as an invalid input condition. Backend validation was subsequently added to the `MealCreate` model so negative calorie values are rejected.

This demonstrates the use of automation not only for regression testing but also for identifying application defects.

## Test Results

Current API automation suite:

```text
24 tests passed
0 tests failed
```

The suite has been executed against the deployed NutriTrackPro backend.

## Quality Engineering Approach

The project applies several practical QA techniques:

* Functional API testing
* Positive testing
* Negative testing
* Boundary-value analysis
* Authentication testing
* Authorization testing
* Input validation
* Response validation
* Regression testing
* Smoke testing
* Automated CI execution
* Defect identification and verification

## Future Improvements

Potential improvements include:

* JSON schema validation
* API contract testing
* More comprehensive data-driven testing
* Additional API endpoint coverage
* HTML test reporting
* Parallel test execution
* Environment-specific configuration
* Automated test result publishing in CI
* Integration with API documentation/OpenAPI specifications

## Author

Kanan Sharma

B.Tech Computer Science Engineering (Artificial Intelligence)

NutriTrackPro QA Automation Project
