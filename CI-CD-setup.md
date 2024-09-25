# GitHub Actions workflow setup and instructions

## Prerequisites
To automatically set code changes to this project you will need the following:
 * [Docker](https://docs.docker.com/engine/installation/)
 To be able to use docker with sudo rights:
 * [Docker post installation steps](https://docs.docker.com/engine/install/linux-postinstall/)
 Dockerhub account
 * [Dockerhub](https://hub.docker.com/)


### Recreate the environment

1. Create Dockerhub account and Github secret to be able to push to the repository
    To create an account in Dockerhub:
   * [Dockerhub](https://hub.docker.com/)
    To create an access token for GitHub:
    Go to the profile in the top right corner of GitHub -> Settings -> Developer Settings -> Personal access tokens -> Tokens (classic)
    Generate a new token there with clicking on all the boxes and save it in a text file locally in your computer.

2. Create secrets for the workflow

The first step is to fork the repository.

Then go to the forked repository: Settings-> Secrets and variables -> Actions -> And we setup the following secretes:

```bash

NAME: AZURE_SSH_KEY
VALUE: The azure ssh key that has been provided to you
NAME: AZURE_USERNAME
VALUE: the username
NAME: AZURE_VM_IP
VALUE: The public ip address of the VM
NAME: DOCKERHUB_USERNAME
VALUE: You dockerhub username
NAME: DOCKERHUB_TOKEN
VALUE: Your dockerhub password or token

```

3. Setup the environment inside the VM
Connect via ssh into the VM:
  ```
  ssh -i <path_to_key.pem> <AZURE_USERNAME>@<AZURE_VM_IP>
 
  ```
Inside we have to install Docker and follow the Docker post installation steps. The links are in the prerequisites


<!-- 2.  Github workflow setup
Go to the Actions tab
Go to new workflow 
And we create a workflow file -->