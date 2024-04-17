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
        sh 'sudo pip install ruff'
        sh 'ruff format'
        sh '''#git config user.email "jenkins@example.com"
#git config user.name "Jenkins"
#git add .
#git commit -m "Formatted code with Ruff"
#git push origin master'''
        git(url: 'https://github.com/boneyd7511/ntca', branch: 'master', changelog: true, credentialsId: '6595730a-f516-4839-a4e7-63ece2d30e72')
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