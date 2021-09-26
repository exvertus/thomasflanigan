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
                echo "Testing 123"
            }
        }
    }
}
