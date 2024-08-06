pipeline {
    environment {
        DOCKER_ID = "ameliendevops"
        DOCKER_TAG = "v.${BUILD_ID}.0"
        DOCKER_PASS = credentials("DOCKER_HUB_PASS")
        KUBECONFIG = credentials("config")
    }
    agent any
    stages {
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

        stage('Docker Run - Cast Service') {
            steps {
                script {
                    sh '''
                    docker run -d -p 8002:8000 --name cast-service $DOCKER_ID/cast-service:$DOCKER_TAG
                    '''
                }
            }
        }

        stage('Docker Run - Movie Service') {
            steps {
                script {
                    sh '''
                    docker run -d -p 8001:8000 --name movie-service $DOCKER_ID/movie-service:$DOCKER_TAG
                    '''
                }
            }
        }

        stage('Test Acceptance') {
            steps {
                script {
                    sh '''
                    curl localhost
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
            environment {
                NAMESPACE = 'dev'
            }
            steps {
                script {
                    sh '''
                    sed -i "s+tag:.*+tag: ${DOCKER_TAG}+g" fastapi/values.yaml
                    sed "s/{{ .Namespace }}/dev/g" fastapi/templates/cast-service-claim0-persistentvolumeclaim.yaml | kubectl apply -f -
                    sed "s/{{ .Namespace }}/dev/g" fastapi/templates/movie-service-claim0-persistentvolumeclaim.yaml | kubectl apply -f -
                    helm upgrade --install app fastapi --values=fastapi/values.yaml --namespace dev
                    '''
                }
            }
        }

        stage('Deploy to QA') {
            environment {
                NAMESPACE = 'qa'
            }
            steps {
                script {
                    sh '''
                    sed -i "s+tag:.*+tag: ${DOCKER_TAG}+g" fastapi/values.yaml
                    sed "s/{{ .Namespace }}/qa/g" fastapi/templates/cast-service-claim0-persistentvolumeclaim.yaml | kubectl apply -f -
                    sed "s/{{ .Namespace }}/qa/g" fastapi/templates/movie-service-claim0-persistentvolumeclaim.yaml | kubectl apply -f -
                    helm upgrade --install app fastapi --values=fastapi/values.yaml --namespace qa
                    '''
                }
            }
        }

        stage('Deploy to Staging') {
            environment {
                NAMESPACE = 'staging'
            }
            steps {
                script {
                    sh '''
                    sed -i "s+tag:.*+tag: ${DOCKER_TAG}+g" fastapi/values.yaml
                    sed "s/{{ .Namespace }}/staging/g" fastapi/templates/cast-service-claim0-persistentvolumeclaim.yaml | kubectl apply -f -
                    sed "s/{{ .Namespace }}/staging/g" fastapi/templates/movie-service-claim0-persistentvolumeclaim.yaml | kubectl apply -f -
                    helm upgrade --install app fastapi --values=fastapi/values.yaml --namespace staging
                    '''
                }
            }
        }

        stage('Manual Approval for Production') {
            when {
                branch 'master'
            }
            steps {
                timeout(time: 15, unit: 'MINUTES') {
                    input message: 'Do you want to deploy in production?', ok: 'Deploy'
                }
            }
        }

        stage('Deploy to Production') {
            environment {
                NAMESPACE = 'prod'
            }
            steps {
                script {
                    sh '''
                    sed -i "s+tag:.*+tag: ${DOCKER_TAG}+g" fastapi/values.yaml
                    sed "s/{{ .Namespace }}/prod/g" fastapi/templates/cast-service-claim0-persistentvolumeclaim.yaml | kubectl apply -f -
                    sed "s/{{ .Namespace }}/prod/g" fastapi/templates/movie-service-claim0-persistentvolumeclaim.yaml | kubectl apply -f -
                    helm upgrade --install app fastapi --values=fastapi/values.yaml --namespace prod
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
            echo 'Pipeline execution failed.'
        }
    }
}
