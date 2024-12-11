pipeline{
    agent any
    stages{
        stage("checkout the code"){
            steps{
                git branch: 'main', url: 'https://github.com/dpraveenpaw/hclwar.git'
            }
        }
        stage("code see"){
            steps
            {
                sh "mvn test"
            }
        }
    
    }
}
