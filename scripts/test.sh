#!/bin/bash

set -e

echo "Running Flake8 linting..."
flake8 src/

echo "Running MyPy type checking..."
mypy src/

echo "Running Safety security scan..."
safety check -r src/requirements.txt

echo "Running Bandit security scan..."
bandit -r src/ -ll -f custom -o bandit_report.json

echo "Running Pytest..."
pytest tests/

echo "All checks passed!"