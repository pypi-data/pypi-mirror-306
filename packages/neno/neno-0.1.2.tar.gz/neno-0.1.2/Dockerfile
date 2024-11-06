FROM jupyter/scipy-notebook@sha256:fca4bcc9cbd49d9a15e0e4df6c666adf17776c950da9fa94a4f0a045d5c4ad33
ARG NENO_VERSION=0.0.11

# global pip cache, to speed up venv setup
RUN mkdir -p $HOME/.pip
RUN echo "[global]\ndownload_cache = ~/.pip/cache" >> $HOME/.pip/pip.conf 

RUN pip install "neno[server]"==${NENO_VERSION} || pip install "neno[server]"==${NENO_VERSION}

WORKDIR /etc/neno
COPY src/neno/config.yaml .

ENTRYPOINT [ "python", "-m", "neno" ]
