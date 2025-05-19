
# Securing Containerized Microservices

---

## Assignment Overview

In this assignment, you will assume the role of a **cybersecurity architect** tasked with securing a vulnerable containerized application. You will receive an intentionally insecure multi-service Python web app and must transform it into a secure deployment. The exercise includes environment setup, code remediation, threat modeling, security architecture design, and verification. Your deliverables will include a screen recording of your analysis and remediation process, along with a technical report.

---

## Assignment Instructions

### Part 1: Environment Setup

1. **Understand the Application:**
   - Review the Flask app in the `before/` directory.
   - Note common vulnerabilities such as hardcoded secrets, `eval()` usage, command injection, and insecure defaults.

2. **Run the Environment:**
   - Use `make start` to launch the application.
   - Test the endpoints: `/`, `/ping?ip=8.8.8.8`, and `/calculate?expr=2+3`.

3. **Initial Scanning:**
   - Run `make check`, `make scan`, and `make host-security`.
   - Record identified vulnerabilities and misconfigurations.

### Part 2: Secure the App and Container

1. **Code Remediation:**
   - Refactor `app.py` to:
     - Eliminate hardcoded passwords.
     - Replace `eval()` with `ast.literal_eval`.
     - Validate all inputs.
     - Restrict Flask to localhost.

2. **Docker Hardening:**
   - Use a minimal base image.
   - Ensure the app runs as a non-root user.
   - Add a `HEALTHCHECK` directive.
   - Implement multi-stage builds if possible.

3. **docker-compose.yml Improvements:**
   - Add `read_only`, `security_opt`, `mem_limit`, and `pids_limit`.
   - Restrict port exposure to `127.0.0.1`.
   - Use `.env` files for secret handling.

### Part 3: Threat Modeling

1. **Threat Model Documentation:**
   - Perform STRIDE analysis on the app.
   - Use MITRE ATT&CK for Containers to identify relevant techniques.
   - Create a table mapping vulnerabilities to controls (e.g., NIST 800-53).

2. **Save and Submit:**
   - Write results in `deliverables/threat_model.md`.

### Part 4: Security Architecture Implementation

1. **Architecture Design:**
   - Draft a diagram showing the hardened app infrastructure (use tools like Lucidchart or draw.io).
   - Save as `deliverables/architecture_diagram.png`.

2. **Auto-Hardening Script:**
   - Write a Python script (`docker_security_fixes.py`) to:
     - Update `daemon.json` with hardening flags.
     - Inject `USER`, `HEALTHCHECK`, and limits into Dockerfile and Compose.

### Part 5: Recording the Simulation

1. **Record Your Screen:**
   - Use OBS or QuickTime.
   - Include:
     - Initial scan and vulnerable app behavior.
     - Code and config remediation.
     - Threat model explanation.
     - Re-scans showing reduced vulnerabilities.

2. **Add Commentary:**
   - Use voiceover or annotations.
   - Describe what you are doing and why.

3. **Export:**
   - Save as MP4.

### Part 6: Summary Report

Write `deliverables/summary_report.md` (1–2 pages) including:
- Steps taken.
- Vulnerabilities found and fixed.
- Architecture and how it improves security.
- Reflection on lessons learned.

---

## Expectations

Students are expected to:
- Submit a screen recording (MP4) demonstrating the analysis, remediation, and verification process.
- Provide a link to publicly accessible GitHub repository with code and documentation.
- Ensure all deliverables are clear, well-organized, and professionally presented.
- Reflect critically on the security improvements and lessons learned.

---

## Grading Rubric

| Category                        | Excellent (90–100%)                                                  | Good (80–89%)                                              | Satisfactory (70–79%)                                      | Needs Improvement (60–69%)                                | Unsatisfactory (0–59%)                       |
|--------------------------------|------------------------------------------------------------------------|------------------------------------------------------------|------------------------------------------------------------|------------------------------------------------------------|----------------------------------------------|
| **Clarity & Organization**     | Clear, structured video/report with annotations and citations         | Mostly clear, minor issues                                 | Adequate, some structure missing                           | Unclear or disorganized                                  | Missing or unreadable                        |
| **Technical Depth**            | In-depth threat mapping, strong security fixes, MITRE alignment      | Mostly strong analysis and fixes                           | Satisfactory but shallow fixes and mapping                | Basic or incorrect fixes                               | No meaningful technical work                 |
| **Completeness of Simulation** | All stages completed, evidence of secure remediation                 | Most stages complete with small issues                     | Many steps complete, some missing or partially done        | Incomplete setup or remediation                        | Little to no simulation                      |
| **Recording Quality**          | Clear, audible, well-paced, detailed                                 | Mostly clear, minor issues                                | Adequate but basic or unclear explanations                | Low quality, poor narration                  | Not submitted or unusable                   |
| **Reflection & Reasoning**     | Insightful report, strong connection to SSDLC, DiD, etc.             | Clear report with basic insight                           | Simple report, shallow reasoning                          | Minimal insight or understanding                        | No reflection or insight                     |

---
# before

PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin\week-7\homework7\before> make start 
docker compose up -d
[+] Running 16/16
 ✔ db Pulled                                                                                                                                                                                                          9.1s 
 ! web Warning              pull access denied for mywebapp, repository does not exist or may require 'docker login'                                                                                                  0.5s 
Compose can now delegate builds to bake for better performance.
 To do so, set COMPOSE_BAKE=true.
[+] Building 9.0s (14/14) FINISHED                                                                                                                                                                    docker:desktop-linux
 => [web internal] load build definition from Dockerfile                                                                                                                                                              0.1s
 => => transferring dockerfile: 315B                                                                                                                                                                                  0.0s 
 => [web internal] load metadata for docker.io/library/python:3.11-alpine                                                                                                                                             1.0s 
 => [web auth] library/python:pull token for registry-1.docker.io                                                                                                                                                     0.0s
 => [web internal] load .dockerignore                                                                                                                                                                                 0.0s
 => => transferring context: 2B                                                                                                                                                                                       0.0s 
 => [web 1/7] FROM docker.io/library/python:3.11-alpine@sha256:d0199977fdae5d1109a89d0b0014468465e014a9834d0a566ea50871b3255ade                                                                                       1.5s 
 => => resolve docker.io/library/python:3.11-alpine@sha256:d0199977fdae5d1109a89d0b0014468465e014a9834d0a566ea50871b3255ade                                                                                           0.0s 
 => => sha256:2c164a0845dbcf6f53df3e9514d68b6a4046aba5a619ed41af7e862824d6e015 250B / 250B                                                                                                                            0.1s 
 => => sha256:a78edf41f9aee79826d32c971b192c51c10860bb102e88c6d1b1b549d0602194 16.21MB / 16.21MB                                                                                                                      0.9s 
 => => sha256:eb8fdeee2de28d2dc60aa8b92f96d32d3b35f16aa134db72e39a9dce441835b3 460.21kB / 460.21kB                                                                                                                    0.1s
 => => sha256:f18232174bc91741fdf3da96d85011092101a032a93a388b79e99e69c2d5c870 3.64MB / 3.64MB                                                                                                                        0.5s 
 => => extracting sha256:f18232174bc91741fdf3da96d85011092101a032a93a388b79e99e69c2d5c870                                                                                                                             0.1s 
 => => extracting sha256:eb8fdeee2de28d2dc60aa8b92f96d32d3b35f16aa134db72e39a9dce441835b3                                                                                                                             0.2s 
 => => extracting sha256:a78edf41f9aee79826d32c971b192c51c10860bb102e88c6d1b1b549d0602194                                                                                                                             0.4s 
 => => extracting sha256:2c164a0845dbcf6f53df3e9514d68b6a4046aba5a619ed41af7e862824d6e015                                                                                                                             0.0s 
 => [web internal] load build context                                                                                                                                                                                 0.1s 
 => => transferring context: 2.69kB                                                                                                                                                                                   0.0s 
 => [web 2/7] RUN addgroup -S appgroup && adduser -S -G appgroup appuser                                                                                                                                              0.7s 
 => [web 3/7] WORKDIR /app                                                                                                                                                                                            0.1s 
 => [web 4/7] COPY requirements.txt .                                                                                                                                                                                 0.1s 
 => [web 5/7] RUN pip install --no-cache-dir -r requirements.txt                                                                                                                                                      3.4s 
 => [web 6/7] COPY . .                                                                                                                                                                                                0.1s 
 => [web 7/7] RUN chown -R appuser:appgroup /app                                                                                                                                                                      0.5s 
 => [web] exporting to image                                                                                                                                                                                          1.2s 
 => => exporting layers                                                                                                                                                                                               0.9s 
 => => exporting manifest sha256:bde4c4445aa57607026be0a4d658dad94bdece2d6377d7d25c870b92451cba16                                                                                                                     0.0s 
 => => exporting config sha256:7f83a3d0ad0035e5e46ecb359611522248984313b70eebc3fc9cda09ad94c4e1                                                                                                                       0.0s 
 => => exporting attestation manifest sha256:ad107ab5aa407b68c1002974c9cdf06034a4fdfd0846579d0a13d3858f91f3c4                                                                                                         0.0s 
 => => exporting manifest list sha256:cc36a7cc10172f86e75a95837f97f8dd83a62ccc3a2ea8c45d76d1e3e18bec4b                                                                                                                0.0s 
 => => naming to docker.io/library/mywebapp:latest                                                                                                                                                                    0.0s 
 => => unpacking to docker.io/library/mywebapp:latest                                                                                                                                                                 0.3s 
 => [web] resolving provenance for metadata file                                                                                                                                                                      0.0s 
[+] Running 5/5
 ✔ web                      Built                                                                                                                                                                                     0.0s 
 ✔ Network before_frontend  Created                                                                                                                                                                                   0.1s 
 ✔ Network before_backend   Created                                                                                                                                                                                   0.1s 
 ✔ Container before-db-1    Started                                                                                                                                                                                   0.7s 
 ✔ Container before-web-1   Started                                                                                                                                                                                   1.1s 
PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin\week-7\homework7\before> make check
"Running code analysis with Bandit..."
docker run --rm -v :/app python:3.9-alpine sh -c "pip install bandit && bandit -r /app"
docker: invalid spec: :/app: empty section between colons

Run 'docker run --help' for more information
make: *** [Makefile:4: check] Error 125
PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin\week-7\homework7\before> make scan
docker scout recommendations mywebapp:latest
    i New version 1.18.0 available (installed version is 1.17.1) at https://github.com/docker/scout-cli
    v Image stored for indexing  
    v Indexed 65 packages

    i Base image was auto-detected. To get more accurate recommendations, build images with max-mode provenance attestations.
      Review docs.docker.com ↗ for more information.
      Alternatively, use  docker scout recommendations --tag <base image tag>  to pass a specific base image tag.

  Target   │  mywebapp:latest 
    digest │  cc36a7cc1017 

## Recommended fixes

  Base image is  python:3.11-alpine 

  Name            │  3.11-alpine 
  Digest          │  sha256:81d42a73add8e508771ee8e923f9f8392ec1c3d1e482d7d594891d06e78fb51c 
  Vulnerabilities │    0C     1H     0M     0L 
  Pushed          │ 1 week ago
  Size            │ 20 MB
  Packages        │ 58
  Flavor          │ alpine
  OS              │ 3.21
  Runtime         │ 3.11.12


  │ The base image is also available under the supported tag(s)  
  3.11-
  │ alpine3.21 ,  3.11.12-alpine ,  3.11.12-alpine3.21 . If you want
  to
  │ display recommendations specifically for a different tag, please
  │ re-run the command using the  --tag  flag.



Refresh base image
  Rebuild the image using a newer base image version. Updating this may result in breaking changes.

  v This image version is up to date.


Change base image
  The list displays new recommended tags in descending order, where the top results are rated as most suitable.


              Tag              │                        Details                        │   Pushed   │       Vulnerabilities
───────────────────────────────┼───────────────────────────────────────────────────────┼────────────┼──────────────────────────────
   3.13-alpine                 │ Benefits:                                             │ 1 week ago │    0C     0H     0M     0L
  Tag is preferred tag         │ • Same OS detected                                    │            │           -1
  Also known as:               │ • Minor runtime version update                        │            │
  • alpine                     │ • Image is smaller by 3.5 MB                          │            │
  • alpine3.21                 │ • Image contains 15 fewer packages                    │            │
  • 3.13.3-alpine              │ • Tag is preferred tag                                │            │
  • 3.13.3-alpine3.21          │ • Image introduces no new vulnerability but removes 1 │            │
  • 3.13-alpine3.21            │                                                       │            │
  • 3-alpine                   │ Image details:                                        │            │
  • 3-alpine3.21               │ • Size: 17 MB                                         │            │
                               │ • Flavor: alpine                                      │            │
                               │ • OS: 3.21                                            │            │
                               │ • Runtime: 3.13.3                                     │            │
                               │                                                       │            │
                               │                                                       │            │
                               │                                                       │            │
   3.12-alpine                 │ Benefits:                                             │ 1 week ago │    0C     0H     0M     0L
  Minor runtime version update │ • Same OS detected                                    │            │           -1
  Also known as:               │ • Minor runtime version update                        │            │
  • 3.12.10-alpine             │ • Image is smaller by 2.4 MB                          │            │
  • 3.12.10-alpine3.21         │ • Image contains 2 fewer packages                     │            │
  • 3.12-alpine3.21            │ • Image introduces no new vulnerability but removes 1 │            │
  • 3.12-alpine3.21            │ • Image introduces no new vulnerability but removes 1 │            │
                               │                                                       │            │
                               │ Image details:                                        │            │
  • 3.12-alpine3.21            │ • Image introduces no new vulnerability but removes 1 │            │
                               │                                                       │            │
  • 3.12-alpine3.21            │ • Image introduces no new vulnerability but removes 1 │            │
  • 3.12-alpine3.21            │ • Image introduces no new vulnerability but removes 1 │            │
  • 3.12-alpine3.21            │ • Image introduces no new vulnerability but removes 1 │            │
  • 3.12-alpine3.21            │ • Image introduces no new vulnerability but removes 1 │            │
  • 3.12-alpine3.21            │ • Image introduces no new vulnerability but removes 1 │            │
                               │                                                       │            │
  • 3.12-alpine3.21            │ • Image introduces no new vulnerability but removes 1 │            │
                               │                                                       │            │
                               │ Image details:                                        │            │
  • 3.12-alpine3.21            │ • Image introduces no new vulnerability but removes 1 │            │
                               │                                                       │            │
  • 3.12-alpine3.21            │ • Image introduces no new vulnerability but removes 1 │            │
  • 3.12-alpine3.21            │ • Image introduces no new vulnerability but removes 1 │            │
  • 3.12-alpine3.21            │ • Image introduces no new vulnerability but removes 1 │            │
                               │                                                       │            │
                               │ Image details:                                        │            │
                               │ • Size: 18 MB                                         │            │
                               │ • Flavor: alpine                                      │            │
                               │ • OS: 3.21                                            │            │
                               │ • Runtime: 3.12.10                                    │            │
                               │                                                       │            │
                               │                                                       │            │
                               │                                                       │            │

PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin\week-7\homework7\before>

PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin> cd week7 
cd : Cannot find path 'C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin\week7' because it does not exist.
At line:1 char:1
+ cd week7
+ ~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (C:\Users\jewel\...05-Loftin\week7:String) [Set-Location], ItemNotFoundException
    + FullyQualifiedErrorId : PathNotFound,Microsoft.PowerShell.Commands.SetLocationCommand

PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin> cd week-7
PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin\week-7> cd homework7
PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin\week-7\homework7> cd before
PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin\week-7\homework7\before> make check
"Running code analysis with Bandit..."
docker run --rm -v :/app python:3.9-alpine sh -c "pip install bandit && bandit -r /app"
docker: invalid spec: :/app: empty section between colons

Run 'docker run --help' for more information
make: *** [Makefile:4: check] Error 125
PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin\week-7\homework7\before> make host-security
"Running Docker Bench for Security..."
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker/docker-bench-security
Unable to find image 'docker/docker-bench-security:latest' locally
latest: Pulling from docker/docker-bench-security
378ed37ea5ff: Pull complete
164e5e0f48c5: Pull complete
48fe0d48816d: Pull complete
cd784148e348: Pull complete
Digest: sha256:ddbdf4f86af4405da4a8a7b7cc62bb63bfeb75e85bf22d2ece70c204d7cfabb8
Status: Downloaded newer image for docker/docker-bench-security:latest
# ------------------------------------------------------------------------------
# Docker Bench for Security v1.3.4
#
# Docker, Inc. (c) 2015-
#
# Checks for dozens of common best-practices around deploying Docker containers in production.
# Inspired by the CIS Docker Community Edition Benchmark v1.1.0.
# ------------------------------------------------------------------------------

Initializing Mon May 19 19:10:04 UTC 2025


[INFO] 1 - Host Configuration
[WARN] 1.1  - Ensure a separate partition for containers has been created
[NOTE] 1.2  - Ensure the container host has been Hardened
[PASS] 1.3  - Ensure Docker is up to date
[INFO]      * Using 28.1.1 which is current
[INFO]      * Check with your operating system vendor for support and security maintenance for Docker
[INFO] 1.4  - Ensure only trusted users are allowed to control Docker daemon
[INFO]      * docker:x:101
[WARN] 1.5  - Ensure auditing is configured for the Docker daemon
[INFO] 1.6  - Ensure auditing is configured for Docker files and directories - /var/lib/docker
[INFO]      * Directory not found
[INFO] 1.7  - Ensure auditing is configured for Docker files and directories - /etc/docker
[INFO]      * Directory not found
[INFO] 1.8  - Ensure auditing is configured for Docker files and directories - docker.service
[INFO]      * File not found
[INFO] 1.9  - Ensure auditing is configured for Docker files and directories - docker.socket
[INFO]      * File not found
[INFO] 1.10  - Ensure auditing is configured for Docker files and directories - /etc/default/docker
[INFO]      * File not found
[INFO] 1.11  - Ensure auditing is configured for Docker files and directories - /etc/docker/daemon.json
[INFO]      * File not found
[INFO] 1.12  - Ensure auditing is configured for Docker files and directories - /usr/bin/docker-containerd
[INFO]      * File not found
[INFO] 1.13  - Ensure auditing is configured for Docker files and directories - /usr/bin/docker-runc
[INFO]      * File not found


[INFO] 2 - Docker daemon configuration
[WARN] 2.1  - Ensure network traffic is restricted between containers on the default bridge
[PASS] 2.2  - Ensure the logging level is set to 'info'
[PASS] 2.3  - Ensure Docker is allowed to make changes to iptables
[PASS] 2.4  - Ensure insecure registries are not used
[PASS] 2.5  - Ensure aufs storage driver is not used
[INFO] 2.6  - Ensure TLS authentication for Docker daemon is configured
[INFO]      * Docker daemon not listening on TCP
[INFO] 2.7  - Ensure the default ulimit is configured appropriately
[INFO]      * Default ulimit doesn't appear to be set
[WARN] 2.8  - Enable user namespace support
[PASS] 2.9  - Ensure the default cgroup usage has been confirmed
[PASS] 2.10  - Ensure base device size is not changed until needed
[WARN] 2.11  - Ensure that authorization for Docker client commands is enabled
[WARN] 2.12  - Ensure centralized and remote logging is configured
[INFO] 2.13  - Ensure operations on legacy registry (v1) are Disabled (Deprecated)
[WARN] 2.14  - Ensure live restore is Enabled
[WARN] 2.15  - Ensure Userland Proxy is Disabled
[INFO] 2.16  - Ensure daemon-wide custom seccomp profile is applied, if needed
[PASS] 2.17  - Ensure experimental features are avoided in production
[WARN] 2.18  - Ensure containers are restricted from acquiring new privileges


[INFO] 3 - Docker daemon configuration files
[INFO] 3.1  - Ensure that docker.service file ownership is set to root:root
[INFO]      * File not found
[INFO] 3.2  - Ensure that docker.service file permissions are set to 644 or more restrictive
[INFO]      * File not found
[INFO] 3.3  - Ensure that docker.socket file ownership is set to root:root
[INFO]      * File not found
[INFO] 3.4  - Ensure that docker.socket file permissions are set to 644 or more restrictive
[INFO]      * File not found
[INFO] 3.5  - Ensure that /etc/docker directory ownership is set to root:root
[INFO]      * Directory not found
[INFO] 3.6  - Ensure that /etc/docker directory permissions are set to 755 or more restrictive
[INFO]      * Directory not found
[INFO] 3.7  - Ensure that registry certificate file ownership is set to root:root
[INFO]      * Directory not found
[INFO] 3.8  - Ensure that registry certificate file permissions are set to 444 or more restrictive
[INFO]      * Directory not found
[INFO] 3.9  - Ensure that TLS CA certificate file ownership is set to root:root
[INFO]      * No TLS CA certificate found
[INFO] 3.10  - Ensure that TLS CA certificate file permissions are set to 444 or more restrictive
[INFO]      * No TLS CA certificate found
[INFO] 3.11  - Ensure that Docker server certificate file ownership is set to root:root
[INFO]      * No TLS Server certificate found
[INFO] 3.12  - Ensure that Docker server certificate file permissions are set to 444 or more restrictive
[INFO]      * No TLS Server certificate found
[INFO] 3.13  - Ensure that Docker server certificate key file ownership is set to root:root
[INFO]      * No TLS Key found
[INFO] 3.14  - Ensure that Docker server certificate key file permissions are set to 400
[INFO]      * No TLS Key found
[WARN] 3.15  - Ensure that Docker socket file ownership is set to root:docker
[WARN]      * Wrong ownership for /var/run/docker.sock
[PASS] 3.16  - Ensure that Docker socket file permissions are set to 660 or more restrictive
[INFO] 3.17  - Ensure that daemon.json file ownership is set to root:root
[INFO]      * File not found
[INFO] 3.18  - Ensure that daemon.json file permissions are set to 644 or more restrictive
[INFO]      * File not found
[INFO] 3.19  - Ensure that /etc/default/docker file ownership is set to root:root
[INFO]      * File not found
[INFO] 3.20  - Ensure that /etc/default/docker file permissions are set to 644 or more restrictive
[INFO]      * File not found


[INFO] 4 - Container Images and Build File
[WARN] 4.1  - Ensure a user for the container has been created
[WARN]      * Running as root: before-db-1
[NOTE] 4.2  - Ensure that containers use trusted base images
[NOTE] 4.3  - Ensure unnecessary packages are not installed in the container
[NOTE] 4.4  - Ensure images are scanned and rebuilt to include security patches
[WARN] 4.5  - Ensure Content trust for Docker is Enabled
[WARN] 4.6  - Ensure HEALTHCHECK instructions have been added to the container image
[WARN]      * No Healthcheck found: [mywebapp:latest]
[WARN]      * No Healthcheck found: [postgres:13]
[INFO] 4.7  - Ensure update instructions are not use alone in the Dockerfile
[INFO]      * Update instruction found: [postgres:13]
[NOTE] 4.8  - Ensure setuid and setgid permissions are removed in the images
[INFO] 4.9  - Ensure COPY is used instead of ADD in Dockerfile
[INFO]      * ADD in image history: [mywebapp:latest]
[INFO]      * ADD in image history: [docker/docker-bench-security:latest]
[NOTE] 4.10  - Ensure secrets are not stored in Dockerfiles
[NOTE] 4.11  - Ensure verified packages are only Installed


[INFO] 5 - Container Runtime
[WARN] 5.1  - Ensure AppArmor Profile is Enabled
[WARN]      * No AppArmorProfile Found: jovial_morse
[WARN]      * No AppArmorProfile Found: before-web-1
[WARN]      * No AppArmorProfile Found: before-db-1
[WARN] 5.2  - Ensure SELinux security options are set, if applicable
[WARN]      * No SecurityOptions Found: jovial_morse
[WARN]      * No SecurityOptions Found: before-web-1
[WARN]      * No SecurityOptions Found: before-db-1
[PASS] 5.3  - Ensure Linux Kernel Capabilities are restricted within containers
[PASS] 5.4  - Ensure privileged containers are not used
[PASS] 5.5  - Ensure sensitive host system directories are not mounted on containers
[PASS] 5.6  - Ensure ssh is not run within containers
[PASS] 5.7  - Ensure privileged ports are not mapped within containers
[NOTE] 5.8  - Ensure only needed ports are open on the container
[PASS] 5.9  - Ensure the host's network namespace is not shared
[WARN] 5.10  - Ensure memory usage for container is limited
[WARN]      * Container running without memory restrictions: jovial_morse
[WARN]      * Container running without memory restrictions: before-web-1
[WARN]      * Container running without memory restrictions: before-db-1
[WARN] 5.11  - Ensure CPU priority is set appropriately on the container
[WARN]      * Container running without CPU restrictions: jovial_morse
[WARN]      * Container running without CPU restrictions: before-web-1
[WARN]      * Container running without CPU restrictions: before-db-1
[WARN] 5.12  - Ensure the container's root filesystem is mounted as read only
[WARN]      * Container running with root FS mounted R/W: jovial_morse
[WARN]      * Container running with root FS mounted R/W: before-web-1
[WARN]      * Container running with root FS mounted R/W: before-db-1
[WARN] 5.13  - Ensure incoming container traffic is binded to a specific host interface
[WARN]      * Port being bound to wildcard IP: 0.0.0.0 in jovial_morse
[WARN]      * Port being bound to wildcard IP: 0.0.0.0 in before-web-1
[WARN] 5.14  - Ensure 'on-failure' container restart policy is set to '5'
[WARN]      * MaximumRetryCount is not set to 5: jovial_morse
[WARN]      * MaximumRetryCount is not set to 5: before-web-1
[WARN]      * MaximumRetryCount is not set to 5: before-db-1
[PASS] 5.15  - Ensure the host's process namespace is not shared
[PASS] 5.16  - Ensure the host's IPC namespace is not shared
[PASS] 5.17  - Ensure host devices are not directly exposed to containers
[INFO] 5.18  - Ensure the default ulimit is overwritten at runtime, only if needed
[INFO]      * Container no default ulimit override: jovial_morse
[INFO]      * Container no default ulimit override: before-web-1
[INFO]      * Container no default ulimit override: before-db-1
[PASS] 5.19  - Ensure mount propagation mode is not set to shared
[PASS] 5.20  - Ensure the host's UTS namespace is not shared
[PASS] 5.21  - Ensure the default seccomp profile is not Disabled
[NOTE] 5.22  - Ensure docker exec commands are not used with privileged option
[NOTE] 5.23  - Ensure docker exec commands are not used with user option
[PASS] 5.24  - Ensure cgroup usage is confirmed
[WARN] 5.25  - Ensure the container is restricted from acquiring additional privileges
[WARN]      * Privileges not restricted: jovial_morse
[WARN]      * Privileges not restricted: before-web-1
[WARN]      * Privileges not restricted: before-db-1
[WARN] 5.26  - Ensure container health is checked at runtime
[WARN]      * Health check not set: jovial_morse
[WARN]      * Health check not set: before-web-1
[WARN]      * Health check not set: before-db-1
[INFO] 5.27  - Ensure docker commands always get the latest version of the image
[WARN] 5.28  - Ensure PIDs cgroup limit is used
[WARN]      * PIDs limit not set: jovial_morse
[WARN]      * PIDs limit not set: before-web-1
[WARN]      * PIDs limit not set: before-db-1
[INFO] 5.29  - Ensure Docker's default bridge docker0 is not used
[INFO]      * Container in docker0 network: jovial_morse
[INFO]      * Container in docker0 network: kind_yalow
[PASS] 5.30  - Ensure the host's user namespaces is not shared
[PASS] 5.31  - Ensure the Docker socket is not mounted inside any containers


[INFO] 6 - Docker Security Operations
[INFO] 6.1  - Avoid image sprawl
[INFO]      * There are currently: 3 images
[INFO] 6.2  - Avoid container sprawl
[INFO]      * There are currently a total of 4 containers, with 4 of them currently running


[INFO] 7 - Docker Swarm Configuration
[PASS] 7.1  - Ensure swarm mode is not Enabled, if not needed
[PASS] 7.2  - Ensure the minimum number of manager nodes have been created in a swarm (Swarm mode not enabled)
[PASS] 7.3  - Ensure swarm services are binded to a specific host interface (Swarm mode not enabled)
[PASS] 7.4  - Ensure data exchanged between containers are encrypted on different nodes on the overlay network
[PASS] 7.5  - Ensure Docker's secret management commands are used for managing secrets in a Swarm cluster (Swarm mode not enabled)
[PASS] 7.6  - Ensure swarm manager is run in auto-lock mode (Swarm mode not enabled)
[PASS] 7.7  - Ensure swarm manager auto-lock key is rotated periodically (Swarm mode not enabled)
[PASS] 7.8  - Ensure node certificates are rotated as appropriate (Swarm mode not enabled)
[PASS] 7.9  - Ensure CA certificates are rotated as appropriate (Swarm mode not enabled)
[PASS] 7.10  - Ensure management plane traffic has been separated from data plane traffic (Swarm mode not enabled)

[INFO] Checks: 105
[INFO] Score: 9
PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin\week-7\homework7\before> make dbuild
"Running code analysis with Bandit..."
docker run --rm -v :/app python:3.9-alpine sh -c "pip install bandit && bandit -r /app"
docker: invalid spec: :/app: empty section between colons

Run 'docker run --help' for more information
make: *** [Makefile:4: check] Error 125
PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin\week-7\homework7\before>

---

# after

PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin\week-7\homework7\after> make start
docker compose up -d
[+] Running 11/11
 ✔ db Pulled                                                                                                                                                                                         7.2s 
   ✔ 752117175404 Pull complete                                                                                                                                                                      0.2s 
   ✔ dca80ca41ba4 Pull complete                                                                                                                                                                      6.4s 
   ✔ e87a4ab71e3e Pull complete                                                                                                                                                                      0.2s 
   ✔ 1d318b8003f7 Pull complete                                                                                                                                                                      0.2s 
   ✔ 2cae8a172409 Pull complete                                                                                                                                                                      0.2s 
   ✔ e8ea8730f798 Pull complete                                                                                                                                                                      0.3s 
   ✔ adbaf2d32053 Pull complete                                                                                                                                                                      0.2s 
   ✔ 8ff80b4b5201 Pull complete                                                                                                                                                                      6.3s
   ✔ a8b21e5461c2 Pull complete                                                                                                                                                                      0.2s
   ✔ 17d9bf165746 Pull complete                                                                                                                                                                      0.2s
[+] Running 4/5
 ✔ Network after_frontend        Created                                                                                                                                                             0.0s 
 ✔ Volume "after_postgres_data"  Created                                                                                                                                                             0.0s 
 ✔ Container after-db-1          Started                                                                                                                                                             0.8s 
 - Container after-web-1         Starting                                                                                                                                                            0.7s 
Error response from daemon: failed to set up container networking: driver failed programming external connectivity on endpoint after-web-1 (9acf458da49af8abbcb8eae48e1068a0024c80d0bb40fe7350cc30d4a7a9a501): failed to bind host port for 127.0.0.1:15000:172.21.0.2:5000/tcp: address already in use
make: *** [Makefile:30: start] Error 1
PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin\week-7\homework7\after> make start
docker compose up -d
[+] Running 2/2
 ✔ Container after-db-1   Running                                                                                                                                                                    0.0s 
 ✔ Container after-web-1  Started                                                                                                                                                                    0.2s 
PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin\week-7\homework7\after> make run
docker run -p 6000:5000 mywebapp
docker: Error response from daemon: failed to set up container networking: driver failed programming external connectivity on endpoint boring_albattani (87ded483fd75d77dad0a3f5651929a33537a226a97affb4f43b0ee993a9b431c): Bind for 0.0.0.0:6000 failed: port is already allocated

Run 'docker run --help' for more information
make: *** [Makefile:19: run] Error 125
PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin\week-7\homework7\after> make check
"Running code analysis with Bandit..."
docker run --rm -v :/app python:3.9-alpine sh -c "pip install bandit && bandit -r /app"
docker: invalid spec: :/app: empty section between colons

Run 'docker run --help' for more information
make: *** [Makefile:4: check] Error 125
PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin\week-7\homework7\after> make host-seurity
make: *** No rule to make target 'host-seurity'.  Stop.
PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin\week-7\homework7\after> make host-security
"Running Docker Bench for Security..."
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker/docker-bench-security
# ------------------------------------------------------------------------------
# Docker Bench for Security v1.3.4
#
# Docker, Inc. (c) 2015-
#
# Checks for dozens of common best-practices around deploying Docker containers in production.
# Inspired by the CIS Docker Community Edition Benchmark v1.1.0.
# ------------------------------------------------------------------------------

Initializing Mon May 19 19:17:33 UTC 2025


[INFO] 1 - Host Configuration
[WARN] 1.1  - Ensure a separate partition for containers has been created
[NOTE] 1.2  - Ensure the container host has been Hardened
[PASS] 1.3  - Ensure Docker is up to date
[INFO]      * Using 28.1.1 which is current
[INFO]      * Check with your operating system vendor for support and security maintenance for Docker
[INFO] 1.4  - Ensure only trusted users are allowed to control Docker daemon
[INFO]      * docker:x:101
[WARN] 1.5  - Ensure auditing is configured for the Docker daemon
[INFO] 1.6  - Ensure auditing is configured for Docker files and directories - /var/lib/docker
[INFO]      * Directory not found
[INFO] 1.7  - Ensure auditing is configured for Docker files and directories - /etc/docker
[INFO]      * Directory not found
[INFO] 1.8  - Ensure auditing is configured for Docker files and directories - docker.service
[INFO]      * File not found
[INFO] 1.9  - Ensure auditing is configured for Docker files and directories - docker.socket
[INFO]      * File not found
[INFO] 1.10  - Ensure auditing is configured for Docker files and directories - /etc/default/docker
[INFO]      * File not found
[INFO] 1.11  - Ensure auditing is configured for Docker files and directories - /etc/docker/daemon.json
[INFO]      * File not found
[INFO] 1.12  - Ensure auditing is configured for Docker files and directories - /usr/bin/docker-containerd
[INFO]      * File not found
[INFO] 1.13  - Ensure auditing is configured for Docker files and directories - /usr/bin/docker-runc
[INFO]      * File not found


[INFO] 2 - Docker daemon configuration
[WARN] 2.1  - Ensure network traffic is restricted between containers on the default bridge
[PASS] 2.2  - Ensure the logging level is set to 'info'
[PASS] 2.3  - Ensure Docker is allowed to make changes to iptables
[PASS] 2.4  - Ensure insecure registries are not used
[PASS] 2.5  - Ensure aufs storage driver is not used
[INFO] 2.6  - Ensure TLS authentication for Docker daemon is configured
[INFO]      * Docker daemon not listening on TCP
[INFO] 2.7  - Ensure the default ulimit is configured appropriately
[INFO]      * Default ulimit doesn't appear to be set
[WARN] 2.8  - Enable user namespace support
[PASS] 2.9  - Ensure the default cgroup usage has been confirmed
[PASS] 2.10  - Ensure base device size is not changed until needed
[WARN] 2.11  - Ensure that authorization for Docker client commands is enabled
[WARN] 2.12  - Ensure centralized and remote logging is configured
[INFO] 2.13  - Ensure operations on legacy registry (v1) are Disabled (Deprecated)
[WARN] 2.14  - Ensure live restore is Enabled
[WARN] 2.15  - Ensure Userland Proxy is Disabled
[INFO] 2.16  - Ensure daemon-wide custom seccomp profile is applied, if needed
[PASS] 2.17  - Ensure experimental features are avoided in production
[WARN] 2.18  - Ensure containers are restricted from acquiring new privileges


[INFO] 3 - Docker daemon configuration files
[INFO] 3.1  - Ensure that docker.service file ownership is set to root:root
[INFO]      * File not found
[INFO] 3.2  - Ensure that docker.service file permissions are set to 644 or more restrictive
[INFO]      * File not found
[INFO] 3.3  - Ensure that docker.socket file ownership is set to root:root
[INFO]      * File not found
[INFO] 3.4  - Ensure that docker.socket file permissions are set to 644 or more restrictive
[INFO]      * File not found
[INFO] 3.5  - Ensure that /etc/docker directory ownership is set to root:root
[INFO]      * Directory not found
[INFO] 3.6  - Ensure that /etc/docker directory permissions are set to 755 or more restrictive
[INFO]      * Directory not found
[INFO] 3.7  - Ensure that registry certificate file ownership is set to root:root
[INFO]      * Directory not found
[INFO] 3.8  - Ensure that registry certificate file permissions are set to 444 or more restrictive
[INFO]      * Directory not found
[INFO] 3.9  - Ensure that TLS CA certificate file ownership is set to root:root
[INFO]      * No TLS CA certificate found
[INFO] 3.10  - Ensure that TLS CA certificate file permissions are set to 444 or more restrictive
[INFO]      * No TLS CA certificate found
[INFO] 3.11  - Ensure that Docker server certificate file ownership is set to root:root
[INFO]      * No TLS Server certificate found
[INFO] 3.12  - Ensure that Docker server certificate file permissions are set to 444 or more restrictive
[INFO]      * No TLS Server certificate found
[INFO] 3.13  - Ensure that Docker server certificate key file ownership is set to root:root
[INFO]      * No TLS Key found
[INFO] 3.14  - Ensure that Docker server certificate key file permissions are set to 400
[INFO]      * No TLS Key found
[WARN] 3.15  - Ensure that Docker socket file ownership is set to root:docker
[WARN]      * Wrong ownership for /var/run/docker.sock
[PASS] 3.16  - Ensure that Docker socket file permissions are set to 660 or more restrictive
[INFO] 3.17  - Ensure that daemon.json file ownership is set to root:root
[INFO]      * File not found
[INFO] 3.18  - Ensure that daemon.json file permissions are set to 644 or more restrictive
[INFO]      * File not found
[INFO] 3.19  - Ensure that /etc/default/docker file ownership is set to root:root
[INFO]      * File not found
[INFO] 3.20  - Ensure that /etc/default/docker file permissions are set to 644 or more restrictive
[INFO]      * File not found


[INFO] 4 - Container Images and Build File
[WARN] 4.1  - Ensure a user for the container has been created
[WARN]      * Running as root: after-db-1
[NOTE] 4.2  - Ensure that containers use trusted base images
[NOTE] 4.3  - Ensure unnecessary packages are not installed in the container
[NOTE] 4.4  - Ensure images are scanned and rebuilt to include security patches
[WARN] 4.5  - Ensure Content trust for Docker is Enabled
[WARN] 4.6  - Ensure HEALTHCHECK instructions have been added to the container image
[WARN]      * No Healthcheck found: [mywebapp:latest]
[WARN]      * No Healthcheck found: [postgres:13-alpine]
[WARN]      * No Healthcheck found: [postgres:13]
[INFO] 4.7  - Ensure update instructions are not use alone in the Dockerfile
[INFO]      * Update instruction found: [postgres:13]
[NOTE] 4.8  - Ensure setuid and setgid permissions are removed in the images
[INFO] 4.9  - Ensure COPY is used instead of ADD in Dockerfile
[INFO]      * ADD in image history: [mywebapp:latest]
[INFO]      * ADD in image history: [postgres:13-alpine]
[INFO]      * ADD in image history: [docker/docker-bench-security:latest]
[NOTE] 4.10  - Ensure secrets are not stored in Dockerfiles
[NOTE] 4.11  - Ensure verified packages are only Installed


[INFO] 5 - Container Runtime
[WARN] 5.1  - Ensure AppArmor Profile is Enabled
[WARN]      * No AppArmorProfile Found: after-web-1
[WARN]      * No AppArmorProfile Found: after-db-1
[WARN]      * No AppArmorProfile Found: jovial_morse
[WARN] 5.2  - Ensure SELinux security options are set, if applicable
[WARN]      * No SecurityOptions Found: after-db-1
[WARN]      * No SecurityOptions Found: jovial_morse
[PASS] 5.3  - Ensure Linux Kernel Capabilities are restricted within containers
[PASS] 5.4  - Ensure privileged containers are not used
[PASS] 5.5  - Ensure sensitive host system directories are not mounted on containers
[PASS] 5.6  - Ensure ssh is not run within containers
[PASS] 5.7  - Ensure privileged ports are not mapped within containers
[NOTE] 5.8  - Ensure only needed ports are open on the container
[PASS] 5.9  - Ensure the host's network namespace is not shared
[WARN] 5.10  - Ensure memory usage for container is limited
[WARN]      * Container running without memory restrictions: after-web-1
[WARN]      * Container running without memory restrictions: after-db-1
[WARN]      * Container running without memory restrictions: jovial_morse
[WARN] 5.11  - Ensure CPU priority is set appropriately on the container
[WARN]      * Container running without CPU restrictions: after-web-1
[WARN]      * Container running without CPU restrictions: after-db-1
[WARN]      * Container running without CPU restrictions: jovial_morse
[WARN] 5.12  - Ensure the container's root filesystem is mounted as read only
[WARN]      * Container running with root FS mounted R/W: after-db-1
[WARN]      * Container running with root FS mounted R/W: jovial_morse
[WARN] 5.13  - Ensure incoming container traffic is binded to a specific host interface
[WARN]      * Port being bound to wildcard IP: 0.0.0.0 in jovial_morse
[WARN] 5.14  - Ensure 'on-failure' container restart policy is set to '5'
[WARN]      * MaximumRetryCount is not set to 5: after-web-1
[WARN]      * MaximumRetryCount is not set to 5: after-db-1
[WARN]      * MaximumRetryCount is not set to 5: jovial_morse
[PASS] 5.15  - Ensure the host's process namespace is not shared
[PASS] 5.16  - Ensure the host's IPC namespace is not shared
[PASS] 5.17  - Ensure host devices are not directly exposed to containers
[INFO] 5.18  - Ensure the default ulimit is overwritten at runtime, only if needed
[INFO]      * Container no default ulimit override: after-web-1
[INFO]      * Container no default ulimit override: after-db-1
[INFO]      * Container no default ulimit override: jovial_morse
[PASS] 5.19  - Ensure mount propagation mode is not set to shared
[PASS] 5.20  - Ensure the host's UTS namespace is not shared
[PASS] 5.21  - Ensure the default seccomp profile is not Disabled
[NOTE] 5.22  - Ensure docker exec commands are not used with privileged option
[NOTE] 5.23  - Ensure docker exec commands are not used with user option
[PASS] 5.24  - Ensure cgroup usage is confirmed
[WARN] 5.25  - Ensure the container is restricted from acquiring additional privileges
[WARN]      * Privileges not restricted: after-db-1
[WARN]      * Privileges not restricted: jovial_morse
[WARN] 5.26  - Ensure container health is checked at runtime
[WARN]      * Health check not set: after-web-1
[WARN]      * Health check not set: after-db-1
[WARN]      * Health check not set: jovial_morse
[INFO] 5.27  - Ensure docker commands always get the latest version of the image
[WARN] 5.28  - Ensure PIDs cgroup limit is used
[WARN]      * PIDs limit not set: after-web-1
[WARN]      * PIDs limit not set: after-db-1
[WARN]      * PIDs limit not set: jovial_morse
[INFO] 5.29  - Ensure Docker's default bridge docker0 is not used
[INFO]      * Container in docker0 network: jovial_morse
[INFO]      * Container in docker0 network: lucid_goldberg
[PASS] 5.30  - Ensure the host's user namespaces is not shared
[PASS] 5.31  - Ensure the Docker socket is not mounted inside any containers


[INFO] 6 - Docker Security Operations
[INFO] 6.1  - Avoid image sprawl
[INFO]      * There are currently: 4 images
[INFO] 6.2  - Avoid container sprawl
[INFO]      * There are currently a total of 5 containers, with 4 of them currently running


[INFO] 7 - Docker Swarm Configuration
[PASS] 7.1  - Ensure swarm mode is not Enabled, if not needed
[PASS] 7.2  - Ensure the minimum number of manager nodes have been created in a swarm (Swarm mode not enabled)
[PASS] 7.3  - Ensure swarm services are binded to a specific host interface (Swarm mode not enabled)
[PASS] 7.4  - Ensure data exchanged between containers are encrypted on different nodes on the overlay network
[PASS] 7.5  - Ensure Docker's secret management commands are used for managing secrets in a Swarm cluster (Swarm mode not enabled)
[PASS] 7.6  - Ensure swarm manager is run in auto-lock mode (Swarm mode not enabled)
[PASS] 7.7  - Ensure swarm manager auto-lock key is rotated periodically (Swarm mode not enabled)
[PASS] 7.8  - Ensure node certificates are rotated as appropriate (Swarm mode not enabled)
[PASS] 7.9  - Ensure CA certificates are rotated as appropriate (Swarm mode not enabled)
[PASS] 7.10  - Ensure management plane traffic has been separated from data plane traffic (Swarm mode not enabled)

[INFO] Checks: 105
[INFO] Score: 9
PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin\week-7\homework7\after> make scan
docker scout recommendations mywebapp:latest
    i New version 1.18.0 available (installed version is 1.17.1) at https://github.com/docker/scout-cli
    v SBOM of image already cached, 65 packages indexed

    i Base image was auto-detected. To get more accurate recommendations, build images with max-mode provenance attestations.
      Review docs.docker.com ↗ for more information.
      Alternatively, use  docker scout recommendations --tag <base image tag>  to pass a specific base image tag.

  Target   │  mywebapp:latest 
    digest │  cc36a7cc1017 

## Recommended fixes

  Base image is  python:3.11-alpine 

  Name            │  3.11-alpine 
  Digest          │  sha256:81d42a73add8e508771ee8e923f9f8392ec1c3d1e482d7d594891d06e78fb51c 
  Vulnerabilities │    0C     1H     0M     0L 
  Pushed          │ 1 week ago
  Size            │ 20 MB
  Packages        │ 58
  Flavor          │ alpine
  OS              │ 3.21
  Runtime         │ 3.11.12


  │ The base image is also available under the supported tag(s)  
  3.11-
  │ alpine3.21 ,  3.11.12-alpine ,  3.11.12-alpine3.21 . If you want
  to
  │ display recommendations specifically for a different tag, please
  │ re-run the command using the  --tag  flag.



Refresh base image
  Rebuild the image using a newer base image version. Updating this may result in breaking changes.

  v This image version is up to date.


Change base image
  The list displays new recommended tags in descending order, where the top results are rated as most suitable.


              Tag              │                        Details                        │   Pushed   │       Vulnerabilities
───────────────────────────────┼───────────────────────────────────────────────────────┼────────────┼──────────────────────────────
   3.13-alpine                 │ Benefits:                                             │ 1 week ago │    0C     0H     0M     0L
  Tag is preferred tag         │ • Same OS detected                                    │            │           -1
  Also known as:               │ • Minor runtime version update                        │            │
  • alpine                     │ • Image is smaller by 3.5 MB                          │            │
  • alpine3.21                 │ • Image contains 15 fewer packages                    │            │
  • 3.13.3-alpine              │ • Tag is preferred tag                                │            │
  • 3.13.3-alpine3.21          │ • Image introduces no new vulnerability but removes 1 │            │
  • 3.13-alpine3.21            │                                                       │            │
  • 3-alpine                   │ Image details:                                        │            │
  • 3-alpine3.21               │ • Size: 17 MB                                         │            │
                               │ • Flavor: alpine                                      │            │
                               │ • OS: 3.21                                            │            │
                               │ • Runtime: 3.13.3                                     │            │
                               │                                                       │            │
                               │                                                       │            │
                               │                                                       │            │
   3.12-alpine                 │ Benefits:                                             │ 1 week ago │    0C     0H     0M     0L
  Minor runtime version update │ • Same OS detected                                    │            │           -1
  Also known as:               │ • Minor runtime version update                        │            │
  • 3.12.10-alpine             │ • Image is smaller by 2.4 MB                          │            │
  • 3.12.10-alpine3.21         │ • Image contains 2 fewer packages                     │            │
  • 3.12-alpine3.21            │ • Image introduces no new vulnerability but removes 1 │            │
                               │                                                       │            │
                               │ Image details:                                        │            │
                               │ • Size: 18 MB                                         │            │
                               │ • Flavor: alpine                                      │            │
                               │ • OS: 3.21                                            │            │
                               │ • Runtime: 3.12.10                                    │            │
                               │                                                       │            │
                               │                                                       │            │
                               │                                                       │            │
