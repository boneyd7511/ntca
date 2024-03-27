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
sudo pip install pylint -y
pylint helloworld.py'''
      }
    }

    stage('Test') {
      steps {
        echo 'Testing..'
        sh '''
          python3 helloworld.py
        '''
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