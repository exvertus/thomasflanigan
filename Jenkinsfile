pipeline {
    agent {
        kubernetes {
            yamlFile 'job-pod.yaml'
            defaultContainer 'python'
        }
    }
    stages {
        stage('Pelican build') {
            steps {
                sh "pip install -r requirements.txt"
                sh "make publish"
            }
        }
        stage('Push image') {
            when {
                branch 'main'
            }
            steps {
                container('kaniko') {
                    sh "/kaniko/executor --dockerfile Dockerfile --context dir://${env.WORKSPACE} --verbosity debug --destination gcr.io/tom-personal-287221/thomasflanigan:rvtest"
                //    sh "/kaniko/executor --dockerfile Dockerfile --context dir://${env.WORKSPACE} --verbosity debug --destination gcr.io/tom-personal-287221/thomasflanigan:latest"
                }
            }
        }
        // stage('Deploy image') {
        //     when {
        //         branch 'main'
        //     }
        //     steps {
        //         container('kubectl') {
        //             sh "kubectl delete pod -l=app=site -n thomasflanigan"
        //         }
        //     }
        // }
    }
}
