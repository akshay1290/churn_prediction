  pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
              checkout scm
               
            }
        }
        stage('Build Image') {
            steps {
                sh 'docker build -t churnstream:v1 .'
                sh 'docker tag myapp:${env.BUILD_NUMBER} myregistry/myapp:${env.BUILD_NUMBER}'
            }
        }
        stage('Run Image') {
            steps {
              sh 'docker run -d -p 8501:8501 --name churnstream1 churnstream:v1'
                }
                
            }
      stage('Testing'){
        steps{
          echo 'Process complete..'
        }
    }
}
