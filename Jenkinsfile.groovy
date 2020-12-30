@Library('aicloud-pipeline-share-lib') _
import cn.aimidea.cd.pipeline.lib.*

pipeline {
    agent { label "docker" }
    triggers {
        gitlab(triggerOnPush: true, triggerOnMergeRequest: true, branchFilterType: 'All', secretToken: "246188d61ddf8a33355c4100a425187b")
    }
    environment{
        ver = ""
    }
    options {
        gitLabConnection('mideagitlab')
    }

    stages {
        stage('build') {
            when {
                expression {
                    return "PUSH" == env.gitlabActionType
                }
            }
            steps {
                script {
                    ver = aiVerGenerate()

                    docker.withRegistry("${env.ALIYUN_DOCKER_REGISTRY_URL}", "${env.ALIYUN_DOCKER_REGISTRY_ACCOUNT}") {
                        def imageTag = "registry-vpc.cn-hangzhou.aliyuncs.com/midea-aiplatform/speech-test:${ver}"
                        def image = docker.build("${imageTag}")
                        image.push()
                        sh "docker rmi -f ${imageTag}"
                    }
                }
            }
            post {
                always {
                    cleanWs()
                }
            }
        }
    }
    post {
        failure {
            updateGitlabCommitStatus name: 'build', state: 'failed'
        }
        success {
            updateGitlabCommitStatus name: 'build', state: 'success'
            script{
                currentBuild.displayName = "${ver}"
                if(env.gitlabSourceRepoHomepage != null){
                    currentBuild.description = "trigger by <a  target='_blank' rel='noopener noreferrer' href='${env.gitlabSourceRepoHomepage}/commit/${env.gitlabAfter}'>${env.gitlabSourceNamespace}/${env.gitlabSourceRepoName}</a>,${env.gitlabUserName}"
                }
            }
        }
        always {
            cleanWs()
        }
    }
}
