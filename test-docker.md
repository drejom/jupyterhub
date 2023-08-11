```bash
docker run -it --rm -p 8000:8000 \
    -e DOCKER_NETWORK_NAME=workbench \
    -e DOCKER_NOTEBOOK_IMAGE=jupyter/minimal-notebook \
    -e DOCKER_NOTEBOOK_DIR=/home/jovyan \
    -e DOCKER_SPAWN_CMD=start-singleuser.sh \
    -e JUPYTERHUB_ADMIN=domeally \
    -v /opt/workbench/jupyterhub/jupyterhub_config.py:/srv/jupyterhub/jupyterhub_config.py \
    -v /opt/workbench/jupyterhub/data:/data \
    -v /var/run/docker.sock:/var/run/docker.sock \
    --name jupyterhub \
    --network workbench \
    ghcr.io/drejom/jupyterhub:latest
```