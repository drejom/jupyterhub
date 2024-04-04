# Start with a Miniconda base image
FROM continuumio/miniconda3

# Install Mamba from Conda-Forge
RUN conda install mamba -n base -c conda-forge

# Copy your environment.yml file into the container
COPY environment.yml /app/environment.yml
WORKDIR /app

# Use Mamba to update the base environment based on environment.yml file
RUN mamba env update -n base -f environment.yml

# Set the command to start JupyterHub
CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]
