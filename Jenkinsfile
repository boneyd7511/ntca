pipeline {
  agent {
    node {
      label 'root-node'
    }

  }
  stages {
    stage('Lint') {
      steps {
        echo 'Linting..'
        sh 'pylint helloworld.py'
        sh '''sudo pip install ruff
ruff check
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