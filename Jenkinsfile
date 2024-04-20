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
                    sh "find . -name '*.py' -exec pylint {} + > ${env.REPORT} 2>&1"
                }
            }
        }
        
        stage('Security Scanner') {
            steps {
                echo 'Beginning Security Scan..'
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh "bandit -r . > ${env.REPORT} 2>&1"
                }
            }
        }

        stage('Format') {
            steps {
                echo 'Formatting..'
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh "ruff format > ${env.REPORT} 2>&1"
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
