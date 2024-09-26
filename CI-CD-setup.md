# GitHub Actions workflow setup and instructions

## Prerequisites
To automatically push code changes, performing tests, building and pushing an image, deploying and application and performing health checks for this project you will need the following:
* [Docker](https://docs.docker.com/engine/install/ubuntu/)
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

    Clone the forked repository:
    ```bash
    
    git clone https://github.com/evripidaros/dev-ops-assignment-api.git
    cd dev-ops-assignment-api
    
    ```
    First you must set the name of your `DOCKERHUB_USERNAME` in  `.env` file with the same name as in GitHub Secrets and then you run the init_setup.sh to install all the prerequisites:

    ```bash

    chmod +x init_setup.sh
    ./init_setup.sh
    
    ```
    On a newly setup machine, relog may be required to setup properly non root docker user


4. Access the Fastapi application

    You can now clone the repository in your local machine, make changes to the code and push back to the repository. 

    You can now access the Fastapi application at `http://<AZURE_VM_IP>:8000` through the following endpoints:

    | Method | Endpoint             | Description                                 | Response Format  |
    |--------|----------------------|---------------------------------------------|------------------|
    | GET    | /                    | Returns a welcome message                   | JSON             |
    | GET    | /health              | Executes health check                       | JSON             |
    | GET    | /items/{item_id}     | Returns item details with optional query parameter q | JSON    |


## CI-CD pipeline steps
   
GitHub Actions is natively integrated with GitHub repositories, thus removing the need for additional webhooks.

- The pipeline will run everytime you push code to the main, staging or testing  branches. 

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

### Design Decisions

* We save all our credentials as secrets for security reasons.
* We assume that there is a stable image tagged manually that is running and passes the healthcheck.
* We could create a rollback mechanism that could retrieve the most recent healthy image.
* If health check failed, we use exit code 1 to break the pipeline and indicate it to the developer.
* Since the deploy will deploy an image either way we could just print an informative message and return 0 (successful run)
* It would be good practice to run the healthcheck outside of the the VM, directly curling to `http://<AZURE_VM_IP>:8000/health` without the ssh login, but that was not possible inside the GitΗub Runner at the moment.
* We used the init_setup.sh inside the repository to simplify the process. Currently the github repository is a sinfge point of reference, for easier initial setup. In a production environment, upon VM creation a configurator would perform such tasks and the repository would not keep more than the required configuration details.

## Monitoring Implementation

We have implemented Prometheus, cAdvidsor, Alertmanager, nodexporter and grafana for monitoring the system.

To deploy the services run:

```bash

docker compose -f docker-compose.monitoring.yml up -d

```

The services can be accessed through your browser the following endpoints:

```bash

Prometheus: <AZURE_VM_IP>:8900
cAdvisor: <AZURE_VM_IP>:8940
Alertmanager: <AZURE_VM_IP>:8903
NodeExporter <AZURE_VM_IP>:8905
Grafana: <AZURE_VM_IP>:8950 username:admin password:admin

```

### Technologies

- cAdvisor is responsible for monitoring everything regarding container performance. The graphs can be seen in the cAdvisor endpoint and also in Grafana.

- Alertmanager is responsible for alerting by modifying the alert.rules. We have implemented 4 alert rules for the cpu load, memory load, storage load and the moitoring of the fastapi service. If they fire up, a slack template is sent to slack.

- NodeExporter is responsible for handling all the metrics of the host VM. In the /metrics tab you can see them in text format.

- Prometheus monitoring monitors a lot of metrics like queries, http requests, latencies etc.

- Grafana is responsible for visualizing all of the above.

### Notes

- After logging into Grafana into the dashborads tab you can see all the corresponding predefined dashboards.

- Docker containers tabs includes the docker containers performance metrics (cAdvisor). We have implemented 2 custom panels that can be visualised through the dashboards.

- Docker host tab monitors  the host VM performance metrics that Nodeexporter exposes.

- Monitor services tab is the prometheus monitoring services.

- If you stop the fastapi container, the custom panels in Docker container tab will indicate that fastapi service is down.

- Alerts can be seen in the http://<AZURE_VM_IP>:8950/alerting/list. If you stop the fastapi container, the rule will fire up indicating that fastapi service is down.

## Todo

- In terms of observability we should add beyond metrics ( Prometheus) also Loki for logging and Tempo for traces.

- A retention strategy for docker images is required.

- Another approach for automated deployment would be the use of [watchtower](https://containrrr.dev/watchtower/). We used a more stable way to avoid additional dependancies.