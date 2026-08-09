# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :x:                |

## Reporting a Vulnerability

We take the security of Virtual Lab seriously. If you discover a security vulnerability, including hardcoded API keys, data exposure in transcripts, or injection vulnerabilities in prompt templates, please report it responsibly.

### How to Report

1. **Do NOT open a public GitHub issue** for security vulnerabilities.
2. Email the maintainers directly or submit a private security advisory via GitHub's Security tab.
3. Include the following details in your report:
   - Description of the issue and its potential impact.
   - Step-by-step instructions or proof-of-concept script to reproduce the vulnerability.
   - Suggested remediation or patch if available.

### Response Timeline

- **Acknowledgement:** Within 48 hours.
- **Assessment & Fix:** Within 7 business days for high-severity vulnerabilities.
- **Public Disclosure:** Coordinated after a fix has been released and verified.

## API Key Safety

Virtual Lab requires API keys for OpenAI, BigModel, and Materials Science APIs. 
- **Never commit `.env` files** or hardcode keys in python scripts or Jupyter notebooks.
- Always use environment variables or `.env` templates (see `.env.example`).
- If an API key is accidentally committed, revoke it immediately at the provider dashboard.
