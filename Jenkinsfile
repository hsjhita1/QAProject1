pipeline {
    agent any
    stages {
        stage('Make all scripts executable') {
            steps{
                sh 'chmod +x ./script/*'
            }
        }
        stage('Prepare environment') {
            steps {
                sh './script/before-installation.sh'
                sh './script/installation.sh'
            }
        }
        stage('Run app') {
            steps{
                sh 'sudo systemctl restart flask.service'
            }
        }
    }
}