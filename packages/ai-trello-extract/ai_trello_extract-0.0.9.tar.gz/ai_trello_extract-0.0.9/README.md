# AI Trello Extract

![AI Trello Extract Banner](ai-trello-extract.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI Version](https://badge.fury.io/py/ai-trello-extract.svg)](https://pypi.org/project/ai-trello-extract/)
[![Build Status](https://github.com/DEV3L/ai-trello-extract/actions/workflows/continuous-integration.yml/badge.svg)](https://github.com/DEV3L/ai-trello-extract/actions/workflows/continuous-integration.yml)

## Table of Contents

- [AI Trello Extract](#ai-trello-extract)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Value Proposition](#value-proposition)
  - [Key Features](#key-features)
  - [Technology Stack](#technology-stack)
  - [Installation](#installation)
  - [Setup](#setup)
    - [1. Register for Trello API Access](#1-register-for-trello-api-access)
    - [2. Clone the Repository](#2-clone-the-repository)
    - [3. Configure Environment Variables](#3-configure-environment-variables)
      - [Environment Variables](#environment-variables)
    - [4. Setup a Virtual Environment and Install Dependencies](#4-setup-a-virtual-environment-and-install-dependencies)
  - [Usage](#usage)
    - [What the Script Does:](#what-the-script-does)
  - [Available Scripts](#available-scripts)
  - [Testing](#testing)
    - [Running Tests](#running-tests)
      - [End-to-End Tests](#end-to-end-tests)
      - [Unit Tests](#unit-tests)
      - [Code Coverage](#code-coverage)
  - [Project Structure](#project-structure)
    - [Critical Files and Directories](#critical-files-and-directories)
  - [Contributing](#contributing)
  - [Code of Conduct](#code-of-conduct)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)
  - [Additional Resources](#additional-resources)

## Introduction

**AI Trello Extract** is a Python-based tool that leverages the `py-trello` library and `python-dotenv` to interact seamlessly with the Trello API. It facilitates the authentication process via OAuth and enables users to retrieve detailed information from Trello boards, lists, and cards. This project exemplifies secure API credential management and organized data retrieval for further processing.

## Value Proposition

Managing and extracting data from Trello boards can be cumbersome, especially when dealing with multiple boards and extensive card details. **AI Trello Extract** streamlines this process by providing a secure and efficient way to authenticate with the Trello API, fetch comprehensive board data, and output it in accessible formats like Markdown and JSON. This enables developers and project managers to integrate Trello data into their workflows, documentation, and analytics effortlessly.

## Key Features

- **OAuth Authentication**: Securely authenticate with the Trello API using OAuth.
- **Comprehensive Data Retrieval**: Fetch details of all accessible Trello boards, including lists and cards.
- **Secure Credential Management**: Utilize environment variables to manage API credentials securely.
- **Flexible Output Formats**: Export Trello data to Markdown files and JSON for versatile use cases.
- **Automated Testing**: Ensure reliability with comprehensive unit and end-to-end tests.
- **Continuous Integration**: Maintain code quality with GitHub Actions workflows.

## Technology Stack

- **Programming Language**: Python 3.12+
- **Libraries**:
  - [`py-trello-api`](https://pypi.org/project/py-trello-api/)
  - [`python-dotenv`](https://pypi.org/project/python-dotenv/)
  - [`loguru`](https://pypi.org/project/loguru/)
- **Tools**:
  - [`Hatch`](https://hatch.pypa.io/latest/)
  - [`pytest`](https://pytest.org/)
  - [`Ruff`](https://github.com/charliermarsh/ruff)
  - [`Twine`](https://twine.readthedocs.io/en/stable/)
- **Continuous Integration**: GitHub Actions

## Installation

Install **AI Trello Extract** via PyPI:

```bash
pip install ai-trello-extract
```

For more details, visit the [PyPI project page](https://pypi.org/project/ai-trello-extract/).

## Setup

### 1. Register for Trello API Access

1. **Sign Up for a Trello Account**:

   - If you don't have a Trello account, sign up at [Trello](https://trello.com/).

2. **Get API Key and Token**:
   - Navigate to the [Trello Developer Portal](https://trello.com/app-key).
   - Copy your **API Key**.
   - Click on the "Token" link to generate a **Token**. This token will be used for authentication in your API requests.

### 2. Clone the Repository

```bash
git clone https://github.com/DEV3L/ai-trello-extract
cd ai-trello-extract
```

### 3. Configure Environment Variables

Copy the default environment configuration and update it with your Trello API credentials:

```bash
cp env.default .env
```

#### Environment Variables

The following environment variables can be configured in the `.env` file:

- `TRELLO_API_KEY`: Your Trello API key.
- `TRELLO_API_TOKEN`: Your Trello API token.
- `TRELLO_BOARD_NAME`: The name of the Trello board you wish to extract data from.
- `OUTPUT_DIRECTORY`: The directory where output files will be saved (default is `bin`).

### 4. Setup a Virtual Environment and Install Dependencies

Ensure you have [Hatch](https://hatch.pypa.io/latest/) installed. If not, install it using `brew`:

```bash
brew install hatch
```

Create and activate the virtual environment:

```bash
hatch env create
hatch shell
```

## Usage

Run the `run_end_to_end.py` script to authenticate with Trello, fetch board details, and export data:

```bash
python run_end_to_end.py
```

### What the Script Does:

1. **Authentication**: Uses credentials from the `.env` file to authenticate with the Trello API.
2. **Data Retrieval**:
   - Fetches and prints details of all accessible Trello boards.
   - Retrieves and prints lists and cards from the specified Trello board.
3. **Data Export**:
   - Writes board data to a Markdown file.
   - Organizes and writes board data into a structured directory with separate files for each list and card.

## Available Scripts

Defined in `pyproject.toml` under `[tool.hatch.envs.default.scripts]`:

- **End-to-End Tests**:

  ```bash
  hatch run e2e
  ```

- **Unit Tests**:

  ```bash
  hatch run test
  ```

- **Publish Package to PyPI**:

  ```bash
  hatch run publish
  ```

## Testing

The project includes comprehensive tests to ensure reliability and correctness.

### Running Tests

#### End-to-End Tests

Execute end-to-end tests to verify the complete workflow:

```bash
hatch run e2e
```

#### Unit Tests

Run unit tests to validate individual components:

```bash
hatch run test
```

#### Code Coverage

To monitor code coverage within your editor (e.g., VSCode), use Coverage Gutters:

```bash
Command + Shift + P => Coverage Gutters: Watch
```

## Project Structure

```
ai-trello-extract/
├── ai_trello_extract/
│   ├── clients/
│   │   └── trello_client.py
│   ├── dataclasses/
│   │   ├── categorized_list.py
│   │   └── trello_card.py
│   ├── env_variables.py
│   ├── formatters/
│   │   ├── escape_markdown.py
│   │   └── generate_markdown.py
│   ├── orchestrators/
│   │   ├── orchestration_service.py
│   │   └── orchestration_service_test.py
│   ├── services/
│   │   ├── trello_service.py
│   │   └── trello_service_test.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── env_variables_test.py
│   │   └── trello_client_test.py
│   ├── functions.py
│   ├── run_end_to_end.py
│   └── generate_markdown_test.py
├── .env.default
├── LICENSE
├── pyproject.toml
├── continuous-integration.yml
└── README.md
```

### Critical Files and Directories

- **`ai_trello_extract/`**: Main package containing modules for clients, dataclasses, formatters, orchestrators, and services.
- **`tests/`**: Contains unit and integration tests.
- **`pyproject.toml`**: Configuration file for project metadata, dependencies, and tools.
- **`continuous-integration.yml`**: GitHub Actions workflow for continuous integration.
- **`run_end_to_end.py`**: Script to execute the full data extraction and export process.
- **`.env.default`**: Template for environment variables configuration.

## Contributing

We welcome contributions! To contribute:

1. **Fork the Repository**: Click the "Fork" button at the top-right corner of the repository page.
2. **Create a New Branch**: Use `git checkout -b feature/YourFeatureName` to create a new branch.
3. **Make Your Changes**: Implement your feature or bug fix.
4. **Ensure All Tests Pass**: Run `hatch run test` to verify.
5. **Submit a Pull Request**: Provide a detailed description of your changes.

## Code of Conduct

We expect all contributors to adhere to our Code of Conduct:

- **Be Respectful**: Treat everyone with respect and kindness.
- **Be Constructive**: Provide constructive feedback and be open to receiving it.
- **Avoid Discrimination**: Do not use discriminatory or offensive language.
- **Report Unacceptable Behavior**: Notify project maintainers of any violations.

By participating in this project, you agree to abide by these guidelines.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- **[Trello](https://trello.com/)**: For providing an excellent API and platform for project management.
- **[Loguru](https://github.com/Delgan/loguru)**: For the elegant logging library.
- **[Hatch](https://hatch.pypa.io/latest/)**: For the efficient project management tool.
- **OpenAI**: For providing the AI assistant that helped in creating this README.

## Additional Resources

- **Documentation**:
  - [Py-Trello API Documentation](https://py-trello-api.readthedocs.io/)
  - [Python-Dotenv Documentation](https://saurabh-kumar.com/python-dotenv/)
- **Tutorials**:
  - [Integrating Trello API with Python](https://www.tutorialspoint.com/python/python_trello_api.htm)
- **Related Projects**:
  - [AI Assistant Manager](https://github.com/DEV3L/ai-assistant-manager)

---

**Note:** If you have any questions or need further assistance, feel free to open an issue or reach out to the maintainers.
