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
                    '''
                }
            }
        }

        stage('Lint - Cast Service') {
            steps {
                script {
                    sh '''
                    pip3 install flake8
                    flake8 cast-service/app --exit-zero --max-line-length=88
                    '''
                }
            }
        }

        stage('Lint - Movie Service') {
            steps {
                script {
                    sh '''
                    pip3 install flake8
                    flake8 movie-service/app --exit-zero --max-line-length=88
                    '''
                }
            }
        }

        stage('Docker Build - Cast Service') {
            steps {
                script {
                    sh '''
                    docker rm -f cast-service || true
                    docker build -t $DOCKER_ID/cast-service:$DOCKER_TAG -f cast-service/Dockerfile cast-service
                    '''
                }
            }
        }

        stage('Docker Build - Movie Service') {
            steps {
                script {
                    sh '''
                    docker rm -f movie-service || true
                    docker build -t $DOCKER_ID/movie-service:$DOCKER_TAG -f movie-service/Dockerfile movie-service
                    '''
                }
            }
        }

        stage('Docker Run and Test - Cast Service') {
            steps {
                script {
                    sh '''
                    docker run -d -p 8002:8000 --name cast-service $DOCKER_ID/cast-service:$DOCKER_TAG
                    sleep 5
                    curl -f http://localhost:8002/api/casts || exit 1
                    '''
                }
            }
        }

        stage('Docker Run and Test - Movie Service') {
            steps {
                script {
                    sh '''
                    docker run -d -p 8001:8000 --name movie-service $DOCKER_ID/movie-service:$DOCKER_TAG
                    sleep 5
                    curl -f http://localhost:8001/api/movies || exit 1
                    '''
                }
            }
        }

        stage('Docker Push') {
            steps {
                script {
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
                    sh '''
                    kubectl apply -f fastapi/templates/storageclass-dev.yaml --namespace dev
                    kubectl apply -f fastapi/templates/cast-service-claim-dev.yaml --namespace dev
                    kubectl apply -f fastapi/templates/movie-service-claim-dev.yaml --namespace dev
                    helm upgrade --install app fastapi --namespace dev --set image.tag=${DOCKER_TAG}
                    '''
                }
            }
        }

        // Similar blocks for QA, Staging and Production
        // ...

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
