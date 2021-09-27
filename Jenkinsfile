pipeline {
    agent {
        kubernetes {
            yamlFile 'job-pod.yaml'
            defaultContainer 'hugo'
        }
    }
    stages {
        stage('Hugo build') {
            steps {
                sh "hugo"
            }
        }
        stage('Push image') {
            when {
                branch 'main'
            }
            steps {
                container('kaniko') {
                   sh "/kaniko/executor --dockerfile Dockerfile --context dir://${env.WORKSPACE} --verbosity debug --destination gcr.io/tom-personal-287221/thomasflanigan:latest"
                }
            }
        }
        stage('Deploy image') {
            steps {
                container('kubectl') {
                    sh "kubectl delete pod -l=app=site -n thomasflanigan"
                }
            }
        }
    }
}
