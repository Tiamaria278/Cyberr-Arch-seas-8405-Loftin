| Threat                 | Vulnerability             | Mitigation                             |
| ---------------------- | ------------------------- | -------------------------------------- |
| Spoofing               | No auth on endpoints      | Add API key or token-based auth        |
| Tampering              | Command injection in ping | Validate and sanitize input            |
| Repudiation            | No logging or audit trail | Add structured logging                 |
| Information Disclosure | Unsecured traffic         | Use HTTPS in production                |
| Denial of Service      | Unlimited requests        | Add rate limiting and input validation |
| Elevation of Privilege | Root container access     | Use non-root users in Docker           |

| ATT\&CK Technique | Description                        | Control             |
| ----------------- | ---------------------------------- | ------------------- |
| T1059             | Command-line interface abuse       | Input validation    |
| T1203             | Exploitation for client execution  | Dependency updates  |
| T1078             | Valid accounts (if secrets leaked) | .env + secrets mgmt |

| Vulnerability     | NIST Control           |
| ----------------- | ---------------------- |
| Root containers   | AC-6 (Least Privilege) |
| Hardcoded secrets | SC-12, SC-28           |
| Unvalidated input | SI-10                  |
