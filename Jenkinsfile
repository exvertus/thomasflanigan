pipeline {
    agent {
        kubernetes {
            yamlFile 'job-pod.yaml'
            defaultContainer 'shell'
        }
    }
    stages {
        stage('Main') {
            steps {
                sh "ls -a /gcp-sa"
            }
        }
    }
}
