# Contributing to OpenBayanMesh-Edge

We welcome contributions to the OpenBayanMesh-Edge project! By participating, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). This document outlines the guidelines for contributing to the project.

## 1. Getting Started

### Prerequisites
-   **Git:** Familiarity with Git for version control.
-   **Python 3.12+:** Basic knowledge of Python programming.
-   **Docker & Docker Compose:** Understanding of containerization concepts.

### Development Environment Setup
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-org/OpenBayanMesh-Edge.git
    cd OpenBayanMesh-Edge
    ```
2.  **Create and configure your `.env` file:**
    Copy `.env.example` to `.env` and fill in the necessary environment variables, especially `TUNNEL_TOKEN`, `TUNNEL_ID`, `NEO4J_PASSWORD`, `REGION`, and `DATA_DOMAINS`.
    ```bash
    cp .env.example .env
    ```
3.  **Install Python dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r src/requirements.txt
    ```
4.  **Run the development stack:**
    ```bash
    docker-compose up --build -d
    ```
    This will start the FastAPI app, Neo4j, and Cloudflared tunnel.

## 2. Running Tests and Linting

Before submitting a Pull Request, ensure all tests pass and your code adheres to our style guidelines.

### Automated Checks
We use `flake8` for linting, `mypy` for type-checking, `safety` for dependency vulnerability scanning, and `bandit` for static security analysis. All these checks are bundled into a single script.

To run all checks locally:

```bash
./test.sh
```

This script will execute:
-   `flake8 src/`: For code style and quality.
-   `mypy src/`: For type consistency.
-   `safety check -r src/requirements.txt`: To scan for known vulnerabilities in dependencies.
-   `bandit -r src/ -ll -f custom -o bandit_report.json`: For static security analysis of the code.
-   `pytest tests/`: For unit and integration tests.

### Running Pytest Separately
To run only the unit and integration tests:

```bash
pytest tests/
```

### Example Test Reports
-   `bandit_report.json`: A JSON file containing the results of the Bandit security scan will be generated in the root directory.

## 3. Code Style and Linting

-   Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code style.
-   Ensure your code passes `flake8` checks. Configuration is in `.flake8`.
-   Ensure your code passes `mypy` type checks. Configuration is in `mypy.ini`.

## 4. Submitting Pull Requests (PRs)

1.  **Fork the repository** and create a new branch for your feature or bug fix.
2.  **Make your changes**, ensuring they align with the project's goals and existing architecture.
3.  **Write clear, concise commit messages** that explain the purpose of your changes.
4.  **Ensure all local tests and checks pass** (`./test.sh`).
5.  **Update documentation** as necessary (e.g., `README.md`, `docs/API.md`, `docs/INSTALL.md`).
6.  **Submit your Pull Request** to the `main` branch.

### Code Review and Security Implications
All PRs will undergo peer review. Reviewers will pay close attention to security implications, performance, and adherence to project standards. Security scans (Safety, Bandit) will be run automatically by CI/CD workflows. If security issues are found, contributors will be notified with remediation recommendations.

### Code of Conduct Agreement
By submitting a PR, you implicitly agree to our [Code of Conduct](CODE_OF_CONDUCT.md). Your first commit or PR will only be merged after you have read and agreed to it.

## 5. Community Interaction

-   **Feedback and Suggestions:** We encourage feedback and suggestions! Please use [GitHub Issues](https://github.com/your-org/OpenBayanMesh-Edge/issues) or [GitHub Discussions](https://github.com/your-org/OpenBayanMesh-Edge/discussions) for general questions, ideas, or feature requests.
-   **Bug Reports:** If you find a bug, please open an issue on GitHub, providing as much detail as possible.
-   **Security Vulnerabilities:** For security vulnerabilities, please follow the private reporting procedure outlined in [`docs/SECURITY.md`](SECURITY.md).
-   **Community Calls:** We aim to schedule regular community calls or asynchronous reviews to coordinate on mesh growth and security topics. Details will be announced via GitHub Discussions or other community channels.

Thank you for contributing to OpenBayanMesh-Edge!
