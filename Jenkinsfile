pipeline {
    environment {
        DOCKER_ID = "ameliendevops"
        DOCKER_TAG = "v.${BUILD_ID}.0"
        DOCKER_PASS = credentials("DOCKER_HUB_PASS")
        KUBECONFIG = credentials("config")
    }
    agent any
    stages {
        stage('Docker Build') {
            parallel {
                stage('Build Cast Service') {
                    steps {
                        script {
                            sh 'docker build -t $DOCKER_ID/cast-service:$DOCKER_TAG -f cast-service/Dockerfile cast-service'
                        }
                    }
                }
                stage('Build Movie Service') {
                    steps {
                        script {
                            sh 'docker build -t $DOCKER_ID/movie-service:$DOCKER_TAG -f movie-service/Dockerfile movie-service'
                        }
                    }
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

        stage('Create or Update StorageClass') {
            steps {
                script {
                    sh 'kubectl apply -f fastapi/templates/storageclass.yaml'
                }
            }
        }

        stage('Apply PVCs and Deploy') {
            parallel {
                stage('Deploy to Dev') {
                    steps {
                        script {
                            sh '''
                            kubectl apply -f fastapi/templates/cast-service-claim-dev.yaml --namespace dev
                            kubectl apply -f fastapi/templates/movie-service-claim-dev.yaml --namespace dev
                            helm upgrade --install app fastapi --values=fastapi/values.yaml --namespace dev
                            '''
                        }
                    }
                }
                stage('Deploy to QA') {
                    steps {
                        script {
                            sh '''
                            kubectl apply -f fastapi/templates/cast-service-claim-qa.yaml --namespace qa
                            kubectl apply -f fastapi/templates/movie-service-claim-qa.yaml --namespace qa
                            helm upgrade --install app fastapi --values=fastapi/values.yaml --namespace qa
                            '''
                        }
                    }
                }
                stage('Deploy to Staging') {
                    steps {
                        script {
                            sh '''
                            kubectl apply -f fastapi/templates/cast-service-claim-staging.yaml --namespace staging
                            kubectl apply -f fastapi/templates/movie-service-claim-staging.yaml --namespace staging
                            helm upgrade --install app fastapi --values=fastapi/values.yaml --namespace staging
                            '''
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
                            kubectl apply -f fastapi/templates/cast-service-claim-prod.yaml --namespace prod
                            kubectl apply -f fastapi/templates/movie-service-claim-prod.yaml --namespace prod
                            helm upgrade --install app fastapi --values=fastapi/values.yaml --namespace prod
                            '''
                        }
                    }
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
