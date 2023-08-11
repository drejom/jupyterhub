
FROM mambaorg/micromamba:latest AS base

USER root

# Copy the default jupyterhub_config.py
COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

# Copy the environment.yml file to the Docker container
COPY environment.yml /tmp/

# Use mamba to update the base environment
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml
RUN micromamba install -y -n base -f /tmp/environment.yml && \
    micromamba clean --all --yes

RUN mkdir /data

WORKDIR /srv/jupyterhub

EXPOSE 8000

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py" ]