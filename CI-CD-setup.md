# GitHub Actions workflow setup and instructions

## Prerequisites
To automatically push code changes, performing tests, building and pushing an image, deploying and application and performing health checks for this project you will need the following:
* [Docker](https://docs.docker.com/engine/installation/)
* [Docker post installation steps](https://docs.docker.com/engine/install/linux-postinstall/)
* [Dockerhub](https://hub.docker.com/)

## Recreate the environment

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

    ssh -i <PATH_TO_KEY.PEM> <AZURE_USERNAME>@<AZURE_VM_IP>
    
    ```
    While inside the VM you have to install Docker and follow the Docker post installation steps. The links are in the prerequisites.  

    After completing the installation of Docker you have to pull the forked repository:
    ```bash

    git clone https://github.com/username/repository.git
    cd repository
    git fetch --all
    git checkout branch-name
    git pull origin branch-name

    ```
    The docker-compose files are the only ones thar are necessary to be present inside the VM, but we download the whole repository in order to deploy the initial version. This couls also be done on the VM creation.

    Create the docker network externally: 
    ```bash

    docker network create monitoring-net
    
    ```

4. Access the Fastapi application

    You can access the Fastapi application through `http://<AZURE_VM_IP>:8000` to the following endpoints:

    | Method | Endpoint             | Description                                 | Response Format  |
    |--------|----------------------|---------------------------------------------|------------------|
    | GET    | /                    | Returns a welcome message                   | JSON             |
    | GET    | /health              | Executes health check                       | JSON             |
    | GET    | /items/{item_id}     | Returns item details with optional query parameter q | JSON    |


## CI-CD pipeline steps
   
GitHub Actions is natively integrated with GitHub repositories, which means it doesn't require additional webhooks to be manually set up for standard workflows like running CI/CD pipelines when code is pushed, pull requests are made, or issues are created.

- The pipeline will run everytime you push code to the main, staging or testing repositories. 

- Three branches were chosen to execute the CI/CD pipeline, main branch is production/live code, staging for collaboration, and testing branch which was used to test the whole pipeline.

- Here is a detailed list of the distinct steps for the CI/CD pipeline:

    - GitHub deploys an ubuntu docker container to run the jobs.

 1. Checkout the repository in order to retrieve latest changes

    2. Setup python into the container.

    3. Setup python environment by installing application dependencies.

    4. Run the tests with Pytest.

    5. Set up the Buildx builder, in order to build and push your Docker image.

    6. Login to Dockerhub using the credentials from secrets.

    7. Build the image, tag it as "latest" and push it to your Dockerhub repository.

    8. Setup the SSH key inside the azure VM to ~/.ssh/known_hosts, in order to connect to the VM.

    9. Pull the new image, stop the previous fastapi containers (if there are any) and rerun the fastapi-container from the new image.

    10. Run healthcheck and rollback if it fails.
        SSH into the VM, curl `http://localhost:8000/health` endpoint.
        If it returns non-zero output, then roll back to an image tagged as "stable".

        <!-- - **Note**: Docker compose was chosen because there may be more containers under development. These can be added as services to the docker compose file. Also we  choose to stop and start only the fastapi service in case there are other services that we do not want to touch. -->

### Design Decisions

* We save all our credentials as secrets for security reasons.
* We assume that there is a stable image tagged manually that is running and passes the healthcheck.
* We could create a rollback mechanism that could retrieve the most recent healthy image.
* If health check failed, we use exit code 1 to break the pipeline and indicate it to the developer.
* Since the deploy will deploy an image either way we could just print an informative message and return 0 (successful run)
* It would be good practice to run the healthcheck outside of the the VM, directly curling to `http://<AZURE_VM_IP>:8000/health` without the ssh login, but that was not possible inside the GitΗub Runner at the moment.

## Monitoring Implementation

We have implemented prometheus, cadvidsor, alertmanager, nodexporter and grafana for monitoring the system.

The services can be accessed through your browser the following endpoints:

```bash

Prometheus <AZURE_VM_IP>:8900
cAdvisor <AZURE_VM_IP>:8940
Alertmanager <AZURE_VM_IP>:8903
Nodeexporter <AZURE_VM_IP>:8905
Grafana <AZURE_VM_IP>:8950 username:admin password:admin

```

- cAdvisor is responsible for monitoring everything regarding container resources consumption. The graphs can be seen in the page and also in grafana.

- Alertmanager is responsible for alerting by modifying the alert.rules. We have implemented 3 alert rules for the cpu load, memory load, storage load and the moitoring of the fastapi service. If they fire up, a message in slack is sent.

- Nodeexporter is responsible for handling all the metrics of the host VM. In the /metrics tab you can see them in text format.

- Prometheus monitoring monitors a lot of metrics like queries, http requests, latencies etc.

- Grafana is responsible for visualizing all of the above.