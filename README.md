# Callculator

[![License](https://img.shields.io/github/license/marcodkts/callculator)](LICENSE)
[![Python version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![Django version](https://img.shields.io/badge/django-5.1%2B-blue)](https://www.djangoproject.com/download/)

This project aims to create a reliable, flexible, and scalable telephone billing application capable of processing detailed call records and delivering accurate billing information, seamlessly integrating with various telecom systems.


## Features



## Installation

### Prerequisites

- Python 3.11+
- Poetry

### Installation Steps

1. Clone the repository:

   ```
   git clone https://github.com/marcodkts/callculator/backend.git
   ```

2. Navigate to the project directory:

   ```
   cd ./callculator
   ```

3. Install dependencies:

   ```
   poetry install
   ```

4. Run migrations:

   ```
   poetry run python manage.py migrate
   ```

5. Start the development server:

   ```
   poetry run python manage.py runserver
   ```

6. Open your web browser and navigate to `http://127.0.0.1:8000` to access the application.


## Contributing

Contributions are welcome! Please see the [contributing guidelines](CONTRIBUTING.md) for more information.

## Acknowledgements

- [Django](https://www.djangoproject.com/) - Web framework for building Python applications.
- [Poetry](https://python-poetry.org/) - Python packaging and dependency management made easy
