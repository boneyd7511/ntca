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
        sh '''sudo apt-get install pip -y
sudo pip install pylint
pylint helloworld.py'''
      }
    }

    stage('Security Scanner') {
      steps {
        echo 'Beginning Security Scan..'
      }
    }

    stage('Deliver') {
      steps {
        echo 'Deliver....'
        sh '''
                echo "doing delivery stuff.."
                '''
      }
    }

  }
}