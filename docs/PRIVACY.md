# Privacy Policy for OpenBayanMesh-Edge

This document outlines the privacy policy for the OpenBayanMesh-Edge project, detailing our commitment to protecting the privacy of operators, volunteers, and API users. It also provides guidance on the responsible handling of data within the mesh.

## 1. No Collection of Personally Identifiable Information (PII)

The OpenBayanMesh-Edge repository and application are designed **not to collect or transmit any Personally Identifiable Information (PII)** from operators, volunteers, or API users. Our core principle is to operate with minimal data footprint, focusing solely on the technical and operational data necessary for the mesh to function.

-   **Operators/Volunteers:** We do not collect personal names, email addresses, physical addresses, or other identifying information beyond what is necessary for node registration (e.g., public keys, node URLs, region information).
-   **API Users:** We do not track individual API users or collect any PII from their requests.

## 2. Log Data Handling and Anonymization

While operational logs are kept to ensure system stability, diagnose issues, and monitor performance, the FastAPI service implements measures to protect sensitive information:

-   **Client IP Addresses:** Client IP addresses are anonymized or omitted from standard logs. Where IP addresses might appear (e.g., in raw access logs from a web server or proxy), they are redacted or truncated to prevent identification.
-   **Sensitive Request Data:** Sensitive data within request bodies or headers (e.g., API keys, passwords, tokens) are redacted from logs using filters.
-   **Forensic Debugging:** In rare cases where forensic debugging is required to resolve critical issues, more detailed logging might be temporarily enabled. Such instances will be clearly documented, and access to these logs will be strictly controlled and limited to authorized maintainers, with all sensitive data purged immediately after the debugging period.

## 3. Telemetry and Monitoring Features (Opt-In)

All telemetry or monitoring features within OpenBayanMesh-Edge are **opt-in**. They are clearly documented and controlled by configuration flags (e.g., `TELEMETRY_ENABLED` environment variable).

-   **Transparency:** Users will be explicitly informed about what data is collected, how it is used, and for what purpose before opting in.
-   **Control:** Node operators have full control over whether to enable these features. By default, telemetry is disabled.
-   **Data Minimization:** If enabled, telemetry data will be aggregated and anonymized, focusing on operational metrics (e.g., API request counts, error rates, uptime) rather than individual user behavior.

## 4. Data Contribution Guidelines

Any data contributed to the OpenBayanMesh-Edge mesh must adhere to strict guidelines to protect privacy and ensure legal compliance:

-   **Public Domain or Official Clearance:** All data must be either in the public domain or have official government or open data clearance for public dissemination.
-   **No Confidential or Restricted Information:** Data must **not** contain any confidential, proprietary, or restricted information.
-   **No PII in Data:** Data contributed to the mesh must not contain any Personally Identifiable Information (PII).

Node operators are solely responsible for ensuring that the data they contribute complies with these guidelines and all applicable laws and regulations.

## 5. Legal and Ethical Use of Government Data

OpenBayanMesh-Edge aims to facilitate the ethical and legal use of open government data. Node operators and data consumers must be aware of and adhere to:

-   **Data Licenses:** Respect the licenses associated with any government or open data sources.
-   **Terms of Use:** Comply with the terms of use of data providers.
-   **Privacy Limitations:** Understand and respect any privacy limitations or restrictions on the use of specific datasets.
-   **Disclosure Rules:** Adhere to any disclosure rules or regulations governing the use and dissemination of government data.

## 6. Handling Privacy Concerns and Breaches

OpenBayanMesh-Edge is committed to promptly addressing any privacy concerns or reported breaches.

-   **Reporting:** If you have a privacy concern or suspect a data breach, please report it immediately to the maintainers via [security@openbayanmesh.org](mailto:security@openbayanmesh.org) (replace with actual email).
-   **Response:** All reports will be investigated in accordance with our security policy. We will provide transparency to affected users and take all necessary steps to mitigate any harm and prevent future occurrences.

By adhering to this privacy policy, OpenBayanMesh-Edge aims to build a trustworthy and privacy-respecting open data mesh for the community.
