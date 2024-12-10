pipeline {
    agent any
    environment {
        GITHUB_REPO = "etzionas/dev-ops-api-example"
        GITHUB_TOKEN = credentials('github_token') // GitHub token from Jenkins credentials
        REPO_OWNER = 'etzionas'
        REPO_NAME = 'dev-ops-api-example'
    }
    triggers{
        GenericTrigger(
            genericVariables: [
                [key: 'workflow_run_status', value: '$.action'],
                [key: 'workflow_run_id', value: '$.workflow_run.id']
            ],
            token: 'github-webhook-secret',
            causeString: 'Triggered by workflow_run event',
            printContributedVariables: true,
            printPostContent: true,
            regexpFilterExpression: '^completed$', // Only trigger when the workflow is finished
            regexpFilterText: '$workflow_run_status' 
        )
    }
    stages {
        stage('Fetch GitHub Action Logs') {
            steps {
                script {
                    def workflowRunId = env.workflow_run_id
                    // if (!workflowRunId) {
                    //     error "Workflow run ID not provided in webhook payload."
                    // }
                    
                    echo "Fetching logs for Workflow Run ID: ${workflowRunId}"

                    // Fetch latest workflow run details
                    def response = sh(script: """
                        curl -s -H "Authorization: Bearer ${GITHUB_TOKEN}" \
                        https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/actions/runs
                        """, returnStdout: true).trim()
                    
                    // Parse the JSON response
                    def json = readJSON text: response
                    def latestRunId = json.workflow_runs[0].id
                    echo "Latest Run ID: ${latestRunId}"

                    // Download the logs
                    sh """
                        curl -s -L -H "Authorization: Bearer ${GITHUB_TOKEN}" \
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
