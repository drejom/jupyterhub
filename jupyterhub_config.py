# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os
import sys


c = get_config()

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

# Spawn containers from this image
c.DockerSpawner.image = os.environ["DOCKER_NOTEBOOK_IMAGE"]
c.DockerSpawner.host_ip = '0.0.0.0'

# JupyterHub requires individual instances of Notebook server,
# therefore we use `start-singleuser.sh` script from the jupyter/docker-stacks,
# as the Docker run command.
# The environment variable DOCKER_SPAWN_CMD can also be used to override.
spawn_cmd = os.environ.get("DOCKER_SPAWN_CMD", "start-singleuser.sh")
c.DockerSpawner.cmd = spawn_cmd

# Connect containers to this Docker network
network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Set the notebook directory explicitly to mount a volume.
# The jupyter/docker-stacks images run the Notebook server with `jovyan` user and notebook directory as `/home/jovyan/work`.
# Following the same naming convention.
notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jovyan/work")
host_shared_dir = '/opt/workbench/jupyterhub/shared' 
docker_shared_vol = 'jupyterhub'
shared_mount = {}
c.DockerSpawner.notebook_dir = notebook_dir

# Determine which volume to share
# If `host_shared_dir` exists, we use it; otherwise, we fall back to Docker's shared volume.
if os.path.exists(host_shared_dir):
    shared_mount[host_shared_dir] = f"{notebook_dir}/shared" 
else:
    shared_mount[docker_shared_vol] = f"{notebook_dir}/shared"

# Mount user's Docker volume from the host to user's notebook directory in the container
c.DockerSpawner.volumes = {
    "jupyterhub-user-{username}": notebook_dir,
    **shared_mount  
}


# Remove containers once they are stopped
c.DockerSpawner.remove = True

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8080

# IP as seen on the docker network. Can also be a hostname.
c.JupyterHub.hub_connect_ip = 'jupyterhub'  

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"

# Authenticate users with Native Authenticator
c.JupyterHub.authenticator_class = "native"

# Allow anyone to sign-up without approval
c.NativeAuthenticator.open_signup = True

# Allowed admins
admin = os.environ.get("JUPYTERHUB_ADMIN")
if admin:
    c.Authenticator.admin_users = ['admin']

# Setup for ngnix
c.JupyterHub.bind_url = 'http://:8000'

# Redirect to JupyterLab, instead of the plain Jupyter notebook
c.Spawner.default_url = '/lab'

# JupiterHub idle culler
c.JupyterHub.load_roles = [
    {
        "name": "jupyterhub-idle-culler-role",
        "scopes": [
            "list:users",
            "read:users:activity",
            "read:servers",
            "delete:servers"
        ],
        # assignment of role's permissions to:
        "services": ["jupyterhub-idle-culler-service"],
    }
]

c.JupyterHub.services = [
    {
        "name": "jupyterhub-idle-culler-service",
        "command": [
            sys.executable,
            "-m", "jupyterhub_idle_culler",
            "--timeout=3600",
        ]
    }
]

# Disable user configuration of containers
c.DockerSpawner.disable_user_config = False
