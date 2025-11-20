pipeline {
    agent any

    stages {
        stage('Cleanup') {
            steps {
                echo 'Fase 1: Pulizia vecchi container e immagini.'
                sh "docker stop sentiment-prod || true" 
                sh "docker rm sentiment-prod || true"
            }
        }

        stage('Build Image') {
            steps {
                echo 'Fase 2: Costruzione della nuova immagine Docker.'
                sh "docker build -t sentiment-api:${env.BUILD_ID} ." 
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Fase 3: Esecuzione Health Check e Test.'
                sh "docker run -d --name test-api -p 8001:8000 sentiment-api:${env.BUILD_ID}"
                
                sleep 5
                
                sh 'curl -sS http://host.docker.internal:8001 | grep "API is running"'

                sh "docker stop test-api"
                sh "docker rm test-api"
            }
        }

        stage('Deploy') {
            when {
                expression { currentBuild.result == 'SUCCESS' }
            }
            steps {
                echo 'Fase 4: Deploy in produzione.'
                sh "docker run -d --name sentiment-prod -p 8000:8000 sentiment-api:${env.BUILD_ID}"
                
                echo "Deploy completato per la versione: ${env.BUILD_ID}"
            }
        }
    }
}
