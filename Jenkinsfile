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
