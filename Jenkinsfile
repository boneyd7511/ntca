pipeline {
  agent {
    node {
      label 'ubuntu-2004'
    }

  }
  stages {
    stage('Lint') {
      steps {
        echo 'Linting..'
        sh '''sudo apt-get update -y
sudo apt install python3-pip -y
pip install pylint'''
        sh 'find . -name "*.py" -exec pylint {} +'
        sh '''ruff check
'''
      }
    }

    stage('Security Scanner') {
      steps {
        echo 'Beginning Security Scan..'
      }
    }

    stage('Format') {
      steps {
        echo 'Formatting....'
        sh 'ruff format'
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