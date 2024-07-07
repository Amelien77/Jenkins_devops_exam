pipeline {
    agent any

    environment {
        DOCKER_ID = "ameliendevops"
        DOCKER_IMAGE_CAST = "cast-service"
        DOCKER_IMAGE_MOVIE = "movie-service"
        DOCKER_TAG = "v.${BUILD_ID}.0"
        KUBE_NAMESPACE_DEV = "dev"
        KUBE_NAMESPACE_QA = "qa"
        KUBE_NAMESPACE_STAGING = "staging"
        KUBE_NAMESPACE_PROD = "prod"
        KUBECONFIG = credentials("kubeconfig")
        DOCKER_PASS = credentials("DOCKER_PASS")
    }

    stages {
        stage('Build Docker Images') {
            steps {
                script {
                    sh 'docker-compose -f docker-compose.yml build'
                }
            }
        }

        stage('Docker Push') {
            steps {
                script {
                    // Login to Docker Hub
                    sh "docker login -u ${DOCKER_ID} -p ${DOCKER_PASS}"

                    // Push Docker images to Docker Hub
                    sh "docker push ${DOCKER_ID}/${DOCKER_IMAGE_CAST}:${DOCKER_TAG}"
                    sh "docker push ${DOCKER_ID}/${DOCKER_IMAGE_MOVIE}:${DOCKER_TAG}"

                    // Logout from Docker Hub
                    sh "docker logout"
                }
            }
        }

        stage('Docker run') {
            steps {
                script {
                    sh 'docker-compose -f docker-compose.yml up -d'
                    sleep 10
                }
            }
        }

        stage('Test Acceptance') {
            steps {
                script {
                    sh 'curl localhost'
                }
            }
        }

        stage('Deploy Dev') {
            steps {
                script {
                    sh '''
                    kubectl apply -f cast-service/helm/templates/cast-service-deployment.yaml --namespace=${KUBE_NAMESPACE_DEV}
                    kubectl apply -f movie-service/helm/templates/movie-service-deployment.yaml --namespace=${KUBE_NAMESPACE_DEV}
                    '''
                }
            }
        }

        stage('Deploy QA') {
            steps {
                script {
                    sh '''
                    kubectl apply -f cast-service/helm/templates/cast-service-deployment.yaml --namespace=${KUBE_NAMESPACE_QA}
                    kubectl apply -f movie-service/helm/templates/movie-service-deployment.yaml --namespace=${KUBE_NAMESPACE_QA}
                    '''
                }
            }
        }

        stage('Deploy Staging') {
            steps {
                script {
                    sh '''
                    kubectl apply -f cast-service/helm/templates/cast-service-deployment.yaml --namespace=${KUBE_NAMESPACE_STAGING}
                    kubectl apply -f movie-service/helm/templates/movie-service-deployment.yaml --namespace=${KUBE_NAMESPACE_STAGING}
                    '''
                }
            }
        }

        stage('Deploy Prod') {
            steps {
                script {
                    timeout(time: 15, unit: "MINUTES") {
                        input message: 'Do you want to deploy in production?', ok: 'Yes'
                    }
                    sh '''
                    kubectl apply -f cast-service/helm/templates/cast-service-deployment.yaml --namespace=${KUBE_NAMESPACE_PROD}
                    kubectl apply -f movie-service/helm/templates/movie-service-deployment.yaml --namespace=${KUBE_NAMESPACE_PROD}
                    '''
                }
            }
        }
    }
}
