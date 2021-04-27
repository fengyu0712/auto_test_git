@Library('aicloud-pipeline-share-lib') _
import cn.aimidea.cd.pipeline.lib.*
String APP_VER = ""

pipeline {
    agent { label "docker" }
    triggers {
        gitlab(triggerOnPush: true, triggerOnMergeRequest: true, branchFilterType: 'All', secretToken: "246188d61ddf8a33355c4100a425187b")
        //分钟，小时，日，月，周
        cron('0 2 * * *')  //表示每天凌晨2点执行一次
    }
    options {
        gitLabConnection('mideagitlab')
    }

    stages {
        stage("init pipeline"){
            steps{
                script{
                    // 初始化流水线全局变量，必须
                    aiInitGlobalEnv()
                    APP_VER = aiVerGenerate()
                    // 打印环境变量
                    sh "printenv"
                }
            }
        }
        stage('build') {
//            when {
//                expression {
//                    return env.gitlabSourceBranch == "master" && env.gitlabActionType == "PUSH"
//                }
//            }
            steps {
                script {

                    docker.withRegistry("${env.ALIYUN_DOCKER_REGISTRY_URL}", "${env.ALIYUN_DOCKER_REGISTRY_ACCOUNT}") {
                        def imageTag = "registry-vpc.cn-hangzhou.aliyuncs.com/midea-aiplatform/speech-test:${APP_VER}"
                        def image = docker.build("${imageTag}")
                        image.push()
                        sh "docker rmi -f ${imageTag}"
                    }

                    // 打包chart
//                    aiChartPackage("charts","${APP_VER}")
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
                currentBuild.displayName = "${APP_VER}"
            }
        }
        always{
            script{
                cleanWs()
                if(env.gitlabSourceRepoHomepage != null){
                    currentBuild.description = "trigger by <a  target='_blank' rel='noopener noreferrer' href='${env.gitlabSourceRepoHomepage}/commit/${env.gitlabAfter}'>${env.gitlabSourceNamespace}/${env.gitlabSourceRepoName}</a>,${env.gitlabUserName}"
                }

            }
        }
    }
}