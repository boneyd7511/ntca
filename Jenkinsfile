pipeline {
    agent any

    stages {
        
        stage("Clone Git Repository") {
            steps {
                git(
                    url: "https://github.com/boneyd7511/ntca",
                    branch: "master",
                    changelog: true,
                    poll: true
                )
            }
        }

        stage("Create Report File") {
            steps {
                script {
                    def time = sh(script: 'date "+%F-%T"', returnStdout: true).trim()
                    env.REPORT = "jenkins-reports/python_report_${time}.txt"
                    sh "touch ${env.REPORT}"
                }
            }
        }
        
        stage('Lint') {
            steps {
                echo 'Linting..'
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh "echo 'LINTING REPORT' >> ${env.REPORT}"
                    sh "find . -name '*.py' -exec pylint {} + >> ${env.REPORT}"
                }
            }
        }
        
        stage('Security Scanner') {
            steps {
                echo 'Beginning Security Scan..'
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh "echo 'SECURITY SCANNER REPORT' >> ${env.REPORT}"
                    sh "bandit -r . >> ${env.REPORT}"
                }
            }
        }

        stage('Format') {
            steps {
                echo 'Formatting..'
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh "echo 'FORMATTING REPORT' >> ${env.REPORT}"
                    sh "ruff format >> ${env.REPORT}"
                }
            }
        }

        stage('Git Push') {
            steps {
                echo 'Trying push to GitHub...'
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    withCredentials([gitUsernamePassword(credentialsId: 'boneyd7511-github-token', gitToolName: 'Default')]) {
                        sh 'git add .'
                        sh 'git commit -m "Formatted code with Ruff"'
                        sh 'git push -u origin master'
                    }
                }
            }
        }

        stage('Validate') {
            steps {
                echo 'Validating..'
            }
        }
    }

    post {
        always {
            publishHTML(allowMissing: false, alwaysLinkToLastBuild: true, keepAll: true, reportDir: '.', reportFiles: 'index.html', reportName: 'My HTML Report')
        }
    }
}
