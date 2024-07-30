pipeline {
    environment {
        DOCKER_ID = "ameliendevops"  // ID Dockerhub
        DOCKER_TAG = "v.${BUILD_ID}.0"  // Tag
        DOCKER_PASS = credentials("DOCKER_HUB_PASS")  // Mot de passe Dockerhub
        KUBECONFIG = credentials("config")  // Configuration Kubernetes
    }
    agent any  // Utiliser n'importe quel agent disponible pour exécuter les étapes
    stages {
        // Étape de construction de l'image Docker pour le service Cast
        stage('Docker Build - Cast Service') {
            steps {
                script {
                    sh '''
                    docker rm -f cast-service || true  // Supprimer le conteneur existant pour éviter les conflits
                    docker build -t $DOCKER_ID/cast-service:$DOCKER_TAG -f cast-service/Dockerfile .  // Construire l'image Docker pour le service Cast
                    '''
                }
            }
        }

        // Étape de construction de l'image Docker pour le service Movie
        stage('Docker Build - Movie Service') {
            steps {
                script {
                    sh '''
                    docker rm -f movie-service || true  // Supprimer le conteneur existant pour éviter les conflits
                    docker build -t $DOCKER_ID/movie-service:$DOCKER_TAG -f movie-service/Dockerfile .  // Construire l'image Docker pour le service Movie
                    '''
                }
            }
        }

        // Étape de lancement du conteneur Cast Service
        stage('Docker Run - Cast Service') {
            steps {
                script {
                    sh '''
                    docker run -d -p 8002:8000 --name cast-service $DOCKER_ID/cast-service:$DOCKER_TAG  // Lancer le conteneur Cast Service
                    '''
                }
            }
        }

        // Étape de lancement du conteneur Movie Service
        stage('Docker Run - Movie Service') {
            steps {
                script {
                    sh '''
                    docker run -d -p 8001:8000 --name movie-service $DOCKER_ID/movie-service:$DOCKER_TAG  // Lancer le conteneur Movie Service
                    '''
                }
            }
        }

        // Étape de test d'acceptation
        stage('Test Acceptance') {
            steps {
                script {
                    sh '''
                    curl -f http://localhost:8001 || exit 1  // Tester la disponibilité du service Movie
                    curl -f http://localhost:8002 || exit 1  // Tester la disponibilité du service Cast
                    '''
                }
            }
        }

        // Étape de push des images dans Docker Hub
        stage('Docker Push') {
            steps {
                script {
                
