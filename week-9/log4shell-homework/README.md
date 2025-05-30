## Setup
 - To create the docker container, run the 'docker compose up --build' command from your terminal. This should build a new docker container that we can test for vulnerabilities. 
 - Wait for the build to complete and t he application to start. ou should see logs indicating the spring boot application has started and is listening on ports 8080.

## Test Application Endpoint
 - Send a post request to the '/log' endpointto verify its operational.

 - Open a new terminal and run the following 'curl' command:

```bash
curl -X POST http://localhost:8080/log -H "Content-Type: text/plain" -d 'Hello Application!'
```

## Output
You should receive a response from the application like this:
```
Logged: Hello Application!
```

You should also see a log message in the terminal where the docker container is running that looks like:
 - `... INFO ... User input: Hello Application!`

 # Log4Shell Exploitation & Defense Playground

This repository demonstrates how to **exploit** the Log4Shell vulnerability (CVE-2021-44228), **defend** against it with version updates and input controls, and **simulate incident response** using the MITRE frameworks (ATT&CK, DEFEND, REACT).

---

## Prerequisites

- Docker & Docker Compose installed
- Python 3.8+ (for attacker LDAP server)
- `ldap3` Python package (`pip install ldap3`)
- `curl` for sending HTTP requests

---

## Environment Setup

1. **Clone & Build**  
   ```bash
   git clone <your-repo-url>
   cd log4shell-homework
   docker compose up --build -d

