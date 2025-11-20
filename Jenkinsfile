pipeline {
    agent any

    stages {
        stage('Setup Docker') { // NUOVA FASE: Risolve il problema "docker: not found"
            steps {
                echo 'Fase 0: Installazione Docker CLI e Curl nel container Jenkins.'
                // Aggiorna e installa i pacchetti necessari per eseguire i comandi Docker e curl
                sh "apt-get update && apt-get install -y docker.io curl"
            }
        }

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
                // Lancia il container sulla porta di test 8001
                sh "docker run -d --name test-api -p 8001:8000 sentiment-api:${env.BUILD_ID}"
                
                // Attende l'avvio dell'API
                sleep 5
                
                // Health check: verifica che l'API risponda (grep "API is running" dal main.py)
                sh 'curl -sS http://host.docker.internal:8001 | grep "API is running"'

                // Rimuove il container di test
                sh "docker stop test-api"
                sh "docker rm test-api"
            }
        }

        stage('Deploy') {
            // Esegue il deploy solo se tutti i test passano
            when {
                expression { currentBuild.result == 'SUCCESS' }
            }
            steps {
                echo 'Fase 4: Deploy in produzione.'
                // Avvia il nuovo container in produzione sulla porta 8000
                sh "docker run -d --name sentiment-prod -p 8000:8000 sentiment-api:${env.BUILD_ID}"
            }
        }
    }
}