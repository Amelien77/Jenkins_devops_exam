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
                    docker rm -f cast-service || true  # Supprimer le conteneur existant pour éviter les conflits
                    docker build -t $DOCKER_ID/cast-service:$DOCKER_TAG -f cast-service/Dockerfile .  # Construire l'image Docker pour le service Cast
                    '''
                }
            }
        }

        // Étape de construction de l'image Docker pour le service Movie
        stage('Docker Build - Movie Service') {
            steps {
                script {
                    sh '''
                    docker rm -f movie-service || true  # Supprimer le conteneur existant pour éviter les conflits
                    docker build -t $DOCKER_ID/movie-service:$DOCKER_TAG -f movie-service/Dockerfile .  # Construire l'image Docker pour le service Movie
                    '''
                }
            }
        }

        // Étape de lancement du conteneur Cast Service
        stage('Docker Run - Cast Service') {
            steps {
                script {
                    sh '''
                    docker run -d -p 8002:8000 --name cast-service $DOCKER_ID/cast-service:$DOCKER_TAG  # Lancer le conteneur Cast Service
                    '''
                }
            }
        }

        // Étape de lancement du conteneur Movie Service
        stage('Docker Run - Movie Service') {
            steps {
                script {
                    sh '''
                    docker run -d -p 8001:8000 --name movie-service $DOCKER_ID/movie-service:$DOCKER_TAG  # Lancer le conteneur Movie Service
                    '''
                }
            }
        }

        // Étape de test d'acceptation
        stage('Test Acceptance') {
            steps {
                script {
                    sh '''
                    curl -f http://localhost:8001 || exit 1  # Tester la disponibilité du service Movie
                    curl -f http://localhost:8002 || exit 1  # Tester la disponibilité du service Cast
                    '''
                }
            }
        }

        // Étape de push des images dans Docker Hub
        stage('Docker Push') {
            steps {
                script {
                    sh '''
                    docker login -u $DOCKER_ID -p $DOCKER_PASS  # Connexion à Docker Hub
                    docker push $DOCKER_ID/cast-service:$DOCKER_TAG  # Pousser l'image Cast Service vers Docker Hub
                    docker push $DOCKER_ID/movie-service:$DOCKER_TAG  # Pousser l'image Movie Service vers Docker Hub
                    '''
                }
            }
        }

        // Étape de déploiement dans l'environnement de développement
        stage('Deploy to Development') {
            steps {
                script {
                    sh '''
                    mkdir -p ~/.kube  # Créer le répertoire .kube si nécessaire
                    cp $KUBECONFIG ~/.kube/config  # Copier le fichier kubeconfig pour accéder au cluster Kubernetes
                    cp fastapi/values.yaml values-dev.yml  # Copier le fichier de valeurs Helm pour l'environnement de développement
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values-dev.yml  # Mettre à jour le tag de l'image dans le fichier de valeurs
                    helm upgrade --install cast-service fastapi --values=values-dev.yml --namespace dev  # Déployer ou mettre à jour le service Cast dans l'environnement de développement
                    helm upgrade --install movie-service fastapi --values=values-dev.yml --namespace dev  # Déployer ou mettre à jour le service Movie dans l'environnement de développement
                    '''
                }
            }
        }

        // Étape de déploiement dans l'environnement de staging
        stage('Deploy to Staging') {
            steps {
                script {
                    sh '''
                    mkdir -p ~/.kube  # Créer le répertoire .kube si nécessaire
                    cp $KUBECONFIG ~/.kube/config  # Copier le fichier kubeconfig pour accéder au cluster Kubernetes
                    cp fastapi/values.yaml values-staging.yml  # Copier le fichier de valeurs Helm pour l'environnement de staging
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values-staging.yml  # Mettre à jour le tag de l'image dans le fichier de valeurs
                    helm upgrade --install cast-service fastapi --values=values-staging.yml --namespace staging  # Déployer ou mettre à jour le service Cast dans l'environnement de staging
                    helm upgrade --install movie-service fastapi --values=values-staging.yml --namespace staging  # Déployer ou mettre à jour le service Movie dans l'environnement de staging
                    '''
                }
            }
        }

        // Étape d'approbation manuelle pour la production
        stage('Manual Approval for Production') {
            when {
                branch 'master'  // Exécuter cette étape uniquement pour la branche master
            }
            steps {
                timeout(time: 15, unit: 'MINUTES') {  // Limiter le temps d'attente pour l'approbation manuelle
                    input message: 'Do you want to deploy in production?', ok: 'Deploy'  // Demander une approbation manuelle avant le déploiement en production
                }
            }
        }

        // Étape de déploiement dans l'environnement de production
        stage('Deploy to Production') {
            when {
                branch 'master'  // Exécuter cette étape uniquement pour la branche master
            }
            steps {
                script {
                    sh '''
                    mkdir -p ~/.kube  # Créer le répertoire .kube si nécessaire
                    cp $KUBECONFIG ~/.kube/config  # Copier le fichier kubeconfig pour accéder au cluster Kubernetes
                    cp fastapi/values.yaml values-prod.yml  # Copier le fichier de valeurs Helm pour l'environnement de production
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values-prod.yml  # Mettre à jour le tag de l'image dans le fichier de valeurs
                    helm upgrade --install cast-service fastapi --values=values-prod.yml --namespace prod  # Déployer ou mettre à jour le service Cast dans l'environnement de production
                    helm upgrade --install movie-service fastapi --values=values-prod.yml --namespace prod  # Déployer ou mettre à jour le service Movie dans l'environnement de production
                    '''
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline executed successfully!'  // Message de succès après l'exécution du pipeline
        }
        failure {
            echo 'Pipeline failed!'  // Message d'erreur si le pipeline échoue
        }
    }
}
