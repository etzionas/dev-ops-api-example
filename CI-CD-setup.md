## Prerequisites
To automatically set code changes to this project you will need the following development kits.
 * [Docker](https://docs.docker.com/engine/installation/)


### Recreate the environment

1.  Github workflow setup
We go to the repo
we go to github actions
new workflow
and we create a workflow file


2.  Create secrets for the workflow
We go to settings-> secrets and variables -> actions and we setup the following:

    ```
    bash
    NAME:AZURE_SSH_KEY
    VALUE: The azure ssh key that has been provides to you
    NAME:AZURE_USERNAME
    VALUE: the username
    NAME:AZURE_VM_IP
    VALUE:
    NAME:DOCKERHUB_TOKEN
    VALUE:
    NAME:DOCKERHUB_USERNAME
    VALUE:
    NAME:DOCKER_PASSWORD
    VALUE:
    NAME:DOCKER_USERNAME
    VALUE:
    ```