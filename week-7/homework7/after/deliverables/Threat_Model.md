## Threat Modeling

## 1. STRIDE Analysis
| Threat                 | Vulnerability             | Mitigation                             |
| ---------------------- | ------------------------- | -------------------------------------- |
| Spoofing               | No auth on endpoints      | Add API key or token-based auth        |
| Tampering              | Command injection in ping | Validate and sanitize input            |
| Repudiation            | No logging or audit trail | Add structured logging                 |
| Information Disclosure | Unsecured traffic         | Use HTTPS in production                |
| Denial of Service      | Unlimited requests        | Add rate limiting and input validation |
| Elevation of Privilege | Root container access     | Use non-root users in Docker           |

## 2. MITRE ATTACK Mapping (Containers)
| Tactic         | Technique ID | Technique Name | Application Relevance |
|----------------|--------------|----------------|------------------------|
| Initial Access | T1190         | Exploit Public-Facing Application | Command injection in `/ping` |
| Execution      | T1059         | Command and Scripting Interpreter | Use of `eval()` |
| Persistence    | T1525         | Implant Container Image | No image signing or validation |
| Privilege Escalation | T1611  | Escape to Host | Root container user |
| Defense Evasion | T1211        | Exploitation for Defense Evasion | Lack of file system isolation |

## 3. Controls Mapping
| Issue | Recommended Control | Framework Reference |
|-------|---------------------|---------------------|
| Hardcoded secrets | Environment secrets | NIST 800-53: SC-12, SC-28 |
| Root container user | Add `USER appuser` | NIST 800-53: AC-6, CM-6 |
| No network restrictions | Isolate with Docker networks | NIST 800-53: SC-7 |
| Missing health check | Add `HEALTHCHECK` | CIS Docker Benchmark |
| Unvalidated inputs | Strict input validation | OWASP Top 10: A1-Injection |

## Conclusion
These threat model identify the major flaws in the system and informs the remediation and architecture redesign. The final implementation significantly reduces the attack surface and enforces least privilege, defense in depth, and secure defaults.