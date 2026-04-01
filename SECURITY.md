# SECURITY

## Reporting Vulnerabilities

If you discover a security vulnerability in FLOW, please report it responsibly.

**Do not open a public issue for security vulnerabilities.**

Instead, email: security@flow-sim.dev

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Security Measures

- All API inputs validated via Pydantic
- Rate limiting on API endpoints
- CORS restricted to configured origins
- File upload size limits enforced
- No arbitrary code execution in solvers
- SQL injection prevention via SQLAlchemy ORM

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✓         |
| < 0.1   | ✗         |
