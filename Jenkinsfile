pipeline {
    agent {
        kubernetes {
            yamlFile 'job-pod.yaml'
            defaultContainer 'python'
        }
    }
    parameters { 
        booleanParam(name: 'BUILD_TEST', defaultValue: false, description: 'Build a test version of the site') 
    }
    stages {
        stage('Build test') {
            when {
                expression { return params.BUILD_TEST }
            }
            steps {
                sh "pip install -r requirements.txt"
                sh "make html"
            }
        }
        stage('Push test image') {
            when {
                expression { return params.BUILD_TEST }
            }
            steps {
                container('kaniko') {
                   sh "/kaniko/executor --dockerfile Dockerfile --context dir://${env.WORKSPACE} --verbosity debug --destination gcr.io/tom-personal-287221/tfsite-test:latest"
                }
            }
        }
        stage('Build live') {
            when {
                branch 'main'
            }
            steps {
                sh "pip install -r requirements.txt"
                sh "make publish"
            }
        }
        stage('Push live image') {
            when {
                branch 'main'
            }
            steps {
                container('kaniko') {
                   sh "/kaniko/executor --dockerfile Dockerfile --context dir://${env.WORKSPACE} --verbosity debug --destination gcr.io/tom-personal-287221/thomasflanigan:latest"
                }
            }
        }
        stage('Deploy live') {
            when {
                branch 'main'
            }
            steps {
                container('kubectl') {
                    sh "kubectl delete pod -l=app=site -n thomasflanigan"
                }
            }
        }
    }
}
