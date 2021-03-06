
# Getting Started
### docker-compose
Compose is a way to more easily run docker containers than the `docker run` command.
* __Note__: If at any point you get errors about ``__pycache__`` directories run `rm -rf __pycache__ test/__pycache__`
* Install docker-compose [here](https://docs.docker.com/compose/install/#install-compose) if you don't already have it installed.
* Copy the file `.env.example` and name the copy `.env`
  * Modify the value after`VOLUMES=` to whatever you want your container's docker volumes to be (the default is your home directory)
    * If you are planning on running the d3m runtime locally, make sure that you will have access to your cloned d3m repository
  * The volumes inside of the container can be accessed at the path `/volumes`
  * Make sure `DATASETS=` is pointing to the datasets you want the container to have access to
  * Modify `SERVER_PORT=` to the port that you want exposed on the docker container. This should be the same port that the grpc server is going to be running on
  * The datasets can be accessed from inside the container at `/datasets`
  * `TA2=` should point to where you have cloned the d3m-ta2 project. It can be accessed from inside of the container at `/d3m-ta2`
* Copy `config.py.example` to `config.py` and replace any variables you would like to change
#### Nvidia Runtime For Docker
* If you want to utilize GPUs from within the ta2 docker container, you will need the Nvidia docker runtime installed
  * [Install Instructions](https://github.com/NVIDIA/nvidia-docker#quickstart)
  * You may need to upgrade your docker version ([instructions](https://docs.docker.com/install/linux/docker-ce/ubuntu/))
* Uncomment following lines in the docker-compose file
```dockerfile
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
```
* Run `nvidia-smi` from inside of the container to see if this worked

### Running Local D3M Runtime
* Option 1:
  * Run `pip3 uninstall d3m`
  * Run `pip3 install --process-dependency-links -e {path_to_your_d3m_repo}`
  * Now you should be running the local D3M runtime and any changes you make should be reflected when you run the code
* Option 2:
  * Run `docker exec -it ta2 bash`
  * Change into where you mounted the d3m runtime code
  * Run d3m commands as you normally would, and it will use the local code
  
# Usage
### Running the Container
Before being able to pull the image you will need to login the D3M's private docker registry.
* Run `docker login registry.datadrivendiscovery.org` and follow the prompts to enter your username and password
* Run `docker-compose up -d`
  * Note: If you get a permission denied error, try rerunning the command with `sudo`
  * If you don't want to use `sudo` follow the instructions [here](https://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo)
* Run `docker exec -it ta2 bash` to access the container from the command line
  
### Running Integration Tests
* Run `docker exec -it ta2 bash`
* Start the server in the background with `python3 ta2_server.py &`
* Run `pytest`
  * To run the tests with multiple workers `pytest -n {num_workers}`

### Bringing Down the Container
* To stop and remove the container run `docker-compose down` from within the directory with the docker-compose.yml file
