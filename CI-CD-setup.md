# GitHub Actions workflow setup and instructions

## Prerequisites
To automatically push code changes, performing tests, building and pushing an image, deploying and application and performing health checks for this project you will need the following:
 * [Docker](https://docs.docker.com/engine/installation/)
 * [Docker post installation steps](https://docs.docker.com/engine/install/linux-postinstall/)
 * [Dockerhub](https://hub.docker.com/)


### Recreate the environment

1. Create Dockerhub account and GitHub Access Token to be able to push to the repository
   - Create an account in [Dockerhub](https://hub.docker.com/)
   - Create an [Access token](https://github.com/settings/tokens) for GitHub:
    Navigate to the profile in the top right corner of GitHub -> Settings -> Developer Settings -> Personal access tokens -> Tokens (classic)  
    Generate a new token there with clicking on all the boxes and save it in a text file locally in your computer.

2. Create secrets for the workflow

    The first step is to fork the repository.

    Then navigate to the forked repository: Settings-> Secrets and variables -> Actions -> And we setup the following secretes:

    ```bash

    NAME: AZURE_SSH_KEY
    VALUE: The azure ssh key that has been provided to you
    NAME: AZURE_USERNAME
    VALUE: Your VM username
    NAME: AZURE_VM_IP
    VALUE: The public ip address of the VM
    NAME: DOCKERHUB_USERNAME
    VALUE: You dockerhub username
    NAME: DOCKERHUB_TOKEN
    VALUE: Your dockerhub password or token

    ```

3. Setup the environment inside the VM
    Connect via ssh into the VM:
    ```bash

    ssh -i <PATH_TOKEY.PEM> <AZURE_USERNAME>@<AZURE_VM_IP>
    
    ```
    While inside the VM you have to install Docker and follow the Docker post installation steps. The links are in the prerequisites.  

    After completing the installation of Docker you have to pull the foked repository:
    ```bash

    git clone https://github.com/username/repository.git
    cd repository
    git fetch --all
    git checkout branch-name
    git pull origin branch-name

    ```
    The docker-compose files are the only ones thar are necessary to be present inside the VM, but we download the whole repo to have these files updated.

    If you followed the above steps correctly you have successfully configured the environment!

### Documentation of how the the CI-CD pipeline works


<!-- 2.  Github workflow setup
Go to the Actions tab
Go to new workflow 
And we create a workflow file -->