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