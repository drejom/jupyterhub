FROM python:3.8-slim

# Install necessary packages for Miniconda installation
RUN apt-get update && apt-get install -y wget bzip2 && rm -rf /var/lib/apt/lists/*

# Install Miniconda
ENV MINICONDA_VERSION 4.9.2
ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/bin:$PATH
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py39_${MINICONDA_VERSION}-Linux-x86_64.sh -O ~/miniconda.sh \
    && /bin/bash ~/miniconda.sh -b -p $CONDA_DIR \
    && rm ~/miniconda.sh \
    && conda clean -tipsy

# Copy the merged environment.yml into the container
COPY environment.yml /app/environment.yml
WORKDIR /app

# Create the environment from the merged environment.yml
RUN conda env create -f environment.yml

# Ensure the environment is activated
SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]

CMD ["/bin/bash", "-c", "source /opt/conda/bin/activate base && jupyterhub -f /srv/jupyterhub/jupyterhub_config.py"]
