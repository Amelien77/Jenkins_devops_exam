pipeline {
    environment {
        DOCKER_ID = "ameliendevops"
        DOCKER_TAG = "v.${BUILD_ID}.0"
        DOCKER_PASS = credentials("DOCKER_HUB_PASS")
        KUBECONFIG = credentials("config")
    }
    agent any
    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    sh '''
                    pip install -r cast-service/requirements.txt
                    pip install -r movie-service/requirements.txt
                    '''
                }
            }
        }

        stage('Lint - Cast Service') {
            steps {
                script {
                    sh 'flake8 cast-service/app --exit-zero --max-line-length=88'
                }
            }
        }

        stage('Lint - Movie Service') {
            steps {
                script {
                    sh 'flake8 movie-service/app --exit-zero --max-line-length=88'
                }
            }
        }

        stage('Docker Compose Build') {
            steps {
                script {
                    // Utilisation de docker-compose pour construire les images
                    sh '''
                    docker-compose down || true
                    docker-compose build
                    '''
                }
            }
        }

        stage('Docker Compose Up and Test') {
            steps {
                script {
                    // Lancer les conteneurs et tester les services
                    sh '''
                    docker-compose up -d
                    sleep 10  # Attendre que les services démarrent
                    curl -f http://localhost:8001/api/v1/movies || exit 1
                    curl -f http://localhost:8002/api/v1/casts || exit 1
                    '''
                }
            }
        }

        stage('Docker Push') {
            steps {
                script {
                    // Pousser les images vers Docker Hub
                    sh '''
                    docker login -u $DOCKER_ID -p $DOCKER_PASS
                    docker push $DOCKER_ID/cast-service:$DOCKER_TAG
                    docker push $DOCKER_ID/movie-service:$DOCKER_TAG
                    '''
                }
            }
        }

        stage('Deploy to Development') {
            steps {
                script {
                    // Déployer sur Kubernetes en environnement dev via Helm
                    sh '''
                    helm upgrade --install app helm --namespace dev --set image.tag=$DOCKER_TAG -f helm/values-dev.yaml
                    '''
                }
            }
        }

        stage('Deploy to QA') {
            steps {
                script {
                    // Déployer sur Kubernetes en environnement QA via Helm
                    sh '''
                    helm upgrade --install app helm --namespace qa --set image.tag=$DOCKER_TAG -f helm/values-qa.yaml
                    '''
                }
            }
        }

        stage('Deploy to Staging') {
            steps {
                script {
                    // Déployer sur Kubernetes en environnement staging via Helm
                    sh '''
                    helm upgrade --install app helm --namespace staging --set image.tag=$DOCKER_TAG -f helm/values-staging.yaml
                    '''
                }
            }
        }

        stage('Deploy to Production') {
            steps {
                script {
                    // Déployer sur Kubernetes en environnement prod via Helm
                    sh '''
                    helm upgrade --install app helm --namespace prod --set image.tag=$DOCKER_TAG -f helm/values-prod.yaml
                    '''
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
