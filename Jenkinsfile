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
        
        stage('Lint') {
            steps {
                echo 'Linting..'
                sh 'find . -name "*.py" -exec pylint {} +'
            }
        }
        
        stage('Security Scanner') {
            steps {
                echo 'Beginning Security Scan..'
                sh '#bandit -r .'
            }
        }

        stage('Format') {
            steps {
                echo 'Formatting..'
                sh 'ruff format'
                withCredentials([gitUsernamePassword(credentialsId: 'boneyd7511-github-token', gitToolName: 'Default')]) {
                    sh 'git add .'
                    sh 'git commit -m "Formatted code with Ruff"'
                    sh 'git push -u origin master'
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
