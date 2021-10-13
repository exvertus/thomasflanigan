pipeline {
    agent {
        kubernetes {
            yamlFile 'job-pod.yaml'
            defaultContainer 'hugo'
        }
    }
    parameters {
        booleanParam(name: 'PREVIEW_DRAFTS', defaultValue: false, description: 'Use to build a preview of the site with drafts built.')
    }
    stages {
        stage('Preview Drafts') {
            when {
                expression {
                    params.PREVIEW_DRAFTS == true
                }
            }
            environment {
                ENV_STAGE = 'test'
            }
            stages {
                stage('Hugo build drafts') {
                    steps {
                        sh "hugo -D"
                        sh "mkdir conf-staging"
                        sh "cp -r ${env.WORKSPACE}/nginx-configs/${env.ENV_STAGE}/default.conf conf-staging"
                    }
                }
                stage('Push image-test') {
                    steps {
                        container('kaniko') {
                           sh "/kaniko/executor --dockerfile Dockerfile --context dir://${env.WORKSPACE} --verbosity debug --destination gcr.io/tom-personal-287221/tlf-test:latest --destination gcr.io/tom-personal-287221/tlf-test:${env.BUILD_TAG}"
                        }
                    }
                }
                stage('Deploy image-test') {
                    steps {
                        container('kubectl') {
                            sh "kubectl delete pod -l=app=test-site -n services"
                        }
                    }
                }
            }
        }
        stage('Deploy Live') {
            when {
                branch 'main'
            }
            environment {
                ENV_STAGE = 'prod'
            }
            stages {
                stage('Hugo build') {
                    steps {
                        sh "hugo --cleanDestinationDir"
                        sh "mkdir conf-staging"
                        sh "cp -r ${env.WORKSPACE}/nginx-configs/${env.ENV_STAGE}/default.conf conf-staging"
                    }
                }
                stage('Push image') {
                    steps {
                        container('kaniko') {
                           sh "/kaniko/executor --dockerfile Dockerfile --context dir://${env.WORKSPACE} --verbosity debug --destination gcr.io/tom-personal-287221/thomasflanigan:latest --destination gcr.io/tom-personal-287221/thomasflanigan:${env.BUILD_TAG}"
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
    }
}
