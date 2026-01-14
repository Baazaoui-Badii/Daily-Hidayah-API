# Daily Hidayah API

A simple REST API that serves random Ayahs and Hadiths, built with FastAPI. It includes JSON logging, Prometheus metrics, and is designed for Cloud-Native deployment with Docker and Kubernetes.

## Prerequisites
- Python 3.9+
- Docker
- Minikube / Kubernetes
- Git

## Project Structure
- `app/`: Application code
- `k8s/`: Kubernetes manifests
- `.github/workflows/`: CI/CD pipeline
- `Dockerfile`: Container definition

## 1. Local Development
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Test endpoints:
   - Guidance: `http://localhost:8000/guidance`
   - Metrics: `http://localhost:8000/metrics`
   - Docs: `http://localhost:8000/docs`

4. Run tests:
   ```bash
   pytest
   ```
5. Run generic security scan (SAST):
   ```bash
   bandit -r app/
   ```

## 2. Docker
1. Build the image:
   ```bash
   docker build -t daily-hidayah-api .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 daily-hidayah-api
   ```

## 3. Kubernetes (Minikube)
1. Start Minikube:
   ```bash
   minikube start
   ```
2. Point your terminal to use minikube's docker-daemon (optional, avoids pushing to hub for local test):
   - Windows (PowerShell): `minikube -p minikube docker-env --shell powershell | Invoke-Expression`
   - *Then rebuild image so Minikube sees it.*

3. Apply manifests:
   ```bash
   kubectl apply -f k8s/
   ```
4. Check status:
   ```bash
   kubectl get pods
   kubectl get svc
   ```
5. Access the service:
   If using NodePort:
   ```bash
   minikube service daily-hidayah-service
   ```

## 4. CI/CD & Secrets
The GitHub Actions pipeline builds and tests on every push. To enable Docker push:
1. Go to GitHub Repo settings -> Secrets.
2. Add `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`.
