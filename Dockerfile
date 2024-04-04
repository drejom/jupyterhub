# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG JUPYTERHUB_VERSION=4.1.5
FROM quay.io/jupyterhub/jupyterhub:$JUPYTERHUB_VERSION

# hadolint ignore=DL3013
RUN python3 -m pip install --no-cache-dir \
    dockerspawner \
    jupyterhub-nativeauthenticator \
    jupyterhub-idle-culler \
    jupyter-server-proxy \
    wrapspawner \
    https://github.com/jupyterhub/batchspawner/archive/main.zip

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]