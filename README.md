\# OpsPulse



OpsPulse is a small containerized service health dashboard built to practice Docker, Docker Compose networking, reverse proxies, automated tests, linting, and CI.



\## Architecture



```mermaid

flowchart LR

&#x20;   Browser\["Browser or PowerShell"]

&#x20;   Nginx\["Nginx container"]

&#x20;   Flask\["Flask + Gunicorn container"]



&#x20;   Browser -->|"localhost:8080"| Nginx

&#x20;   Nginx -->|"Compose DNS: app:5000"| Flask

```



Nginx is the only service exposed to the host. Flask listens on port `5000` inside the Compose network and is not published as a host port. The Flask container runs as the non-root `app` user.



\## Endpoints



| Method | Path | Description |

| --- | --- | --- |

| GET | `/` | Simple service status page |

| GET | `/health` | Returns HTTP 200 when the application responds |

| GET | `/ready` | Returns HTTP 200 when the application is ready |

| GET | `/api/status` | Returns JSON status and application version |



The default version is `0.1.0`. Compose sets `APP\_VERSION` for the application.



\## Run with Docker Compose



Requirements: Docker Desktop with the Linux engine and Docker Compose.



From the project directory, run:



```powershell

docker compose up --build

```



Open \[http://localhost:8080](http://localhost:8080).



To stop the services, press `Ctrl+C` if Compose is running in the foreground. If you started it in the background with `-d`, run:



```powershell

docker compose down

```



Check service state and logs:



```powershell

docker compose ps

docker compose logs app

docker compose logs nginx

```



\## Run locally with Python



Create a virtual environment and install the development dependencies:



```powershell

py -3.12 -m venv .venv

.\\.venv\\Scripts\\python.exe -m pip install -r requirements-dev.txt

```



Start Flask for local development:



```powershell

.\\.venv\\Scripts\\python.exe -m flask --app app run --host 127.0.0.1 --port 5000

```



Open \[http://127.0.0.1:5000](http://127.0.0.1:5000). Stop the local server with `Ctrl+C`.



\## Tests and linting



Run the test suite:



```powershell

.\\.venv\\Scripts\\python.exe -m pytest -q

```



Run Ruff:



```powershell

.\\.venv\\Scripts\\ruff.exe check .

```



\## CI workflow



GitHub Actions runs on pushes and pull requests. It installs the development dependencies, runs Ruff and pytest, builds the Docker image, starts the Compose services, and makes a smoke request to `/health`. The workflow shuts down its Compose services when the job finishes. It does not deploy to a developer's computer or publish an image to GHCR.



\## Troubleshooting



\### Port 8080 is already in use



The Nginx host port is configured in `compose.yaml`:



```yaml

ports:

&#x20; - "8080:80"

```



If port `8080` is occupied, change the left side to another free port, such as `"8081:80"`. Then open `http://localhost:8081`.



\### Nginx shows 502 Bad Gateway



Check whether the app is healthy and inspect both services' logs:



```powershell

docker compose ps

docker compose logs app

docker compose logs nginx

```



Nginx reaches Flask by the Compose service name `app` on port `5000`.



\### Flask is not reachable at localhost:5000



This is expected when using Docker Compose. Flask is only available inside the Compose network. Send requests through Nginx at `http://localhost:8080`.



\### Docker cannot connect to its engine



Open Docker Desktop and wait for the engine to start. Check that Docker is using its Linux engine:



```powershell

docker info --format '{{.OSType}}'

```



The expected output is `linux`.

