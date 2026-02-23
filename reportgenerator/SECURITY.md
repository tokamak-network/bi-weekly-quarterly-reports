# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly.

**Do NOT open a public issue.**

Instead, email: **security@tokamak.network**

We will respond within 48 hours.

## Supported Versions

| Version | Supported |
|---------|-----------|
| main    | ✅ Active |

## Security Considerations

- API keys are stored in environment variables (never committed)
- CSV uploads are processed in-memory, not persisted
- AI API calls are rate-limited and logged
