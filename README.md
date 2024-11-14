# Callculator

[![License](https://img.shields.io/github/license/marcodkts/callculator)](LICENSE)
[![Python version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![Django version](https://img.shields.io/badge/django-5.1%2B-blue)](https://www.djangoproject.com/download/)
[![codecov](https://codecov.io/github/marcodkts/callculator/branch/dev/graph/badge.svg?token=3EC11XA42Q)](https://codecov.io/github/marcodkts/callculator)

## Project Description
Callculator is a telephone billing application designed to process detailed call records and generate accurate monthly bills for specific phone numbers. The application is flexible and robust to ensure seamless integration with various telecom systems, which may exhibit inconsistencies or errors. Callculator provides a RESTful HTTP API for efficient record submission and billing retrieval.

## Features
- Accepts detailed call records (start and end types).
- Calculates and retrieves monthly billing information.
- Integrates pricing rules based on call timing.
- Adheres to reliable data handling, preventing record loss and inconsistency.

## Installation Instructions

### Prerequisites
- Python >= 3.11
- Poetry
- Virtual Environment (optional but recommended)
- Required Python libraries (listed in `requirements.txt`)

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repository/callculator.git
   cd callculator
   ```
2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application**:
   ```bash
   python app.py
   ```

### Testing
Run unit tests using:
```bash
pytest .
```
Ensure the `tests` directory contains comprehensive test cases for call record processing and billing calculations.

## Environment Setup
- **System**: Ubuntu 20.04 / Windows 10
- **IDE**: Visual Studio Code / PyCharm
- **Libraries**: Flask/Django, pytest, Swagger (for API documentation)

## API Documentation
The Callculator API offers endpoints for submitting call records and retrieving billing information. It follows OpenAPI 3.0.3 standards.

### Endpoints
#### 1. Call Record Submission
- **URL**: `/callculator/callrecord/`
- **Method**: POST
- **Description**: Submit call records (start or end type).
- **Request Body**:
  ```json
  {
    "id": 1,
    "type": "START",
    "timestamp": "2024-11-14T12:00:00Z",
    "call_id": 12345,
    "source": "9988526423",
    "destination": "9933468278"
  }
  ```
- **Response**: 200 OK with confirmation.

#### 2. Retrieve Billing Information
- **URL**: `/callculator/billing/`
- **Method**: GET
- **Parameters**:
  - `phone_number` (required): Subscriber’s phone number in format `AAXXXXXXXXX`.
  - `dateref` (optional): Reference date in `YYYY-MM` format.
- **Response**:
  ```json
  {
    "dateref": "2024-10",
    "phone_number": "9988526423",
    "records": [
      {
        "destination": "9933468278",
        "date": "2024-10-12",
        "time": "12:00:00",
        "duration": "2h00m00s",
        "cost": 3.96
      }
    ]
  }
  ```

#### 3. Health Check
- **URL**: `/callculator/health_check/`
- **Method**: GET
- **Description**: Simple endpoint for verifying service health.

## Pricing Rules
1. **Standard Rate** (6:00 to 22:00):
   - Fixed fee: R$ 0.36
   - Per minute: R$ 0.09 (charged per complete minute)
2. **Reduced Rate** (22:00 to 6:00):
   - Fixed fee: R$ 0.36
   - No per-minute charge.

## Example Usage
For a call starting at 21:57 and ending at 22:17:
- **Total Cost**:
  - Fixed fee: R$ 0.36
  - 2 minutes at standard rate: R$ 0.18
  - Total: R$ 0.54

## Acknowledgements

- [Django](https://www.djangoproject.com/) - Web framework for building Python applications.
- [Poetry](https://python-poetry.org/) - Python packaging and dependency management made easy
