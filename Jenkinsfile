pipeline {
    agent any

    environment {
        DOCKER_ID = "ameliendevops"
        DOCKER_IMAGE_CAST = "cast-service"
        DOCKER_IMAGE_MOVIE = "movie-service"
        DOCKER_TAG = "v.${BUILD_ID}.0"
        KUBE_NAMESPACE_DEV = "dev" 
        KUBE_NAMESPACE_QA = "qa"  # Quality Assurance
        KUBE_NAMESPACE_STAGING = "staging"
        KUBE_NAMESPACE_PROD = "prod"
        KUBECONFIG = credentials("kubeconfig") 
    }

    stages {
        stage('Build Docker Images') { // Construire les images Docker pour les services de l'application.
            steps {
                script {
                    // Construire les images en utilisant docker-compose
                    sh '''
                    docker-compose -f docker-compose.yml build
                    '''
                }
            }
        }

        stage('Docker run') { // Exécuter les conteneurs Docker pour des tests rapides et locaux.
            steps {
                script {
                    // Démarrer les conteneurs nécessaires pour les tests d'acceptation
                    sh '''
                    docker-compose -f docker-compose.yml up -d
                    sleep 10
                    '''
                }
            }
        }
        stage('Test Acceptance') { #Vérifier que les conteneurs répondent correctement.
            steps {
                script {
                    sh '''
                    curl localhost
                    '''
                }
            }
        }

        stage('Deploy Dev') {
            steps {
                script {
                    sh '''
                    kubectl apply -f cast-service/kubernetes/deployment.yaml --namespace=${KUBE_NAMESPACE_DEV}
                    kubectl apply -f movie-service/kubernetes/deployment.yaml --namespace=${KUBE_NAMESPACE_DEV}
                    '''
                }
            }
        }

        stage('Deploy QA') {
            steps {
                script {
                    sh '''
                    kubectl apply -f cast-service/kubernetes/deployment.yaml --namespace=${KUBE_NAMESPACE_QA}
                    kubectl apply -f movie-service/kubernetes/deployment.yaml --namespace=${KUBE_NAMESPACE_QA}
                    '''
                }
            }
        }

        stage('Deploy Staging') {
            steps {
                script {
                    sh '''
                    kubectl apply -f cast-service/kubernetes/deployment.yaml --namespace=${KUBE_NAMESPACE_STAGING}
                    kubectl apply -f movie-service/kubernetes/deployment.yaml --namespace=${KUBE_NAMESPACE_STAGING}
                    '''
                }
            }
        }

        stage('Deploy Prod') {  #deploy prod avec "input" pour demander une action manuelle pour une livraison continue 
            steps {
                timeout(time: 15, unit: "MINUTES") {
                    input message: 'Do you want to deploy in production?', ok: 'Yes'
                }
                script {
                    sh '''
                    kubectl apply -f cast-service/kubernetes/deployment.yaml --namespace=${KUBE_NAMESPACE_PROD}
                    kubectl apply -f movie-service/kubernetes/deployment.yaml --namespace=${KUBE_NAMESPACE_PROD}
                    '''
                }
            }
        }
    }
}
