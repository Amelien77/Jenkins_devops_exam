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
            steps {
                script {
                    sh '''
                    sudo mkdir -p /var/lib/jenkins/.kube
                    sudo cp $KUBECONFIG /var/lib/jenkins/.kube/config
                    cp fastapi/values.yaml values-dev.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values-dev.yml
                    helm upgrade --install cast-service fastapi --values=values-dev.yml --namespace dev
                    helm upgrade --install movie-service fastapi --values=values-dev.yml --namespace dev
                    '''
                }
            }
        }

        stage('Deploy to QA') {
            steps {
                script {
                    sh '''
                    sudo mkdir -p /var/lib/jenkins/.kube
                    sudo cp $KUBECONFIG /var/lib/jenkins/.kube/config
                    cp fastapi/values.yaml values-qa.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values-qa.yml
                    helm upgrade --install cast-service fastapi --values=values-qa.yml --namespace qa
                    helm upgrade --install movie-service fastapi --values=values-qa.yml --namespace qa
                    '''
                }
            }
        }

        stage('Deploy to Staging') {
            steps {
                script {
                    sh '''
                    sudo mkdir -p /var/lib/jenkins/.kube
                    sudo cp $KUBECONFIG /var/lib/jenkins/.kube/config
                    cp fastapi/values.yaml values-staging.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values-staging.yml
                    helm upgrade --install cast-service fastapi --values=values-staging.yml --namespace staging
                    helm upgrade --install movie-service fastapi --values=values-staging.yml --namespace staging
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
            when {
                branch 'master'
            }
            steps {
                script {
                    sh '''
                    sudo mkdir -p /var/lib/jenkins/.kube
                    sudo cp $KUBECONFIG /var/lib/jenkins/.kube/config
                    cp fastapi/values.yaml values-prod.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values-prod.yml
                    helm upgrade --install cast-service fastapi --values=values-prod.yml --namespace prod
                    helm upgrade --install movie-service fastapi --values=values-prod.yml --namespace prod
                    '''
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline executed successfully!'
        }
    }
}
