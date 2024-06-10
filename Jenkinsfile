pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'myapp'
        DOCKER_REGISTRY = 'mydockerregistry'
        KUBECONFIG_CREDENTIAL_ID = 'your-kubeconfig-credential-id'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/your-repo/your-app.git', branch: 'main'
            }
        }
        stage('Build') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${env.BUILD_ID}")
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    dockerImage.inside {
                        sh 'python -m unittest discover'
                    }
                }
            }
        }
        stage('Code Analysis') {
            steps {
                script {
                    dockerImage.inside {
                        sh 'sonar-scanner'
                    }
                }
            }
        }
        stage('Security Scan') {
            steps {
                script {
                    dockerImage.inside {
                        sh 'trivy image ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${env.BUILD_ID}'
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    withCredentials([file(credentialsId: "${KUBECONFIG_CREDENTIAL_ID}", variable: 'KUBECONFIG')]) {
                        sh 'kubectl apply -f k8s/deployment.yaml'
                        sh 'kubectl apply -f k8s/service.yaml'
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
