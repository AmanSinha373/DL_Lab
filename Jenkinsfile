pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'my-dl-lab-exam'
        DOCKER_TAG = 'latest'
    }

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build(":")
                }
            }
        }

        stage('Test Docker Image') {
            steps {
                script {
                    dockerImage.inside {
                        sh 'python dl_final_lab_exam_(aman_kumar_sinha).py'
                    }
                }
            }
        }

        stage('Push Docker Image to Registry') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
                        dockerImage.push("")
                    }
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    dockerImage.remove()
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
        }
    }
}
