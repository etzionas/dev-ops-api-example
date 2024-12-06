pipeline {
    agent any
    environment {
        GITHUB_REPO = "etzionas/dev-ops-api-example"
        GITHUB_TOKEN = credentials('github_token') // GitHub token from Jenkins credentials
        REPO_OWNER = 'etzionas'
        REPO_NAME = 'dev-ops-api-example'
    }
    stages {
        stage('Fetch GitHub Action Logs') {
            steps {
                script {
                    // Fetch latest workflow run details
                    def response = sh(script: """
                        curl -s -H "Authorization: Bearer ${{ secrets.TOKEN }}" \
                        https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/actions/runs
                        """, returnStdout: true).trim()
                    
                    // Parse the JSON response
                    def json = readJSON text: response
                    def latestRunId = json.workflow_runs[0].id
                    echo "Latest Run ID: ${latestRunId}"

                    // Download the logs
                    sh """
                        curl -s -L -H "Authorization: Bearer ${{ secrets.TOKEN }}" \
                        https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/actions/runs/${latestRunId}/logs \
                        -o logs.zip
                    """

                    // Unzip and display logs
                    sh 'unzip -o logs.zip -d logs && cat logs/**/*.txt'
                }
            }
        }
    }
}
