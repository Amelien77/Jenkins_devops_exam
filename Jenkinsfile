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
                    sh '''
                    flake8 cast-service/app --exit-zero --max-line-length=88
                    '''
                }
            }
        }

        stage('Lint - Movie Service') {
            steps {
                script {
                    sh '''
                    flake8 movie-service/app --exit-zero --max-line-length=88
                    '''
                }
            }
        }

        stage('Docker Compose Build and Run') {
            steps {
                script {
                    sh '''
                    docker-compose -f docker-compose.yml up --build -d
                    '''
                }
            }
        }

        stage('Run Tests - Cast Service') {
            steps {
                script {
                    sh '''
                    sleep 5
                    curl -f http://cast_service:8002/api/v1/casts || exit 1
                    '''
                }
            }
        }

        stage('Run Tests - Movie Service') {
            steps {
                script {
                    sh '''
                    sleep 5
                    curl -f http://movie_service:8001/api/v1/movies || exit 1
                    '''
                }
            }
        }

        stage('Docker Push') {
            steps {
                script {
                    sh '''
                    docker login -u $DOCKER_ID -p $DOCKER_PASS
                    docker-compose -f docker-compose.yml push
                    '''
                }
            }
        }

        stage('Deploy to Development') {
            steps {
                script {
                    sh '''
                    helm upgrade --install app helm --namespace dev --set image.tag=$DOCKER_TAG -f helm/values-dev.yaml
                    '''
                }
            }
        }

        stage('Deploy to QA') {
            steps {
                script {
                    sh '''
                    helm upgrade --install app helm --namespace qa --set image.tag=$DOCKER_TAG -f helm/values-qa.yaml
                    '''
                }
            }
        }

        stage('Deploy to Staging') {
            steps {
                script {
                    sh '''
                    helm upgrade --install app helm --namespace staging --set image.tag=$DOCKER_TAG -f helm/values-staging.yaml
                    '''
                }
            }
        }

        stage('Deploy to Production') {
            steps {
                script {
                    sh '''
                    helm upgrade --install app helm --namespace prod --set image.tag=$DOCKER_TAG -f helm/values-prod.yaml
                    '''
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    sh '''
                    docker-compose -f docker-compose.yml down
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
