# Security Policy

## Overview

Politheon Inc. takes security seriously. This document outlines our security practices, vulnerability reporting process, and links to internal security resources for all repositories under the Politheon-HQ organization.

## Reporting a Vulnerability

If you discover a security vulnerability in any Politheon repository, **do not open a public issue.** Instead:

1. Email **security@politheon.com** with a description of the vulnerability, steps to reproduce, and any relevant screenshots or logs.
2. You will receive an acknowledgment within **48 hours**.
3. We will work with you to understand the scope and severity, and will provide updates as we investigate and remediate.

If the vulnerability involves a third-party dependency, please still report it to us so we can assess the impact on our systems and coordinate disclosure.

## Supported Versions

Security updates are applied to the **main** branch of all active repositories. We do not maintain security patches for feature branches or deprecated repositories.

## Security Tooling

The following security tools are enabled across all Politheon-HQ repositories:

- **GitHub Secret Scanning** — Continuously scans repositories for exposed credentials and secrets. Alerts are routed to repository admins and the security team.
- **Push Protection** — Blocks pushes that contain detected secrets before they reach the repository. If your push is blocked, see our [Push Protection Runbook](docs/push-protection-runbook.md).
- **Dependabot** — Monitors dependencies for known vulnerabilities and opens automated pull requests for security patches.
- **CodeQL / Code Scanning** — Static analysis runs on pull requests to detect security vulnerabilities and code quality issues.
- **Trivy Container Scanning** — Daily vulnerability scans run against production container images.

## Internal Security Resources

| Resource | Description |
|---|---|
| [Push Protection Runbook](docs/push-protection-runbook.md) | What to do when your push is blocked by secret scanning |
| [Branch Protection & PR Requirements](#branch-protection--pr-requirements) | Required reviews, checks, and merge policies |
| [Secrets Management Guidelines](#secrets-management-guidelines) | How to store and rotate credentials |

## Branch Protection & PR Requirements

All repositories in the Politheon-HQ organization enforce the following policies via GitHub rulesets:

- **Required pull request reviews** — At least one approving review is required before merging to protected branches.
- **Required status checks** — CI checks (linting, tests, security scans) must pass before a PR can be merged.
- **No direct pushes to `main`** — All changes must go through a pull request.
- **Conversation resolution** — All review comments must be resolved before merging.
- **Signed commits** — Commit signature verification is required on production branches.

## Secrets Management Guidelines

### Approved Secret Storage

- **GitHub Actions Secrets** — For CI/CD pipelines and GitHub Actions workflows.
- **Azure Key Vault** — For application secrets, API keys, and credentials used in production and development environments.
- **Environment variables** — For local development only. Never commit `.env` files.

### Prohibited Practices

- **Never hardcode secrets** in source code, configuration files, comments, or documentation.
- **Never commit `.env` files** or any file containing credentials. Ensure `.gitignore` includes all relevant patterns.
- **Never share secrets** over Slack, email, or any unencrypted channel. Use Azure Key Vault or GitHub Secrets to share credentials between team members and systems.
- **Never store secrets in Notion, Google Docs, or other collaboration tools.**

### Credential Rotation

- Rotate all secrets immediately if exposure is suspected.
- Rotate production credentials on a regular schedule as defined in our SOC 2 controls.
- Document all rotation events for audit purposes.

## Compliance

Politheon is pursuing SOC 2 Type II compliance. Our security policies, access controls, and operational procedures are designed to meet the Trust Services Criteria for Security, Availability, and Confidentiality. For questions about our compliance posture, contact **security@politheon.com**.

## Contact

- **Security issues:** security@politheon.com
- **CTO:** Hanna Bodnar
- **General questions:** Open an issue in this repository or reach out via internal Slack channels.
