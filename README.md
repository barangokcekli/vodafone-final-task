
# DevOps Workflow Implementation


## Table of Contents
- [Setup and Version Control](#setup-and-version-control)
- [Dockerization](#dockerization)
- [Kubernetes Deployment](#kubernetes-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring](#monitoring)
- [Conclusion](#conclusion)

## Setup and Version Control

### Create a Simple Web Application
A basic Flask app is created with the following content in `app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, DevOps!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Initializing Git Repository and Committing
```bash
mkdir devops-challenge
cd devops-challenge
git init
git add app.py
git commit -m "initial"
```

### Create a Remote Repository and Push

```bash
git remote add origin https://github.com/barangokcekli/vodafone-final-task.git
git branch -M main
git push -u origin main
```

## Dockerization


I've created a `Dockerfile` in my project directory with the following content:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

Create a `requirements.txt` file:
```
Flask==2.0.2
```

### Building and Running Docker Container 
```bash
docker build -t flask-app .
docker run -d -p 5000:5000 flask-app
```


## Kubernetes Deployment
I've setted up a local Kubernetes cluster using Minikube
,
```bash
minikube start
```


Then I've created `deployment.yaml` and `service.yaml` files.

**deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
      - name: flask-app
        image: flask-app:latest
        ports:
        - containerPort: 5000
```

**service.yaml**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-app-service
spec:
  type: NodePort
  selector:
    app: flask-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
    nodePort: 30007
```

To deploy the Kubernetes:
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```


## CI/CD Pipeline


### Jenkins Pipeline Script (Jenkinsfile)
```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    dockerImage = docker.build("flask-app")
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    dockerImage.inside {
                        sh 'echo "Run tests here"'
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    kubectl.apply("--filename deployment.yaml")
                    kubectl.apply("--filename service.yaml")
                }
            }
        }
    }
}
```


## Monitoring

I've setted up Prometheus in my cluster using helm:

Deploy Prometheus in your Kubernetes cluster using Helm:
```bash
helm install prometheus stable/prometheus
```

Then modified my Flask app to expose metrics using `prometheus_client`.

**app.py**
```python
from flask import Flask
from prometheus_client import Counter, generate_latest

app = Flask(__name__)
c = Counter('requests', 'Number of requests served', ['endpoint'])

@app.route('/')
def home() {
    c.labels('/').inc()
    return "Hello, DevOps!"
}

@app.route('/metrics')
def metrics():
    return generate_latest(), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

I've setted up Grafana using Helm:
```bash
helm install grafana stable/grafana
```
Then I accessed it by Grafana via `minikube service grafana --url` and configure it to use Prometheus as a data source.

### Define Basic Monitoring Thresholds and Alerts in Prometheus


**alert.rules**
```yaml
groups:
  - name: example
    rules:
    - alert: HighRequestLatency
      expr: http_request_duration_seconds{quantile="0.95"} > 0.5
      for: 1m
      labels:
        severity: page
      annotations:
        summary: High request latency
```

