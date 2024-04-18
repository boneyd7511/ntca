pipeline {
    agent any

    stages {
        stage('Lint') {
            steps {
                echo 'Linting..'
                sh '''
                    #sudo apt update -y
                    #sudo apt install python3-pip -y
                    #sudo apt install pylint
                '''
                sh '#find . -name "*.py" -exec pylint {} +'
            }
        }

        stage('Security Scanner') {
            steps {
                echo 'Beginning Security Scan..'
                sh '#sudo pip install bandit'
                sh '#bandit -r .'
            }
        }

        stage('Format') {
            steps {
                echo 'Formatting....'
                sh '#sudo pip install ruff'
                sh 'ruff format'
                sh '''
                    #git config user.email "jenkins@example.com"
                    #git config user.name "Jenkins"
                    #git add .
                    #git commit -m "Formatted code with Ruff"
                    #git push https://boneyd7511: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@github.com/boneyd7511/ntca master
                '''
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
