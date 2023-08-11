# Jupyterhub server
[![Docker](https://github.com/drejom/jupyterhub/actions/workflows/build_publish_docker_image.yaml/badge.svg)](https://github.com/drejom/jupyterhub/actions/workflows/build_publish_docker_image.yaml)

Run notebooks via a variety of Spawners

Tag a new version to trigger GitHub Actions to build & push a new image to GitHub Packages

## Features

- new users via nativeauthenticator
- dockerspawn
- cull idle notebooks

## Run locally

```sh
docker run -it --rm -p 8000:8000 \
    -e DOCKER_NETWORK_NAME=workbench \
    -e DOCKER_NOTEBOOK_IMAGE=jupyter/minimal-notebook \
    -e DOCKER_NOTEBOOK_DIR=/home/jovyan \
    -e DOCKER_SPAWN_CMD=start-singleuser.sh \
    -e JUPYTERHUB_ADMIN=${USER} \
    -v jupyterhub_data:/data \
    -v /var/run/docker.sock:/var/run/docker.sock \
    --name jupyterhub \
    ghcr.io/drejom/jupyterhub:latest

# Mount to ovveride default
# -v /opt/workbench/jupyterhub/jupyterhub_config.py:/srv/jupyterhub/jupyterhub_config.py 

```

## Roadmap
- ssh spawner
- slurm spawner
- dashboards
- launch other services via hub (eg llm apps)
  - jupyter-server-proxy
    - Memgraph (https://medium.com/memgraph/memgraph-lab-2-5-0-is-out-232228bb6187)
    - code https://github.com/seblum/jupyterhub-server-image/tree/main
    - code, pluto, docserver, bookserver
           https://github.com/Rahuketu86/RemoteConnect
    - OpenVINO for Intel GPU
    - vLLM https://vllm.readthedocs.io/

## Further reading and inspo

    [Setup on a RPi](https://towardsdatascience.com/setup-your-home-jupyterhub-on-a-raspberry-pi-7ad32e20eed)

    [Setup NGNIX proxy](https://hands-on.cloud/nginx-jupyter-proxy-example/)
 
    [Medium-scale JupyterHub deployments](https://opendreamkit.org/2018/10/17/jupyterhub-docker/) (with Traefik)