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
sudo apt-get install python3-pip -y
sudo pip install pylint'''
        sh '#find . -name "*.py" -exec pylint {} +'
      }
    }

    stage('Security Scanner') {
      steps {
        echo 'Beginning Security Scan..'
        sh 'sudo pip install bandit'
        sh '#bandit -r .'
      }
    }

    stage('Format') {
      steps {
        echo 'Formatting....'
        sh 'pip install ruff'
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